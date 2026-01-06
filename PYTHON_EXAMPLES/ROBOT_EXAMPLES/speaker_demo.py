# Speaker Test
# HW version: UAMTbot 1.0
# NOTE: library Robot.py must be present on Pico

import time
from Robot import Robot

bot = Robot() # inicializace (speaker -> pin 7)

print("DEMO START")

bot.buzzer_beep(1000, 0.1)
time.sleep(0.1)
bot.buzzer_beep(2000, 0.1)

time.sleep(1)

for freq in range(200, 3000, 100):
    bot.buzzer_tone(freq, 0.02, volume = 3000)
    
time.sleep(1)

for freq in range(3000, 100, -100):
    bot.buzzer_tone(freq, 0.02) # při vynechání výchozí hodnota volume = 2000
    
time.sleep(1)

for _ in range(3):
    bot.buzzer_tone(600, 0.3)
    bot.buzzer_tone(1200, 0.3)

time.sleep(1)

bot.buzzer_tone(988, 0.08)
bot.buzzer_tone(1319, 0.3)

bot.buzzer_pwm.duty_u16(0)
print("DEMO FINISHED")