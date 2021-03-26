#! /usr/bin/env python3
import struct
from time import time
import threading
import queue as Queue

from cl_inherited_comms import PDC_server
from cl_utils import db_client_cls as db_client
from cl_utils import Thread_safe_queue as TH_Queue
#8 bit time quality msg
TIME_FLAGS = 0b0010
TIME_QUALITY = 0x5
lis = [TIME_FLAGS, TIME_QUALITY ]
TIME_MSG = bytes(lis) 
#TIME_MSG = 0b00100101
from frame import ConfigFrame2
from frame import DataFrame

data_rate=30
ieee_cfg2_sample = ConfigFrame2(12345, 1000000, 1, "Station A", 7734, (False, False, True, False),
                                        4, 3, 1,
                                        ["VA", "VB", "VC", "I1", "ANALOG1", "ANALOG2", "ANALOG3",
                                        "BREAKER 1 STATUS", "BREAKER 2 STATUS", "BREAKER 3 STATUS",
                                        "BREAKER 4 STATUS", "BREAKER 5 STATUS", "BREAKER 6 STATUS",
                                        "BREAKER 7 STATUS", "BREAKER 8 STATUS", "BREAKER 9 STATUS",
                                        "BREAKER A STATUS", "BREAKER B STATUS", "BREAKER C STATUS",
                                        "BREAKER D STATUS", "BREAKER E STATUS", "BREAKER F STATUS",
                                        "BREAKER G STATUS"],
                                        [(915527, "v"), (915527, "v"), (915527, "v"), (45776, "i")],
                                        [(1, "pow"), (1, "rms"), (1, "peak")], [(0x0000, 0xffff)],
                                        60, 22, data_rate)

def main(   th_Q        : TH_Queue              ,
            pmu34_db    : db_client             , 
            pdc         : PDC_server            , 
            pmu_IP      : str = '10.64.37.34'   , 
            pmu_port    : int = 12345               
        ):
    sqn_num = int(0)
    try :
        while True:
            #recv
            loop_start_time = time()
            data_recvd , addr_of_client = pdc.recv()
            #
            server_ct = time()
            SOC_server = int(server_ct)
            FRASEC_server = int (  (server_ct - SOC_server) * (10**6) )

            SOC_Client = struct.unpack('!HHHIIHIIIIHHIIIHH',data_recvd)[3]
            FRASEC_Client = struct.unpack('!HHHIIHIIIIHHIIIHH',data_recvd)[4]
            FRASEC_diff = FRASEC_server - FRASEC_Client
            SOC_diff = SOC_server - SOC_Client
            print( SOC_server , SOC_Client , FRASEC_server , FRASEC_Client , FRASEC_diff)
            #store over db
            '''
            db_start_time = time()
            entry = pmu34_db.create_me_json(measurement='comm_delay',
                                    tag_name='pmu_34',tag_field='fracsec_diff',
                                    field_name='pdc_pmu_diff',field_value=FRASEC_diff)
            pmu34_db.write_to_db(data_json=entry,verbose_mode=False)
            db_end_time = time()
            '''
            #push to queue
            '''
            db_start_time = time()
            entry = pmu34_db.create_me_json(measurement='comm_delay',
                        tag_name='pmu_34',tag_field='fracsec_diff',
                        field_name='pdc_pmu_diff',field_value=FRASEC_diff)
            th_Q.put_in_queue(item = entry)
            db_end_time = time()
            '''
            #send
            sqn_num = sqn_num + 1
            msg = str(sqn_num)
            pdc.send_to(pmu_IP=addr_of_client[0] , pmu_port=addr_of_client[1] , payload = msg.encode() )
            loop_end_time = time()

            #print( (loop_end_time-loop_start_time) , (db_end_time - db_start_time) , ((loop_end_time-loop_start_time) / (db_end_time - db_start_time)) )
    
    except KeyboardInterrupt :
        print("exited by user")

