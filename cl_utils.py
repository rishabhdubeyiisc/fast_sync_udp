#!/usr/bin/env python3
from influxdb import InfluxDBClient
import datetime
import pytz
from utils import check_sudo

class LogIt():
    def __init__(   self , 
                    logger_name     : str   = 'logger'      , 
                    logging_level   : str   = 'DEBUG'       , 
                    filename        : str   = 'log_logger.log'  , 
                    to_log          : bool  = True
                 ):
        import logging
        check_sudo()

        self._logger_dict = { 'CRITICAL' : 50 , 'ERROR' : 40 , 'WARNING' : 30 , 'INFO' : 20 , 'DEBUG' : 10}

        self._logger_formatter = logging.Formatter('%(asctime)s : %(module)s : %(threadName)s : %(levelname)s : %(funcName)s : %(message)s')

        #creating a logger for transactions
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(self._logger_dict[logging_level])

        self._logger_file_handler = logging.FileHandler(filename = filename , mode='w')
        self._logger_file_handler.setFormatter(self._logger_formatter)

        self.logger.addHandler(self._logger_file_handler)

        #log master
        self.to_log = to_log
        #create log header
        self.logger.info("log file")

    def log(self ,msg : str):
        if self.to_log :
            self.logger.debug(msg)
    
    def log_info (self ,msg : str):
        self.logger.info(msg)
'''
class db_client_cls:
    _counter = int(0)
    def __init__(   self, 
                    IFhost          : str = "localhost" , 
                    IFport          : int = 8086        , 
                    IFDbname        : str = 'CPU'       , 
                    logging_level   : str = 'DEBUG'     ,
                    to_log          : bool = False   
                ):
        db_client_cls._counter += 1
        self._instance_id = db_client_cls._counter 
        self._logger = LogIt(    
                                logger_name = ( "db_cl_" + IFDbname + ".log"), 
                                logging_level = logging_level , 
                                filename= ("log_db_cl_" + str(db_client_cls._counter) +"_" + IFDbname + ".log") ,
                                to_log=to_log
                            )
        
        self._IFhost = IFhost
        self._IFport = IFport
        self._IFDbname = IFDbname
        #create a client
        self._client = InfluxDBClient(host=self._IFhost, port=self._IFport , database=self._IFDbname)
        print("IFDbname -> {}".format(self._IFDbname))
        print(self._get_db_list())
        to_run_script= input("press y/Y if DB created -> ")
        if (to_run_script.lower() != 'y'):
            exit(-99)
        self._swtich_to_DB()
        #info logs
        self._logger.log_info( f"Host , Port -> {self._IFhost} - {self._IFport} ")
        self._logger.log_info( f"DB_source_Name -> {self._IFDbname} ")

    def _create_DB_by_name(self ):
        self._logger.log_info( f"create_DB_by_name -> {self._IFDbname} ")
        self._client.create_database(self._IFDbname)

    def _get_db_list(self):
        self._logger.log_info( f"DB source list -> {self._client.get_list_database()} ")
        return self._client.get_list_database()

    def _swtich_to_DB(self):
        self._client.switch_database(self._IFDbname)
        self._logger.log_info( f"Switching to -> {self._IFDbname} ")

    def write_point_to_db ( self , data_json , ERR_str = "") -> bool:          
        is_data_wr = self._client.write_points(data_json)
        if(not is_data_wr):
            self._logger.log_info( f"ERR [DATA NOT WRITTEN] -> {self._IFDbname}")
        return is_data_wr

    def write_list_to_db ( self , data_json_list ,batch_size , ERR_str = "") -> bool:
        is_data_wr = self._client.write_points(points=data_json_list,batch_size=batch_size)
        if(not is_data_wr):
            self._logger.log_info( f"ERR [DATA NOT WRITTEN] -> {self._IFDbname}")
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

'''
class db_client_cls:
    _counter = int(0)
    def __init__(   self, 
                    IFhost          : str = "localhost" , 
                    IFport          : int = 8086        , 
                    IFDbname        : str = 'CPU'       , 
                    logging_level   : str = 'DEBUG'     ,
                    to_log          : bool = False   
                ):
        db_client_cls._counter += 1
        self._instance_id = db_client_cls._counter 
        self._logger = LogIt(    
                                logger_name = ( "db_cl_" + IFDbname + ".log"), 
                                logging_level = logging_level , 
                                filename= ("log_db_cl_" + str(db_client_cls._counter) +"_" + IFDbname + ".log") ,
                                to_log=to_log
                            )
        
        self._IFhost = IFhost
        self._IFport = IFport
        self._IFDbname = IFDbname
        #create a client
        self._client = InfluxDBClient(host='localhost',port=8089,database= self._IFDbname , use_udp=True, udp_port=8089)
        #self._client = InfluxDBClient(host=self._IFhost, port=self._IFport , database=self._IFDbname)
        print("IFDbname -> {}".format(self._IFDbname))
        print(self._get_db_list())
        to_run_script= input("press y/Y if DB created -> ")
        if (to_run_script.lower() != 'y'):
            exit(-99)
        self._swtich_to_DB()
        #info logs
        self._logger.log_info( f"Host , Port -> {self._IFhost} - {self._IFport} ")
        self._logger.log_info( f"DB_source_Name -> {self._IFDbname} ")

    def _create_DB_by_name(self ):
        self._logger.log_info( f"create_DB_by_name -> {self._IFDbname} ")
        self._client.create_database(self._IFDbname)

    def _get_db_list(self):
        self._logger.log_info( f"DB source list -> {self._client.get_list_database()} ")
        return self._client.get_list_database()

    def _swtich_to_DB(self):
        self._client.switch_database(self._IFDbname)
        self._logger.log_info( f"Switching to -> {self._IFDbname} ")

    def write_point_to_db ( self , data_json , ERR_str = "") -> bool:          
        is_data_wr = self._client.write_points(data_json)
        if(not is_data_wr):
            self._logger.log_info( f"ERR [DATA NOT WRITTEN] -> {self._IFDbname}")
        return is_data_wr

    def write_list_to_db ( self , data_json_list ,batch_size , ERR_str = "") -> bool:
        is_data_wr = self._client.write_points(points=data_json_list,batch_size=batch_size)
        if(not is_data_wr):
            self._logger.log_info( f"ERR [DATA NOT WRITTEN] -> {self._IFDbname}")
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
        from cl_utils import LogIt
        self._logger = LogIt(logger_name="queue",logging_level='DEBUG',filename='log_queue.log',to_log=to_log_queue)
        self._q = Queue.Queue(BUF_SIZE)
        self._to_log = to_log_queue
        self._logger.log_info(__name__)

    def put_in_queue(self , item):
        if not self._q.full():
            self._q.put(item)
            if self._to_log :
                self._logger.log(f"PUT item , queue_size -> {item} , {self._q.qsize()} " )

    def remove_from_queue(self):
        '''
            return item
        '''
        item = None
        if not self._q.empty():
            item = self._q.get()
            if self._to_log :
                self._logger.log(f"GET item , queue_size -> {item} , {self._q.qsize()} " )

        return item
    
    def size(self)-> int :
        return self._q.qsize()
