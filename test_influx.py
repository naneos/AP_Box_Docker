import argparse
import time
import datetime
import sys
from influxdb import InfluxDBClient

 
# Set required InfluxDB parameters.
# (this could be added to the program args instead of beeing hard coded...)
host = "naneosbox" #Could also set local ip address
port = 8086
# user = "root"
# password = "root"


def get_args():
    '''This function parses and returns arguments passed in'''
    # Assign description to the help doc
    parser = argparse.ArgumentParser(description='Program writes measurements data from SenseHat to specified influx db.')
    # Add arguments
    parser.add_argument(
        '-db','--database', type=str, help='Database name', required=True)
    parser.add_argument(
        '-sn','--session', type=str, help='Session', required=True)
    now = datetime.datetime.now()
    parser.add_argument(
        '-rn','--run', type=str, help='Run number', required=False,default=now.strftime("%Y%m%d%H%M"))
    
    # Array of all arguments passed to script
    args=parser.parse_args()
    # Assign args to variables
    dbname=args.database
    runNo=args.run
    session=args.session
    return dbname, session,runNo
    
def get_data_points():
    # Get the three measurement values from the SenseHat sensors
    temperature = 7
    pressure = 8
    humidity = 9
    # Get a local timestamp
    timestamp=datetime.datetime.utcnow().isoformat()
    print ("{0} {1} Temperature: {2}{3}C Pressure: {4}mb Humidity: {5}%" .format(session,runNo,
    round(temperature,1),u'u00b0'.encode('utf8'),round(pressure,3),round(humidity,1)))
    
    # Create Influxdb datapoints (using lineprotocol as of Influxdb >1.1)
    datapoints = [
            {
                "measurement": session,  #thats somethin like table
                "tags": {
                    "Device": "P2_piezo_HW3"
                },
                "time": timestamp,
                "fields": {
                    "a": 33,
                    "b": 77,
                    "c": 333
                }
            }
        ]
    return datapoints

# Match return values from get_arguments()
# and assign to their respective variables
dbname = 'p2_data'
session = 'session'
runNo = 'runNo'   
print("Session: ", session)
print("Run No: ", runNo)
print("DB name: ", dbname)

# Initialize the Influxdb client
client = InfluxDBClient(host, port, dbname)
# client.create_database('p2_data')
client.switch_database('p2_data')

datapoints = get_data_points()
bResult=client.write_points(datapoints)
print("Write points {0} Bresult:{1}".format(datapoints,bResult))