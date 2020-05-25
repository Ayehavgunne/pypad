import sys
import time
from typing import Optional, Set

import json5
import psutil
from serial import Serial
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo

from directx_keys import press_key, release_key

CHECK_APP_SECONDS = 5
MY_DEVICE_ID = "VID:PID=F055:9800"


def is_running(process_name: str) -> str:
    for proc in psutil.process_iter():
        try:
            proc_file_name = proc.exe().replace("\\", "/").split("/")[-1].lower()
            if process_name.lower() in proc_file_name:
                return proc_file_name
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def find_app(mappings: dict) -> Optional[str]:
    for exe_name in mappings.keys():
        if is_running(exe_name):
            return exe_name


def find_device() -> ListPortInfo:
    for port in comports():
        if MY_DEVICE_ID in port.hwid:
            return port


def find_port() -> Optional[Serial]:
    try:
        port = find_device()
        if not port:
            return None
        serial = Serial(port.device, 115200, timeout=1)
        print("Connected")
        return serial
    except SerialException:
        return None


def get_time() -> float:
    return time.time()


def get_buttons(serial: Serial) -> Optional[Set[str]]:
    try:
        return set(serial.readline().decode("utf-8").strip().split(","))
    except SerialException:
        return None


def main() -> None:
    mappings = json5.load(open("mappings.json5"))
    serial = find_port()
    while True:
        if find_device():
            current_app = find_app(mappings)
            if current_app:
                print(f"Found app {current_app}")
                start = get_time()
                keymap = mappings[current_app]
                previous_buttons = set()

                while current_app:
                    buttons = get_buttons(serial)
                    if buttons is None:
                        break

                    for button in previous_buttons - buttons:
                        if button in keymap:
                            release_key(keymap[button].upper().split('+'))
                    for button in buttons - previous_buttons:
                        if button in keymap:
                            press_key((keymap[button].upper().split('+')))

                    previous_buttons = buttons

                    now = get_time()
                    if now > start + CHECK_APP_SECONDS:
                        start = now
                        current_app = find_app(mappings)
            else:
                time.sleep(5)

            if not find_device():
                print("Disconnected")
        else:
            time.sleep(5)
            serial = find_port()


if __name__ == "__main__":
    print("Starting up")
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down")
        sys.exit(0)
