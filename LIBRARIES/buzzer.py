import machine
import time
from machine import Pin, PWM

from core import debug_print

class Buzzer:
    """
    Třída pro ovládání bzučáku pomocí PWM signálu
    
    Zprostředkovává generování zvukových tónů a akustické signalizace robota.
    """
    
    def __init__(self, pin=7):
        self.is_connected = True
        self.pin = pin
        self.buzzer_pwm = machine.PWM(machine.Pin(self.pin))
        self.buzzer_pwm.duty_u16(0)
        debug_print(f"[BUZZER] Inicializace bzučáku na pinu {self.pin}")

    def beep(self, frequency=1000, duration=0.1):
        """
        Pípnutí

        :param freq: Frekvence (výchozí hodnota = 1000)
        :param duration: Délka pípnutí ve vteřinách (výchozí hodnota = 0.1)
        """
        debug_print(f"[BUZZER] Pípnutí: frekvence {frequency} Hz, délka {duration} s")
        self.buzzer_pwm.freq(frequency)
        self.buzzer_pwm.duty_u16(3000)
        time.sleep(duration)
        self.buzzer_pwm.duty_u16(0)
        
    def tone(self, frequency: int, duration: float, volume: int = 2000):
        """
        Přehraje tón

        :param frequency: Frekvence tónu
        :param duration: Délka tónu
        :param volume: Hlasitost (Výchozí hodnota = 2000)
        
        .. note::
           Pro nejvyšší hlasitost použijte frequency = 2700 Hz a volume = 32768
        """
        if frequency < 50:
            self.buzzer_pwm.duty_u16(0)
            debug_print("[BUZZER] Tón příliš nízký.")
            return
        
        debug_print(f"[BUZZER] Tón: frekvence {frequency} Hz, délka {duration} s, hlasitost {volume}")
        self.buzzer_pwm.freq(int(frequency))
        self.buzzer_pwm.duty_u16(volume)
        time.sleep(duration)
        self.buzzer_pwm.duty_u16(0)
        time.sleep(0.05)
