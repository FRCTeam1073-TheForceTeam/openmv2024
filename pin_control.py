# Untitled - By: williamvanuitert - Wed Jan 24 2024

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

Class GetPins(id, baut_rate, pin1, pin2, dataBits, serialPortParity, stopBits):
    def __init__(self):
        name = self.id
        rate = self.baut_rate
        pin2 = self.pin1
        pin3 = self.pin2
        bits = self.dataBits
        parity = self.serialPortParity
        stop = self.stopBits

    def transmit():
        pass

    def recieve():
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


while(True):

    clock.tick()
    img = sensor.snapshot()
    #print(clock.fps())
