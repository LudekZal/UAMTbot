"""
Jádro HW vrstvy robota UAMTbot.

Tento modul slouží jako komunikační uzel pro veškerý HW.
Čte nastavení z 'uamtbot_config.py' a inicializuje povolené moduly.
Využívá třídu DummyModule k omezení pádu programu při přístupu k chybějícímu / nepovolenému HW
"""

import uamtbot_config
from machine import Pin, I2C, PWM

# --------------------------------
# Výchozí nastavení pinů, které se použijí, nejsou-li definovány v config
STATUS_LED_PIN = 12

DEFAULT_LED_PIN = 22
DEFAULT_LED_NUM_PIXELS = 10

DEFAULT_BUZZER_PIN = 7

DEFAULT_DISPLAY_I2C_BUS = 0
DEFAULT_DISPLAY_SDA_PIN = 4
DEFAULT_DISPLAY_SCL_PIN = 5

DEFAULT_IMU_I2C_BUS = 1
DEFAULT_IMU_SDA_PIN = 10
DEFAULT_IMU_SCL_PIN = 11

DEFAULT_MOTOR1_DIR = 16
DEFAULT_MOTOR1_PWM = 17
DEFAULT_MOTOR1_SLEEP = 18
DEFAULT_MOTOR2_DIR = 19
DEFAULT_MOTOR2_PWM = 20
DEFAULT_MOTOR2_SLEEP = 21

DEFAULT_LASER_I2C_BUS = 0
DEFAULT_LASER_SDA_PIN = 4
DEFAULT_LASER_SCL_PIN = 5

DEFAULT_MUX_ADC_PIN = 26
DEFAULT_MUX_S0_PIN = 15
DEFAULT_MUX_S1_PIN = 14

DEFAULT_SW7_PIN = 13
DEFAULT_REFLEX_L_PIN = 28
DEFAULT_REFLEX_R_PIN = 27
# --------------------------------

def debug_print(message):
    """
    Vypíše zprávu po provedení funkce do konzole, pokud je v konfiguraci povolen DEBUG_MODE.
    """
    if getattr(uamtbot_config, "DEBUG_MODE", False):
        print(message + "\n")

class DummyModule:
    """
    Záchytný modul pro deaktivované nebo nefunkční periferie.
    
    V případě zachycení funkce vypíše do konzole varování.
    """
    # Při použití vypnutého modulu neshodí program, ale vypíše varování
    def __init__(self, module_name):
        self.module_name = module_name
        self.is_connected = False
    
    def __getattr__(self, func_name):   
        def catch(*args, **kwargs):
            debug_print(f"[VAROVÁNÍ] Ignoruji příkaz {func_name}. Chybí modul {self.module_name}")
        return catch
class Robot:
    """
    Hlavní třída reprezentující HW robota.
    
    Sdružuje všechny senzory a akční členy do jednoho objektu.
    Moduly jsou dostupné jako atributy (např. 'robot.leds', 'robot.motors' atd.).
    """
    
    def __init__(self):
        """
        Inicializuje základní stavovou LED a postupně načítá všechny dostupné moduly podle konfigurace
        
        V případě vypnutí nebo chyby je modul nahrazen DummyModulem.
        """
        led_pin = getattr(uamtbot_config, "STATUS_LED_PIN", 12)
        self.status_led = Pin(led_pin, Pin.OUT)
        self.status_led.value(0)
        self.leds = DummyModule("LEDS") 
        self.buzzer = DummyModule("BUZZER") 
        self.display = DummyModule("DISPLAY") 
        self.motors = DummyModule("MOTORS")
        self.imu = DummyModule("IMU") 
        debug_print("[CORE] Prázdná instance vytvořena, čtu konfigurační soubor")
        
# ----------LED ----------
        if getattr(uamtbot_config, "USE_LEDS", False):
            #from uamt_bot.leds import Leds
            from leds import Leds
        
            pin_led = getattr(uamtbot_config, "LED_PIN", DEFAULT_LED_PIN)
            num_pixels = getattr(uamtbot_config, "NUM_PIXELS", DEFAULT_LED_NUM_PIXELS)
            self.leds = Leds(pin = pin_led, num_pixels=num_pixels)
            debug_print(f"[CORE] Přidán modul LED na pin {pin_led}")
        else:
            self.leds = DummyModule("LED")
            
