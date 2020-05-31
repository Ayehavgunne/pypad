import ujson  # pylint: disable=import-error
from time import sleep

import pyb  # pylint: disable=import-error

import keys
from joystick import Joystick

keyboard = pyb.USB_HID()
vcp = pyb.USB_VCP()

PINS = {
    1: "X1",
    2: "X2",
    3: "X3",
    4: "X4",
    5: "X5",
    6: "X6",
    7: "X7",
    8: "X8",
    9: "X9",
    # 10: "X10",
    11: "X11",
    12: "X12",
    13: "X17",
    14: "X18",
    15: "X19",
    16: "X20",
    17: "X21",
    18: "X22",
    19: "Y1",
    20: "Y2",
    21: "Y3",
    22: "Y4",
    23: "Y5",
    24: "Y6",
    25: "Y7",
    26: "Y8",
    27: "Y9",
    28: "Y10",
    # 29: "Y11",
    # 30: "Y12",
}

# mappings = {2: "a", 3: "s", 19: "w", 25: "d", 29: "d"}
mappings = {}
switches = {
    num: pyb.Pin(pin, pyb.Pin.IN, pyb.Pin.PULL_DOWN) for num, pin in PINS.items()
}
joystick = Joystick("Y12", "Y11", "X10")


def send_keys(key_list=None):
    if key_list is None:
        key_list = []

    key_list = [key.upper() for key in key_list if key is not None]

    codes = bytearray(8)

    for mod in keys.MOD_NAMES:
        if mod in key_list:
            codes[0] += getattr(keys, mod, keys.NONE)
            key_list = [key for key in key_list if key != mod]

    key_list = [getattr(keys, key_str, keys.NONE) for key_str in set(key_list)]

    if len(key_list) > 6:  # can only send up to 6 keys over USB HID
        key_list = key_list[:6]

    for index, key in enumerate(key_list):
        codes[index + 2] = key

    keyboard.send(codes)


sleep(2)

while True:
    active_switches = []
    for num, switch in switches.items():
        if num in (28, 10, 9, 27):  # wiring issues, skipping over for now
            continue
        if switch.value():
            active_switches.append(num)
    if active_switches:
        send_keys([mappings.get(index) for index in active_switches])
    else:
        send_keys()

    # vcp.send("x:{},y:{}".format(joystick.x, joystick.y).encode("utf-8"), timeout=50)
    # vcp.send(b"\r\n", timeout=50)
    map_data = vcp.readline()
    if map_data:
        vcp.send(b'report: ', timeout=50)
        vcp.send(map_data, timeout=50)
        vcp.send(b'\r\n', timeout=50)
        try:
            mappings = ujson.loads(map_data.decode('utf-8'))
        except ValueError as err:
            vcp.send(str(err).encode('utf-8'), timeout=50)
