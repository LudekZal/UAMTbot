# Knihovna pro školního robota (UAMTbot)

Tento repozitář obsahuje ovládací knihovnu a testovací skripty pro školního robota postaveného na mikrokontroléru **Raspberry Pi Pico**.

## Umístění souborů v repozitáři

Repozitář je rozdělen do složek. Pro zprovoznění robota jsou klíčové tyto cesty:

* `LIBRARIES/Robot.py` – Hlavní knihovna s třídou pro ovládání robota.
* `PYTHON_EXAMPLES/` – Ukázkové soubory pro testování jednotlivých periferií.
* `PYTHON_EXAMPLES/ROBOT_EXAMPLES/` – Ukázkové soubory pro testování funkčnosti knihovny `Robot.py`.

---

## Instalace a nahrání na PICO

Aby kód fungoval, **je nutné ručně nahrát knihovny do paměti Raspberry Pi Pico**. Postupujte následovně:

1.  Připojte Raspberry Pi Pico k počítači a otevřete editor (Thonny IDE / VS Code).
2.  V tomto repozitáři otevřete složku `LIBRARIES` a stáhněte si soubory:
    * `Robot.py`
    * `sh1106.py`
    * `ICM42688.py`
3.  Všechny tři soubory **nahrajte do kořenového adresáře** v Raspberry Pi Pico.
4.  Následně otevřete složku `PYTHON_EXAMPLES/ROBOT_EXAMPLES/` a vyberte si skript, který chcete vyzkoušet.
5.  Skript můžete spustit přímo v editoru nebo jej nahrát na Pico pod názvem `main.py` (pro automatické spuštění po startu).

---

## Jak použít

Pro využití knihovny ve vlastním skriptu stačí importovat třídu `Robot`.

```python
# Import knihovny (funguje, pouze pokud jsou soubory nahrané v Picu)
from Robot import Robot
import time

# Inicializace
robot = Robot()

# Rozsvícení LED (červená)
robot.leds_set(1, 255, 0, 0)
    
# Pípnutí
robot.buzzer_beep()
    
# Zobrazení baterie na displeji
robot.display_battery(66)
    
time.sleep(2)

robot.stop()
```
## Dokumentace

Ke knihovně je vytvořená dokumentace ve formě webové stránky (HTML).

**Jak ji zobrazit:**
1. Stáhněte si z repozitáře soubor `Dokumentace_HTML.zip`.
2. Rozbalte ZIP soubor ve svém počítači.
3. Ve vzniklé složce otevřete soubor `index.html`.
