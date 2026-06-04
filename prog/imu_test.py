# NOTE: USE_IMU = True NEEDED
import time
import uamtbot_config

def run(robot):
    """
    Testovací skript pro modul imu
    """
    robot.display.clear()
    robot.display.text_centered("Test IMU", 20)
    robot.display.text_centered("Probiha...", 40)
    robot.display.show()
    time.sleep(1)
    
    if not robot.imu.is_connected:
        robot.display.clear()
        robot.display.text_centered("IMU OFF", 20)
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
        robot.display.clear()
        
        sw3, sw4, sw5, sw7 = robot.buttons.read_states()
        if sw7:
            robot.buzzer.beep()
            break
        
        pitch, roll = robot.imu.get_tilt()
        
        is_crashed = robot.imu.check_crash(threshold_g = 2.0)
        
        temp = robot.imu.read_temperature()
        
        robot.display.text_centered(f"Pitch: {pitch:.1f}", 5)
        robot.display.text_centered(f"Roll: {roll:.1f}", 20)
        robot.display.text_centered(f"Temp: {temp:.1f} C", 35)
        
        if is_crashed:
            robot.leds.all(0,128,0)
        else:
            robot.leds.all(0,0,0)
            robot.display.text_centered("SW7 pro ukonceni", 50)
            
        robot.display.show()
        
        time.sleep(0.1)

    robot.leds.all(0,0,0)
    robot.display.clear()