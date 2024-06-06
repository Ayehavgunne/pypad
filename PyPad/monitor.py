import asyncio
import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Optional

import psutil
import termios
import yaml
from dotenv import find_dotenv, load_dotenv
from serial import Serial
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo

load_dotenv(find_dotenv(filename="../.myenv"))
# from PyPad.config_man.config_man import start_server  # isort:skip

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="/var/log/pypad.log",
    format="%(asctime)s %(levelname)s: %(message)s",
    encoding="utf-8",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

FILE_DIR = Path(__file__).parent

CHECK_APP_SECONDS = 5
BAUD_RATE = 115200
MY_DEVICE_ID = os.getenv("DEVICE_ID")
last_modified = 0


def detect_file_changes(file_path: Path) -> float:
    return file_path.lstat().st_mtime


def is_running(process: psutil.Process) -> bool:
    if not process:
        return False
    try:
        return process.status() in (
            psutil.STATUS_RUNNING,
            psutil.STATUS_SLEEPING,
            psutil.STATUS_DISK_SLEEP,
            psutil.STATUS_WAKING,
            psutil.STATUS_PARKED,
            psutil.STATUS_LOCKED,
            psutil.STATUS_IDLE,
            psutil.STATUS_WAITING,
        )
    except psutil.NoSuchProcess:
        return False


def get_proc_exe_name(process: psutil.Process) -> str:
    return process.name().split(".")[0]


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
        logger.info("Connected")
        return serial
    except SerialException as err:
        logger.error(err)
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


def send_serial(serial: Serial, message: Any) -> bool:
    try:
        serial.reset_output_buffer()
        serial.write(f"{str(message)}\n".encode("utf-8"))
        logger.info("Done")
        return True
    except (AttributeError, SerialException, termios.error) as err:
        logger.error(err)
        return False


def get_key_map(keymap: dict) -> str:
    return json.dumps(
        {
            str(key).upper(): str(value).upper() for key, value in keymap.items()
        }
    )


async def main() -> None:
    # loop = asyncio.get_event_loop()
    # loop.create_task(start_server())

    map_file = FILE_DIR / "mappings.yaml"
    mappings = yaml.load(map_file.open(), Loader=yaml.FullLoader)
    last_modified = detect_file_changes(map_file)

    serial = find_serial()
    warn_disconnected = False
    connected = False
    running = False
    last_check = running
    current_app = find_app(mappings)
    start = get_time()
    current_app_name = ""
    map_sent = False

    while True:
        if warn_disconnected:
            logger.info("Disconnected")
            warn_disconnected = False
            running = False
            map_sent = False

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
                logger.info(f"Found app {current_app_name}")
            last_check = False
            if not running:
                map_sent = False
            continue

        if last_check != running and running and not map_sent:
            keymap = get_key_map(mappings[current_app_name])
            logger.info("Sending map...")
            map_sent = send_serial(serial, keymap)
            last_check = running

        now = get_time()
        if now > start + CHECK_APP_SECONDS:
            start = now
            last_check = running
            running = is_running(current_app)
            if not running:
                logger.info(f"{current_app_name} closed")
                logger.info("Clearing map...")
                keymap = "\n"
                map_sent = False
            if running and not map_sent:
                logger.info("Sending map...")
            if running and last_modified != detect_file_changes(map_file):
                last_modified = detect_file_changes(map_file)
                mappings = yaml.load(map_file.open(), Loader=yaml.FullLoader)
                keymap = get_key_map(mappings[current_app_name])
                logger.info("Map changed. Sending map...")
            if not map_sent:
                map_sent = send_serial(serial, keymap)

        await asyncio.sleep(5)


if __name__ == "__main__":
    try:
        logger.info("Starting up")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down")
