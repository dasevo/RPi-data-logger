import Sensors
import smbus2 as SMBus

RPibus = SMBus(1)
m_LPS22HB = Sensors.LPS22HB(RPibus, 
                 0x5C, #sensor address
                 0x10, #control register 1 address
                 0x20) #sampling frequency of 10Hz (0x10 for 1Hz, 0x20 for 10Hz, 0x30 for 25Hz, 0x40 for 50Hz, 0x50 for 75Hz)



p = m_LPS22HB.readData(0x28, 3, 4096) #pressure reading in hPa
t = m_LPS22HB.readData(0x2B, 2, 100) #temperature reading in deg C

m_SHTC3 = Sensors.SHTC3(RPibus, 0x70)
m_SHTC3.wakeUp()
rh = m_SHTC3.readHumidity() #[%]
t = m_SHTC3.readTemp() #[°C]
m_SHTC3.sleep()

m_TCS34725 = Sensors.TCS34725(RPibus, 0x6a)
m_TCS34725.wakeUp()
c = m_TCS34725.readClear()
r = m_TCS34725.readRed()
g = m_TCS34725.readGreen()
b = m_TCS34725.readBlue()
m_TCS34725.sleep()

m_ICM20948 = Sensors.ICM20948(RPibus, 0x68)
m_ICM20948.wakeUp()
aX = m_ICM20948.readAccelX()
aY = m_ICM20948.readAccelY()
aZ = m_ICM20948.readAccelZ()
gX = m_ICM20948.readGyroX()
gY = m_ICM20948.readGyroY()
gZ = m_ICM20948.readGyroZ()
mX = m_ICM20948.readMagX()
mY = m_ICM20948.readMagY()
mZ = m_ICM20948.readMagZ()

print("tlak: " + p)
print("teplota: " + t)
print("clear: " + c)
print("red: " + r)
print("green: " + g)
print("blue: " + b)
print("ax: " + aX)
print("ay: " + aY)
print("az: " + aZ)
print("gx: " + gX)
print("gy: " + gY)
print("gz: " + gZ)
print("mx: " + mX)
print("my: " + mY)
print("mz: " + mZ)