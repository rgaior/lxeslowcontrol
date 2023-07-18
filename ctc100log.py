import serial
import time
import csv
# import module
from datetime import datetime
import config 

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
def log():
    while True:
        try:
            print('toto')
            # in1 = ser.write("IN1?\n".encode())
            # ser_bytes = ser.readlines()[0] 
            # t1 = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            # in2 = ser.write("IN2?\n".encode())
            # ser_bytes = ser.readlines()[0] 
            # t2 = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            # in3 = ser.write("IN3?\n".encode())
            # ser_bytes = ser.readlines()[0] 
            # t3 = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            # in4 = ser.write("IN4?\n".encode())
            # ser_bytes = ser.readlines()[0] 
            # t4 = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            # filename = datafolder + getfilename()
            # print(filename)
            # with open(filename,"a") as f:
            #     print('here')
            #     writer = csv.writer(f,delimiter=",")
            #     writer.writerow([datetime.now(),t1,t2,t3,t4])
            time.sleep(1)
        except:
            print("Keyboard Interrupt")
        break



if __name__ == "__main__":
    main()
