import pyb  # pylint: disable=import-error

pyb.usb_mode("VCP+HID", hid=pyb.hid_keyboard)
