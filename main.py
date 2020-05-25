import serial
import time

ser = serial.Serial('COM5', 115200, timeout=1)

while ser.is_open:
    signal = ser.readline()
    if signal:
        signal = signal.decode('utf-8').strip()
        print(signal)
