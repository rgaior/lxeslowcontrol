import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import numpy as np
import pandas as pd
from datetime import datetime
import time
import config

folder = config.hvlogfolder
filename = config.hvlogfile
logfilename = folder + filename
#ex : '2023-07-07T07:14:49'
#ex : [2023-07-07T07:12:23]: [DT5521HEM] bd [0] ch [0] par [IMon] val [-0.0014];


bucket = config.dbbucket
org = config.dborg
token = config.dbbucket
url= config.dburl



client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)


write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


nsec = 10

def get_last_date_log(logfilename):
    with open(logfilename, 'r') as f:
        lines = f.readlines()
        last = lines[-1]
        lastdateascii = last.split(' ')[0][1:-2]
        lastdate = datetime.strptime(lastdateascii,'%Y-%m-%dT%H:%M:%S')
        return lastdate
        

def get_last_date_db():
    df = query_api.query_data_frame('from(bucket:"test") '
                                '|> range(start: -100d) '
                                '|> filter(fn: (r) => r._measurement == "DT5521HEM") '
                                '|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") '
                                '|> keep(columns: ["_start","_stop","_time","_measurement"])')
    return np.max(df['_time']).to_pydatetime().replace(tzinfo=None)


def fill_all_file(logfilename):
    with open(logfilename, 'r') as f:
        lines = f.readlines()
        for l in lines:
            print(l)
            log_to_db(l)



def log_to_db(line):
#ex : [2023-07-07T07:12:23]: [DT5521HEM] bd [0] ch [0] par [IMon] val [-0.0014];
    line_s = line.split(' ')
    dateascii = line_s[0][1:-2]
    date = datetime.strptime(dateascii,'%Y-%m-%dT%H:%M:%S')
    measurement_name = line_s[1][1:-1]
    channel = int(line_s[5][1:-1])
    param = line_s[7][1:-1]
    param_val = float(line_s[9][1:-2])
    fields = {}
    fields[param] = param_val
    record =[
        {
            "measurement":measurement_name,
            "tags": {"channel": channel},
            "fields":fields,
            "time": date
        }
    ]
    write_api.write(bucket, org, record= record)


def log():
    while True:
        time.sleep(nsec)
        print("logging hv")
        # last_date_log = get_last_date_log(folder + filename)
        # last_date_db = get_last_date_db()
        # print ("last_date_log", last_date_log)
        # print ("last_date_db", last_date_db)

        # if (last_date_db == last_date_log):
        #     print('no new entry in the log w.r.t. the data base')

        # else:
        #     print('new entries in the log file')
        #     last_entries = []
        #     with open(logfilename, 'r') as f:
        #         lines = f.readlines()
        #         invlines = lines[::-1]
        #         for l in invlines:
        #             l_s = l.split(' ')
        #             print(l_s)
        #             dateascii = l_s[0][1:-2]
        #             date_log = datetime.strptime(dateascii,'%Y-%m-%dT%H:%M:%S')
        #             if date_log == last_date_db:
        #                 break
        #             else: 
        #                 log_to_db(l)
        #         print('ended the db update')


#fill_all_file(folder + filename)


