import asyncio
import json
import time
from pathlib import Path
from typing import Any, Optional

import psutil
import yaml
from dotenv import find_dotenv, load_dotenv
from serial import Serial
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo

load_dotenv(find_dotenv(filename=".myenv"))
from config_man.config_man import start_server  # isort:skip


CHECK_APP_SECONDS = 5
BAUD_RATE = 115200
MY_DEVICE_ID = (Path(__file__).parent / ".my_device_id").open().readline().strip()


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


async def main() -> None:
    loop = asyncio.get_event_loop()
    loop.create_task(start_server())

    with open("mappings.yaml") as map_file:
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

        if not running:
            current_app = find_app(mappings)
            running = is_running(current_app)
            if is_running and current_app:
                current_app_name = get_proc_exe_name(current_app)
                print(f"Found app {current_app_name}")
            last_check = False
            continue

        if last_check != running and running:
            keymap = mappings[current_app_name]
            keymap = {
                str(key).upper(): str(value).upper() for key, value in keymap.items()
            }
            print("Sending map")
            send_serial(serial, json.dumps(keymap))
            last_check = running

        now = get_time()
        if now > start + CHECK_APP_SECONDS:
            start = now
            last_check = running
            running = is_running(current_app)
            with open("mappings.yaml") as map_file:
                new_mappings = yaml.load(map_file, Loader=yaml.FullLoader)
                if new_mappings != mappings:
                    mappings = new_mappings
                    last_check = not running
            if not running:
                send_serial(serial, "\n")
                print(f"{current_app_name} closed")

        await asyncio.sleep(5)


if __name__ == "__main__":
    print("Starting up")
    asyncio.run(main())
