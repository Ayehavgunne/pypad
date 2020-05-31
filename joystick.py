import pyb  # pylint: disable=import-error


class Joystick:
    _X_CENTER = 2050.0
    _Y_CENTER = 2010.0
    _POS_X = 4095.0 - _X_CENTER
    _POS_Y = 4095.0 - _Y_CENTER
    _X_DEADZONE = 45.0
    _Y_DEADZONE = 45.0

    def __init__(self, x, y, b):
        self._jx = pyb.ADC(x)
        self._jy = pyb.ADC(y)
        self._jb = pyb.Pin(b, pyb.Pin.IN, pyb.Pin.PULL_DOWN)

    @property
    def x(self):
        """Return value from -1.0 to 1.0."""
        x = self._jx.read() - self._X_CENTER
        if abs(x) > self._X_DEADZONE:
            x = x / self._POS_X
            return x if x >= -1 else -1
        return 0

    @property
    def y(self):
        """Return value from -1.0 to 1.0."""
        y = self._jy.read() - self._Y_CENTER
        if abs(y) > self._Y_DEADZONE:
            y = y / self._POS_Y
            return y if y >= -1 else -1
        return 0

    @property
    def button(self):
        """return True or False."""
        return not self._jb.value()
