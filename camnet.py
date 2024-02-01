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
#import numpy as np
import random

CAM_ID = '1'


class SerialComms():
    def __init__(self, cam_id, baud_rate = 1000000, bits = 8, parity = 0, stop = 1, timeout_char = 2000):
        self.cam_id = cam_id
        self.baud_rate = baud_rate
        self.bits = bits
        self.parity = parity
        self.stop = stop
        self.timeout_char = timeout_char
        #self.uart = UART(3, self.baud_rate, self.bits, self.parity, self.stop, self.timeout_char)
        self.uart = UART(3, baudrate=self.baud_rate, bits=self.bits, parity=self.parity, stop=self.stop, timeout_char=self.timeout_char)

        self.control_pin = Pin("P3", Pin.OUT)
        self.control_pin.value(0)

    def transmit(self, payload):
        self.control_pin.value(1)
        for element in payload:
            self.uart.write(element)
            self.uart.write(',')

        self.uart.write('1,' + payload)
        #time.sleep_ms(1000)
        self.control_pin.value(0)


class Camera():
    def __init__(self):
        pass

    def apriltags(self, args=6):
        num_apriltags = 1 #change to call april tag stuff
        answer = [0] * args * num_apriltags
        for array_length in range(len(answer)):
            answer[array_length] = random.randint(1, 10)
        #answer = np.array(([0]*args)*num_apriltags)

        #for answer_rows in range(args):
            #for answer_colunms in range (num_apriltags):
                #answer[args][num_apriltags] = random.randint(1, 10) #change to call april tag stuff

    def gamepiece(self):
        pass


# Always pass UART 3 for the UART number for your OpenMV Cam.
# The second argument is the UART baud rate. For a more advanced UART control
# example see the BLE-Shield driver.

serialcomms = SerialComms(1)
camera = Camera()
array = []
while True:
    output = serialcomms.uart.read(1)  # ".read()" by itself doesn't work, there's number of bytes, timeout, etc.
    print(output)
    array.append(output)
    time.sleep_ms(500)

    if output ==  '\n' or output == '\r' or output == '\r\n':
        continue
    results = array[0]
    if(results != CAM_ID):
        array = []
        continue
    else:
        if(array[2] == 'a'):
            response = camera.apriltags()
        elif(array[2] == 'g'):
            response = camera.gamepiece()
        response = array[0] + ',' + array[2] + response
        serialcomms.transmit(response)

