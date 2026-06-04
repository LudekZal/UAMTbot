# NOTE: USE_LED = True NEEDED
import time

def run(robot):
    """
    Testovací skript pro modul leds
    """
    robot.display.clear()
    robot.display.text_centered("Test LED", 20)
    robot.display.text_centered("Probiha...", 40)
    robot.display.show()
    
    if not robot.leds.is_connected:
        robot.display.clear()
        robot.display.text_centered("LEDS OFF", 20)
        robot.display.text_centered("SW7 pro navrat", 40)
        robot.display.show()
    
        while True:
            sw3, sw4, sw5, sw7 = robot.buttons.read_states()
            if sw7:
                robot.buzzer.beep()
                break
            time.sleep(0.1)
        return
    
    NUM_LEDS = len(robot.leds.np)
    
    for _ in range(3):
        for i in range(1, NUM_LEDS + 1):
            robot.leds.set(i, 128, 0, 0)
            robot.leds.show()
            time.sleep(0.05)
            robot.leds.set(i, 0, 0, 0)
            
        for i in range(NUM_LEDS - 1, 0, -1):
            robot.leds.set(i, 128, 0, 0)
            robot.leds.show()
            time.sleep(0.05)
            robot.leds.set(i, 0, 0, 0)
    
    time.sleep(2)
    
    for i in range(1, NUM_LEDS + 1):
        r = i * (128 // NUM_LEDS)
        b = 128 - r
        robot.leds.set(i, r, 0, b)
        time.sleep(0.1)
    robot.leds.clear()
    