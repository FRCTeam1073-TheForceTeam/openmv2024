#!/bin/python3

import sensor
import image
import time
import math
import sys
import os
#from pyb import UART
from machine import Pin, UART
# I guess the rt1060 doesn't have pyb shrug man emoji
import machine
import mjpeg
#import camnet

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
#sensor.set_vflip(False)
#sensor.set_hmirror(True)
print(f'done with sensor {time.time()}')



# Always pass UART 3 for the UART number for your OpenMV Cam.
# unless it's the rt1060 on peppersass then it's 1.
# see pinout diagram https://openmv.io/products/openmv-cam-rt
# The second argument is the UART baud rate. For a more advanced UART control
# example see the BLE-Shield driver.
uart = UART(1, 1000000, bits=8, parity=0, stop=1, timeout_char=2000)  # default (200) was too low
control_pin = Pin("P3", Pin.OUT)
control_pin.value(0)  # 0 should be receive
print('done setting uart and pins.')

def get_camid():
    for filename in os.listdir():
        print(filename)
        splitted = filename.split('-')
        if len(splitted) == 2:
            if splitted[0] == 'camid':
                return splitted[1]


def transmitAprilTag(camid, cmd, output):
    print(f'raw output arg to transmit(): {output} type: {type(output)}')
    response = bytearray(8)
    response[0] = 0   #ID out rio
    response[1] = cmd # Cmd responding to
    response[2] = output[0]  #Found Tag ID
    response[3] = output[1]  #X center
    response[4] = output[2]  #Y Center
    response[5] = output[3]  #Area

    control_pin.value(1)
    uart.write(response)
    uart.flush()
    control_pin.value(0)

input_buffer = bytearray(8)

camid = get_camid()
print(f'camid: {camid}')
if not camid:
    print('camid got messed up somehow')
    sys.exit(1)

while True:
    img = sensor.snapshot()
    tid = 0
    byte_count = uart.any()
    print(f'byte_count: {byte_count}')
    if byte_count >= 8:
        bytes_read = uart.readinto(input_buffer, 8)  # ".read()" by itself doesn't work, there's number of bytes, timeout, etc.
        msg_camid = input_buffer[0]
        cmd = input_buffer[1]
        print(f'msg: {input_buffer}')
        found = False
        if msg_camid != camid:
            print(f"we got a msg but it's not for our camid ({camid})")
        elif cmd == 3:
            tid = input_buffer[2]
            print(f'tid: {tid}')
            img = sensor.snapshot()
            for tag in img.find_apriltags():  # defaults to TAG36H11 without "families".
                if tag.id() == tid:
                    img.draw_rectangle(tag.rect(), color=(255, 0, 0))
                    img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0))
                    tag_data = (tag.id(), (tag.cx() /4), (tag.cy() /4), (tag_area /64))
                    print("Tag ID %d, Tag Cener X %i, Tag Center Y %i, Tag Area %i" % print_args)
                    #found_tags.append(tag_data)
                    transmit(camid, cmd, tag_data)
                    found = True
                    break
            transmit(camid, cmd, (0xFF, 0, 0, 0))
        else:
            print(f"Unknow command: {cmd}")
            transmit(camid, cmd, (0, 0, 0, 0))

    time.sleep_ms(10)
