import math
import time
from machine import I2C, Pin
from icm42688 import ICM42688

from core import debug_print

class Imu:
    """
    Třída pro komunikaci s inerciální měřicí jednotkou ICM42688 přes I2C.
    
    Slouží k získávání dat z akcelerometru a gyroskopu pro výpočet orientace, náklonu a zrychlení robota. Třída sama provádí probuzení senzoru a ověřuje dostupnost I2C sběrnice.
    
    Při volání 'robot.imu.func' lze využívat funkce dostupné v knihovně 'icm42688.py', např. 'read_temperature()'.
    """
    def __init__(self, i2c_bus, address = 0x69):
        self.is_connected = False
        
        if i2c_bus is None:
            return
        
        try:
            self.imu = ICM42688(i2c_bus, address = address)
            self.imu.wake()
            self.is_connected = True
            debug_print("[IMU] Modul úspěšně inicializován.")
        
        except Exception as e:
            debug_print(f"[VAROVÁNÍ] Modul IMU neodpovídá (Chyba: {e}).")

    def get_tilt(self):
        """Vrátí náklon (Pitch, Roll)"""
        if not self.is_connected:
            debug_print("[IMU] Senzor je offline (vracím náklon (0, 0)).")
            return (0, 0)
        
        ax, ay, az = self.imu.read_accel_data()
        
        pitch = math.atan2(ay, math.sqrt(ax*ax + az*az)) * 57.3 # přepočet na stupně (180/pi) 
        roll = math.atan2(-ax, az) * 57.3
        debug_print(f"[IMU] Vracím hodnoty pitch a roll")   
        return (pitch, roll)
        
    def check_crash(self, threshold_g = 3.0):
        """
        Zkontroluje, zda nedošlo k nárazu (překročení limitu g)

        :param threshold_g: Prahová hodnota g (výchozí 3.0 g)

        .. note::
           Při použití s motors_set() je možné, že se aktivuje při uvedení do pohybu
        """
        ax, ay, az = self.imu.read_accel_data()
        
        total_accel = (ax**2 + ay**2 + az**2) ** 0.5
        
        if total_accel >= threshold_g:
            debug_print(f"[IMU] Detekován náraz o síle {total_accel:.2f}g")
            return True
        debug_print("[IMU] Náraz nedetekován")
        return False
        
    def __getattr__(self, func):
        # Pokud někdo zavolá např. robot.imu.read_accel_data() napřímo
        if self.is_connected and hasattr(self.imu, func):
            debug_print(f"[IMU] Použita funkce {func} z knihovny ICM42688")
            return getattr(self.imu, func)
            
        def nonexistent(*args, **kwargs):
            debug_print(f"[IMU] Funkce {func} nenalezena")
            pass
        return nonexistent
