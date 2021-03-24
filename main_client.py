#! /usr/bin/env python3
from struct import pack as struct_pack
from time import time

from cl_inherited_comms import Pmu_Client
from utils import sync_me
from utils import check_sudo
from frame import DataFrame
from frame import ConfigFrame2
from frame import CommonFrame

MAX_16_BIT = (2**16 - 1)

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


def main(pmu : Pmu_Client):
    pack_time_start = 0
    pack_time_end = 0
    packet_num = 0
    while packet_num < MAX_16_BIT :
        #create payload
        ct = time() + pmu.get_time_offset()
        SOC = int(ct)
        FRASEC = int (  (ct - SOC) * (10**6) )
        # pack time calc
        pack_time_start = time()
        #payload = struct_pack('!8I',SOC, FRASEC , SOC , FRASEC , SOC, FRASEC , SOC , FRASEC )
        #payload = frame_data_build(SOC = SOC , FRACSEC = FRASEC)
        payload = DataFrame(pmu_id_code=12345 , 
              stat = ("ok", True, "timestamp", False, False, False, 0, "<10", 0),
              phasors=  [(14635, 0), (-7318, -12676), (-7318, 12675), (1092, 0)] ,
              freq= 2500 ,
              dfreq=0,
              analog=[100, 1000, 10000],
              digital=[0x3c12],
              cfg = ieee_cfg2_sample ,
              soc= SOC ,
              frasec= FRASEC
              )
        payload = payload.convert2bytes()
        pack_time_end = time()
        print(pack_time_end - pack_time_start)
        #send to PDC
        pmu.send_to_PDC(payload)
        #recv from pdc
        data_recv = pmu.recv_frm_PDC()
        print ("Server says " + str (data_recv.decode('utf-8')))
        packet_num = packet_num + 1

def send_common_frame(pmu : Pmu_Client):
    pack_time_start = 0
    pack_time_end = 0
    packet_num = 0
    while packet_num < 10 :
        #create payload
        ct = time() + pmu.get_time_offset()
        SOC = int(ct)
        FRASEC = int (  (ct - SOC) * (10**6) )
        # pack time calc
        pack_time_start = time()
        frame = CommonFrame(ieee_version=3 , soc= SOC , fracsec=FRASEC)
        payload = frame.build()
        pack_time_end = time()
        print(pack_time_end - pack_time_start)
        #send to PDC
        pmu.send_to_PDC(payload)
        #recv from pdc
        data_recv = pmu.recv_frm_PDC()
        print ("Server says " + str (data_recv.decode('utf-8')))
        packet_num = packet_num + 1

def send_data_frame(pmu : Pmu_Client):
    pack_time_start = 0
    pack_time_end = 0
    packet_num = 0
    try :
        while MAX_16_BIT :
            #create payload
            ct = time() + pmu.get_time_offset()
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
            print(pack_time_end - pack_time_start)
            #send to PDC
            pmu.send_to_PDC(payload)
            #recv from pdc
            data_recv = pmu.recv_frm_PDC()
            print ("Server says " + str (data_recv.decode('utf-8')))
            packet_num = packet_num + 1    
    except KeyboardInterrupt :
        print("Exited by user")
if __name__ == "__main__":
    check_sudo()

    IP_of_PDC       = '10.64.37.35'
    PDC_port_open   = 9991
    buffer          = 1024
    '''
    initial_lock =   2.6 * (10**(-3)) # 10 us
    sync_lock_precision = (10**(-4)) # 0.1 ms
    '''
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
    #sync to server
    '''
    pmu_c1 = Pmu_Client(
                            IP_to_send          =   IP_of_PDC       ,
                            port_to_send        =   PDC_port_open   ,
                            buffer              =   buffer          ,
                            trans_logging_level =   'DEBUG'          ,
                            to_log_trans        =   True            ,
                            ntp_server_sync     =   True            ,
                            set_deamon          =   False           ,
                            sync_lock_precision =   sync_lock_precision ,
                            ntp_sync_wait       =   1.0             ,
                            to_log_syncer       =   True            ,
                            sync_logging_level  =   'DEBUG'
                        )
    '''
    pmu_c1 = Pmu_Client( IP_to_send=IP_of_PDC,
            port_to_send=PDC_port_open,
            buffer=buffer,
            trans_logging_level='DEBUG',
            to_log_trans=True,
            
            ntp_server = "10.64.37.35",
            ntp_server_sync=False,
            sync_lock_precision=(10**(-3)),
            ntp_sync_wait=30, 
            to_log_ntp_syncer=True,
            ntp_sync_logging_level='DEBUG',
            
            ptp_server_sync=True ,
            ptp_sync_wait=1.0, 
            to_log_ptp_syncer=True,
            ptp_sync_logging_level='DEBUG')
    #game
    send_data_frame(pmu_c1)