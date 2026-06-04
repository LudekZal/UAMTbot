# NOTE: USE_LASER = True NEEDED
import time

def run(robot):
    """
    Testovací skript pro modul laser
    """
    robot.display.clear()
    robot.display.text_centered("Test ToF Laser", 20)
    robot.display.text_centered("Probiha...", 40)
    robot.display.show()
    
    if not robot.laser.is_connected:
        robot.display.clear()
        robot.display.text_centered("ToF Laser OFF", 20)
        robot.display.text_centered("SW7 pro navrat", 40)
        robot.display.show()
        
        while True:
            sw3, sw4, sw5, sw7 = robot.buttons.read_states()
            if sw7:
                robot.buzzer.beep()
                break
            time.sleep(0.1)
        return
    
    while True:
        sw3, sw4, sw5, sw7 = robot.buttons.read_states()
        if sw7:
            robot.buzzer.beep()
            break
        
        dist = robot.laser.distance_mm()
        
        robot.display.clear()
        robot.display.text_centered("Distance: ", 5)
        robot.display.text_centered(f"{dist:.1f} mm", 20)
        
        robot.display.text_centered("SW7 pro ukonceni", 50)
        robot.display.show()
        
        time.sleep(0.1)
        