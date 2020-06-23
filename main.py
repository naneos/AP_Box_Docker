### this file reads in the data from P2's serial / USB port

import serial
import queue
import threading

import datetime
from influxdb import InfluxDBClient
dbname = 'naneos_db'
import re
def write_P2_data_to_influx(string_P2, timestamp):
    splitedValues = re.split(r'\t[ ]*',string_P2)
    datapoints = [
                {
                    "measurement": 'p2_data',  #thats somethin like table
                    "tags": {
                        "Device": "P2_piezo_HW3"
                    },
                    "time": timestamp,
                    "fields": {
                        "seconds":          float(splitedValues[0]),
                        "number":           float(splitedValues[1]),
                        "diameter":         float(splitedValues[2]),
                        "LDSA":             float(splitedValues[3]),
                        "surface":          splitedValues[4],
                        "mass":             splitedValues[5],
                        "A1":               splitedValues[6],
                        "A2":               splitedValues[7],
                        "i_diff":           splitedValues[8],
                        "HV":               splitedValues[9],
                        "EM1":              splitedValues[10],
                        "EM2":              splitedValues[11],
                        "DV":               splitedValues[12],
                        "temperature":      splitedValues[13],
                        "rel_humidity":     splitedValues[14],
                        "pressure":         splitedValues[15],
                        "flow":             splitedValues[16],
                        "U_battery":        splitedValues[17],
                        "I_pump":           splitedValues[18],
                        "message_error":    splitedValues[19]
                    }
                }
            ]
    message_result = client.write_points(datapoints)
    print(message_result)


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
        print(line)

        write_P2_data_to_influx(line, timestamp)
        

       
except (KeyboardInterrupt, SystemExit):
    print('Mesurement interrupted')

serPartector.close()
