import spidev

spi = spidev.SpiDev()
spi.open(0,0) # opens CS0

temp_bytes = spi.readbytes(4)

temp = int.from_bytes(temp_bytes, byteorder='big')
error_open_connection = bool(temp & 0x01)
error_short_circuit_GND = bool((temp >> 1) & 0x01)
error_short_circuit_VCC = bool((temp >> 2) & 0x01)

spi.close

print("Error open connection: " + str(error_open_connection))
print("Error short circuit to GND: " + str(error_short_circuit_GND))
print("Error short circuit to VCC: " + str(error_short_circuit_VCC))