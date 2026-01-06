# David Hanák
# HW version: UAMTbot 1.0
# NOTE: display must be connected to P17
# NOTE: libraries sh1106.py and ICM42688.py must be present on PICO
import machine
import time
import math
from machine import Pin, PWM, I2C
from sh1106 import SH1106_I2C
from neopixel import NeoPixel
from ICM42688 import ICM42688

# Constants
LEDS = 10
WIDTH = 128 # OLED Display parameters
HEIGHT = 64

class Robot:
    """
    Hlavní třída robota UAMTbot.
    
    Tato třída sdružuje vysokoúrovňové funkce periferií:
    NeoPixelu
    IMU
    Displeje
    Motorů
    Speakeru
    """
# ---------- INIT -------------
    def __init__(self):
        """Inicializace robota
    
        Při startu se:
        1. Přiřadí všechny potřebné piny jednotlivým periferiím
        2. Inicializují hodnoty periferií
        3. Vypíše uvítací text na displej

        .. note::
           Displej a IMU má ošetření pomocí try-except, pokud jsou špatně zapojené / nastavené, inicializace selže.
        """
        
        # --- 1. LED ---
        self.num_pixels = LEDS 
        self.np = NeoPixel(machine.Pin(22), self.num_pixels)
        self.leds_clear()
        
        # --- 2. Buzzer ---
        self.buzzer_pwm = machine.PWM(machine.Pin(7))
        self.buzzer_pwm.duty_u16(0)
        
        # --- 3. Display ---
        try:
            # I2C init
            self.disp_i2c = I2C(0, sda=machine.Pin(4), scl=machine.Pin(5), freq=400000)
            
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
            
        # --- 4. Motors ---
        self.mot1_pwm = PWM(Pin(17))
        self.mot1_dir = Pin(16, Pin.OUT)
        self.mot1_sleep = Pin(18, Pin.OUT)
        
        self.mot2_pwm = PWM(Pin(20))
        self.mot2_dir = Pin(19, Pin.OUT)
        self.mot2_sleep = Pin(21, Pin.OUT)
        
        self.motors_stop()
        
        # --- 5. IMU ---
        self.imu = None
        try:
            self.imu_i2c = I2C(1, sda = machine.Pin(10), scl = machine.Pin(11), freq = 400000)
            self.imu = ICM42688(self.imu_i2c, address = 0x69)
            self.imu.wake()
            self.current_pitch = 0.0
            self.last_time = time.ticks_ms()
            print("IMU OK")
        except Exception as e:
            print(f"Chyba IMU: {e}")
            
            
    def stop(self):
        """
        Zastaví všechny funkce (užitečné pro konec)
    
        """
        self.leds_clear()
        self.buzzer_pwm.duty_u16(0)
        self.display.fill(0)
        self.display.show()
        self.motors_stop()
        self.imu.sleep()

# ---------- DISPLAY METHODS -------------
    def display_animate(self):
        """
        Spustí animaci. placeholder

        .. note::
           Tato funkce je zde jako ukázka, jak funguje animace        
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

        :param percent: procentuální výplň baterie 
        """
        if self.display:
            self.display.rect(100, 0, 20, 10, 1)
            width = int(18 * (percent / 100))
            self.display.fill_rect(101, 1, width, 8, 1) 
            self.display.show()
            
    def display_dashboard(self):
        """ Zobrazí přehled stavu IMU: Teplota a náklon """
        if not self.display or not self.imu:
            return
        
        temp = self.imu.read_temperature()
        pitch, roll = self.imu_get_tilt()
        
        self.display.fill(0)
        self.display.text("STAV ROBOTA", 0, 0, 1)
        self.display.hline(0, 9, 80, 1)
        
        text_temp = f"Temp: {temp:.2f}"
        self.display.text(f"Temp: {temp:.2f}", 0, 15, 1)
        x_pos = len(text_temp) * 8
        self.display.rect(x_pos + 5, 13, 3, 3, 1)
        self.display.text("C", x_pos + 10, 15, 1)
        self.display.text(f"Pitch: {pitch:.2f}", 0, 30, 1)
        self.display.text(f"Roll: {roll:.2f}", 0, 45, 1)
        self.display.show()
    
    def display_clear(self):
        """
        Vyčistí displej
        """
        self.display.fill(0)
        self.display.show()

# ---------- LED METHODS -------------
    def leds_clear(self):
        """ Zhasne všechny diody """
        self.np.fill((0, 0, 0))
        self.np.write()
        
    def leds_set(self, led_num: int, r: int, g: int, b: int, show=True):
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
        """ Světelná indikace chyby - 3x blikne """
        for _ in range(3):
            self.leds_all(128, 0, 0)
            time.sleep(0.2)
            self.leds_clear()
            time.sleep(0.2)
            