def recv_func( pdc : PDC_server ):
    sqn_num = int(0)
    try :
        while True:
            #recv
            data_recvd , addr_of_client = pdc.recv()
            #
            server_ct = time() - 0
            SOC_server = int(server_ct)
            FRASEC_server = int (  (server_ct - SOC_server) * (10**6) )

            SOC_Client = struct.unpack('!HHHIIHIIIIHHIIIHH',data_recvd)[3]
            FRASEC_Client = struct.unpack('!HHHIIHIIIIHHIIIHH',data_recvd)[4]
            FRASEC_diff = FRASEC_server - FRASEC_Client
            SOC_diff = SOC_server - SOC_Client
            print( SOC_server , SOC_Client , FRASEC_server , FRASEC_Client , FRASEC_diff)
    except KeyboardInterrupt :
        print("exited by user")

def send_func(  pdc         : PDC_server            , 
                pmu_IP      : str = '10.64.37.34'   , 
                pmu_port    : int = 12345           
            ):
    sqn_num = int(0)
    try :
        sqn_num = sqn_num + 1
        msg = str(sqn_num)
        pdc.send_to(pmu_IP=pmu_IP , pmu_port= pmu_port, payload = msg.encode() )

    except KeyboardInterrupt :
        print("exited by user")

def upload_func(pmu34_db    : db_client , th_Q : TH_Queue):
    while True:
        #store over db
        entry = th_Q.remove_from_queue()
        #print("entry : {} ".format(entry))
        if entry != None :
            #print("entry : {} ".format(entry))
            pmu34_db.write_to_db(data_json=entry,verbose_mode=False)
        #import time
        #time.sleep(1.0)

def recv_data_frame(   th_Q        : TH_Queue              ,
            pmu34_db    : db_client             , 
            pdc         : PDC_server            , 
            pmu_IP      : str = '10.64.37.34'   , 
            pmu_port    : int = 12345               
        ):
    sqn_num = int(0)
    while True:
        #recv
        loop_start_time = time()
        data_recvd , addr_of_client = pdc.recv()
        #
        server_ct = time()
        SOC_server = int(server_ct)
        FRASEC_server = int (  (server_ct - SOC_server) * (10**6) )

        #print(DataFrame.extract_frame_type(data_recvd))
        frame = DataFrame.convert2frame(data_recvd,ieee_cfg2_sample)
        #print(frame)
        SOC_Client = frame.get_soc()
        FRASEC_Client = frame.get_frasec()[0]
        print(SOC_server , SOC_Client , FRASEC_server , FRASEC_Client , FRASEC_server - FRASEC_Client )
        #store over db
        '''
        db_start_time = time()
        entry = pmu34_db.create_me_json(measurement='comm_delay',
                                tag_name='pmu_34',tag_field='fracsec_diff',
                                field_name='pdc_pmu_diff',field_value=FRASEC_diff)
        pmu34_db.write_to_db(data_json=entry,verbose_mode=False)
        db_end_time = time()
        '''
        #push to queue
        '''
        db_start_time = time()
        entry = pmu34_db.create_me_json(measurement='comm_delay',
                    tag_name='pmu_34',tag_field='fracsec_diff',
                    field_name='pdc_pmu_diff',field_value=FRASEC_diff)
        th_Q.put_in_queue(item = entry)
        db_end_time = time()
        '''
        #send
        sqn_num = sqn_num + 1
        msg = str(sqn_num)
        pdc.send_to(pmu_IP=addr_of_client[0] , pmu_port=addr_of_client[1] , payload = msg.encode() )
        loop_end_time = time()

        #print( (loop_end_time-loop_start_time) , (db_end_time - db_start_time) , ((loop_end_time-loop_start_time) / (db_end_time - db_start_time)) )


