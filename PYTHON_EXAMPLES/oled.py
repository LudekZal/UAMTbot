# UAMT_BOT demo - line follow
# Ludek Zalud, 26.6.2025
# HW version: UAMTbot 0.9
# Functions: OLED display with SH1106 driver demo
# NOTE: the display has to be physically connected to I2C(0)
# NOTE: library sh1106.py must be present on PICO

from machine import I2C, ADC
from sh1106 import SH1106_I2C
import framebuf
import time

WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height

i2c = I2C(0)                                            # Init I2C using I2C0 defaults, SCL=Pin(GP9), SDA=Pin(GP8), freq=400000
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config


oled = SH1106_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display

# Raspberry Pi logo as 32x32 bytearray
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

# Load the raspberry pi logo into the framebuffer (the image is 32x32)
fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

while True:
    for i in range(0, 40):
        oled.fill(0)
        oled.blit(fb, 96, i)
        oled.rect(96, i, 30, 30, 0xffff)
        oled.line(50, 32, 96, i+15, 0xffff)

        oled.text("UAMT_BOT",5,5)
        oled.text("**DEMO**",5,15)
        oled.show()
        time.sleep_ms(1)