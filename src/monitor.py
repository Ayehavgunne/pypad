from dataclasses import dataclass
import json
import logging
import getpass
import os
import time
from pathlib import Path
import signal
from typing import Optional, Union
import psutil
import termios
import yaml
import subprocess
from dotenv import find_dotenv, load_dotenv
from serial import Serial
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo

load_dotenv(find_dotenv(filename="../.myenv"))

logger = logging.getLogger(__name__)
log_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
file_handler = logging.FileHandler("./pypad.log")
file_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

FILE_DIR = Path(__file__).parent
BAUD_RATE = int(os.getenv("BAUD_RATE", 115200))
last_modified = 0


def find_device(device_id: str) -> ListPortInfo | None:
    for port in comports():
        if device_id in port.hwid:
            return port


def find_serial(device_id: str) -> Serial | None:
    try:
        port = find_device(device_id)
        if not port:
            return None
        serial = Serial(port.device, BAUD_RATE, timeout=1, write_timeout=0.005)
        logger.info("Connected")
        return serial
    except SerialException as err:
        logger.error(err)
        return None


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


def find_app_proc(mappings: dict) -> psutil.Process | None:
    for proc in psutil.process_iter():
        for exe_name in mappings.keys():
            try:
                proc_file_name = get_proc_exe_name(proc).lower()
                if exe_name.lower() == proc_file_name:
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass


def get_mapping_file_contents(map_file: Path) -> dict:
    return yaml.load(map_file.open(), Loader=yaml.FullLoader)


def get_key_map(keymap: dict) -> str:
    return json.dumps(
        {str(key).upper(): str(value).upper() for key, value in keymap.items()}
    )


def detect_file_changes(file_path: Path) -> float:
    return file_path.lstat().st_mtime


def send_serial(serial: Serial, message: str) -> bool:
    try:
        serial.reset_output_buffer()
        serial.write(f"{message}\n".encode("utf-8"))
        logger.info("Done")
        return True
    except (AttributeError, SerialException, termios.error) as err:
        logger.error(err)
        return False


def change_logiops_cfg_file(file_name: str | None = None) -> None:
    user = getpass.getuser()
    link_path = f"/home/{user}/logid.cfg"
    subprocess.run(["rm", link_path])
    if file_name:
        subprocess.run(["ln", "-s", f"/home/{user}/code/pypad/src/logiops_cfgs/{file_name}.cfg", link_path])
    else:
        subprocess.run(["ln", "-s", f"/home/{user}/logid-default.cfg", link_path])
    subprocess.run(["systemctl", "--user", "restart", "logid"])


@dataclass
class EventData:
    pass


@dataclass
class ConnectedEventData(EventData):
    serial: Serial


@dataclass
class RunningEventData(EventData):
    app_name: str
    app_map: dict
    serial: Serial


@dataclass
class NotRunningEventData(EventData):
    serial: Serial


@dataclass
class Event:
    name: str
    data: EventData | None


class State:
    def on_event(self, event: Event) -> "State":
        pass

    def run(self) -> None:
        pass


class AppState(State):
    pass


class Running(AppState):
    def __init__(self, event_data: RunningEventData) -> None:
        self.app_name = event_data.app_name
        self.app_map = event_data.app_map
        self.serial = event_data.serial
        self.map_sent = False
        self.logid_sent = False

    def on_event(self, event: Event) -> Optional[Union["NotRunning", "Running", "MapFileChanged"]]:
        if event.name == "not_running":
            return NotRunning(event.data)
        if event.name == "map_file_changed":
            return MapFileChanged(event.data)

    def run(self) -> None:
        if not self.map_sent:
            logger.info("Sending keymap to device...")
            keymap = get_key_map(self.app_map)
            self.map_sent = send_serial(self.serial, keymap)
        if not self.logid_sent and (FILE_DIR / "logiops_cfgs" / f"{self.app_name}.cfg").exists:
            logger.info("Reloading logid with game specific config")
            change_logiops_cfg_file(self.app_name)
            self.logid_sent = True


