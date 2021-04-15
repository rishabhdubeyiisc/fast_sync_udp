#! /usr/bin/env python3
from time import time
from time import sleep as time_sleep

from cl_inherited_comms import Pmu_Client
from utils import check_sudo
from frame import DataFrame
from frame import ConfigFrame2

MAX_16_BIT = (2**16 - 1)
ms_20 = 20 * ( 10 ** (-3) )

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


ieee_data_sample = DataFrame(   12345 , 
                                ("ok", True, "timestamp", False, False, False, 0, "<10", 0),
                                [(14635, 0), (-7318, -12676), (-7318, 12675), (1092, 0)], 
                                2500, 
                                0,
                                [100, 1000, 10000],
                                [0x3c12], 
                                ieee_cfg2_sample)

def send_data_frame(pmu : Pmu_Client):
    pack_time_start = 0
    pack_time_end = 0
    packet_num = 0
    
    loop_send_time  = int(time()) + 1    
    begin_send_time = int(time())
    duration_in_sec = 60 * 10
    while loop_send_time - begin_send_time < duration_in_sec :
        #create payload
        ct = time() 
        SOC = int(ct)
        FRASEC = int (  (ct - SOC) * (10**6) )
        # pack time calc
        pack_time_start = time()
        ieee_data_sample = DataFrame(   12345 , 
                                ("ok", True, "timestamp", False, False, False, 0, "<10", 0),
                                [(14635, 0), (-7318, -12676), (-7318, 12675), (1092, 0)], 
                                2500, 
                                0,
                                [100, 1000, 10000],
                                [0x3c12], 
                                ieee_cfg2_sample)
        payload = ieee_data_sample.convert2bytes()
        pack_time_end = time()
        #print(pack_time_end - pack_time_start)
        #send to PDC
        pmu.send_to_PDC(payload)
        #recv from pdc
        data_recv = pmu.recv_frm_PDC()
        #print ("Server says " + str (data_recv.decode('utf-8')))
        packet_num = packet_num + 1
        loop_send_time = int(time())
        #time_sleep(ms_20)

if __name__ == "__main__":
    check_sudo()

    IP_of_PDC       = '10.64.37.35'
    port            = 9991
    buffer          = 1024

    pmu_c1 = Pmu_Client( IP_to_send=IP_of_PDC,
            port_to_send=port,
            buffer=buffer,
            trans_logging_level='DEBUG',
            to_log_trans=True,
            
            ntp_server = "10.64.37.35",
            ntp_server_sync=False,
            sync_lock_precision=(10**(-3)),
            ntp_sync_wait=30, 
            to_log_ntp_syncer=False,
            ntp_sync_logging_level='DEBUG',
            
            ptp_server_sync=True ,
            ptp_sync_wait=0.5, 
            to_log_ptp_syncer=False,
            ptp_sync_logging_level='DEBUG')
    #game
    send_data_frame(pmu_c1)

    #pmu_c1.send_to_PDC(0xDEAD.to_bytes(2,"big"))