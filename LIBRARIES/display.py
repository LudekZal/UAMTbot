# This library depends on sh1106.py library by Robert Hammelrath (https://github.com/robert-hh/SH1106)
# which is distributed under the MIT License (see the attached LICENSE_sh1106.txt file)


import time
from sh1106 import SH1106_I2C
from core import debug_print

class Display:
    """
    Třída pro ovládání OLED displeje s řadičem SH1106 komunikujícího přes I2C.
    
    Poskytuje rozhraní pro vypisování textu a jednoduché grafiky. Při inicializaci provádí test spojení s displejem. Pokud displej fyzicky chybí nebo neodpovídá, označí modul jako odpojený.
    
    Při volání 'robot.display.func' lze využívat funkce z knihovny 'sh1106.py'.
    """
    def __init__(self, i2c_bus, width=128, height=64):
        self.width = width
        self.height = height
        self.is_connected = False
        
        try:
            self.disp = SH1106_I2C(self.width, self.height, i2c_bus)
            self.is_connected = True
            
            self.disp.fill(0)
            self.disp.text("UAMT Bot", 30, 20, 1)
            self.disp.text("Ready...", 35, 35, 1)
            self.disp.show()
            debug_print("[DISPLEJ] Modul úspěšně inicializován.")
            
        except Exception as e:
            # Displej fyzicky chybí, nebo je špatně zapojen
            debug_print(f"[VAROVÁNÍ] Displej není připojen (Chyba I2C: {e}).")

    def clear(self):
        """Vyčistí displej"""
        if not self.is_connected: return
        self.disp.fill(0)
        self.disp.show()
        debug_print("[DISPLAY] Čistím displej")
        
    def text_centered(self, text, y, color=1):
        """
        Vypíše text zarovnaný na střed displeje.
        
        :param text: Řetězec k vypsání
        :param y: Vertikální pozice (0-64)
        """
        if not self.is_connected: return
        
        text_width = (len(text) * 6) + ((len(text) - 1) * 2)
        
        x = (self.width - text_width) // 2
        x = max(0, x)
        
        self.disp.text(text, x, y, color)
        debug_print(f"[DISPLAY] Centruji text {text} na pozici X:{x}, Y:{y}")
          
    def battery(self, percent):
        """
        Vykreslí baterii v rohu

        :param percent: procentuální výplň baterie 
        """
        if not self.is_connected: return
        self.disp.rect(100, 0, 20, 10, 1)
        width = int(18 * (percent / 100))
        self.disp.fill_rect(101, 1, width, 8, 1) 
        self.disp.show()
        debug_print("[DISPLAY] Vykresluji baterku na displeji")
        
    def progress_bar(self, percent, x=10, y=40, width=108, height=10):
        """
        Vykreslí načítací pruh
        :param percent: Procentuální zaplnění (0-100)
        """
        if not self.is_connected: return
        
        percent = max(0, min(100, percent))
        self.disp.rect(x, y, width, height, 1)
        bar = int((width - 4) * (percent / 100))
        if bar > 0:
            self.disp.fill_rect(x + 2, y + 2, bar, height - 4, 1)
        
        debug_print(f"[DISPLAY] Vykreslen progress bar: {percent} %")
                      
    def __getattr__(self, func):
        """ Zachycuje funkce, které nejsou součástí knihovny display.py a hledá, jestli se nenachází v knihovně sh1106.py"""
        if self.is_connected and hasattr(self.disp, func):
            debug_print(f"[DISPLAY] Použita funkce {func} z knihovny SH1106")
            return getattr(self.disp, func)
        
        def nonexistent(*args, **kwargs):
            debug_print(f"[DISPLAY] Funkce {func} nenalezena")
            pass
        return nonexistent