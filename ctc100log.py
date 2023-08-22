import serial
import time
import csv
# import module
from datetime import datetime
import pytz
from datetime import timezone
import config 
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from backports.zoneinfo import ZoneInfo
    

bucket = config.dbbucket
org = config.dborg
token = config.dbtoken
url= config.dburl



client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)

nsec = 1

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


def getfilename():
    # get current date and time
#    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    current_datetime = datetime.now().strftime("%Y-%m-%d")
#    print("Current date & time : ", current_datetime)
    
    # convert datetime obj to string
    str_current_datetime = str(current_datetime)
 
    # create a file object along with extension
    file_name = str_current_datetime+".txt"
 
    return file_name 

port = config.ctcport
ser = serial.Serial(port, baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
ser.flushInput()

datafolder = config.templogfolder

def fill_db(channel,date,val):
    jp = ZoneInfo('Asia/Tokyo')
#    date_log = date.replace(tzinfo=pytz.timezone('Japan'))
    date_log = date.replace(tzinfo= jp)
    date_log=date_log.astimezone(tz=pytz.timezone('UTC'))
    record =[
        {
            "measurement":"temperature",
            "tags": {"channel": channel},
            "fields":{'val':val},
            "time": date_log
        }
    ]
    write_api.write(bucket, org, record= record)


def get_var(ser,varname):
    s = varname+"?\n"
    var = ser.write(s.encode())
    #var = ser.write("IN1?\n".encode())
    ser_bytes = ser.readlines()[0] 
    print(ser_bytes)
    var = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    return var

var_list = ["IN1", "IN2", "IN3", "IN4", "AIO1", "AIO2", "AIO3", "AIO4"]
 
def log():
    while True:
        try:
            val_array = []
            for v in var_list:
                print(v)
                v_val = get_var(ser,v)
                print(v_val)
                val_array.append(v_val)
#                print(datetime.now())
                fill_db(v, datetime.now(),v_val)
            filename = datafolder + getfilename()
            print(filename)
            with open(filename,"a") as f:
                writer = csv.writer(f,delimiter=",")            
                writer.writerow([datetime.now()] + val_array)                
            time.sleep(nsec)
        except:
            print("Keyboard Interrupt")
            break



if __name__ == "__main__":
    main()
