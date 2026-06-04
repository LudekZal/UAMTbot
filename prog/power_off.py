# NOTE: Press SW6 to reset
import machine
import time

def run(robot):
    """
    Uspí robota
    
    Pro opětovné zapnutí je třeba zmáčknou tlačítko SW6
    """
    
    robot.motors.stop()
    robot.leds.all(0, 0, 0)
    robot.display.clear()
    robot.display.text_centered("Vypinam", 20)
    robot.display.text_centered("Stiskni SW6", 40)
    robot.display.text_centered("Pro probuzeni",55)
    robot.display.show()
    time.sleep(5)
    
    robot.display.clear()
    
    machine.deepsleep()