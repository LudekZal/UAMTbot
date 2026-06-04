from machine import ADC, Pin
import time

class AnalogHub:
    """
    Třída pro obsluhu analogového multiplexoru.
    
    Spravuje přepínaní kanálů multiplexoru pomocí řídicích pinů (S0,S1) a čtení hodnot z analogového pinu ADC0.
    
    :param pin_adc: Číslo GPIO pinu připojeného k výstupu multiplexoru
    :param s0: Číslo GPIO pinu řídicího signálu MUX_S0
    :param s1: Číslo GPIO pinu řídicího signálu MUX_S1
    """
    BUTTONS    = 0
    VCC        = 1
    REFLEX     = 2
    UNIVERSAL  = 3
    def __init__(self, pin_adc, s0, s1):
        self.is_connected = True
        self.mux = ADC(Pin(pin_adc))
        self.s0 = Pin(s0, Pin.OUT)
        self.s1 = Pin(s1, Pin.OUT)
        
    def _read_mux(self, channel):
        """
        [Interní metoda] Přepne multiplexor na zadaný kanál a přečte hodnotu ADC.
        Krátké zpoždění slouží k ustálení napětí.
        
        :param channel: Identifikátor kanálu z konstant třídy (0-3)
        :return: Hodnota z 16bit ADC (0-65535)
        """
        self.s0.value(channel & 0x01)
        self.s1.value((channel >> 1) & 0x01)
        time.sleep_us(1000)
        self.mux.read_u16()
        time.sleep_us(100)
        return self.mux.read_u16()
    
class Buttons:
    """
    Třída pro čtení stavu uživatelských tlačítek s integrovaným debouncingem.
    
    Tři tlačítka (SW3,4,5) jsou čtena přes multiplexor, čtvrté (SW7) je připojeno na digitální pin.
    
    :param hub: Inicializovaná instance sdíleného multiplexoru
    :param pin_btn7: Číslo GPIO pinu pro digitální tlačítko. Výchozí hodnota je 13
    """
    def __init__(self, hub, pin_btn7=13):
        self.is_connected = True
        self.hub = hub
        self.btn7 = Pin(pin_btn7, Pin.IN, Pin.PULL_UP)
        self.STATES = [
            (160,     (0, 0, 0)), # 0 V
            (16780, (0, 0, 1)), # 0.767 V
            (25610, (0, 1, 0)), # 1.179 V
            (36000, (1, 0, 0)) # 1.650 V
        ]
                
        self.TOLERANCE = 1000 # appx 0.05 V tolerance
        
        self.DEBOUNCE_DELAY_MS = 30      
        self.last_reading = (0, 0, 0)    
        self.stable_state = (0, 0, 0)    
        self.last_debounce_time = time.ticks_ms()
        
    def read_states(self):
        """
        Přečte a vrátí stavy všech čtyř tlačítek.
        
        Obsahuje neblokující SW debouncing.
        
        :return: tuple: N-tice 4 boolean hodnot (0 nebo 1) představujících stavy tlačítek (1 - stisknuto, 0 - uvolněno)
        """
        raw_val = self.hub._read_mux(AnalogHub.BUTTONS)
        current_reading = (0, 0, 0)
        
        for target_adc, states_tuple in self.STATES:
            if abs(raw_val - target_adc) <= self.TOLERANCE:
                current_reading = states_tuple
                break
        
        current_time = time.ticks_ms()
        
        if current_reading != self.last_reading:
            self.last_debounce_time = current_time
        if time.ticks_diff(current_time, self.last_debounce_time) > self.DEBOUNCE_DELAY_MS:
            self.stable_state = current_reading
        
        self.last_reading = current_reading
        
        btn7_state = 1 if self.btn7.value() == 0 else 0
        
        return self.stable_state + (btn7_state,)
    
class Voltage:
    """
    Třída pro měření napětí napájecí baterie robota.
    
    Využívá HW odporový dělič připojený na vstup multiplexoru.
    :param hub: Inicializovaná instance sdíleného multiplexoru
    """
    def __init__(self, hub):
        self.is_connected = True
        self.hub = hub
        self.VREF = 3.3
        self.RATIO = 6
    
    def read_voltage(self):
        """
        Změří a vypočítá skutečné napětí baterie.
        
        :return: float: Aktuální napětí baterie ve voltech (V)
        """
        raw_val = self.hub._read_mux(AnalogHub.VCC)
        pin_voltage = (raw_val / 65535) * self.VREF
        battery_voltage = pin_voltage * self.RATIO
        
        return battery_voltage

class ReflexSensors:
    """
    Třída pro obsluhu reflexních senzorů.
    
    Sjednocuje čtení ze dvou nezávislých ADC pinů (27,28) a jednoho senzoru sdíleného přes multiplexor.
    
    :param hub: Inicializovaná instance sdíleného multiplexoru
    :param pin_left: Číslo GPIO pinu pro levý senzor
    :param pin_right: Číslo GPIO pinu pro pravý senzor
    """
    def __init__(self, hub, pin_left, pin_right):
        self.is_connected = True
        self.hub = hub
        self.adc_left = ADC(Pin(pin_left))
        self.adc_right = ADC(Pin(pin_right))
    
    def read_raw(self):
        """
        Vrátí surové hodnoty z ADC (0-65535) pro všechny tři senzory.

        :return: tuple: N-tice (levý, střední, pravý) s hodnotami v rozsahu 0-65535
        
        .. note::
           Nízká hodnota = světlý povrch, vysoká hodnota = tmavý povrch
        """
        left = self.adc_left.read_u16()
        right = self.adc_right.read_u16()
        
        center = self.hub._read_mux(AnalogHub.REFLEX)
        
        return (left, center, right)
    
    def read_percent(self):
        """
        Vrátí procentuální hodnoty (0-100 %) pro všechny tři senzory.

        :return: tuple: N-tice (levý, pravý, střední) s hodnotami v rozsahu 0-100 %
        """
        l_raw, c_raw, r_raw = self.read_raw()
        
        l_pct = int((l_raw / 65535) * 100)
        c_pct = int((c_raw / 65535) * 100)
        r_pct = int((r_raw / 65535) * 100)
        
        return (l_pct, c_pct, r_pct)
    
    def read_states(self, threshold=50):
        """
        Porovná procentuální hodnoty s nastaveným prahem a vrátí logické stavy.
            
        :param threshold: Práh pro vrácení hodnoty True. Výchozí hodnota je 50
        :return: tuple: N-tice (levý, střední, pravý) logických hodnot (True/False).
        """
        l_pct, c_pct, r_pct = self.read_percent()
        
        return (l_pct > threshold, c_pct > threshold, r_pct > threshold)





