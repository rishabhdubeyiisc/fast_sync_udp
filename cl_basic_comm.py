#! /usr/bin/env python3
#python libs
import socket
import threading
import logging
from threading import Thread

from time import time
from time import sleep as time_sleep

#my imports
from utils import get_my_ipv4
from utils import time_sync
from utils import check_sudo
#classes

class Pmu_Client():
    '''
        send
        recv 
    '''
    logger_dict = { 'CRITICAL' : 50 , 'ERROR' : 40 , 'WARNING' : 30 , 'INFO' : 20 , 'DEBUG' : 10}
    client_dict = { '10.64.37.31' : 'pmu_31' , '10.64.37.32' : 'pmu_32' , '10.64.37.33' : 'pmu_33' , '10.64.37.34' : 'pmu_34' , '10.64.37.35' : 'pmu_35'}

    logger_formatter = logging.Formatter('%(asctime)s : %(module)s : %(threadName)s : %(levelname)s : %(funcName)s : %(message)s')

    def __init__ (  self , 
                    IP_to_send          : str   = '10.64.37.35' , 
                    port_to_send        : int   = 12345         , 
                    buffer              : int   = 1024          ,
                    to_log              : bool  = True          , 
                    ntp_sync_wait       : float = 1.0           ,
                    sync_lock_precision : float = (10**(-5))    ,
                    ntp_server_sync     : bool  = True          ,
                    sync_logging_level  : str   = 'DEBUG'       ,
                    trans_logging_level : str   = 'CRITICAL'
                 ) :

        #check sudo
        check_sudo()
        #get own ip
        self.pmu_ip = get_my_ipv4()
        self.pmu_name = self.client_dict[self.pmu_ip]
        self.log_file_name = "log_" + str(self.pmu_name) + "_trans.log"
        self.log_sync_file_name = "log_" + str(self.pmu_name) + "_sync.log"
        self.syncer_name = str(self.pmu_name) + "_syncer"
        #creating a logger for server
        self.logger_transaction = logging.getLogger(self.pmu_name)
        self.logger_transaction.setLevel(self.logger_dict[trans_logging_level])

        self.logger_transaction_file_handler = logging.FileHandler(self.log_file_name,mode='w')
        self.logger_transaction_file_handler.setFormatter(self.logger_formatter)

        self.logger_transaction.addHandler(self.logger_transaction_file_handler)
        #creating a logger for time sync
        self.logger_sync = logging.getLogger(self.syncer_name)
        self.logger_sync.setLevel(self.logger_dict[sync_logging_level])

        self.logger_sync_file_handler = logging.FileHandler(self.log_sync_file_name,mode='w')
        self.logger_sync_file_handler.setFormatter(self.logger_formatter)

        self.logger_sync.addHandler(self.logger_sync_file_handler)
        #master for logging
        self.to_log = to_log
        #syncer
        self.time_offset    = 0.0
        self.ntp_sync_wait  = ntp_sync_wait
        self.sync_lock_precision = sync_lock_precision
        if ntp_server_sync:
            self.sync_deamon()

        #now server

        self.cl_sock    = socket.socket( family = socket.AF_INET , 
                                         type = socket.SOCK_DGRAM)

        self.PDC_IP         = IP_to_send
        self.PDC_port       = port_to_send
        self.BUFFER_SIZE    = buffer

    def __del__(self):
        self.cl_sock.close()

    def send_to_PDC (self , payload : bytes ):
        self.cl_sock.sendto( payload ,( self.PDC_IP , self.PDC_port ) )
        if (self.to_log):
            self.logger_transaction.debug("payload - {}".format(payload))

    def recv_frm_PDC(self) -> bytes:
        '''
        return bytes of data recvd
        '''
        data_recvd , server_addr = self.cl_sock.recvfrom(self.BUFFER_SIZE)
        if (self.to_log):
            self.logger_transaction.debug("msg , addr - {} , {}".format(data_recvd,server_addr))
        return data_recvd

    def comm_debug(self):
        '''
        send recv in that order
        '''
        #send
        #recv
        pass

    def get_time_offset (self):
        return self.time_offset

    def sync_func(self ):
        while( True ):
            actual_time_offset = time_sync(verbose=False)
            if (self.to_log):
                self.logger_sync.debug(' __sync_func__ actual_time_offset : {} '.format(actual_time_offset) )
            if ( -self.sync_lock_precision <= actual_time_offset <= self.sync_lock_precision ):
                self.ntp_sync_wait = 10
                self.time_offset = 0.0
                if (self.to_log):
                    self.logger_sync.debug(' __sync_func__ LOCKED actual , framed : {} - {}'.format(actual_time_offset,self.time_offset) )
            else :
                self.ntp_sync_wait = 0.1
                self.time_offset = actual_time_offset
            time_sleep(self.ntp_sync_wait)

    def sync_deamon(self):
        if (self.to_log):
            self.logger_sync.info('__sync_deamon__ : started')
        sync_deamon_TH = Thread( target = self.sync_func )
        sync_deamon_TH.setDaemon(True)
        sync_deamon_TH.start()

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
                  to_log                : bool  = True        ,
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
        self.logger_transaction = logging.getLogger("PDC_server_trans")
        self.logger_transaction.setLevel(self.logger_dict[trans_logging_level])

        self.logger_transaction_file_handler = logging.FileHandler('log_PDC_server.log',mode='w')
        self.logger_transaction_file_handler.setFormatter(self.logger_formatter)

        self.logger_transaction.addHandler(self.logger_transaction_file_handler)
        #creating a logger for time sync
        self.logger_sync = logging.getLogger("PDC_server_syncer")
        self.logger_sync.setLevel(self.logger_dict[sync_logging_level])

        self.logger_sync_file_handler = logging.FileHandler('log_PDC_server_sync.log',mode='w')
        self.logger_sync_file_handler.setFormatter(self.logger_formatter)

        self.logger_sync.addHandler(self.logger_sync_file_handler)
        #log master
        self.to_log = to_log
        #syncer
        self.ntp_sync_wait          = ntp_sync_wait
        self.time_offset            = float(0)
        self.addr_of_client         = None
        self.sync_lock_precision    = sync_lock_precision

        if ntp_server_sync :
            self.sync_deamon()
        #now server

        self.ip_server_is_binding   = ip_server_is_binding
        self.port_opening           = port_opening
        self.buffer_size            = buffer_size
        
        self.server_sock            = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        try:
            self.server_sock.bind((self.ip_server_is_binding,self.port_opening))
        except socket.error as err :
            print("bind error " , str(err) )

    def __del__(self):
        self.server_sock.close()

    def recv(self) -> bytes:
        ''' 
            returns data recvd in byes
        '''
        data_recvd , addr_of_client = self.server_sock.recvfrom(self.buffer_size)
        
        self.addr_of_client = addr_of_client
        if(self.to_log):
            self.logger_transaction.debug(' msg recv : {} - {}'.format(data_recvd,addr_of_client) )
        return data_recvd , addr_of_client

    def send_to( self , payload  : bytes  , pmu_IP = '127.0.0.1',  pmu_port : int = 12345 ):
        '''sends bytes type data'''
        self.server_sock.sendto(payload,(pmu_IP , pmu_port))
        if(self.to_log):
            self.logger_transaction.debug(' msg send_to : {}'.format(payload) )

    def base_comm(self):
        #recv
        #send
        pass
    
    def get_time_offset(self) -> float:
        return self.time_offset
    
    def sync_func(self ):
        while( True ):
            actual_time_offset = time_sync(verbose=False)
            
            if(self.to_log):
                self.logger_sync.debug(' __sync_func__ actual_time_offset : {} '.format(actual_time_offset) )
            
            if ( -self.sync_lock_precision <= actual_time_offset <= self.sync_lock_precision ):
                self.ntp_sync_wait = 1000
                self.time_offset = 0.0
                
                if(self.to_log):
                    self.logger_sync.debug(' __sync_func__ LOCKED actual , framed : {} - {}'.format(actual_time_offset,self.time_offset) )
            
            else :
                self.ntp_sync_wait = 0.1
                self.time_offset = actual_time_offset
            time_sleep(self.ntp_sync_wait)

    def sync_deamon(self):
        if (self.to_log):
            self.logger_sync.info('__sync_deamon__ : started')
        sync_deamon_TH = Thread( target = self.sync_func )
        sync_deamon_TH.setDaemon(True)
        sync_deamon_TH.start()

    