# NOTE: USE_MOTORS = True NEEDED
import time

def run(robot):
    """
    Testovací skript pro modul motors
    """
    robot.display.clear()
    robot.display.text_centered("Test Motors", 20)
    robot.display.text_centered("Probiha...", 40)
    robot.display.show()   

    if not robot.motors.is_connected:
        robot.display.clear()
        robot.display.text_centered("Motors OFF", 20)
        robot.display.text_centered("SW7 pro navrat", 40)
        robot.display.show()
        
        while True:
            sw3, sw4, sw5, sw7 = robot.buttons.read_states()
            if sw7:
                robot.buzzer.beep()
                break
            time.sleep(0.1)
        return
    
    # Forward & Backward
    robot.motors.set(3000, 1, 3000, 1)
    time.sleep(1)
    robot.motors.stop()   
    time.sleep(0.5)
    
    robot.motors.set(3000, 0, 3000, 1)
    time.sleep(1)
    robot.motors.stop()   
    time.sleep(0.5)

    # Spin
    robot.motors.set(3000, 0, 3000, 1)  
    time.sleep(0.5)
    robot.motors.stop()
    time.sleep(0.5)
    
    robot.motors.set(3000, 1, 3000, 0)  
    time.sleep(0.5)
    robot.motors.stop()
    time.sleep(1)
    
    # Ramp
    robot.motors.ramp(4000, 1, 4000, 1, 2000)
    robot.motors.stop_ramp(4000, 4000, 2000)
    
    robot.motors.stop()