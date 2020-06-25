import spidev

def readTemp():
    spi = spidev.SpiDev()
    spi.open(0,0) # opens CS0

    temp_bytes = spi.readbytes(4)

    temp = int.from_bytes(temp_bytes, byteorder='little')
    error_open_connection = bool(temp & 0x01)
    error_short_circuit_GND = bool((temp >> 1) & 0x01)
    error_short_circuit_VCC = bool((temp >> 2) & 0x01)
    temp_internal = (((temp >> 4) & 0x7FF) * 0.0625) * ((-1) * ((temp >> 15) & 0x01))
    temp_thermocouple = (((temp >> 18) & 0x3FFF) * 0.25) * ((-1) * ((temp >> 31) & 0x01))

    spi.close

    print("Error open connection: " + str(error_open_connection))
    print("Error short circuit to GND: " + str(error_short_circuit_GND))
    print("Error short circuit to VCC: " + str(error_short_circuit_VCC))
    print("Internal junction temperature: " + str(temp_internal) + " °C")
    print("Thermocouple temperature: " + str(temp_thermocouple) + " °C")

    return(temp_thermocouple)


if __name__ == "__main__":
    readTemp()
    pass