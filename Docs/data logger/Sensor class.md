#### 1. Address check
- Run `bus.read_byte_data(address, 0x0F)`
- Expected return is `0xB1`
#### 2. Init the sensor
- Make sure the sensor is awake
- `CTRL_REG1 = 0x10`
- `FREQ_REG = 0x20` (this sets sampling to 10 Hz)
- `bus.write_byte_data(addr, CTRL_REG1, FREQ_REG`

#### 3. Read data registers
- Define the bytes that are supposed to be read
- `data = bus.read_i2c_block_data(address, starting_register, number_of_bytes`
- After reading the data stream, convert the data stream into raw data
- `raw_data = (data[n] << 8*n) | (data[n-1] <<8*(n-1)) | ... | data[0]`
- Then convert the raw tdata into real units data

#### 4. Optional
- To make sure that the sensor has new data, we can run a status check: `STATUS_REG = 0x27`