def recv_common_frame(   th_Q        : TH_Queue              ,
            pmu34_db    : db_client             , 
            pdc         : PDC_server            , 
            pmu_IP      : str = '10.64.37.34'   , 
            pmu_port    : int = 12345               
        ):
    sqn_num = int(0)
    try :
        while True:
            #recv
            loop_start_time = time()
            data_recvd , addr_of_client = pdc.recv()
            print(extract_frame_type(data_recvd))
            #
            frame = DataFrame.convert2frame(data_recvd,ieee_cfg2_sample)
            server_ct = time()
            SOC_server = int(server_ct)
            FRASEC_server = int (  (server_ct - SOC_server) * (10**6) )

            #SOC_Client = struct.unpack('!HHHIIHIIIIHHIIIHH',data_recvd)[3]
            #FRASEC_Client = struct.unpack('!HHHIIHIIIIHHIIIHH',data_recvd)[4]
            #FRASEC_diff = FRASEC_server - FRASEC_Client
            #SOC_diff = SOC_server - SOC_Client
            #print( SOC_server , SOC_Client , FRASEC_server , FRASEC_Client , FRASEC_diff)
            #store over db
            '''
            db_start_time = time()
            entry = pmu34_db.create_me_json(measurement='comm_delay',
                                    tag_name='pmu_34',tag_field='fracsec_diff',
                                    field_name='pdc_pmu_diff',field_value=FRASEC_diff)
            pmu34_db.write_to_db(data_json=entry,verbose_mode=False)
            db_end_time = time()
            '''
            #push to queue
            '''
            db_start_time = time()
            entry = pmu34_db.create_me_json(measurement='comm_delay',
                        tag_name='pmu_34',tag_field='fracsec_diff',
                        field_name='pdc_pmu_diff',field_value=FRASEC_diff)
            th_Q.put_in_queue(item = entry)
            db_end_time = time()
            '''
            #send
            sqn_num = sqn_num + 1
            msg = str(sqn_num)
            pdc.send_to(pmu_IP=addr_of_client[0] , pmu_port=addr_of_client[1] , payload = msg.encode() )
            loop_end_time = time()

            #print( (loop_end_time-loop_start_time) , (db_end_time - db_start_time) , ((loop_end_time-loop_start_time) / (db_end_time - db_start_time)) )
    
    except KeyboardInterrupt :
        print("exited by user")

if __name__ == "__main__":
    IP_to_bind      = '10.64.37.35'
    port_opening    = 9991
    pmu_IP          = '10.64.37.31'
    buffer_size     = 1024
    '''
    comm class
    PDC = PDC_server(ip_server_is_binding   = IP_to_bind,
                     port_opening           = port_opening ,
                     buffer_size            = 1024  ,
                     ntp_server_sync        = True  ,
                     ntp_sync_wait          = 0.1   ,
                     sync_lock_precision    = (10 **(-4) ),
                     sync_logging_level     = 'DEBUG',
                     trans_logging_level    = 'DEBUG'
                     )  
    '''
    '''
    inherited
    '''
    '''
    PDC = PDC_server(
                        ip_server_is_binding   = IP_to_bind    ,
                        port_opening           = port_opening  ,
                        buffer_size            = buffer_size   ,
                        trans_logging_level    = 'DEBUG'       ,
                        to_log_trans           = False         ,
                        ntp_server_sync        = False          ,
                        set_deamon             = False         ,
                        sync_lock_precision    = (10**(-4))    ,
                        ntp_sync_wait          = 1.0           ,
                        to_log_syncer          = True          ,
                        sync_logging_level     = 'DEBUG'
                    )
    '''
    PDC = PDC_server (    ip_server_is_binding = IP_to_bind , 
                    port_opening         = port_opening       , 
                    buffer_size          = buffer_size        ,
                    trans_logging_level  = 'INFO'     ,
                    to_log_trans      = True        ,
                    ntp_server_sync         = True        , 
                    set_deamon          = True        ,
                    sync_lock_precision    = (10**(-4))  ,
                    ntp_sync_wait        = 1.0         ,
                    to_log_syncer         = True        ,
                    sync_logging_level     = 'DEBUG'     ,

                    ptp_server_sync    = True          ,
                    ptp_sync_wait     = 1.0            ,
                    to_log_ptp_syncer   = True          ,
                    ptp_sync_logging_level = 'DEBUG'       
                 )
    #creating RT time series DB
    pmu34_db = db_client(IFDbname='PMU_34')
    #TODO create thread safe queue
    th_Q = TH_Queue(BUF_SIZE=0 , to_log_queue=True)
    #TODO create analytics and main_thread
    analytic_TH = threading.Thread(target=upload_func , args=(pmu34_db , th_Q , ) )
    analytic_TH.setDaemon(True)
    #analytic_TH.start()
    #threaded main
    
    
    #debug func
    recv_data_frame( th_Q = th_Q , pmu34_db = pmu34_db , pdc = PDC ,pmu_IP = pmu_IP,pmu_port = 12345)