# ---------- BUZZER ----------
        if getattr(uamtbot_config, "USE_BUZZER", False):
            #from uamt_bot.buzzer import Buzzer
            from buzzer import Buzzer
            
            pin_buzzer = getattr(uamtbot_config, "BUZZER_PIN", DEFAULT_BUZZER_PIN)
            self.buzzer = Buzzer(pin = pin_buzzer)
            debug_print(f"[CORE] Přidán modul Buzzer na pin {pin_buzzer}")
        else:
            self.buzzer = DummyModule("Buzzer")
# ---------- DISPLAY ---------- 
        if getattr(uamtbot_config, "USE_DISPLAY", False ):
            #from uamt_bot.display import Display
            from display import Display
            
            bus_id = getattr(uamtbot_config, "I2C_DISPLAY", DEFAULT_DISPLAY_I2C_BUS)
            sda_pin = getattr(uamtbot_config, "SDA_PIN_DISPLAY", DEFAULT_DISPLAY_SDA_PIN)
            scl_pin = getattr(uamtbot_config, "SCL_PIN_DISPLAY", DEFAULT_DISPLAY_SCL_PIN)
            
            try:
                i2c_disp = I2C(bus_id, sda = Pin(sda_pin), scl = Pin(scl_pin), freq = 400000)
                self.display = Display(i2c_disp)
                
                if self.display.is_connected:
                    debug_print(f"[CORE] Přidán modul Display na pinech SDA = {sda_pin} a SCL = {scl_pin}, ID = {bus_id}")
                else:
                    debug_print(f"[CORE] Display je zapnutý v configu, ale neodpovídá. Vytvářím DummyModule.")
                    self.display = DummyModule("Display")
            except  Exception as e:
                debug_print(f"[CORE] Chyba při vytváření I2C pro displej: {e}")
                self.display = DummyModule("Displej")
        else:
            self.display = DummyModule("Displej")

# ---------- IMU ----------
        if getattr(uamtbot_config, "USE_IMU", False):
            #from uamt_bot.display import Display
            from imu import Imu
            
            bus_id = getattr(uamtbot_config, "I2C_IMU", DEFAULT_IMU_I2C_BUS)
            sda_pin = getattr(uamtbot_config, "SDA_PIN_IMU", DEFAULT_IMU_SDA_PIN)
            scl_pin = getattr(uamtbot_config, "SCL_PIN_IMU", DEFAULT_IMU_SCL_PIN)
            i2c_imu = None
            try:
                i2c_imu = I2C(bus_id, sda = Pin(sda_pin), scl = Pin(scl_pin), freq = 100000)
            except Exception as e:
                debug_print(f"[VAROVÁNÍ] HW chyba I2C pro IMU: {e}")
                
            self.imu = Imu(i2c_imu)
            
            if self.imu.is_connected:
                debug_print(f"[CORE] Přidán modul IMU na pinech SDA = {sda_pin} a SCL = {scl_pin}, ID = {bus_id}")
            else:
                debug_print(f"[VAROVÁNÍ] IMU je zapnutá v configu, ale neodpovídá.")

        else:
            self.imu = DummyModule("IMU")

# ---------- MOTORS ----------
        if getattr(uamtbot_config, "USE_MOTORS", False):
            from motors import Motors
            
            mot1_dir = getattr(uamtbot_config, "MOT1_DIR_PIN", DEFAULT_MOTOR1_DIR)
            mot1_pwm = getattr(uamtbot_config, "MOT1_PWM_PIN", DEFAULT_MOTOR1_PWM)
            mot1_sleep = getattr(uamtbot_config, "MOT1_SLEEP_PIN", DEFAULT_MOTOR1_SLEEP)
            
            mot2_dir = getattr(uamtbot_config, "MOT2_DIR_PIN", DEFAULT_MOTOR2_DIR)
            mot2_pwm = getattr(uamtbot_config, "MOT2_PWM_PIN", DEFAULT_MOTOR2_PWM)
            mot2_sleep = getattr(uamtbot_config, "MOT2_SLEEP_PIN", DEFAULT_MOTOR2_SLEEP)
            
            self.motors = Motors(mot1_dir, mot1_pwm, mot1_sleep, mot2_dir, mot2_pwm, mot2_sleep)
            
            if self.motors.is_connected:
                debug_print("[CORE] Přidán modul Motors")
            else:
                debug_print("[VAROVÁNÍ] Motory jsou zapnuté v configu, ale HW chyba. Vytvářím DummyModule.")
                self.motors = DummyModule("Motory")
        else:
            self.motors = DummyModule("Motory")
            
