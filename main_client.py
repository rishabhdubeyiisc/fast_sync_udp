#! /usr/bin/env python3
from struct import pack as struct_pack
from time import time


from frame_data import frame_data_build
from cl_inherited_comms import Pmu_Client

def main(pmu : Pmu_Client):
    pack_time_start = 0
    pack_time_end = 0
    while True :
        #create payload
        ct = time() + pmu.get_time_offset()
        SOC = int(ct)
        FRASEC = int (  (ct - SOC) * (10**6) )
        # pack time calc
        pack_time_start = time()
        #payload = struct_pack('!8I',SOC, FRASEC , SOC , FRASEC , SOC, FRASEC , SOC , FRASEC )
        payload = frame_data_build(SOC = SOC , FRACSEC = FRASEC)
        pack_time_end = time()
        print(pack_time_end - pack_time_start)
        #send to PDC
        pmu.send_to_PDC(payload)
        #recv from pdc
        data_recv = pmu.recv_frm_PDC()
        print ("Server says " + str (data_recv.decode('utf-8')))

if __name__ == "__main__":
    
    IP_of_PDC       = '10.64.37.35'
    PDC_port_open   = 9991
    buffer          = 1024
    '''
    cl_comm
    pmu_c1 = Pmu_Client(IP_to_send          = IP_of_PDC,
                     port_to_send           = PDC_port_open,
                     buffer                 = 1024,
                     ntp_sync_wait          = 0.1,
                     ntp_server_sync        = True,
                     sync_lock_precision    =(10**(-4)),
                     sync_logging_level     ='DEBUG',
                     trans_logging_level    ='DEBUG')
    '''
    pmu_c1 = Pmu_Client(
                            IP_to_send          =   IP_of_PDC       ,
                            port_to_send        =   PDC_port_open   ,
                            buffer              =   buffer          ,
                            trans_logging_level =   'INFO'          ,
                            to_log_trans        =   True            ,
                            ntp_server_sync     =   True            ,
                            set_deamon          =   False           ,
                            sync_lock_precision =   (10**(-4))      ,
                            ntp_sync_wait       =   1.0             ,
                            to_log_syncer       =   True            ,
                            sync_logging_level  =   'DEBUG'
                        )
    main(pmu_c1)