# ---------- BUZZER METHODS -------------
    def buzzer_beep(self, freq=1000, duration=0.1):
        """
        Pípnutí
            
        :param freq: Frekvence (výchozí hodnota = 1000)
        :param duration: Délka pípnutí ve vteřinách (výchozí hodnota = 0.1)
        """

        self.buzzer_pwm.freq(freq)
        self.buzzer_pwm.duty_u16(3000)
        time.sleep(duration)
        self.buzzer_pwm.duty_u16(0)
        
    def buzzer_tone(self, frequency: int, duration: float, volume: int = 2000):
        """
        Přehraje tón
        
        :param frequency: Frekvence tónu
        :param duration: Délka tónu
        :param volume: Hlasitost (Výchozí hodnota = 2000)

        .. note::
           Pro nejvyšší hlasitost použijte frequency = 2700 Hz a volume = 32768
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
    def motors_set(self, speedL, dirL, speedR, dirR):
        """
        Skokový rozjezd motorů
        
        :param speedL: Rychlost levého motoru
        :param speedR: Rychlost pravého motoru
        :param dirL: Směr jízdy levého motoru (0 = dozadu, 1 = dopředu)
        :param dirR: Směr jízdy pravého motoru (0 = dozadu, 1 = dopředu)

        .. note::
           Nastaví rychlost motorů okamžitě, způsobuje cukání při startu / zastavení       
        """
        self.mot1_sleep.on()
        self.mot2_sleep.on()    
        self.mot1_pwm.duty_u16(10000)
        self.mot2_pwm.duty_u16(10000)
        if(dirL == 0):
            self.mot1_dir.off()
        else:
            self.mot1_dir.on()
        if(dirR == 0):
            self.mot2_dir.on()
        else:
            self.mot2_dir.off()
            
        self.mot1_pwm.freq(speedL)    
        self.mot2_pwm.freq(speedR)
        
    def motors_ramp(self, speedL, dirL, speedR, dirR):
        """
        Postupný rozjezd motorů
        
        :param speedL: Konečná rychlost levého motoru
        :param speedR: Konečná rychlost pravého motoru
        :param dirL: Směr jízdy levého motoru (0 = dozadu, 1 = dopředu)
        :param dirR: Směr jízdy pravého motoru (0 = dozadu, 1 = dopředu) 
        """
        self.mot1_sleep.on()
        self.mot2_sleep.on()
        self.mot1_pwm.duty_u16(10000)
        self.mot2_pwm.duty_u16(10000)
        if(dirL == 0):
            self.mot1_dir.off()
        else:
            self.mot1_dir.on()
        if(dirR == 0):
            self.mot2_dir.on()
        else:
            self.mot2_dir.off()
        faster = speedL
        if(speedR > faster):
            faster = speedR
        for x in range(100, faster + 100, 100):
            spL = x
            if(x > speedL):
                spL = speedL
            spR = x
            if(x > speedR):
                spR = speedR
            self.mot1_pwm.freq(spL)    
            self.mot2_pwm.freq(spR)
            time.sleep(0.01)
            
    def motors_stop_ramp(self, start_speedL, start_speedR):
        """
        Postupné zpomalení motorů
        
        :param start_speedL: Počáteční rychlost levého motoru
        :param start_speedR: Počáteční rychlost pravého motoru
        """
        faster = start_speedL
        if(start_speedR > faster):
            faster = start_speedR
        for x in range(faster, 100, -100):
            spL = x
            if(x > start_speedL):
                spL = start_speedL
            spR = x
            if(x > start_speedR):
                spR = start_speedR
            self.mot1_pwm.freq(spL)    
            self.mot2_pwm.freq(spR)
            time.sleep(0.01)
           
        self.mot1_pwm.duty_u16(0)
        self.mot2_pwm.duty_u16(0)
    
    def motors_stop(self):
        """ Zastaví motory a uspí drivery """
        self.mot1_pwm.duty_u16(0)
        self.mot2_pwm.duty_u16(0)
        self.mot1_sleep.off()
        self.mot2_sleep.off()
        
# ---------- IMU METHODS -------------     
    def imu_get_tilt(self):
        """Vrátí náklon (Pitch, Roll)"""
        if not self.imu: return (0, 0)
        
        ax, ay, az = self.imu.read_accel_data()
        
        pitch = math.atan2(ay, math.sqrt(ax*ax + az*az)) * 57.3 # přepočet na stupně (180/pi) 
        roll = math.atan2(-ax, az) * 57.3
            
        return (pitch, roll)
        
    def imu_check_crash(self, threshold_g = 3.0):
        """
        Zkontroluje, zda nedošlo k nárazu (překročení limitu g)

        :param threshold_g: Prahová hodnota g (výchozí 3.0 g)

        .. note::
           Při použití s motors_set() je možné, že se aktivuje při uvedení do pohybu
        """
        ax, ay, az = self.imu.read_accel_data()
        
        total_accel = (ax**2 + ay**2 + az**2) ** 0.5
        
        if total_accel >= threshold_g:
            print(f"Crash detected! G-Force: {total_accel:2f}")
            self.leds_error()
            self.motors_stop()
            return True
        
        return False