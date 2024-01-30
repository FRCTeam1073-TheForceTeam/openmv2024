# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# UART Control
#
# This example shows how to use the serial port on your OpenMV Cam. Attach pin
# P4 to the serial input of a serial LCD screen to see "Hello World!" printed
# on the serial LCD display.

import time
from pyb import UART
from machine import Pin

# Always pass UART 3 for the UART number for your OpenMV Cam.
# The second argument is the UART baud rate. For a more advanced UART control
# example see the BLE-Shield driver.
uart = UART(3, 2000000, bits=8, parity=0, stop=1, timeout_char=2000)  # default (200) was too low

control_pin = Pin("P3", Pin.OUT)
control_pin.value(0)  # 0 should be receive

while True:
    output = uart.readline()  # ".read()" by itself doesn't work, there's number of bytes, timeout, etc.
    print(output)
    time.sleep_ms(500)

