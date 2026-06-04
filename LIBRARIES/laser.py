from machine import Pin, I2C
import time
import vl53l1x
from core import debug_print
class LaserSensor():
    """
    Třída pro oblushu laserového senzoru vzdálenosti (Time-of-Flight) přes I2C.
    
    Funguje jako wrapper nad externí knihovnou vl53l1x.

    :param i2c_bus: Inicializovaná instance sběrnice I2C
    """
    def __init__(self, i2c_bus):
        self.is_connected = False
        try:
            self.sensor = vl53l1x.VL53L1X(i2c_bus)
            debug_print("[LASER] Senzor inicializován")
            self.is_connected = True
        except Exception as e:
            debug_print("[LASER] Chyba inicializace", e)
            
    def distance_mm(self):
        """
        Změří a vrátí aktuální vzdálenost překážky.

        :return: int: Vzdálenost v mm
        """
        if not self.is_connected: return
        
        distance = self.sensor.read()
        return distance
    
    def __getattr__(self, func):
        """
        Zachycuje funkce, které nejsou součástí knihovny laser.py a hledá, jestli se nenachází v knihovně vl53l1x.py
        """
        if self.is_connected and hasattr(self.sensor, func):
            debug_print(f"[LASER] Použita funkce {func} z knihovny vl53l1x")
            return getattr(self.sensor, func)
        
        def nonexistent(*args, **kwargs):
            debug_print(f"[LASER] Funkce {func} nenalezena")
            pass
        return nonexistent
