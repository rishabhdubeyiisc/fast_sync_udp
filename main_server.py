#! /usr/bin/env python3
import struct
from time import time
import threading
import queue

from cl_comm import PDC_server
from cl_inherited_comms import PDC_server
from cl_db_client import db_client_cls as db_client
#8 bit time quality msg
TIME_FLAGS = 0b0010
TIME_QUALITY = 0x5
lis = [TIME_FLAGS, TIME_QUALITY ]
TIME_MSG = bytes(lis) 
#TIME_MSG = 0b00100101

def main(   pmu34_db    : db_client, 
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
            server_ct = time() + pdc.get_time_offset()
            SOC_server = int(server_ct)
            FRASEC_server = int (  (server_ct - SOC_server) * (10**6) )

            SOC_Client = struct.unpack('!HHHIIHIIIIHHIIIHH',data_recvd)[3]
            FRASEC_Client = struct.unpack('!HHHIIHIIIIHHIIIHH',data_recvd)[4]
            FRASEC_diff = FRASEC_server - FRASEC_Client
            SOC_diff = SOC_server - SOC_Client
            print( SOC_server , SOC_Client , FRASEC_server , FRASEC_Client , FRASEC_diff)
            #store over db
            db_start_time = time()
            entry = pmu34_db.create_me_json(measurement='comm_delay',
                                    tag_name='pmu_34',tag_field='fracsec_diff',
                                    field_name='pdc_pmu_diff',field_value=FRASEC_diff)
            pmu34_db.write_to_db(data_json=entry,verbose_mode=False)
            db_end_time = time()
            #send
            sqn_num = sqn_num + 1
            msg = str(sqn_num)
            pdc.send_to(pmu_IP=addr_of_client[0] , pmu_port=addr_of_client[1] , payload = msg.encode() )
            loop_end_time = time()

            print( (loop_end_time-loop_start_time) , (db_end_time - db_start_time) , ((loop_end_time-loop_start_time) / (db_end_time - db_start_time)) )
    
    except KeyboardInterrupt :
        print("exited by user")

def receiver(   pmu34_db    : db_client, 
                pdc         : PDC_server            ,           
            ):
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
            #store over db
            entry = pmu34_db.create_me_json(measurement='comm_delay',
                                    tag_name='pmu_34',tag_field='fracsec_diff',
                                    field_name='pdc_pmu_diff',field_value=FRASEC_diff)
            pmu34_db.write_to_db(data_json=entry,verbose_mode=False)

    except KeyboardInterrupt :
        print("exited by user")

def cmd_send(   pmu34_db    : db_client, 
            pdc         : PDC_server            , 
            pmu_IP      : str = '10.64.37.34'   , 
            pmu_port    : int = 12345           
            
        ):
    sqn_num = int(0)
    try :
        sqn_num = sqn_num + 1
        msg = str(sqn_num)
        pdc.send_to(pmu_IP=addr_of_client[0] , pmu_port=addr_of_client[1] , payload = msg.encode() )

    except KeyboardInterrupt :
        print("exited by user")

if __name__ == "__main__":
    IP_to_bind      = '10.64.37.35'
    port_opening    = 9991
    pmu_IP          = '10.64.37.34'
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
    PDC = PDC_server(
                        ip_server_is_binding   = IP_to_bind    ,
                        port_opening           = port_opening  ,
                        buffer_size            = buffer_size   ,
                        trans_logging_level    = 'DEBUG'       ,
                        to_log_trans           = False         ,
                        ntp_server_sync        = True          ,
                        set_deamon             = False         ,
                        sync_lock_precision    = (10**(-4))    ,
                        ntp_sync_wait          = 1.0           ,
                        to_log_syncer          = True          ,
                        sync_logging_level     = 'DEBUG'
                    )
    #creating RT time series DB
    pmu34_db = db_client(IFDbname='PMU_34')

    main(pdc = PDC , pmu_IP= pmu_IP  , pmu_port= port_opening , pmu34_db=pmu34_db)