#! /usr/bin/env python3
#python libs
import socket
import logging
from threading import Thread 
import threading

from time import sleep as time_sleep
#my imports
from utils import time_sync
from utils import check_sudo
from utils import get_my_ipv4

class PDC_server():
    '''
        recv / send
    '''
    logger_dict = { 'CRITICAL' : 50 , 'ERROR' : 40 , 'WARNING' : 30 , 'INFO' : 20 , 'DEBUG' : 10}
    logger_formatter = logging.Formatter('%(asctime)s : %(module)s : %(threadName)s : %(levelname)s : %(funcName)s : %(message)s')
    def __init__ (self, 
                  ip_server_is_binding  : str   = '127.0.0.1' , 
                  port_opening          : int   = 12345       , 
                  buffer_size           : int   = 1024        ,
                  ntp_server_sync       : bool  = False       ,
                  ntp_sync_wait         : float = 1.0         ,
                  sync_lock_precision   : float = (10**(-5))  ,
                  sync_logging_level    : str   = 'DEBUG',
                  trans_logging_level   : str   = 'CRITICAl'
                 ):

        #check sudo
        check_sudo()
        #get pdc ip
        pdc_ip = get_my_ipv4()
        #creating a logger for server
        self.logger_transaction = logging.getLogger(__name__)
        self.logger_transaction.setLevel(self.logger_dict[trans_logging_level])

        self.logger_transaction_file_handler = logging.FileHandler('PDC_server.log',mode='w')
        self.logger_transaction_file_handler.setFormatter(self.logger_formatter)

        self.logger_transaction.addHandler(self.logger_transaction_file_handler)
        #creating a logger for time sync
        self.logger_sync = logging.getLogger("PDC_server_syncer")
        self.logger_sync.setLevel(self.logger_dict[sync_logging_level])

        self.logger_sync_file_handler = logging.FileHandler('PDC_server_sync.log',mode='w')
        self.logger_sync_file_handler.setFormatter(self.logger_formatter)

        self.logger_sync.addHandler(self.logger_sync_file_handler)
        #now server

        self.ip_server_is_binding   = ip_server_is_binding
        self.port_opening           = port_opening
        self.buffer_size            = buffer_size
        
        self.server_sock            = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.ntp_sync_wait          = ntp_sync_wait
        self.time_offset            = float(0)
        self.addr_of_client         = None
        self.sync_lock_precision    = sync_lock_precision

        if ntp_server_sync :
            self.sync_deamon()

        try:
            self.server_sock.bind((self.ip_server_is_binding,self.port_opening))
        except socket.error as err :
            print("bind error " , str(err) )

    def __del__(self):
        self.server_sock.close()

    def get_time_offset(self) -> float:
        return self.time_offset

    def recv(self) -> bytes:
        ''' 
            returns data recvd in byes
        '''
        data_recvd , addr_of_client = self.server_sock.recvfrom(self.buffer_size)
        self.logger_transaction.debug(' msg recv : {} - {}'.format(data_recvd,addr_of_client) )
        self.addr_of_client = addr_of_client
        return data_recvd , addr_of_client

    def send_to( self , payload  : bytes  , pmu_IP = '127.0.0.1',  pmu_port : int = 12345 ):
        '''sends bytes type data'''
        self.logger_transaction.debug(' msg send_to : {}'.format(payload) )
        self.server_sock.sendto(payload,(pmu_IP , pmu_port))

    def base_comm(self):
        #recv
        #send
        pass

    def sync_func(self ):
        while( True ):
            actual_time_offset = time_sync(verbose=False)
            self.logger_sync.debug(' __sync_func__ actual_time_offset : {} '.format(actual_time_offset) )
            if ( -self.sync_lock_precision <= actual_time_offset <= self.sync_lock_precision ):
                self.ntp_sync_wait = 1000
                self.time_offset = 0.0
                self.logger_sync.debug(' __sync_func__ LOCKED actual , framed : {} - {}'.format(actual_time_offset,self.time_offset) )
            else :
                self.ntp_sync_wait = 0.1
                self.time_offset = actual_time_offset
            time_sleep(self.ntp_sync_wait)

    def sync_deamon(self):
        self.logger_sync.info('__sync_deamon__ : started')
        sync_deamon_TH = Thread( target = self.sync_func )
        sync_deamon_TH.setDaemon(True)
        sync_deamon_TH.start()

    