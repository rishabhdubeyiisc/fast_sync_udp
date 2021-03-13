#! /usr/bin/env python3
from struct import pack as struct_pack
from time import time
from payloads import common_frame_build
from payloads import set_frasec
from cl_client import Pmu_Client

#protocol specific values
DATA_FRAME_VALUE    = int(0xAA01)
MAX_FRAME_SIZE      = int(0xFFFF)
IDCODE_VALUE        = int(0x0002)
SOC_VALUE           = int(0x99887766)

TIME_FLAGS = 0b0010
TIME_QUALITY = 0x5
lis = [TIME_FLAGS, TIME_QUALITY ]
TIME_MSG = bytes(lis) 

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
        payload = struct_pack('!8I',SOC, FRASEC , SOC , FRASEC , SOC, FRASEC , SOC , FRASEC )
        pack_time_end = time()
        print(pack_time_end - pack_time_start)
        #send to PDC
        pmu.send_to_PDC(payload)
        #recv from pdc
        data_recv = pmu.recv_frm_PDC()
        print ("Server says " + str (data_recv.decode('utf-8')))

if __name__ == "__main__":
    IP_of_PDC = '10.64.37.35'
    PDC_port_open = 12345

    pmu_c1 = Pmu_Client(IP_to_send          = IP_of_PDC,
                     port_to_send           = PDC_port_open,
                     buffer                 = 1024,
                     ntp_sync_wait          = 0.1,
                     ntp_server_sync        = True,
                     sync_lock_precision    =(10**(-4)),
                     sync_logging_level     ='DEBUG',
                     trans_logging_level    ='DEBUG')
    
    main(pmu_c1)