# Knihovna pro školního robota

Tento repozitář obsahuje ovládací knihovnu a testovací skript pro školního robota postaveného na Raspberry Pi Pico.

## Umístění souborů v repozitáři

Repozitář je rozdělen do složek. Pro zprovoznění robota vás zajímají tyto cesty:

* `LIBRARIES/Robot.py` – Hlavní knihovna s třídou pro ovládání robota.
* `PYTHON_EXAMPLES/test.py` – Ukázkový soubor pro otestování funkčnosti.

## Instalace a nahrání na PICO

Aby kód fungoval, **je nutné ručně nahrát knihovnu do paměti Raspberry Pi Pico**. Postupujte následovně:

1.  Připojte Raspberry Pi Pico k počítači a otevřete editor (Thonny IDE / VS Code).
2.  V tomto repozitáři otevřete složku `libraries`.
3.  Soubor **`Robot.py` nahrajte do Raspberry Pi Pico**.
    * *Kam přesně?* Uložte ho přímo do kořenového adresáře (root) nebo do složky `/lib` na Picu.
4.  Následně otevřete soubor `python_examples/test.py`. Ten můžete buď také nahrát na Pico, nebo jej spustit přímo z editoru.

## Jak použít

Ukázka použití je v souboru `python_examples/test.py`. Příklad kódu:

```python
# Import knihovny (funguje, pokud je Robot.py nahraný v Picu)
from Robot import Robot

# Inicializace (upravte piny dle potřeby)
robot = Robot()

# Testování funkcí (příklad)
robot.leds_set(1, 255, 0, 0)
robot.buzzer_beep()
robot.leds_clear()
robot.display_battery(66)
