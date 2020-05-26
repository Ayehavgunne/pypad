from time import sleep

import pyb  # pylint: disable=import-error


class Joystick:
    _X_CENTER = 2055.0
    _Y_CENTER = 2010.0
    _POS_X = 4095.0 - _X_CENTER
    _POS_Y = 4095.0 - _Y_CENTER
    _X_DEADZONE = 45.0
    _Y_DEADZONE = 45.0

    def __init__(self, x, y, b):
        self._jx = pyb.ADC(x)
        self._jy = pyb.ADC(y)
        self._jb = pyb.Pin(b, pyb.Pin.IN, pyb.Pin.PULL_DOWN)
        self._x = 0
        self._y = 0

    @property
    def x(self):
        """Return value from -1.0 to 1.0."""
        x = self._jx.read() - self._X_CENTER
        if abs(x) > self._X_DEADZONE:
            return x / self._POS_X
        return 0

    @property
    def y(self):
        """Return value from -1.0 to 1.0."""
        y = self._jy.read() - self._Y_CENTER
        if abs(y) > self._Y_DEADZONE:
            return y / self._POS_Y
        return 0

    @property
    def button(self):
        """return True or False."""
        return not self._jb.value()


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

vcp = pyb.USB_VCP()
switches = {
    num: pyb.Pin(pin, pyb.Pin.IN, pyb.Pin.PULL_DOWN) for num, pin in PINS.items()
}
joystick = Joystick("Y12", "Y11", "X10")


while True:
    active_switches = []
    for num, switch in switches.items():
        if num in (28, 10, 9, 27):  # wiring issues, skipping over for now
            continue
        if switch.value():
            active_switches.append(str(num))
    if active_switches and not vcp.any():
        vcp.send(",".join(active_switches).encode("utf-8"), timeout=50)
    x_value = joystick.x
    y_value = joystick.y
    vcp.send(b"|")
    if x_value:
        vcp.send("x:{}".format(x_value).encode("utf-8"))
        if y_value:
            vcp.send(b",")
    if y_value:
        vcp.send("y:{}".format(y_value).encode("utf-8"))
    vcp.send(b"\r\n", timeout=50)
