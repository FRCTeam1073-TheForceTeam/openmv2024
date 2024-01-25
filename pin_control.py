# Untitled - By: williamvanuitert - Wed Jan 24 2024

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

#tx_pin = machine.Pin("P3", Pin.OUT)s
#rx_pin = machine.Pin("P2", Pin.OUT)

clock = time.clock()

Class GetPins(id, baud_rate, pin1, pin2, dataBits, serialPortParity, stopBits):
    def __init__(self):
        self.id = name
        self.baud_rate = rate
        self.tx_pin = pin1
        self.rx_pin = pin2
        self.dataBits = bits
        self.serialPortParity = parity
        self.stopBits = stop

        self.tx_pin.value(0)# "active high" 1 means enable transmit
        self.rx_pin.value(0) # "active low" 0 means enable read.


    def transmit():
        pass

    def recieve():

        msg = []

        while True:
            output = uart.read(1)  # ".read()" by itself doesn't work, there's number of bytes, timeout, etc.
            msg.append(output)
            if output ==  '\n':
              break
        print(output)

        if(output[0] != self.id):
            return
        else:
            pass


Class Camera(id):
    def __init__(self):
        name = self.id

    def FindAprilTags():
        pass

    def LineDetection():
        pass


    def FindGamePiece():
        pass

cam = Camera(1, yavtastuff)
while True:
    msg = waitformsg()
    if msg[1] == 'A':
      # do april tag stuff

while(True):

    clock.tick()
    img = sensor.snapshot()
    #print(clock.fps())
