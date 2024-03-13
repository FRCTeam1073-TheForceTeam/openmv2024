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
uart = UART(1, 1000000, bits=8, parity=0, stop=1, timeout=30, timeout_char=30)
control_pin = Pin("P3", Pin.OUT)
control_pin.value(0)  # 0 should be receive
print('Done setting uart and pins.')


# Allocate packet buffers:
input_buffer = bytearray(8)
response_buffer = bytearray(8)

def get_camid():
    for filename in os.listdir():
        print(filename)
        splitted = filename.split('-')
        if len(splitted) == 2:
            if splitted[0] == 'camid':
                return splitted[1]


def transmitAprilTag(camid, cmd, output):
    print(f'raw output arg to transmit(): {output} type: {type(output)}')
    response_buffer[0] = 0   #ID out rio
    response_buffer[1] = cmd # Cmd responding to
    response_buffer[2] = output[0]  #Found Tag ID
    response_buffer[3] = output[1]  #X center
    response_buffer[4] = output[2]  #Y Center
    response_buffer[5] = output[3]  #Area

    control_pin.value(1)
    uart.write(response_buffer)
    uart.flush()   # Wait for bytes to all send before we drop the transmit line.
    control_pin.value(0)


camid = get_camid()
print(f'camid: {camid}')
if not camid:
    print('camid got messed up somehow')
    sys.exit(1)

while True:
    tid = 0
    byte_count = uart.any()
    print(f'byte_count: {byte_count}')
    if byte_count >= 1:
        # As soon as we get a byte we start reading all 8 bytes.
        bytes_read = uart.readinto(input_buffer, 8)

        if bytes_read == None:
            print("Read timeout...")
            continue
        else:
            print(f'msg: {input_buffer}')

        # Extract camera ID and command byte from input buffer.
        msg_camid = input_buffer[0]
        cmd = input_buffer[1]

        # Check if this message is for us.
        if msg_camid != camid:
            print(f"Not for camid ({camid})")
        elif cmd == 3:   # Find apriltag command is 3
            tid = input_buffer[2]   # 3rd byte is which tag ID to find.
            print(f'find tid: {tid}')
            img = sensor.snapshot()
            found = False
            for tag in img.find_apriltags():  # defaults to TAG36H11 without "families".
                if tag.id() == tid:
                    img.draw_rectangle(tag.rect(), color=(255, 0, 0))
                    tag_data = (tag.id(), (tag.cx() /4), (tag.cy() /4), (tag_area /64))
                    print("Found Tag ID %d, CX %i, CY %i, Area %i" % tag_data)
                    transmit(camid, cmd, tag_data)
                    found = True
                    break

            # If we never found the match then we send a "not found" message.
            if found == False:
                transmit(camid, cmd, (0xFF, 0, 0, 0))
        else:
            print(f"Unknow command: {cmd}")
            # Send a response from us even if unknown.
            transmit(camid, cmd, (0xFF, 0, 0, 0))

    time.sleep_ms(10)
