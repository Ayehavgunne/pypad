#!/bin/bash

FILES=/dev/hidraw*
for f in $FILES
do
	FILE=${f##*/}
	DEVICE="$(cat /sys/class/hidraw/${FILE}/device/uevent | grep HID_NAME | cut -d '=' -f2)"
	echo $FILE $DEVICE
done
