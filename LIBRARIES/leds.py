import machine
import time
from machine import Pin
from pio_neopixel import Neopixel
import time

from core import debug_print

class Leds:
    """
    Třída pro ovládání adresovatelného RGB LED pásku.
    
    Umožňuje individuální i hromadné nastavení barev jednotlivých diod.
    
    Při volání 'robot.leds.func' lze využívat funkce z knihovny 'neopixel.py'.
    """
    def __init__(self, pin=22, num_pixels=10):
        self.is_connected = False
        self.num_pixels = num_pixels
        self.pin = pin
        try:
            self.np = Neopixel(self.num_pixels, 0, self.pin) # Původní inicializace     
            self.np.fill((0, 0, 0))
            self.np.show()
            self.is_connected = True 
            debug_print(f"[LEDS] Inicializace LED")
        except Exception as e:
            debug_print(f"[VAROVANI] Chyba inicializace LED: {e}")

    def clear(self):
        """ Zhasne všechny diody """
        if not self.is_connected:
            return
        self.np.fill((0, 0, 0))
        self.np.show()
        debug_print(f"[LEDS] Zhasnutí všech LED")
        
    def set(self, led_num: int, r: int, g: int, b: int, show=True):
        """
        Nastaví barvu vybrané LED podle číslování na desce
        
        :param led_num: Číslo LED (1 - LEDS)
        :param r: Červená složka (0-255)
        :param g: Zelená složka (0-255)
        :param b: Modrá složka (0-255)
        :param show: Rozsvítit okamžitě (výchozí hodnota = True)

        .. note::
           Jako číslo LED použijte označení na desce (LED 1 - 10)
        """
        if not self.is_connected:
            return
        
        if 1 <= led_num <= self.num_pixels:
            self.np[led_num - 1] = (g, r, b)
            
            if show:
                self.np.show()
                debug_print(f"[LEDS] LED {led_num} rozsvícena na hodnotu hodnotu ({r}, {g}, {b})")
            else:
                debug_print(f"[LEDS] Nastavena hodnota ({r}, {g}, {b}) na LED {led_num}")
        else:
            debug_print("LED mimo rozsah 1-10")

            
    def all(self, r: int, g: int, b: int):
        """
        Nastaví barvu celého pásku najednou.
        
        :param r: Červená složka (0-255)
        :param g: Zelená složka (0-255)
        :param b: Modrá složka (0-255)
        """
        if not self.is_connected:
            return
        
        self.np.fill((g, r, b))
        self.np.show()
        debug_print(f"[LEDS] Všechny LED rozsvíceny (RGB: {r},{g},{b})")
        
    def error(self):
        """ Světelná indikace chyby - 3x blikne """
        if not self.is_connected:
            return
        debug_print(f"[LEDS] LED error")
        for _ in range(3):
            self.all(128, 0, 0)
            time.sleep(0.2)
            self.clear()
            time.sleep(0.2)
            
    def __getattr__(self, func):
        """ Zachycuje funkce, které nejsou součástí knihovny leds.py a hledá, jestli se nenachází v knihovně neopixel.py"""
        if hasattr(self.np, func):
            debug_print(f"[LEDS] Použita funkce {func} z knihovny neopixel")
            return getattr(self.np, func)
        
        def nonexistent(*args, **kwargs):
            debug_print(f"[LEDS] Funkce {func} nenalezena")
            pass
        return nonexistent
        