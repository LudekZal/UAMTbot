# OLED Display Test
# HW version: UAMTbot 1.0
# NOTE: libraries Robot.py, sh1106.py and ICM42688.py must be present on PICO

from Robot import Robot
import time

bot = Robot() # init
time.sleep(1)

bot.display_dashboard() # vlastní metody, používá display_xxx
bot.display_battery(67)

time.sleep(2)

bot.display_clear()
time.sleep(0.1)
bot.display.line(10, 40, 120, 40, 2)  # nízkoúrovňové metody, používá display.xxx
bot.display.text("FEKT - UAMTbot", 10, 30)
bot.display.show() # pro zobrazení je třeba volat show()