#!/bin/bash

FILES=/dev/hidraw*
MOUSE=""
for f in $FILES
do
    FILE=${f##*/}
    DEVICE="$(cat /sys/class/hidraw/${FILE}/device/uevent | grep HID_NAME | cut -d '=' -f2)"
    if [[ "$DEVICE" == "Logitech Wireless Mouse MX Master 3" ]]; then
    	echo $FILE $DEVICE
    	MOUSE=$FILE
    	break
    fi
    if [[ "$DEVICE" == "Logitech MX Master 3 for Mac" ]]; then
    	echo $FILE $DEVICE
    	MOUSE=$FILE
    	break
    fi
done

if [[ ! -z $MOUSE ]]; then
	sudo chgrp uucp /dev/$MOUSE
	sudo chmod 660 /dev/$MOUSE
	systemctl --user restart logid
fi
