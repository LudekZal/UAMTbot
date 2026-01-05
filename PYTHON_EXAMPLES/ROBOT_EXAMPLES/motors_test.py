# Motors Test
# HW version: UAMTbot 1.0
# NOTE: library Robot.py must be present on PICO
import time
from machine import Pin
from Robot import Robot

# Tlačítko SW7
sw1 = Pin(13, mode=Pin.IN, pull=Pin.PULL_UP)


bot = Robot() # init (inicializace jednotlivých pinů motorů viz Robot.py)

while True:

    val = sw1.value()
    
    # Pokud je stisknuto (0)
    if val == 0:
        print("Tlačítko stisknuto")

        time.sleep(1.0)

        bot.motors_ramp(1000, 1, 1000, 1) 

        time.sleep(1) 

        bot.motors_stop_ramp(1000, 1000)
        time.sleep(0.5) 

        bot.motors(2000, 1, 2000, 0)

        time.sleep(3)

    bot.motors_stop() 