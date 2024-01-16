# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Robust Linear Regression Example
#
# This example shows off how to use the get_regression() method on your OpenMV Cam
# to get the linear regression of a ROI. Using this method you can easily build
# a robot which can track lines which all point in the same general direction
# but are not actually connected. Use find_blobs() on lines that are nicely
# connected for better filtering options and control.
#
# We're using the robust=True argument for get_regression() in this script which
# computes the linear regression using a much more robust algorithm... but potentially
# much slower. The robust algorithm runs in O(N^2) time on the image. So, YOU NEED
# TO LIMIT THE NUMBER OF PIXELS the robust algorithm works on or it can actually
# take seconds for the algorithm to give you a result... THRESHOLD VERY CAREFULLY!

import sensor
import time

THRESHOLD = (65, 79, -27, -5, -45, -23)
BINARY_VISIBLE = True  # Binary pass first to see what linear regression is running on.

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)  # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
sensor.skip_frames(time=2000)  # WARNING: If you use QQVGA it may take seconds
clock = time.clock()  # to process a frame sometimes.

while True:
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD]) if BINARY_VISIBLE else sensor.snapshot()

    # Returns a line object similar to line objects returned by find_lines() and
    # find_line_segments(). You have x1(), y1(), x2(), y2(), length(),
    # theta() (rotation in degrees), rho(), and magnitude().
    #
    # magnitude() represents how well the linear regression worked. It means something
    # different for the robust linear regression. In general, the larger the value the
    # better...
    line = img.get_regression([(100, 255) if BINARY_VISIBLE else THRESHOLD], robust=True)

    print("X1: " + str(line.line()[0]) + ", X2: " + str(line.line()[2]))
    print("Y1: " + str(line.line()[1]) + ", Y2: " + str(line.line()[3]))

    if line:
        img.draw_line(line.line(), color=(255, 0, 0), thickness=2)

    #print(
     #   "FPS %f, mag = %s" % (clock.fps(), str(line.magnitude()) if (line) else "N/A")
    #)

    def degrees(radians):
        return (180 * radians) / math.pi


# About negative rho values:
#
# A [theta+0:-rho] tuple is the same as [theta+180:+rho].