# Untitled - By: williamvanuitert - Wed Jan 24 2024

import sensor, image, time
import machine
from machine import Pin
from pyb import UART

#sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
#sensor.set_framesize(sensor.QVGA)
#sensor.skip_frames(time = 2000)


# commenting out, moving to __init__
#tx_rx_pin = machine.Pin("P3", Pin.OUT)
#tx_rx_pin.value(0)# "active high" 1 means enable transmit


# not using this on new transceiver because there's only one pin
#tx_rx_pin.value(1)
#rx_pin = machine.Pin("P2", Pin.OUT)

clock = time.clock()

#pins = ControlPins(id=1, baud_rate=921600, bits=8, parity=0, stop=1)
class ControlPins():
    def __init__(self, cam_id, baud_rate, bits, serialPortParity, stopBits, timeout_char):
        self.cam_id = cam_id
        self.baud_rate = baud_rate
        self.bits = bits
        self.serialPortParity = serialPortParity
        self.stopBits = stopBits
        self.timeout_char = timeout_char
        self.tx_rx_pin = machine.Pin("P3", Pin.OUT)
        self.tx_rx_pin.value(0)# "active high" 1 means enable transmit
        self.uart = UART(3, 921600, bits=8, parity=0, stop=1, timeout_char=2000)

        #self.rx_pin.value(0) # "active low" 0 means enable read.


    def transmit(self, message):
        self.tx_rx_pin.value(1)

        #self.rx_pin.value(1)

        uart.write(self.id, "Hello World!\r")
        time.sleep_ms(1000)


    def receive(self):
        print('called rec')

        msg = []

        while True:
            #print('in inner while true')
            output = self.uart.read(1)  # ".read()" by itself doesn't work, there's number of bytes, timeout, etc.
            if not output:
                print('continuing')
                continue
            msg.append(output)
            print(msg)
            if output ==  '\n' or output == '\r' or output == '\r\n':
              break
        print(output)

        if(output[0] != self.id):
            return
            msg = []
        else:
           pass


class Camera():
    def __init__(self, cam_id):
       self.cam_id = cam_id

    def FindAprilTags():
        pass

    def LineDetection():
        pass

    def FindGamePiece():
        pass

pin = ControlPins(1, 921600, 8, 0, 1, 2000)
print('made pin')
cam = Camera(1) #add yavta stuff
while True:
    print('in while tre, outer')
    msg = pin.receive()
    if msg[1] == 'A':
      msg = []
      # do april tag stuff
      print('transmitting')
      pins.transmit(cam.id, "April Tag Data Stuff")


#while(True):
#    clock.tick()
#    img = sensor.snapshot()
#    print(clock.fps())
