#!/bin/python3

import sensor
import image
import time
import math
import sys
import os
from pyb import UART
from machine import Pin
import machine
import mjpeg

import camnet

uart = UART(3, 2000000, bits=8, parity=0, stop=1, timeout_char=2000)  # default (200) was too low

control_pin = Pin("P3", Pin.OUT)
control_pin.value(0)  # 0 should be receive

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.


sc = camnet.SerialComms('1')


while True:
    output = uart.readline()  # ".read()" by itself doesn't work, there's number of bytes, timeout, etc.
    #output = uart.read(4)
    #print(output)
    #output_as_string = str(output)
    #print(output_as_string)
    if output == b'ti\n':
        print('got teleop init')
        #sc.transmit(['somedata', 'more', '\n'])


        led = machine.LED("LED_RED")

        led.on()

        #files = os.listdir()
        #for filename in filenames:
        #    splitted = filename.split('.')
        #    num = splitted[1]

        #if "example.mjpeg" in files:
        #    filename = "example2.mjpeg"
        m = mjpeg.Mjpeg("telope1.mjpeg")
        print(dir(m))

        #clock = time.clock()  # Create a clock object to track the FPS.
        for i in range(50):
            #clock.tick()
            m.add_frame(sensor.snapshot())
            #print(clock.fps())

        print(os.getcwd())
        print('you were supposed to see files by now')
        print(os.listdir())
        machine.reset()
    elif output == b'ai\n':
        print('got autonomous init')
    elif output == b'di\n':
        print('got disable init')
        m.close()
        led.off()
    elif output is None:
        #continue
        print(output)
    #else:
    #    print(f'got something weird: {output}')
    time.sleep_ms(500)
