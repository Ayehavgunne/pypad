from directx_keys import press_key, release_key
import json5
from serial import Serial
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo
import sys
import time
import psutil
from typing import Optional, Set

CHECK_APP_SECONDS = 5
MY_DEVICE_ID = "VID:PID=F055:9800"

print("Starting up")

mappings = json5.load(open("mappings.json5"))
current_app = None


def find_exe(process_name: str) -> str:
    for proc in psutil.process_iter():
        try:
            proc_file_name = proc.exe().replace("\\", "/").split("/")[-1].lower()
            if process_name.lower() in proc_file_name:
                return proc_file_name
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def find_app() -> Optional[str]:
    for exe_name in mappings.keys():
        if find_exe(exe_name):
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


def read_serial(serial: Serial) -> Optional[Set[str]]:
    try:
        return set(serial.readline().decode("utf-8").strip().split(","))
    except SerialException:
        return None


def main():
    serial = find_port()
    while True:
        if find_device():
            current_app = find_app()
            if current_app:
                print(f"Found app {current_app}")
                start = get_time()
                keymap = mappings[current_app]
                previous_buttons = set()

                while current_app:
                    buttons = read_serial(serial)
                    if buttons is None:
                        break

                    for button in previous_buttons - buttons:
                        if button in keymap:
                            release_key(keymap[button].upper())
                    for button in buttons - previous_buttons:
                        if button in keymap:
                            press_key(keymap[button].upper())

                    previous_buttons = buttons

                    now = get_time()
                    if now > start + CHECK_APP_SECONDS:
                        start = now
                        current_app = find_app()
            else:
                time.sleep(5)

            if not find_device():
                print("Disconnected")
        else:
            time.sleep(5)
            serial = find_port()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down")
        sys.exit(0)
