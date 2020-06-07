from time import sleep

import keys
import pyb  # pylint: disable=import-error
import ujson  # pylint: disable=import-error
from joystick import Joystick

WASD_MODE = True
debug_mode = False
keyboard = pyb.USB_HID()
vcp = pyb.USB_VCP()

PINS = [
    "X1",
    "X2",
    "X3",
    "X4",
    "X5",
    "X6",
    "X7",
    "X8",
    "X9",
    "X10",
    "X11",
    "X12",
    "X17",
    "X18",
    "X19",
    "X20",
    "X21",
    "X22",
    "Y1",
    "Y2",
    "Y3",
    "Y5",
    "Y6",
    "Y7",
    "Y8",
    "Y9",
    "Y10",
]


def toggle_debug():
    global debug_mode
    debug_mode = not debug_mode


mappings = {}
switches = [pyb.Pin(pin, pyb.Pin.IN, pyb.Pin.PULL_DOWN) for pin in PINS]
joystick = Joystick("Y12", "Y11", "Y4")
active_switches = []
previous_switches = []
usr_switch = pyb.Switch()
usr_switch.callback(toggle_debug)


def send_keys(key_list=None):
    if key_list is None:
        key_list = []

    codes = bytearray(8)

    key_list = [key.upper() for key in key_list if key is not None]

    for mod in keys.MOD_NAMES:
        if mod in key_list:
            codes[0] += getattr(keys, mod, keys.NONE)
            key_list = [key for key in key_list if key != mod]

    key_list = [getattr(keys, key_str, keys.NONE) for key_str in set(key_list)]

    # Can only send up to 6 nom-modifier keys over USB HID even though the USB spec
    # allows for an arbitrary number of keys to be sent. Sending more than 6 characters
    # doesn't seem to work for me here because I am pretty sure somewhere in the C code
    # behind the USB connection it only allows a buffer size of 8 bytes >:(
    # https://www.devever.net/~hl/usbnkro
    if len(key_list) > 6:
        key_list = key_list[:6]

    for index, key in enumerate(key_list):
        codes[index + 2] = key

    keyboard.send(codes)


sleep(2)

while True:
    active_switches = []

    for num, switch in enumerate(switches, start=1):
        if num in (9, 10, 13, 26, 27):  # wiring issues, skipping over for now
            continue
        if switch.value():
            active_switches.append(str(num))

    if WASD_MODE:
        x = joystick.x
        y = joystick.y
        if abs(x) > 0:
            if x < 0:
                active_switches.insert(0, "joy_left")
            else:
                active_switches.insert(0, "joy_right")
        if abs(y) > 0:
            if y < 0:
                active_switches.insert(0, "joy_down")
            else:
                active_switches.insert(0, "joy_up")
    else:
        vcp.send("x:{},y:{}".format(joystick.x, joystick.y).encode("utf-8"), timeout=50)
        vcp.send(b"\r\n", timeout=50)

    if active_switches != previous_switches:
        if debug_mode:
            vcp.send(
                ", ".join(
                    PINS[int(switch)]
                    for switch in active_switches
                    if "joy" not in switch
                ).encode("utf-8"),
                timeout=50,
            )
            vcp.send(b"\r\n", timeout=50)
        send_keys([mappings.get(index) for index in active_switches])

    map_data = vcp.readline()
    if map_data:
        try:
            mappings = ujson.loads(map_data.decode("utf-8"))
        except ValueError as err:
            if debug_mode:
                with open("errors.log", "w") as error_file:
                    error_file.write(str(err))
                    error_file.write("\n")
            pass

    previous_switches = active_switches
