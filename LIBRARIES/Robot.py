# David Hanák
# HW version: UAMTbot 1.0
# NOTE: display must be connected to P17
# NOTE: library sh1106.py must be present on PICO
import machine
import time
from machine import Pin, PWM, SoftI2C, I2C
from sh1106 import SH1106_I2C
from neopixel import NeoPixel

# Constants
LEDS = 10
WIDTH = 128
HEIGHT = 64

class Robot:
# ---------- INIT -------------
    def __init__(self):
        """Inicializace robota"""
        
        # --- 1. LED ---
        self.num_pixels = LEDS 
        self.np = NeoPixel(machine.Pin(22), self.num_pixels)
        self.leds_clear()
        
        # --- 2. Buzzer ---
        self.buzzer_pwm = machine.PWM(machine.Pin(7))
        self.buzzer_pwm.duty_u16(0)
        
        # --- 3. Display ---
        try:
            # Pins 4 (SDA) a 5 (SCL) - SoftI2C
            self.disp_i2c = SoftI2C(sda=machine.Pin(4), scl=machine.Pin(5), freq=100000)
            
            # Display init
            self.display = SH1106_I2C(WIDTH, HEIGHT, self.disp_i2c)
            
            self.display.fill(0)
            self.display.text("UAMT Bot", 30, 20, 1)
            self.display.text("Ready...", 35, 35, 1)
            self.display.show()
            print("Displej OK")
            
        except Exception as e:
            import sys
            print(f"Chyba displeje: {e}")
            sys.print_exception(e)
            self.display = None

# ---------- DISPLAY METHODS -------------
    def display_animate(self):
        """
        Spustí animaci. placeholder
        """
        if not self.display:
            print("Animace přeskočena (není displej)")
            return

        for i in range(0, 35):
            self.display.fill(0)
            

            self.display.fill_rect(96, i, 24, 24, 1) 
                      
            self.display.line(96, i+5, 94, i+5, 1)
            self.display.line(96, i+12, 94, i+12, 1)
            self.display.line(96, i+19, 94, i+19, 1)
            
            self.display.line(50, 32, 96, i+12, 1)

            self.display.text("UAMT_BOT", 5, 5, 1)
            self.display.text("**DEMO**", 5, 15, 1)
            self.display.text("v 1.0", 5, 50, 1)
            
            self.display.show()
            time.sleep_ms(5) 

    def display_battery(self, percent):
        """
        Vykreslí baterii v rohu

        param: percent: procentuální výplň baterie 
        """
        if self.display:
            self.display.rect(100, 0, 20, 10, 1)
            width = int(18 * (percent / 100))
            self.display.fill_rect(101, 1, width, 8, 1) 
            self.display.show()

# ---------- LED METHODS -------------
    def leds_clear(self):
        """ Zhasne všechny diody """
        self.np.fill((0, 0, 0))
        self.np.write()
        
    def leds_set(self, led_num: int, r: int, g: int, b: int, show=True):
        """
        Nastaví barvu vybrané LED podle číslování na desce
        
        param: led_num: Číslo LED (1 - LEDS)
        """
        if 1 <= led_num <= self.num_pixels:
            self.np[led_num - 1] = (r, g, b)
            if show:
                self.np.write()
        else:
            print("LED mimo rozsah 1-10")
            
    def leds_all(self, r: int, g: int, b: int):
        """
        Nastaví barvu celého pásku najednou.
        
        :param r: Červená složka (0-255)
        :param g: Zelená složka (0-255)
        :param b: Modrá složka (0-255)
        """
        self.np.fill((r, g, b))
        self.np.write()
        
    def leds_error(self):
        """ Světelná indikace chyby """
        for _ in range(3):
            self.leds_all(128, 0, 0)
            time.sleep(0.2)
            self.leds_clear()
            time.sleep(0.2)
            
# ---------- BUZZER METHODS -------------
    def buzzer_beep(self, freq=1000, duration=0.1):
        """ Pípnutí """

        self.buzzer_pwm.freq(freq)
        self.buzzer_pwm.duty_u16(3000)
        time.sleep(duration)
        self.buzzer_pwm.duty_u16(0)
        
    def buzzer_tone(self, frequency: int, duration: float, volume: int = 2000):
        """
        Přehraje tón
        
        :param frequency: Frekvence tónu
        :param duration: Délka tónu
        :param volume: Hlasitost (default = 2000)
        """
        if frequency < 50:
            self.pwm.duty_u16(0)
            return
        
        self.buzzer_pwm.freq(int(frequency))
        self.buzzer_pwm.duty_u16(volume)
        time.sleep(duration)
        self.buzzer_pwm.duty_u16(0)
        time.sleep(0.05)
        
# ---------- MOTORS METHODS -------------