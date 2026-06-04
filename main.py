"""
Hlavní program robota UAMTbot
Autor: David Hanák

Program zajišťuje chod grafického interaktivního menu, dynamické načítání testovacích skriptů a ošetření chybových stavů.

Vyžaduje připojený displej a tlačítka

Ovládání displeje:
SW3 -> dolů, SW4 -> nahoru, SW5 -> potvrdit, SW7 -> vrácení z programu
"""

import uamtbot_config
from core import Robot, debug_print
import sys
import time
import gc

sys.path.append('/prog')

robot = Robot()   
robot.display.clear()

# available programs in format: (Name (visible on display), file_name)
programs = [
    ("LED", "led_test"),
    ("Buzzer", "buzzer_test"),
    ("Motors", "motors_test"),
    ("IMU", "imu_test"),
    ("ToF Laser", "laser_test"),
    ("Analog", "analog_test"),
    ("Vypnout", "power_off")
]
current_idx = 0
top_idx = 0
current_state = "MENU"
VISIBLE_ITEMS = 3
refresh_display = True
error_msg = " "

last_press = time.ticks_ms()
press_block_ms = 400

if not robot.display.is_connected or not robot.buttons.is_connected:
    current_state = "ERROR"
    robot.leds.error()
    debug_print(f"BUTTONS nebo DISPLAY VYPNUTO")
    sys.exit()


while True:
    if current_state == "MENU":
        
        if refresh_display:           
            robot.display.clear()
            robot.display.text_centered("Vyber program: ", 5)
        
            visible_programs = programs[top_idx : top_idx + VISIBLE_ITEMS]
        
            for i, (name, module_name) in enumerate(visible_programs):
                actual_idx = top_idx + i
                y_pos = 25 + (i * 12)
                prefix = "> " if actual_idx == current_idx else "  "
                robot.display.text(f"{prefix}{name}", 5, y_pos, 1)
            
            robot.display.show()
            refresh_display = False
        
        sw3, sw4, sw5, sw7 = robot.buttons.read_states()
        current_time = time.ticks_ms()
        
        if time.ticks_diff(current_time, last_press) > press_block_ms:
            if sw3:
                current_idx = (current_idx + 1) % len(programs)
                if current_idx >= top_idx + VISIBLE_ITEMS:
                    top_idx = current_idx - VISIBLE_ITEMS + 1
                elif current_idx == 0:
                    top_idx = 0
                    
                refresh_display = True    
                robot.buzzer.beep()
                last_press = current_time
            
            elif sw4:
                current_idx = (current_idx - 1) % len(programs)
                if current_idx < top_idx:
                    top_idx = current_idx
                elif current_idx == len(programs) - 1:
                    top_idx = max(0, len(programs) - VISIBLE_ITEMS)
                    
                refresh_display = True    
                robot.buzzer.beep()
                last_press = current_time
                
            elif sw5:
                current_state = "RUNNING"
                robot.buzzer.tone(2000, 0.5)
                last_press = current_time
            
    elif current_state == "RUNNING":
        program_name, module_name = programs[current_idx]
        
        robot.display.clear()
        robot.display.text_centered("Spoustim", 20)
        robot.display.text_centered(program_name, 40)
        robot.display.show()
        time.sleep(1)
        
        try:
            mod = __import__(module_name)
            mod.run(robot)
        except Exception as e:
            current_state = "ERROR"
            error_msg = str(e)[:15]
            debug_print(f"CHYBA V PROGRAMU {module_name}!")
            sys.print_exception(e)
            robot.motors.stop()
            robot.leds.all(128, 0, 0)
            robot.buzzer.tone(200, 1, 1000)
            
        if current_state != "ERROR":
            robot.motors.stop()
            robot.display.clear()
        
            if module_name in sys.modules:
                del sys.modules[module_name]
                gc.collect()
            current_state = "MENU"
            refresh_display = True
            last_press = time.ticks_ms()
    
    elif current_state == "ERROR":
        robot.display.clear()
        robot.display.text_centered("Error!", 15)
        robot.display.text_centered(error_msg, 35)
        robot.display.text_centered("SW7 pro navrat", 55)
        robot.display.show()
        
        sw3, sw4, sw5, sw7 = robot.buttons.read_states()
        current_time = time.ticks_ms()
        
        if time.ticks_diff(current_time, last_press) > press_block_ms:
            if sw7:
                robot.leds.all(0, 0, 0)
                program_name, module_name = programs[current_idx]
                if module_name in sys.modules:
                    del sys.modules[module_name]
                    gc.collect()
                current_state = "MENU"
                refresh_display = True
                last_press = current_time
                
    time.sleep(0.1)



