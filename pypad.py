import json

# import pyxinput
import sys
import time
from typing import Any, Optional, Set, Tuple

import psutil
import yaml
from serial import Serial
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo

CHECK_APP_SECONDS = 5
BAUD_RATE = 115200
MY_DEVICE_ID = "VID:PID=F055:9801"
# DEBUG_MODE = False


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
        print("Connected                    ")
        return serial
    except SerialException:
        return None


def get_time() -> float:
    return time.time()


def read_serial(serial: Serial) -> Optional[str]:
    try:
        serial.reset_input_buffer()
        result = serial.readline()
    except SerialException:
        return None
    try:
        result = result.decode("utf-8").strip()
        if result:
            if result.startswith("report: ") or result.startswith("syntax"):
                print(result)
            return result
    except UnicodeDecodeError:
        return None


def send_serial(serial: Serial, message: Any) -> None:
    try:
        serial.reset_output_buffer()
        serial.write(f"{str(message)}\n".encode("utf-8"))
    except SerialException as err:
        print(err)


# def get_joystick_pos(message: str) -> Optional[Tuple[float, float]]:
#     x = 0
#     y = 0
#     cords = message.split(",")
#     for cord in cords:
#         if "x" in cord:
#             try:
#                 x = float(cord.split(":")[1])
#             except (ValueError, IndexError):
#                 pass
#         if "y" in cord:
#             try:
#                 y = float(cord.split(":")[1])
#             except (ValueError, IndexError):
#                 pass
#     return x, y


# def to_vjoy_int(coord: float) -> int:
#     return int((coord + 1) * 0x4000)


# def get_buttons(message: str) -> Optional[Set[str]]:
#     return set(int(button) for button in message.split("|")[0].split(",") if button)


def main() -> None:
    with open("mappings.yaml") as map_file:
        mappings = yaml.load(map_file, Loader=yaml.FullLoader)
    serial = find_serial()
    warn_disconnected = False
    connected = False
    running = False
    last_check = running
    current_app = find_app(mappings)
    start = get_time()
    # joystick = pyxinput.vController()

    while True:
        if warn_disconnected:
            print("Disconnected")
            warn_disconnected = False
            running = False

        if not find_device():
            time.sleep(5)
            if connected:
                warn_disconnected = True
                connected = False
            serial = find_serial()
            continue

        connected = True

        if not running:
            time.sleep(5)
            current_app = find_app(mappings)
            running = is_running(current_app)
            if is_running and current_app:
                current_app_name = get_proc_exe_name(current_app)
                print(f"Found app {current_app_name}            ")
            last_check = False
            continue

        # having trouble with games recognizing a virtual xbox controller
        # using https://github.com/bayangan1991/PYXInput
        # message = read_serial(serial)
        # if message:
        #     x, y = get_joystick_pos(message)
        #     # joystick.set_value('AxisLx', x)
        #     # joystick.set_value('AxisLy', y)
        #     if DEBUG_MODE:
        #         print(
        #             f"X:{x:.4f}\tY:{y:.4f}", end="\r",
        #         )

        if last_check != running and running:
            keymap = mappings[current_app_name]
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
                print(f"{current_app_name} closed")


if __name__ == "__main__":
    print("Starting up")
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down            ")
        sys.exit(0)
