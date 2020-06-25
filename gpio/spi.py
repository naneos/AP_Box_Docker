import spidev

spi = spidev.SpiDev()
spi.open(0,0) # opens CS0

temp_bytes = spi.readbytes(4)
temp = int.from_bytes(temp_bytes)

spi.close

print(temp)