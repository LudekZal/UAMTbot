# UAMT_BOT demo - line follow
# Ludek Zalud, 25.6.2025
# HW version: UAMTbot 0.9
# Functions: blinks with blue LED once for 100 ms

from machine import Pin, PWM, I2C
import time

led = Pin(12, Pin.OUT) #blue LED

led.on() #blue LED ON
time.sleep_ms(100)
led.off() #blue LED OFF