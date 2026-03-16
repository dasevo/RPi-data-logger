import Sensor
import smbus2 as SMBus

RPibus = SMBus(1)
m_LPS22HB = Sensor.LPS22HB(RPibus, 
                 0x5C, #sensor address
                 0x10, #control register 1 address
                 0x20) #sampling frequency of 10Hz (0x10 for 1Hz, 0x20 for 10Hz, 0x30 for 25Hz, 0x40 for 50Hz, 0x50 for 75Hz)



p = m_LPS22HB.readData(0x28, 3, 4096) #pressure reading in hPa
t = m_LPS22HB.readData(0x2B, 2, 100) #temperature reading in deg C