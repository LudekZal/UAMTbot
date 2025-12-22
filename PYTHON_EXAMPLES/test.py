from Robot import Robot
import time


bot = Robot()
print("Inicializace robota")
time.sleep(1)

bot.display_battery(45)

# 3. Test LED
bot.leds_set(1, 0, 255, 0)
time.sleep(1)
bot.leds_set(5, 0, 0, 255)
time.sleep(1)

bot.leds_clear()
bot.leds_all(50,50,50)
time.sleep(1)
bot.leds_clear()


# Animace
bot.display_animate()
bot.display.fill(0)
bot.display.show()

bot.leds_error()

bot.buzzer_tone(1000, 0.5)
time.sleep(1)
bot.buzzer_beep()

print("Konec testu")
