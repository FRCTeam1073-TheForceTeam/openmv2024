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
led = machine.LED("LED_RED")
led_g = machine.LED("LED_GREEN")
led_b = machine.LED("LED_BLUE")

led_g.on()
def get_camid():
    for filename in os.listdir():
        print(filename)
        splitted = filename.split('-')
        if len(splitted) == 2:
            if splitted[0] == 'camid':
                return splitted[1]

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

#def family_name(tag):
#    if tag.family() == image.TAG16H5:
#        return "TAG16H5"
#    if tag.family() == image.TAG25H7:
#        return "TAG25H7"
#    if tag.family() == image.TAG25H9:
#        return "TAG25H9"
#    if tag.family() == image.TAG36H10:
#        return "TAG36H10"
#    if tag.family() == image.TAG36H11:
#        return "TAG36H11"
#    if tag.family() == image.ARTOOLKIT:
#        return "ARTOOLKIT"


def transmit(camid, cmd, output): #TODO code for camera to reply to rio
    print(f'raw output arg to transmit(): {output} type: {type(output)}')
    #output = output.encode('ascii')
    output_strings = []
    for i in range(len(output)):  # ['TAGWHATEVER', '11.01', 1']
        output_strings.append(str(output[i]))
    control_pin.value(1)
    output_strings = [camid, cmd] + [output_strings]
    print(f'output strings list: {output_strings}')
    for output_string in output_strings:
        print(f'output string being transmitted: {output_string}')
        for character in output_string:
            uart.write(character)
        uart.write(',')
    uart.write('\n')
    print('should have just sent a newline')
    control_pin.value(0)



m = None
camid = get_camid()
print(f'camid: {camid}')
if not camid:
    print('camid got messed up somehow')
    sys.exit(1)
while True:
    img = sensor.snapshot()
    tid = 0
    if uart.any() > 0:
        print(f'uart.any(): {uart.any()}')
        try:
            msg = uart.readline()  # ".read()" by itself doesn't work, there's number of bytes, timeout, etc.
            msg = msg.decode('ascii').strip()
        except UnicodeError:
            print("Unicode Error; Don't care")
            continue
            # 1,ap,11\n
        cmd_args = msg.split(',')
        msg_camid = cmd_args[0]
        cmd = cmd_args[1]
        print(f'msg: {msg}')
        print(f'cmd_args: {cmd_args}')
        print(f'cmd: {cmd}')
        if msg_camid != camid:
            print(f"we got a msg but it's not for our camid ({camid}): {msg}")
        #elif msg == bytes(f'{CAMID},ti\n', 'ascii'):  #b'1,ti\n'
        elif msg == f'{camid},ti':
            led_g.off()
            led_b.off()
            led.on()
            print('got teleop init')
            filename = compute_filename('ti')
            m = mjpeg.Mjpeg(filename)
        #elif msg == f'{camid},ap,{tid}':
        elif cmd == 'ap':
            found_tags = []
            tid = int(cmd_args[2])
            led = machine.LED("LED_RED")
            led.off()
            led_g.off()
            led_b.on()
            img = sensor.snapshot()
            for tag in img.find_apriltags():  # defaults to TAG36H11 without "families".
                #[(4,1,65,7918,33)]
                if tag.id() == tid or tid == 0:
                    img.draw_rectangle(tag.rect(), color=(255, 0, 0))
                    img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0))
                    tag_area = (tag.w() * tag.h())
                    print_args = (tag.id(), tag.cx(), tag.cy(), tag_area)
                    print("Tag ID %d, Tag Cener X %i, Tag Center Y %i, Tag Area %i" % print_args)
                    found_tags.append(print_args)
                else:
                    print(f"wrong tag ID. expected: {tid} got: {tag.id()}")
            print(f'done iterating through tags, transmitting {found_tags}')
            transmit(camid, cmd, found_tags)
            print(f'done transmitting found tags')
            led_b.off()
        elif msg == f'{camid},ai':
            led = machine.LED("LED_RED")
            led_g.off()
            led_b.on()
            led.on()
            print('got auto init')
            filename = compute_filename('ai')
            m = mjpeg.Mjpeg(filename)
        elif msg == f'{camid},di':
            print("got di")
            if m is not None:  # if already disabled, do nothing
                m.close()
                m = None
                led.off()
                led_g.off()
                led_b.off()

        else:
            print("It didn't work")
    # done with msg handling, do video
    #print(m)
    #if m:
    #    m.add_frame(sensor.snapshot())
    #    print('added frame')
    #print('sleeping')
    time.sleep_ms(50)
    #time.sleep_ms(200)
