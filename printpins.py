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
from pyb import UART

# Always pass UART 3 for the UART number for your OpenMV Cam.
# The second argument is the UART baud rate. For a more advanced UART control
# example see the BLE-Shield driver.
# uart = UART(3, 19200, bits=8, parity=0, stop=1, timeout_char=200)

uart = UART(3, 19200, bits=8, parity=0, stop=1, timeout_char=200)
tx_pin = machine.Pin("P3", Pin.OUT)
rx_pin = machine.Pin("P2", Pin.OUT)
tx_pin.value(1)
rx_pin.value(0)
configs = 'config vals'

print('about to loop')
while True:
    #print('looping')
    #print(f'any: {uart.any()}')
    input = UART.read(uart)
    #print(f'type: {type(input)}')
    print(input)
