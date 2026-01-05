# NeoPixel Test
# HW version: UAMTbot 1.0
# NOTE: library Robot.py must be present on Pico

import time
from Robot import Robot

# --- KONFIGURACE ---
PIN_LED = 22       
POCET_LED = 10    

# init
bot = Robot()

print("DEMO START")


# Ukazka pouziti set_all a clear

bot.leds_all(0, 128, 0) 
time.sleep(0.5)
bot.leds_clear()
time.sleep(1)


# Ukazka metody blink_error
print("Simulace chyby")
bot.leds_error()
time.sleep(1)

# Animace
print("Animace")

for _ in range(3):
    for i in range(1, POCET_LED + 1):
        bot.leds_set(i, 150, 0, 0) 
        time.sleep(0.05)
        bot.leds_set(i, 0, 0, 0)   
        
    for i in range(POCET_LED, 0, -1):
        bot.leds_set(i, 150, 0, 0)
        time.sleep(0.05)
        bot.leds_set(i, 0, 0, 0)
        
time.sleep(1)

# Míchání barev
for i in range(1, POCET_LED + 1):
    r = i * (128 // POCET_LED)
    b = 128 - r
    bot.leds_set(i, r, 0, b)
    time.sleep(0.1)

time.sleep(1)
print("DEMO FINISHED")
bot.leds_clear()
