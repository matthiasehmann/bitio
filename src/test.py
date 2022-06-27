#-------------------------------------------------------------------------------
# Name:        test.py
# Purpose:
#
# Author:
#
# Created:     11.05.2022
# Copyright:   (c)  2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import microbit
import time
from libs.neopixel import NeoPixel

##p : Pixel2
##
##class Pixel2(Pixel):
##    def lauflicht(self):
##        self.einschalten()


class Pixel:
    x: int
    y: int
    helligkeit: int

    def __init__(self, neues_x: int, neues_y: int, neue_helligkeit: int):
        self.x = neues_x
        self.y = neues_y
        self.helligkeit = neue_helligkeit
        self.einschalten();

    def einschalten(self):
        microbit.display.set_pixel(self.x,self.y,self.helligkeit)
        print(microbit.display.get_pixel(self.x,self.y))

    def ausschalten(self):
        microbit.display.clear()


def test_pixel():
    p1 = Pixel(1,0,2)

def test_digitalPin(p):
##    p.set_pull(p.PULL_UP)
##    while True:
##        print(p.read_digital())
##        time.sleep(0.1)
    print(p.get_mode())
    p.write_digital(1)

def test_display():
    microbit.display.on()
    print(microbit.display.is_on())
    print(microbit.display.read_light_level())
    microbit.display.off()
    print(microbit.display.is_on())

def test_analogPin(p):
    #print(p.read_analog())
    p.write_analog(200)

def test_neopixel():
    neo = NeoPixel(microbit.pin0, 8)
    neo.clear()
    neo[0] = (128,128,0)
    neo[1] = (0,128,128)
    neo.show()

def test_accelerometer():
    print(microbit.accelerometer.get_gestures())

def test_audio():
    microbit.audio.play(microbit.Sound.GIGGLE)
    microbit.audio.play(microbit.Sound.HELLO)

def test_music():
   # microbit.music.play(['c1:4','d1:4','e1:8'])
    microbit.music.play('c1:4')

def test_pin_logo():
    while True:
        print(microbit.pin_logo.is_touched())
#test_display()
#test_digitalPin(microbit.pin5)
#test_analogPin(microbit.pin0)
#test_accelerometer()
#test_neopixel()
##test_audio()
test_pin_logo()

##def vl():
##    microbit.display.clear()
##    for i in range(0,5):
##        microbit.display.set_pixel(i,i,i)
##    while True:
##        for i in range(0,9):
##            microbit.display.set_pixel(0,0,i)
##            microbit.sleep(300)
##        for i in range(9,0,-1):
##            microbit.display.set_pixel(0,0,i)
##            microbit.sleep(300)


##vl()
# END
