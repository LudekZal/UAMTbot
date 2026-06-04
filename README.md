# UAMTbot - Software pro školního robota

Tento repozitář obsahuje softwarovou architekturu a diagnostické skripty pro školního robota postaveného na mikrokontroléru Raspberry Pi Pico.

## Umístění souborů v repozitáři

Repozitář je logicky rozdělen tak, aby odděloval hardwarové ovladače od uživatelských programů. Pro správný chod jsou klíčové tyto složky a soubory:

* **`/lib`** – Ovladače hardwarových periferií a jádro systému (`core.py`).
* **`/prog`** – Ukázkové a testovací skripty pro jednotlivé periferie (např. `led_test.py`).
* **`main.py`** – Hlavní spouštěcí program (stavový automat a scrollovací grafické menu).
* **`uamtbot_config.py`** – Konfigurační soubor pro mapování pinů a povolení/zakázání jednotlivých periferií.

## Zprovoznění

Aby systém správně fungoval, je nutné zachovat strukturu složek při nahrávání do paměti Raspberry Pi Pico. Postupujte následovně:

1. Ujistěte se, že máte na Raspberry Pi Pico nainstalovaný **MicroPython**.
2. Připojte Pico k počítači přes USB a otevřete vývojové prostředí (např. **Thonny IDE**).
3. V Thonny jít do Run -> Configure interpreter... a zvolit Raspberry Pi Pico, v pravém dolním rohu pak vybrat dostupný komunikační port.
4. Do kořenového adresáře Pica zkopírujte složky **`lib`** a **`prog`**.
5. Následně do kořenového adresáře zkopírujte i soubory **`main.py`** a **`uamtbot_config.py`**.

## Programování

Díky sjednocující vrstvě je ovládání robota velmi intuitivní. Pro vytvoření vlastního programu stačí importovat konfiguraci a třídu `Robot`:

```python
import uamtbot_config
from core import Robot
import time

# Inicializace (automaticky načte moduly povolené v uamtbot_config.py)
robot = Robot()

robot.leds.all(128, 0, 0)

robot.buzzer.beep()

# Zobrazení textu na displeji
robot.display.clear()
robot.display.text_centered("UAMTbot", 30)
robot.display.show()

time.sleep(2)

robot.clear()
robot.leds.all(0, 0, 0)

## Dokumentace

Ke knihovně je vytvořená dokumentace ve formě webové stránky (HTML).

**Jak ji zobrazit:**
1. Stáhněte si z repozitáře soubor `Dokumentace_HTML.zip`.
2. Rozbalte ZIP soubor ve svém počítači.
3. Ve vzniklé složce otevřete soubor `index.html`.