# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# AprilTags Example
#
# This example shows the power of the OpenMV Cam to detect April Tags
# on the OpenMV Cam M7. The M4 versions cannot detect April Tags.

import sensor
import image
import time
import math
import sys
import os
from pyb import UART
from machine import Pin
import machine
import struct

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(True)  # must turn this off to prevent image washout...
clock = time.clock()
uart = UART(3, 2000000, bits=8, parity=0, stop=1, timeout_char=2000)  # default (200) was too low
control_pin = Pin("P3", Pin.OUT)
control_pin.value(0)

# Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

# The apriltag code supports up to 6 tag families which can be processed at the same time.
# Returned tag objects will have their tag family and id within the tag family.

tag_families = 0
tag_families |= image.TAG16H5  # comment out to disable this family
tag_families |= image.TAG25H7  # comment out to disable this family
tag_families |= image.TAG25H9  # comment out to disable this family
tag_families |= image.TAG36H10  # comment out to disable this family
tag_families |= image.TAG36H11  # comment out to disable this family (default family)
tag_families |= image.ARTOOLKIT  # comment out to disable this family

# What's the difference between tag families? Well, for example, the TAG16H5 family is effectively
# a 4x4 square tag. So, this means it can be seen at a longer distance than a TAG36H11 tag which
# is a 6x6 square tag. However, the lower H value (H5 versus H11) means that the false positive
# rate for the 4x4 tag is much, much, much, higher than the 6x6 tag. So, unless you have a
# reason to use the other tags families just use TAG36H11 which is the default family.


def family_name(tag):
    if tag.family() == image.TAG16H5:
        return "TAG16H5"
    if tag.family() == image.TAG25H7:
        return "TAG25H7"
    if tag.family() == image.TAG25H9:
        return "TAG25H9"
    if tag.family() == image.TAG36H10:
        return "TAG36H10"
    if tag.family() == image.TAG36H11:
        return "TAG36H11"
    if tag.family() == image.ARTOOLKIT:
        return "ARTOOLKIT"

def transmit(output): #TODO code for camera to reply to rio
    print(f'raw output arg to transmit(): {output} type: {type(output)}')
    #output = output.encode('ascii')
    output_strings = []
    for i in range(len(output)):  # ['TAGWHATEVER', '11.01', 1']
        output_strings.append(str(output[i]))
    control_pin.value(1)
    for output_string in output_strings:
        for character in output_string:
            uart.write(character)
        uart.write(',')
    uart.write('\n')
    print('should have just sent a newline')
    control_pin.value(0)


def get_camid():
    for filename in os.listdir():
        print(filename)
        splitted = filename.split('-')
        if len(splitted) == 2:
            if splitted[0] == 'camid':
                return splitted[1]
CAMID = get_camid()

while True:
    if uart.any() > 0:
        print(f'uart.any(): {uart.any()}')
        msg = uart.readline()  # ".read()" by itself doesn't work, there's number of bytes, timeout, etc.
        msg = msg.decode('ascii').strip()
        print(f'msg: {msg}')
        if msg[0] != CAMID:
            print("Not for us")
        elif msg ==  f'{CAMID},ap':
            look = True
            while look == True:
                img = sensor.snapshot()
                for tag in img.find_apriltags(families=tag_families):  # defaults to TAG36H11 without "families".
                    img.draw_rectangle(tag.rect(), color=(255, 0, 0))
                    img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0))
                    print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi, tag.cx(), tag.cy(), tag.h(), tag.w())
                    print("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)
                    transmit(print_args)
                    #transmit(struct.pack(print_args))
                    #transmit('1,a')

                    if(img.find_apriltags()):
                        look = False
        else:
            print("It doesn't work")
    time.sleep_ms(500)