class MapFileChanged(Running):
    pass


class NotRunning(AppState):
    def __init__(self, event_data: NotRunningEventData) -> None:
        self.serial = event_data.serial
        self.map_sent = False

    def on_event(self, event: Event) -> Running | None:
        if event.name == "running":
            return Running(event.data)

    def run(self) -> None:
        if not self.map_sent:
            logger.info("No app running. Clearing keymap from device...")
            self.map_sent = send_serial(self.serial, "\n")
            change_logiops_cfg_file()


class DeviceState(State):
    pass


class Connected(DeviceState):
    def __init__(self, event_data: ConnectedEventData) -> None:
        self.serial = event_data.serial
        self.state: AppState = NotRunning(NotRunningEventData(self.serial))
        self.map_file = FILE_DIR / "mappings.yaml"
        self.mappings = get_mapping_file_contents(self.map_file)
        self.last_modified = detect_file_changes(self.map_file)
        self.current_app_name = ""

    def on_event(self, event: Event) -> Optional["Disconnected"]:
        if event.name == "disconnected":
            logger.info("Disconnected")
            return Disconnected()

    def on_connected_event(self, event: Event) -> None:
        self.state = self.state.on_event(event) or self.state

    def run(self) -> None:
        current_app = find_app_proc(self.mappings)
        running = is_running(current_app)

        if running and not isinstance(self.state, Running):
            self.current_app_name = get_proc_exe_name(current_app)
            logger.info(f"Found app {self.current_app_name}")
            self.on_connected_event(
                Event(
                    "running",
                    RunningEventData(self.current_app_name, self.mappings[self.current_app_name], self.serial),
                )
            )
        elif running and self.last_modified != detect_file_changes(self.map_file):
            self.last_modified = detect_file_changes(self.map_file)
            logger.info("Map file changed")
            self.mappings = get_mapping_file_contents(self.map_file)
            if self.current_app_name in self.mappings:
                self.on_connected_event(
                    Event(
                        "map_file_changed",
                        RunningEventData(self.current_app_name, self.mappings[self.current_app_name], self.serial),
                    )
                )
            else:
                logger.info(f"{self.current_app_name} was removed")
                self.current_app_name = ""
                self.on_connected_event(
                    Event("not_running", NotRunningEventData(self.serial))
                )
        elif not running and not isinstance(self.state, NotRunning):
            logger.info(f"{self.current_app_name} closed")
            self.current_app_name = ""
            self.on_connected_event(
                Event("not_running", NotRunningEventData(self.serial))
            )

        self.state.run()


class Disconnected(DeviceState):
    def on_event(self, event: Event) -> Connected | None:
        if event.name == "connected":
            return Connected(event.data)


class Device:
    def __init__(self) -> None:
        self.state: DeviceState = Disconnected()
        self.stop = False
        self.device_id = os.getenv("DEVICE_ID")
        self.poll_interval = int(os.getenv("CHECK_APP_SECONDS", 5))
        self.serial = find_serial(self.device_id)

        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)

    def exit(self, signum, frame):
        self.stop = True

    def on_event(self, event: Event) -> None:
        self.state = self.state.on_event(event) or self.state

    def run(self) -> None:
        logger.info("Starting up")

        while not self.stop:
            if not find_device(self.device_id):
                self.on_event(Event("disconnected", None))
            elif not isinstance(self.state, Connected):
                self.serial = find_serial(self.device_id)
                self.on_event(Event("connected", ConnectedEventData(self.serial)))

            self.state.run()

            time.sleep(self.poll_interval)

        while not (send_serial(self.serial, "\n")):
            logger.info("Having trouble clearing keymap from device...")
            time.sleep(0.5)

        logger.info("Shutting down")


if __name__ == "__main__":
    device = Device()
    device.run()
