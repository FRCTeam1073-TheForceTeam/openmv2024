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
#import camnet

from camid import CAMID  # TODO: make CAMIDs regular strs not b''
print(f'camera id: {CAMID}')

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
sensor.set_vflip(False)
sensor.set_hmirror(True)

# Always pass UART 3 for the UART number for your OpenMV Cam.
# The second argument is the UART baud rate. For a more advanced UART control
# example see the BLE-Shield driver.
uart = UART(3, 2000000, bits=8, parity=0, stop=1, timeout_char=2000)  # default (200) was too low
control_pin = Pin("P3", Pin.OUT)
control_pin.value(0)  # 0 should be receive
#sc = camnet.SerialComms('1')

def compute_filename(prefix):  # prefix is 'ti' or 'ai'
    infixes = [1]  # the suffix will be '.mjpeg', the number is the "infix" because it goes in between prefix and suffix, like "ti.5.mjpeg"
    for filename in os.listdir():
        if 'mjpeg' not in filename:
            continue
        splitted = filename.split('.')
        if len(splitted) == 3 and splitted[1].isdigit():
            existing_infix_int = int(splitted[1])
            infixes.append(existing_infix_int)

    infixes.sort()  # .sort() is in-place
    # infixes[-1] is now the highest number of the files that already exist
    infix = infixes[-1] + 1
    filename = f'{prefix}.{infix}.mjpeg'
    return filename

def transmit(output): #TODO code for camera to reply to rio
    control_pin.value(1)
    for element in output:
        uart.write(element)
        uart.write(',')
    uart.write('\n')
    control_pin.value(0)

m = None
while True:
    #transmit('camera')
    #print('top of while')
    #print(uart.any())
    if uart.any() > 0:
        print(f'uart.any(): {uart.any()}')
        msg = uart.readline()  # ".read()" by itself doesn't work, there's number of bytes, timeout, etc.
        msg = msg.decode('ascii').strip()
        print(f'msg: {msg}')
        if msg[0] != CAMID:
            print(f"we got a msg but it's not for our camid ({CAMID}): {msg}")
        #elif msg == bytes(f'{CAMID},ti\n', 'ascii'):  #b'1,ti\n'
        elif msg == f'{CAMID},ti':
            led = machine.LED("LED_RED")
            led.on()
            print('got teleop init')
            filename = compute_filename('ti')
            m = mjpeg.Mjpeg(filename)
            #transmit(b'ti')
        #elif msg == b'ai\n':
        elif msg == f'{CAMID},ai':
            led = machine.LED("LED_RED")
            led.on()
            print('got auto init')
            filename = compute_filename('ai')
            m = mjpeg.Mjpeg(filename)
            #transmit(b'ai')
        #elif msg == b'di\n':
        #elif msg == bytes(f'{CAMID},di\n', 'ascii'):
        elif msg == f'{CAMID},di':
            print("got di")
            if m is not None:  # if already disabled, do nothing
                m.close()
                m = None
                led.off()
                #transmit(b'di')
                #machine.reset()

        else:
            print("It didn't work")
            print(f'{CAMID},ai')
    # done with msg handling, do video
    print(m)
    if m:
        m.add_frame(sensor.snapshot())
        print('added frame')
    #time.sleep_ms(50)
    time.sleep_ms(50)