# ---------- LASER DISTANCE SENSOR (VL53L1X) ----------
        if getattr(uamtbot_config, "USE_LASER", False):
            from laser import LaserSensor
            
            bus_id_laser = getattr(uamtbot_config, "I2C_LASER", DEFAULT_LASER_I2C_BUS)
            sda_pin_laser = getattr(uamtbot_config, "SDA_PIN_LASER", DEFAULT_LASER_SDA_PIN)
            scl_pin_laser = getattr(uamtbot_config, "SCL_PIN_LASER", DEFAULT_LASER_SCL_PIN)
            
            try:
                # Inicializace I2C pro laser
                i2c_laser_bus = I2C(bus_id_laser, sda=Pin(sda_pin_laser), scl=Pin(scl_pin_laser), freq=400000)
                self.laser = LaserSensor(i2c_laser_bus)
                               
                if getattr(self.laser, "is_connected", False):
                    debug_print(f"[CORE] Přidán modul Laser na pinech SDA = {sda_pin_laser} a SCL = {scl_pin_laser}, ID = {bus_id_laser}")
                else:
                    debug_print(f"[VAROVÁNÍ] Laser je zapnutý v configu, ale neodpovídá. Vytvářím DummyModule.")
                    self.laser = DummyModule("Laser")
            except Exception as e:
                debug_print(f"[VAROVÁNÍ] Chyba při vytváření I2C pro laser: {e}")
                self.laser = DummyModule("Laser")
        else:
            self.laser = DummyModule("Laser")

# ---------- ANALOG HUB (MUX)  ----------
        self._analog_hub = DummyModule("AnalogHub")
        self.buttons = DummyModule("Buttons")
        self.reflex = DummyModule("Reflex")
        self.voltage = DummyModule("Voltage")
        
        if getattr(uamtbot_config, "USE_MUX", False):
            try:
                from analog import AnalogHub
                
                pin_mux_adc = getattr(uamtbot_config, "MUX_ADC_PIN", DEFAULT_MUX_ADC_PIN)
                pin_mux_s0 = getattr(uamtbot_config, "MUX_S0_PIN", DEFAULT_MUX_S0_PIN)
                pin_mux_s1 = getattr(uamtbot_config, "MUX_S1_PIN", DEFAULT_MUX_S1_PIN)
                
                self._analog_hub = AnalogHub(pin_adc = pin_mux_adc, s0 = pin_mux_s0, s1 = pin_mux_s1)
                debug_print(f"[CORE] Přidán modul AnalogHub na pinech ADC={pin_mux_adc}, S0={pin_mux_s0}, S1={pin_mux_s1}")
                
                # ---------- BUTTONS  ----------
                if getattr(uamtbot_config, "USE_BUTTONS", False):
                    from analog import Buttons
                    pin_btn7 = getattr(uamtbot_config, "SW7_PIN", DEFAULT_SW7_PIN)
                    self.buttons = Buttons(self._analog_hub, pin_btn7=pin_btn7)
                    debug_print("[CORE] Přidán sub-modul Buttons (MUX + pin {pin_btn7})")
                # ---------- REFLEX SENSORS  ----------
                if getattr(uamtbot_config, "USE_REFLEX", False):
                    from analog import ReflexSensors
                    pin_refl_l = getattr(uamtbot_config, "REFLEX_L_PIN", DEFAULT_REFLEX_L_PIN)
                    pin_refl_r = getattr(uamtbot_config, "REFLEX_R_PIN", DEFAULT_REFLEX_R_PIN)
                    self.reflex = ReflexSensors(self._analog_hub, pin_left = pin_refl_l, pin_right = pin_refl_r)
                    debug_print("[CORE] Přidán sub-modul ReflexSensors (MUX + piny {pin_refl_l}, {pin_refl_r})")
                # ---------- BATTERY VOLTAGE  ----------
                if getattr(uamtbot_config, "USE_VOLTAGE", False):
                    from analog import Voltage
                    self.voltage = Voltage(self._analog_hub)
                    debug_print("[CORE] Přidán sub-modul Voltage (MUX)")
                    
            except Exception as e:
                debug_print(f"[VAROVÁNÍ] Chyba při inicializaci AnalogHubu nebo jeho sub-modulu, {e}")
                self._analog_hub = DummyModule("AnalogHub")
                self.buttons = DummyModule("Buttons")
                self.reflex = DummyModule("Reflex")
                self.voltage = DummyModule("Voltage")
                

