# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor
import time
import math

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
clock = time.clock()  # Create a clock object to track the FPS.

while True:
    clock.tick()  # Update the FPS clock.
    img = sensor.snapshot()  # Take a picture and return the image.
    #print(clock.fps())  # Note: OpenMV Cam runs about half as fast when connected
    # to the IDE. The FPS should increase once disconnected.

    x_coor = [-140, 120]
    y_coor = [-50, 30]
    f_x = [x_coor[0] + 160, x_coor[1] + 160]
    f_y = [-y_coor[0] + 120, -y_coor[1] + 120]
    #img.draw_line(320, 120, 0, 120, color=(255, 0, 0), thickness=1) #draws a line in the middle of the screen for referance

    img.draw_line(f_x[0], f_y[0], f_x[1], f_y[1], color=(0, 255, 0), thickness=2) #test line acting like tape

    img.draw_circle(f_x[0], f_y[0], 4, color=(0, 0, 255), fill=True)
    img.draw_circle(f_x[1], f_y[1], 4, color=(0, 0, 255), fill=True)

    if(f_y[0] >= f_y[1]):
        img.draw_line(0, f_y[0], 320, f_y[0], color=(255, 0, 0), fill=True)
    elif(f_y[0] <= f_y[1]):
        img.draw_line(0, f_y[1], 320, f_y[1], color=(255, 0, 0), fill=True)

    x_dist = abs(f_x[1] - f_x[0])
    y_dist = abs(f_y[1] - f_y[0])
    theta = math.atan(y_dist/x_dist) * (180/math.pi)
    print(theta)



