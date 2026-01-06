# IMU Test
# HW version: UAMTbot 1.0
# NOTE: display must be connected to P17
# NOTE: libraries sh1106.py and ICM42688.py must be present on PICO

from Robot import Robot
import time

bot = Robot()
bot.display_dashboard()

a = bot.imu.read_gyro_range() # range 0 -> default (+- 2000 dsp)
print(a)
time.sleep(0.5)

bot.imu.write_gyro_range(1)  # změna rozsahu
b = bot.imu.read_gyro_range()
print(b)
time.sleep(0.5)

c = bot.imu.read_temperature()  # měření teploty
print(f"Temperature: {c:.2f}")

pitch, roll = bot.imu_get_tilt()
print(f"Náklon (osa y): {pitch}")
print(f"Náklon (osa x): {roll}")



