from smbus2 import SMBus

class Sensor:
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address
        self.checkAddress()

    def checkAddress(self):
        if self.bus.read_byte_data(self.address, 0x0F) != 0xB1:
            raise RuntimeError("sensor on address " + self.address + " not detected")

    def sendMessage(self, message):
        self.bus.write_byte_data(self.address, message)
        
    def sendMessage(self, reg, message):
        self.bus.write_byte_data(self.address, reg, message)
        
    def readRawData(self, firstReg, regCount):
        data = self.bus.read_i2c_block_data(self.address, firstReg, regCount)
        return data


class LPS22HB(Sensor):
    def __init__(self, CTRL_REG1, sampling):
        self.CTRL_REG1 = CTRL_REG1
        self.sampling = sampling
        pass
            
    def setSamplingSpeed(self):
        self.bus.write_byte_data(self.address, self.CTRL_REG1, self.sampling)
    
    def readData(self, firstReg, regCount, conversionFactor):
        byteData = self.readRawData(firstReg, regCount)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData / conversionFactor
        return unitData

class SHTC3(Sensor):
    def __init__(self):
        pass
    
    def wakeUp(self):
        self.sendMessage(0x3517)
        
    def sleep(self):
        self.sendMessage(0xB098)
    
    def readTemp(self):
        byteData = self.readRawData(0x609C, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = -45+175*rawData #TODO test if the values are correct (rawData/2^16) from datasheet
        return unitData
    
    def readHumidity(self):
        byteData = self.readRawData(0x401A, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = 100*rawData #TODO test if the values are correct (rawData/2^16) from datasheet
        return unitData
    
class TCS34725(Sensor):
    def __init__(self):
        pass
    
    def readClear(self):
        byteData = self.readRawData(0x14, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData
        return unitData
    
    def readRed(self):
        byteData = self.readRawData(0x16, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData
        return unitData
    
    def readGreen(self):
        byteData = self.readRawData(0x18, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData
        return unitData
    
    def readBlue(self):
        byteData = self.readRawData(0x1A, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData
        return unitData
    
    def sleep(self):
        self.sendMessage(0x0, 0x09)
        
    def wakeUp(self):
        self.sendMessage(0x0, 0x03)
        
class ICM20948(Sensor):
    def __init__(self):
        self.sendMessage(0x7F, 0x00) #switches to user bank 0
        #self.sendMessage(0x01, 0x01) #
        #self.sendMessage(0x14, 0x01)
        self.sendMessage(0x06, 0x28) #power mgmt settings (wakeup)
        #magnetometer setup
        self.sendMessage(0x7F, 0x03) #switches to user bank 3
        self.sendMessage(0x03, 0x0C) #defines magnetometer address in write mode
        self.sendMessage(0x04, 0x31) #
        self.sendMessage(0x5, 0x96)
        self.sendMessage(0x03, (0x80|0x0C))
        
        #self.sendMessage(0x31, 0x1)
    
    def wakeUp(self):
        pass
    
    def readAccelX(self):
        self.sendMessage(0x7F, 0x00) #switches to user bank 0
        byteData = self.readRawData(0x2D, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData / 16384.0 #[g]
        return unitData
    
    def readAccelY(self):
        self.sendMessage(0x7F, 0x00) #switches to user bank 0
        byteData = self.readRawData(0x2F, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData / 16384.0 #[g]
        return unitData
    
    def readAccelZ(self):
        self.sendMessage(0x7F, 0x00) #switches to user bank 0
        byteData = self.readRawData(0x31, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData / 16384.0 #for +-2g range [g]
        return unitData
    
    def readGyroX(self):
        self.sendMessage(0x7F, 0x00) #switches to user bank 0
        byteData = self.readRawData(0x33, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData / 131.0 #for +- 250 dps [dps]
        return unitData
    
    def readGyroY(self):
        self.sendMessage(0x7F, 0x00) #switches to user bank 0
        byteData = self.readRawData(0x35, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData / 131.0 #for +- 250 dps [dps]
        return unitData
    
    def readGyroZ(self):
        self.sendMessage(0x7F, 0x00) #switches to user bank 0
        byteData = self.readRawData(0x37, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData / 131.0 #for +- 250 dps [dps]
        return unitData
    
    def readMagX(self):
        self.sendMessage(0x7F, 0x00) #switches to user bank 0
        byteData = self.readRawData(0x3B, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData / 131.0 #[mu T]
        return unitData
    
    def readMagY(self):
        self.sendMessage(0x7F, 0x00) #switches to user bank 0
        byteData = self.readRawData(0x3D, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData * 0.15 #[mu T]
        return unitData
    
    def readMagZ(self):
        self.sendMessage(0x7F, 0x00) #switches to user bank 0
        byteData = self.readRawData(0x3F, 2)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData / 131.0 #[mu T]
        return unitData
    