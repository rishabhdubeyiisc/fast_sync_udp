#! /usr/bin/env python3
import struct
from time import time

from cl_comm import PDC_server
from cl_inherited_comms import PDC_server

#8 bit time quality msg
TIME_FLAGS = 0b0010
TIME_QUALITY = 0x5
lis = [TIME_FLAGS, TIME_QUALITY ]
TIME_MSG = bytes(lis) 
#TIME_MSG = 0b00100101


def main(pdc : PDC_server , pmu_IP : str = '10.64.37.34' , pmu_port : int = 12345 ):
    sqn_num = int(0)
    try :
        while True:
            #recv
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
            #send
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
                    
    main(pdc = PDC , pmu_IP= pmu_IP  , pmu_port= port_opening)