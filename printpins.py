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
import machine

# Always pass UART 3 for the UART number for your OpenMV Cam.
# The second argument is the UART baud rate. For a more advanced UART control
# example see the BLE-Shield driver.
# uart = UART(3, 19200, bits=8, parity=0, stop=1, timeout_char=200)

uart = UART(3, 921600, bits=8, parity=0, stop=1, timeout_char=2000)  # default (200) was too low
tx_pin = machine.Pin("P3", Pin.OUT)
tx_pin.value(0)# "active high" 1 means enable transmit
rx_pin = machine.Pin("P2", Pin.OUT)
rx_pin.value(0) # "active low" 0 means enable read.
configs = 'config vals'

print('about to loop')
while True:
    output = uart.read(1)  # ".read()" by itself doesn't work, there's number of bytes, timeout, etc.
    print(output)
    time.sleep_ms(21)

# next steps:
# objective: read from java AND reply to java e.g. read q (for "query") and return config values
# write something to handle tx/rx
#    PRO TIP: it's easy to make mistakes fiddling with little numbers. do it right once in a function or w/e and use that instead.
# do actual vision!
# start creating/developing skeleton
# in java, build something general for other robot code to use. like, "SerialComms.gamepiece() or whatever, I dunno, you guys figure it out.
