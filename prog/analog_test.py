# NOTE: USE_VOLTAGE, REFLEX = True NEEDED
import time

def run(robot):
    """
    Testovací skript pro modul analog
    """
    robot.display.clear()
    robot.display.text_centered("Test LED", 20)
    robot.display.text_centered("Probiha...", 40)
    robot.display.show()
    
    if not robot.voltage.is_connected or not robot.reflex.is_connected:
        robot.display.clear()
        robot.display.text_centered("Volt / Refl OFF", 20)
        robot.display.text_centered("SW7 pro navrat", 45)
        robot.display.show()
        
        while True:
            sw3, sw4, sw5, sw7 = robot.buttons.read_states()
            if sw7:
                robot.buzzer.beep()
                break
            time.sleep(0.1)
        return
    
    current_screen = 0

    last_press = time.ticks_ms()
    press_block_ms = 400  

    while True:
        sw3, sw4, sw5, sw7 = robot.buttons.read_states()
        current_time = time.ticks_ms()

        if sw7 and time.ticks_diff(current_time, last_press) > press_block_ms:               
            current_screen += 1
            last_press = current_time
            
            if current_screen > 2:
                break 

        robot.display.clear()
    
        # SCR 0 - BUTTONS
        if current_screen == 0:
            robot.display.text_centered("BUTTONS", 5)
            robot.display.text_centered(f"SW3: {sw3}", 20)
            robot.display.text_centered(f"SW4: {sw4}", 32)
            robot.display.text_centered(f"SW5: {sw5}", 44)
            robot.display.text_centered("SW7 -> BATERIE", 56)
        # SCR 1 - VOLTAGE   
        elif current_screen == 1:
            v = robot.voltage.read_voltage()
            robot.display.text_centered("BATERIE", 5)
            robot.display.text_centered(f"{v:.2f} V", 20)
            robot.display.text_centered("SW7 -> REFLEX", 40)           
        # SCR 2 - REFLEX
        elif current_screen == 2:
            robot.display.text_centered("REFLEX", 5)  
            
            l_pct, c_pct, r_pct = robot.reflex.read_percent()
            reflex_text = f"L:{l_pct}% C:{c_pct}% R:{r_pct}%"
            
            robot.display.text_centered(f"Levy: {l_pct}", 20)
            robot.display.text_centered(f"Stred: {c_pct} %", 32)
            robot.display.text_centered(f"Pravy: {r_pct} %", 44)
            robot.display.text_centered("SW7 -> KONEC", 56)
        
        robot.display.show() 
        time.sleep(0.1)
        
    robot.display.clear()