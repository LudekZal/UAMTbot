# NOTE: Pro "připojení" modulu použít USE_<MODUL> = True, jinak False (případně zakomentovat řádek), následně nahrát do Pica
# NOTE: Pro IMU a konektory nelze použít stejné ID 
# NOTE: Display a Laserový senzor využívají stejnou i2c, je nutné je zapojit paralelně na stejné piny

DEBUG_MODE = False  # výpis akcí do konzole
# ---------- LEDS  ----------
USE_LEDS = False
LED_PIN = 22
NUM_PIXELS = 10
# ---------- BUZZER  ----------
USE_BUZZER = False
BUZZER_PIN = 7   
# ---------- DISPLAY  ----------
USE_DISPLAY = True
I2C_DISPLAY = 0 # id
SDA_PIN_DISPLAY = 4
SCL_PIN_DISPLAY = 5
# ---------- MOTORS  ----------
USE_MOTORS = True
MOT1_DIR_PIN = 16
MOT1_PWM_PIN = 17
MOT1_SLEEP_PIN = 18
MOT2_DIR_PIN = 19
MOT2_PWM_PIN = 20
MOT2_SLEEP_PIN = 21
# ---------- IMU  ----------
USE_IMU = True
I2C_IMU = 1 # i2c id (0 / 1)
SDA_PIN_IMU = 10 
SCL_PIN_IMU = 11
# ---------- DISTANCE (VL53L1X ToF sensor)  ----------
USE_LASER = False # VL53L1X tof sensor
I2C_LASER = 0
SDA_PIN_LASER = 4
SCL_PIN_LASER = 5
# ---------- MUX  ----------
USE_MUX = True
MUX_ADC_PIN = 26
MUX_S0_PIN = 15
MUX_S1_PIN = 14
# ---------- BUTTONS  ----------
USE_BUTTONS = True
SW7_PIN = 13
# ---------- REFLEX SENSORS  ----------
USE_REFLEX = True
REFLEX_L_PIN = 28
REFLEX_R_PIN = 27
# ---------- BATTERY VOLTAGE  ----------
USE_VOLTAGE = False

# I2C help
# i2c -> ID 0 - sda 0 scl 1
#               sda 4 scl 5
#        ID 1 - sda 2 scl 3