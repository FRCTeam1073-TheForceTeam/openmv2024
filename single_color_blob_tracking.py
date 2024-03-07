# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Single Color RGB565 Blob Tracking Example
#
# This example shows off single color RGB565 tracking using the OpenMV Cam.

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

threshold_index = 0  # 0 for red, 1 for green, 2 for blue

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...
thresholds = [(10, 90, 50, 74, 38, 58)]  #orange note color

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must be turned off for color tracking
sensor.set_auto_whitebal(False)  # must be turned off for color tracking
uart = UART(3, 2000000, bits=8, parity=0, stop=1, timeout_char=2000)  # default (200) was too low
control_pin = Pin("P3", Pin.OUT)
control_pin.value(0)  # 0 should be receive
clock = time.clock()

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

def transmit(output): #TODO code for camera to reply to rio
    control_pin.value(1)
    for element in output:
        uart.write(element)
        uart.write(',')
    uart.write('\n')
    control_pin.value(0)

while True:
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs(
        [thresholds[threshold_index]],
        pixels_threshold=200,
        area_threshold=1000,
        merge=True,
        margin=150
    ):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        if blob.elongation() > 0.5:
            img.draw_edges(blob.min_corners(), color=(255, 0, 0))
            img.draw_line(blob.major_axis_line(), color=(0, 255, 0))
            img.draw_line(blob.minor_axis_line(), color=(0, 0, 255))
        # These values are stable all the time.
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        # Note - the blob rotation is unique to 0-180 only.
        img.draw_keypoints(
            [(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20
        )
        print(f'X Translation: {blob.cx()}')
        print(f'Y Translation: {blob.cy()}')
        print(f'Pixels of Color:{blob.pixels()}')
        print(f'Density: {round(blob.density() * 100, 2)}%')
    #print(clock.fps())
