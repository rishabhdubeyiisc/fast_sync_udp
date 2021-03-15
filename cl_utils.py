#!/usr/bin/env python3
from influxdb import InfluxDBClient
import datetime
import pytz

class db_client_cls:
    def __init__(self, IFhost = "localhost" , IFport = 8086 , IFDbname = 'CPU'):
        self.IFhost = IFhost
        self.IFport = IFport
        self.IFDbname = IFDbname
        #create a client
        self.client = InfluxDBClient(host=IFhost, port=IFport , database=IFDbname)
        print(self.get_db_list())
        to_run_script= input("press y/Y if DB created : ")
        if (to_run_script.lower() != 'y'):
            exit(-99)
        self.swtich_to_DB()

    def create_DB_by_name(self ):
        self.client.create_database(self.IFDbname)

    def get_db_list(self):
        return self.client.get_list_database()

    def swtich_to_DB(self):
        self.client.switch_database(self.IFDbname)

    def write_to_db ( self , data_json , ERR_str = "", verbose_mode = True) -> bool:
        if (verbose_mode):
            print(data_json)
        is_data_wr = self.client.write_points(data_json)
        if(not is_data_wr):
            print("ERR : data not written " + ERR_str )
        return is_data_wr

    def create_me_json (self, 
                        measurement = 'comm_delay'  , 
                        tag_name    = 'pmu_34'      , tag_field = 'fracsec_diff' , 
                        field_name  = 'pdc_pmu_diff', field_value = 0):
        time_stamp = datetime.datetime.now(pytz.utc)
        data_json = [
                        {
                            'measurement' : measurement ,
                            'tags' : { tag_name : tag_field },
                            'time' : time_stamp ,
                            'fields' : { field_name : float(field_value)}
                        }
                    ]

        return data_json

class Thread_safe_queue():
    def __init__(self , BUF_SIZE = 0 , to_log_queue = True):
        '''
            BUF_SIZE = 0 -> infinite size queue
        '''
        import queue as Queue
        import logging
        from utils import LogIt
        self.logger = LogIt(logger_name="queue",logging_level='DEBUG',filename='queue.log',to_log=to_log_queue)
        self.q = Queue.Queue(BUF_SIZE)
        self.to_log = to_log_queue

    def put_in_queue(self , item):
        if not self.q.full():
            self.q.put(item)
            if self.to_log :
                self.logger.log('Putting ' + str(item) + ' : ' + str(self.q.qsize()) + ' items in queue')

    def remove_from_queue(self):
        item = None
        if not self.q.empty():
            item = self.q.get()
                if self.to_log :
                self.logger.log('Getting ' + str(item)  + ' : ' + str(self.q.qsize()) + ' items in queue')
        return item
