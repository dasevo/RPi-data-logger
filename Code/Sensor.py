from smbus2 import SMBus

class Sensor:
    def __init__(self, bus, address, CTRL_REG1, sampling):
        self.bus = bus
        self.address = address
        self.CTRL_REG1 = CTRL_REG1
        self.sampling = sampling
        self.checkAddress()

    def checkAddress(self):
        if self.bus.read_byte_data(self.address, 0x0F) != 0xB1:
            raise RuntimeError("sensor on address " + self.address + " not detected")
        
    def setSamplingSpeed(self):
        self.bus.write_byte_data(self.address, self.CTRL_REG1, self.sampling)

    def sendMessage(self, message):
        self.bus.write_byte_data(self.address, message)

    def readRawData(self, firstReg, regCount):
        data = self.bus.read_i2c_block_data(self.address, firstReg, regCount)
        return data

    def readData(self, firstReg, regCount, conversionFactor):
        byteData = self.readRawData(firstReg, regCount)
        rawData = int.from_bytes(byteData, "little")
        unitData = rawData / conversionFactor
        return unitData

