# UAMT_BOT demo - line follow
# Ludek Zalud, 26.6.2025
# HW version: UAMTbot 0.9
# Functions: NEOPIXEL LED demo
# NOTE: neopixel.py library has to be present on PICO

import time
from neopixel import Neopixel
from machine import Pin, PWM, I2C

numpix = 10 #number of neopixel LEDs
strip = Neopixel(numpix, 0, 22, "GRB")


for i in range(0,10):
    strip.set_pixel(i, (0, 0, 255))
    time.sleep_ms(50)
    strip.show()

for i in range(0,6):
    strip.set_pixel(i, (0, 255, 0))
    time.sleep_ms(50)
    strip.show()
    
for i in range(0,3):
    strip.set_pixel(i, (255, 0, 0))
    time.sleep_ms(50)
    strip.show()
    
strip.set_pixel(0, (100, 100, 100))
time.sleep_ms(1)
strip.show()