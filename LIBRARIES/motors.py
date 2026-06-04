import time
from machine import PWM, Pin

from core import debug_print

class Motors:
    """
    Třída pro řízení dvou motorů.
    
    Zapouzdřuje nízkoúrovňové nastavování duty cycle a digitálních výstupů do jednoduchého rozhraní pro jízdu robota.
    """
    def __init__(self, m1_dir = 16 , m1_pwm = 17, m1_sleep = 18, m2_dir = 19, m2_pwm = 20, m2_sleep = 21):
        self.is_connected = False;
        
        try:
            self.mot1_pwm = PWM(Pin(m1_pwm))
            self.mot1_dir = Pin(m1_dir, Pin.OUT)
            self.mot1_sleep = Pin(m1_sleep, Pin.OUT)
            
            self.mot2_pwm = PWM(Pin(m2_pwm))
            self.mot2_dir = Pin(m2_dir, Pin.OUT)
            self.mot2_sleep = Pin(m2_sleep, Pin.OUT)
            
            self.is_connected = True
            
            debug_print("[MOTORS] Modul úspěšně inicializován.")
        except Exception as e:
            debug_print("[VAROVÁNÍ] Chyba inicializace motorů: {e}")
            
    def set(self, speedL, dirL, speedR, dirR):
        """
        Skokový rozjezd motorů
        
        :param speedL: Rychlost levého motoru
        :param speedR: Rychlost pravého motoru
        :param dirL: Směr jízdy levého motoru (0 = dozadu, 1 = dopředu)
        :param dirR: Směr jízdy pravého motoru (0 = dozadu, 1 = dopředu)

        .. note::
           Nastaví rychlost motorů okamžitě, způsobuje cukání při startu / zastavení       
        """
        if not self.is_connected: return
        
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
        debug_print("[MOTORS] Nastavuji rychlost levého a pravého motoru")
        
    def ramp(self, speedL, dirL, speedR, dirR, duration_ms=500):
        """
        Postupný rozjezd motorů s definovanou dobour trvání
        
        :param speedL: Konečná rychlost levého motoru
        :param speedR: Konečná rychlost pravého motoru
        :param dirL: Směr jízdy levého motoru (0 = dozadu, 1 = dopředu)
        :param dirR: Směr jízdy pravého motoru (0 = dozadu, 1 = dopředu)
        :param duration_ms: Doba rozjezdu v milisekundách (výchozí hodnota 500 ms)
        
        .. warning::
            Tato funkce je blokující! Z důvodu plynulosti přechodu program během rozjezdu čeká a nečte hodnoty z ostatních senzorů
        """
        if not self.is_connected: return
        
        self.mot1_sleep.on()
        self.mot2_sleep.on()
        self.mot1_pwm.duty_u16(10000)
        self.mot2_pwm.duty_u16(10000)
        
        if (dirL == 0):
            self.mot1_dir.off()
        else:
            self.mot1_dir.on()
            
        if (dirR == 0):
            self.mot2_dir.on()
        else:
            self.mot2_dir.off()
        
        step_time_ms = 10
        steps_total = max(1, duration_ms // step_time_ms)
        
        incL = speedL / steps_total
        incR = speedR / steps_total
        
        for i in range(1, steps_total + 1):
            current_speedL = int(i * incL)
            current_speedR = int(i * incR)
            # Pico PWM limitations
            if current_speedL >= 10:
                self.mot1_pwm.freq(current_speedL)
            if current_speedR >= 10:
                self.mot2_pwm.freq(current_speedR)
            
            time.sleep_ms(step_time_ms)
        
        if speedL >= 10: self.mot1_pwm.freq(speedL)
        if speedR >= 10: self.mot2_pwm.freq(speedR)
        debug_print(f"[MOTORS] Rozjezd dokončen za {duration_ms} ms")
            
    def stop_ramp(self, start_speedL, start_speedR, duration_ms=500):
        """
        Postupné zpomalení motorů z definované rychlosti do nuly.
        
        :param start_speedL: Počáteční rychlost levého motoru
        :param start_speedR: Počáteční rychlost pravého motoru
        :param duration_ms: Doba rozjezdu v milisekundách (výchozí hodnota 500 ms)
        
        .. warning::
            Tato funkce je blokující! Z důvodu plynulosti přechodu program během rozjezdu čeká a nečte hodnoty z ostatních senzorů
        """
        if not self.is_connected: return
               
        step_time_ms = 10
        steps_total = max(1, duration_ms // step_time_ms)

        decL = start_speedL / steps_total
        decR = start_speedR / steps_total
        debug_print(f"[MOTORS] Zastavuji motory")
        for i in range(1, steps_total + 1):
            current_speedL = int(start_speedL - (i * decL))
            current_speedR = int(start_speedR - (i * decR))
            
            if current_speedL >= 10:
                self.mot1_pwm.freq(current_speedL)
            if current_speedR >= 10:
                self.mot2_pwm.freq(current_speedR)           
            
            time.sleep_ms(step_time_ms)
            
        self.stop()
        debug_print("[MOTORS] Motory zastaveny")
        
    def stop(self):
        """ Zastaví motory a uspí drivery """
        self.mot1_pwm.duty_u16(0)
        self.mot2_pwm.duty_u16(0)
        self.mot1_sleep.off()
        self.mot2_sleep.off()
        debug_print("[MOTORS] Motory zastaveny")
