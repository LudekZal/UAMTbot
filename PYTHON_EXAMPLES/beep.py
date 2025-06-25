# UAMT_BOT demo - line follow
# Ludek Zalud, 25.6.2025
# HW version: UAMTbot 0.9
# Functions: beep with buzzer

from machine import Pin, PWM, I2C
import time

buz_pwm = PWM(Pin(7))

buz_pwm.duty_u16(10000)
buz_pwm.freq(442) # frequency - basic A

time.sleep_ms(100) # wait 100 ms

buz_pwm.duty_u16(20000)
buz_pwm.freq(884) # frequency - octave higher A

time.sleep_ms(100) # wait 100 ms

buz_pwm.duty_u16(0) # switch off PWM
