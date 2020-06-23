### this file reads in the data from P2's serial / USB port

import serial
import queue
import threading

import datetime
from influxdb import InfluxDBClient
dbname = 'naneos_db'
import re
def write_P2_data_to_influx(P2_data, timestamp):
    datapoints = [
                {
                    "measurement": 'p2_data',  #thats somethin like table
                    "tags": {
                        "Device": "P2_piezo_HW3"
                    },
                    "time": timestamp,
                    "fields": {
                        "seconds":          P2_data[0],
                        "number":           P2_data[1],
                        "diameter":         P2_data[2],
                        "LDSA":             P2_data[3],
                        "surface":          P2_data[4],
                        "mass":             P2_data[5],
                        "A1":               P2_data[6],
                        "A2":               P2_data[7],
                        "i_diff":           P2_data[8],
                        "HV":               P2_data[9],
                        "EM1":              P2_data[10],
                        "EM2":              P2_data[11],
                        "DV":               P2_data[12],
                        "temperature":      P2_data[13],
                        "rel_humidity":     P2_data[14],
                        "pressure":         P2_data[15],
                        "flow":             P2_data[16],
                        "U_battery":        P2_data[17],
                        "I_pump":           P2_data[18],
                        "message_error":    P2_data[19]
                    }
                }
            ]
    message_result = client.write_points(datapoints)
    print(message_result)

def P2_string2data(string_P2):
    try:
        splitedValues = re.split(r'\t[ ]*',string_P2)
        val = []

        val[0] = float(splitedValues[0])
        val[1] = int(splitedValues[1])
        val[2] = int(splitedValues[2])
        val[3] = float(splitedValues[3])
        val[4] = float(splitedValues[4])
        val[5] = float(splitedValues[5])
        val[6] = float(splitedValues[6])
        val[7] = float(splitedValues[7])
        val[8] = float(splitedValues[8])
        val[9] = int(splitedValues[9])
        val[10] = float(splitedValues[10])
        val[11] = float(splitedValues[11])
        val[12] = int(splitedValues[12])
        val[13] = float(splitedValues[13])
        val[14] = int(splitedValues[14])
        val[15] = float(splitedValues[15])
        val[16] = float(splitedValues[16])
        val[17] = float(splitedValues[17])
        val[18] = float(splitedValues[18])
        val[19] = int(splitedValues[19])
        return val
    except:
        print("ERROR: Serial data corrupted")

serQueue = queue.Queue(100)

def serialReadPartector(s):
    while True:
        sourceLine = s.readline().decode(encoding="ASCII")
        serialStream = sourceLine.replace('\n', '')
        serQueue.put(serialStream)

def openPort(port, baudrate):
    ser = serial.Serial()
    ser.port = (port) # on linux devices /dev/tty... + chmod 777
    ser.baudrate = baudrate
    while ser.isOpen() is False:
        if ser.isOpen():
            pass
        else:
            try:
                ser.open()
            except:
                print("openPort: Eception!")
                ser.close()
    return ser

## normal connection
# client = InfluxDBClient('naneosbox', 8088, dbname)

# drop + creation of new table
client = InfluxDBClient('naneosbox', 8086)
client.create_database(dbname)
client.switch_database(dbname)

serPartector = openPort('/dev/ttyACM0', 9600) #  /dev/ttyACM0 opens the device (P2) on the choosen Port
threading.Thread(target=serialReadPartector, args=(serPartector,), ).start() # starts the Serial Thread
line = serQueue.get(True) # throw first value away -> because it is sometimes incomplete
print(line)

try:
    while True:
        line = serQueue.get(True)
        timestamp=datetime.datetime.utcnow().isoformat()
        
        P2_data = P2_string2data(line)
        write_P2_data_to_influx(P2_data, timestamp)
        
        

       
except (KeyboardInterrupt, SystemExit):
    print('Mesurement interrupted')

serPartector.close()
