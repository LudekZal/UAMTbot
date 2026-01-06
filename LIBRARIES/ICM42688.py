import machine
import time

class ICM42688:
    """Class for reading gyro rates and acceleration data from an ICM-42688 module via I2C."""
    
    def __init__(self, i2c:machine.I2C, address:int = 0x69):
        """
        Creates a new ICM42688 class.
        :param i2c: A setup I2C module of the machine module.
        :param address: The I2C address (0x69 is default for this chip).
        """
        self.address = address
        self.i2c = i2c
        
        # Check ID
        if self.who_am_i() != 0x47:
            print("Warning: Unknown Chip ID")
        
        # Reset device to default settings (Bank 0)
        self.i2c.writeto_mem(self.address, 0x11, bytes([0x01]))
        time.sleep(0.1)
        
    def wake(self) -> None:
        """Wake up the ICM-42688 and enable sensors (Low Noise Mode)."""
        # PWR_MGMT0 (0x4E): Set Gyro (bits 3:2) and Accel (bits 1:0) to Low Noise (11)
        # 0x0F = 0000 1111
        self.i2c.writeto_mem(self.address, 0x4E, bytes([0x0F]))
        time.sleep(0.05) # Wait for sensors to stabilize

    def sleep(self) -> None:
        """Places ICM-42688 in sleep mode."""
        # PWR_MGMT0 (0x4E): Set bits to 0 to turn off sensors
        self.i2c.writeto_mem(self.address, 0x4E, bytes([0x00]))
        
    def who_am_i(self) -> int:
        """Returns the address of the ICM-42688 (should be 0x47)."""
        # Register 0x75
        return self.i2c.readfrom_mem(self.address, 0x75, 1)[0]
    
    def read_temperature(self) -> float:
        """Reads the temperature in celsius."""
        # Register 0x1D (TEMP_DATA1)
        data = self.i2c.readfrom_mem(self.address, 0x1D, 2)
        raw_temp:float = self._translate_pair(data[0], data[1])
        # Formula for ICM-42688: (Raw / 132.48) + 25
        temp:float = (raw_temp / 132.48) + 25
        return temp

    def read_gyro_range(self) -> int:
        """Reads the gyroscope range index (0-3)."""
        # GYRO_CONFIG0 (0x4F). Bits 7:5 hold the range (FS_SEL).
        raw = self.i2c.readfrom_mem(self.address, 0x4F, 1)[0]
        # Shift right by 5 to get the top 3 bits
        return (raw >> 5) & 0x07
        
    def write_gyro_range(self, range:int) -> None:
        """
        Sets the gyroscope range setting.
        Range 0: +/- 2000 dps (default)
        Range 1: +/- 1000 dps
        Range 2: +/- 500 dps
        Range 3: +/- 250 dps
        Range 4: +/- 125 dps
        Range 5: +/- 62.5 dps
        Range 6: +/- 31.25 dps
        Range 7: +/- 15.625 dps
        """
        if not 0 <= range <= 7:
            raise ValueError("range musí být 0–7")

        reg = self.i2c.readfrom_mem(self.address, 0x4F, 1)[0]

        reg &= 0b00011111      # deletes bits 5-7
        reg |= (range << 5)   # sets bits 5-7

        self.i2c.writeto_mem(self.address, 0x4F, bytes([reg]))
        
    def read_gyro_data(self) -> tuple[float, float, float]:
        """Read the gyroscope data, in a (gx, gy, gz) tuple."""
        
        # Read range to determine scale modifier
        gr:int = self.read_gyro_range()
        modifier:float = 16.4 # Default for range 0 (+/- 2000)
        
        if gr == 0: modifier = 16.4
        elif gr == 1: modifier = 32.8
        elif gr == 2: modifier = 65.5
        elif gr == 3: modifier = 131.0
            
        # Register 0x25 is GYRO_DATA_X1
        data = self.i2c.readfrom_mem(self.address, 0x25, 6) 
        gx:float = (self._translate_pair(data[0], data[1])) / modifier
        gy:float = (self._translate_pair(data[2], data[3])) / modifier
        gz:float = (self._translate_pair(data[4], data[5])) / modifier
        
        return (gx, gy, gz)
                
    def read_accel_range(self) -> int:
        """Reads the accelerometer range index."""
        # ACCEL_CONFIG0 (0x50). Bits 7:5 hold the range.
        raw = self.i2c.readfrom_mem(self.address, 0x50, 1)[0]
        return (raw >> 5) & 0x07
    
    def write_accel_range(self, range:int) -> None:
        """
        Sets the accelerometer setting.
        Range 0: +/- 16g
        Range 1: +/- 8g
        Range 2: +/- 4g
        Range 3: +/- 2g
        """
        if not 0 <= range <= 3:
            raise ValueError("Required range 0-3")

        reg = self.i2c.readfrom_mem(self.address, 0x50, 1)[0]

        reg &= 0b00011111      # smaže jen bity 7–5
        reg |= (range << 5)   # nastaví nové

        self.i2c.writeto_mem(self.address, 0x50, bytes([reg]))
        
    def read_accel_data(self) -> tuple[float, float, float]:
        """Read the accelerometer data, in a (ax, ay, az) tuple."""
        
        # Read range
        ar:int = self.read_accel_range()
        modifier:float = 2048.0 # Default for range 0 (+/- 16g)
        
        # ICM ranges are reversed compared to MPU (0 is usually highest g)
        if ar == 0: modifier = 2048.0   # 16g
        elif ar == 1: modifier = 4096.0 # 8g
        elif ar == 2: modifier = 8192.0 # 4g
        elif ar == 3: modifier = 16384.0 # 2g
            
        # Register 0x1F is ACCEL_DATA_X1
        data = self.i2c.readfrom_mem(self.address, 0x1F, 6) 
        ax:float = (self._translate_pair(data[0], data[1])) / modifier
        ay:float = (self._translate_pair(data[2], data[3])) / modifier
        az:float = (self._translate_pair(data[4], data[5])) / modifier
        
        return (ax, ay, az)
            
    #### UTILITY FUNCTIONS ####
        
    def _translate_pair(self, high:int, low:int) -> int:
        """Converts a byte pair to a usable value. Borrowed from https://github.com/m-rtijn/mpu6050/blob/0626053a5e1182f4951b78b8326691a9223a5f7d/mpu6050/mpu6050.py#L76C39-L76C39."""
        value = (high << 8) + low
        if value >= 0x8000:
            value = -((65535 - value) + 1)
        return value
