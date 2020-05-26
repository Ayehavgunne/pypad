import sys
import time
from typing import Optional, Set, Tuple

import psutil
import yaml
from serial import Serial
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo

from directx_keys import press_key, release_key

CHECK_APP_SECONDS = 5
BAUD_RATE = 115200
MY_DEVICE_ID = "VID:PID=F055:9800"
DEBUG_MODE = True


def is_running(process: psutil.Process) -> bool:
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
        serial = Serial(port.device, BAUD_RATE, timeout=1)
        print("Connected")
        return serial
    except SerialException:
        return None


def get_time() -> float:
    return time.time()


def read_serial(serial: Serial) -> Optional[str]:
    try:
        return serial.readline().decode("utf-8").strip()
    except SerialException:
        return None


def get_joystick_pos(message: str) -> Optional[Tuple[float, float]]:
    x = 0
    y = 0
    message = message.split("|")
    cords = message[1].split(",")
    for cord in cords:
        if "x" in cord:
            x = float(cord.split(":")[1])
        if "y" in cord:
            y = float(cord.split(":")[1])
    return x, y


def get_buttons(message: str) -> Optional[Set[str]]:
    return set(int(button) for button in message.split("|")[0].split(",") if button)


def main() -> None:
    mappings = yaml.load(open("mappings.yaml"), Loader=yaml.FullLoader)
    serial = find_serial()
    while True:
        if find_device():
            current_app = find_app(mappings)
            if current_app:
                current_app_name = get_proc_exe_name(current_app)
                print(f"Found app {current_app_name}")
                serial.reset_input_buffer()
                running = True
                keymap = mappings[current_app_name]
                previous_buttons = set()
                start = get_time()

                while running:
                    message = read_serial(serial)
                    buttons = get_buttons(message)
                    x, y = get_joystick_pos(message)
                    if buttons is None:
                        break
                    elif DEBUG_MODE:
                        print(
                            f"{', '.join(str(button) for button in buttons)} X:{x} Y:{y}                                                             ",
                            end="\r",
                        )

                    for button in previous_buttons - buttons:
                        if button in keymap:
                            release_key(keymap[button].upper().split("+"))
                    for button in buttons - previous_buttons:
                        if button in keymap:
                            press_key(keymap[button].upper().split("+"))

                    previous_buttons = buttons

                    now = get_time()
                    if now > start + CHECK_APP_SECONDS:
                        start = now
                        running = is_running(current_app)
                print(f"{current_app_name} stopped running")
            else:
                time.sleep(5)

            if not find_device():
                print("Disconnected")
        else:
            time.sleep(5)
            serial = find_serial()


if __name__ == "__main__":
    print("Starting up")
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down")
        sys.exit(0)
