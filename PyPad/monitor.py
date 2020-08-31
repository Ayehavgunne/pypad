import asyncio
import json
import os
import time
from pathlib import Path
from typing import Any, Optional

import psutil
import yaml
from serial import Serial
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo

FILE_DIR = Path(__file__).parent

CHECK_APP_SECONDS = 5
BAUD_RATE = 115200
MY_DEVICE_ID = os.getenv("DEVICE_ID")


def is_running(process: psutil.Process) -> bool:
    if not process:
        return False
    try:
        return process.status() == psutil.STATUS_RUNNING
    except psutil.NoSuchProcess:
        return False


def get_proc_exe_name(process: psutil.Process) -> str:
    return process.exe().replace("\\", "/").split("/")[-1].split(".")[0]


def find_app(mappings: dict) -> Optional[psutil.Process]:
    for proc in psutil.process_iter():
        for exe_name in mappings.keys():
            try:
                proc_file_name = get_proc_exe_name(proc).lower()
                if exe_name.lower() == proc_file_name:
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass


def find_device() -> ListPortInfo:
    for port in comports():
        if MY_DEVICE_ID in port.hwid:
            return port


def find_serial() -> Optional[Serial]:
    try:
        port = find_device()
        if not port:
            return None
        serial = Serial(port.device, BAUD_RATE, timeout=1, write_timeout=0.005)
        print("Connected")
        return serial
    except SerialException:
        return None


def get_time() -> float:
    return time.time()


def read_serial(serial: Serial) -> Optional[str]:
    try:
        result = serial.readline()
    except (AttributeError, SerialException):
        return None
    try:
        result = result.decode("utf-8").strip()
        if result:
            return result
    except UnicodeDecodeError:
        return None


def send_serial(serial: Serial, message: Any) -> None:
    try:
        serial.reset_output_buffer()
        serial.write(f"{str(message)}\n".encode("utf-8"))
    except (AttributeError, SerialException) as err:
        print(err)


async def monitor() -> None:
    with (FILE_DIR / "mappings.yaml").open() as map_file:
        mappings = yaml.load(map_file, Loader=yaml.FullLoader)

    serial = find_serial()
    warn_disconnected = False
    connected = False
    running = False
    last_check = running
    current_app = find_app(mappings)
    start = get_time()
    current_app_name = ""

    while True:
        await asyncio.sleep(0.01)  # to allow other tasks to run
        if warn_disconnected:
            print("Disconnected")
            warn_disconnected = False
            running = False

        if not find_device():
            if connected:
                warn_disconnected = True
                connected = False
            serial = find_serial()
            continue

        connected = True

        now = get_time()
        if now > start + CHECK_APP_SECONDS:
            start = now
            running = is_running(current_app)
            with (FILE_DIR / "mappings.yaml").open() as map_file:
                try:
                    new_mappings = yaml.load(map_file, Loader=yaml.FullLoader)
                except Exception as err:
                    print(err)
                else:
                    if new_mappings != mappings:
                        mappings = new_mappings
                        last_check = False

        if not running:
            if last_check:
                send_serial(serial, "\n")
                print(f"{current_app_name} closed")
            current_app = find_app(mappings)
            running = is_running(current_app)
            if running:
                current_app_name = get_proc_exe_name(current_app)
                print(f"Found app {current_app_name}")
            last_check = False
            continue

        if not last_check and running:
            try:
                keymap = mappings[current_app_name]
            except KeyError:
                running = False
            else:
                keymap = {
                    str(key).upper(): str(value).upper()
                    for key, value in keymap.items()
                }
                print("Sending map")
                send_serial(serial, json.dumps(keymap))
                last_check = True

        await asyncio.sleep(5)
