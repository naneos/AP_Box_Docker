import spidev

spi = spidev.SpiDev()
spi.open(0,0) # opens CS0

temp = spi.readbytes(4)

spi.close

print(temp)