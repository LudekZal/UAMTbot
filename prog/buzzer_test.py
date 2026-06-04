# NOTE: USE_BUZZER = True NEEDED
import time

c_major_scale = [262, 294, 330, 349, 392, 440, 494, 523]

def run(robot):
    """
    Testovací skript pro modul buzzer
    """
    robot.display.clear()
    robot.display.text_centered("Test Buzzer", 20)
    robot.display.text_centered("Probiha...", 40)
    robot.display.show()
    
    if not robot.buzzer.is_connected:
        robot.display.clear()
        robot.display.text_centered("BUZZER OFF", 20)
        robot.display.text_centered("SW7 pro navrat", 40)
        robot.display.show()
    
        while True:
            sw3, sw4, sw5, sw7 = robot.buttons.read_states()
            if sw7:
                robot.buzzer.beep()
                break
            time.sleep(0.1)
        return
    
    robot.buzzer.beep()
    time.sleep(0.1)
    robot.buzzer.beep(2000, 0.1)
    
    time.sleep(1)
    
    for freq in range(100, 3000, 100):
        robot.buzzer.tone(freq, 0.02, 3000)
        
    time.sleep(1)
    
    for freq in range(3000, 100, -100):
        robot.buzzer.tone(freq, 0.02) # při vynechání výchozí hodnota volume = 2000
        
    time.sleep(1)
    
    for freq in c_major_scale:
        robot.buzzer.tone(freq, 0.2, 3000)