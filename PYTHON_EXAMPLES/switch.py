# UAMT_BOT demo - line follow
# Ludek Zalud, 26.6.2025
# HW version: UAMTbot 0.9
# Functions: press SW1 to light blue LED, press SW2 to beep twice, press SW3 to light blue LED and beep

from machine import Pin, PWM, I2C
import time

#switches
sw1 = Pin(13, mode=Pin.IN, pull=Pin.PULL_UP)
sw2 = Pin(14, mode=Pin.IN, pull=Pin.PULL_UP)
sw3 = Pin(15, mode=Pin.IN, pull=Pin.PULL_UP)

led = Pin(12, Pin.OUT) #blue LED

buz_pwm = PWM(Pin(7)) #buzzer

while(True):
    if(sw1.value() == 0): #switch 1 pressed, lit LED
        led.on()
    else:
        led.off()        
    if(sw2.value() == 0): #switch 2 pressed, make 2 beeps
        print("SW2_PRESS")       
        buz_pwm.duty_u16(10000)
        buz_pwm.freq(442)
        time.sleep_ms(200)
        buz_pwm.duty_u16(10000)
        buz_pwm.freq(884)
        time.sleep_ms(200)              
        buz_pwm.duty_u16(0) #switch off PWM
        buz_pwm.freq(1000)
    if(sw3.value() == 0): #switch 3 pressed, make sound and light
        led.on()
        buz_pwm.duty_u16(10000)
        buz_pwm.freq(442)        
    else:
        led.off()
        buz_pwm.duty_u16(0) #switch off PWM
        buz_pwm.freq(1000)