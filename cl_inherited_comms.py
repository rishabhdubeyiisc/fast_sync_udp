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
class base(object):
    def __init__(   self
                ):
        '''
        do sudo check , resolve ip , gives name , logger_formatter
        '''
        check_sudo()

        self._logger_dict = { 'CRITICAL' : 50 , 'ERROR' : 40 , 'WARNING' : 30 , 'INFO' : 20 , 'DEBUG' : 10}

        self._logger_formatter = logging.Formatter('%(asctime)s : %(module)s : %(threadName)s : %(levelname)s : %(funcName)s : %(message)s')

        self._ip_name_dict = { '10.64.37.31' : 'pmu_31' , '10.64.37.32' : 'pmu_32' , '10.64.37.33' : 'pmu_33' , '10.64.37.34' : 'pmu_34' , '10.64.37.35' : 'pdc_35'}
        #get own ip and name resolve
        self._pmu_ip     = get_my_ipv4()
        self._pmu_name   = self._ip_name_dict[self._pmu_ip]
        self._log_file_name = str(self._pmu_name) + "_trans.log"
        self._log_sync_file_name = str(self._pmu_name) + "_sync.log"
        self._syncer_name = str(self._pmu_name) + "_syncer"
    
    def get_name_from_ip(self):
        '''
        return name of pmu from dictionary
        '''
        return self._pmu_name
    
    def get_trans_logger_name(self):
        return self._pmu_name

    def get_trans_file_name(self):
        return self._log_file_name

    def get_sync_logger_name(self):
        return self._syncer_name

    def get_sync_file_name(self):
        return self._log_sync_file_name

    def get_logging_level(self , trans_logging_level ):
        return self._logger_dict[trans_logging_level]
    
    def get_formatter(self):
        return self._logger_formatter

    def get_ip(self):
        return self._pmu_ip

class log_trans(base):
    '''logger_transaction <- public'''
    def __init__(   self , 
                    trans_logging_level : str = 'DEBUG' , 
                    to_log_trans : bool = True
                ):
        
        base.__init__(self)
        #creating a logger for transactions
        self.logger_transaction = logging.getLogger(self._pmu_name)
        self.logger_transaction.setLevel(self._logger_dict[trans_logging_level])

        self._logger_transaction_file_handler = logging.FileHandler(self._log_file_name,mode='w')
        self._logger_transaction_file_handler.setFormatter(self._logger_formatter)

        self.logger_transaction.addHandler(self._logger_transaction_file_handler)

        #log master
        self.to_log_trans = to_log_trans
        #create log header
        self.logger_transaction.info("log file")

class log_sync(base):
        def __init__(   self , 
                    sync_logging_level : str = 'DEBUG' , 
                    to_log_syncer : bool = True
                ):

            base.__init__(self)
            #
            self.logger_sync = logging.getLogger(self._syncer_name)
            self.logger_sync.setLevel(self._logger_dict[sync_logging_level])

            self._logger_sync_file_handler = logging.FileHandler(self._log_sync_file_name,mode='w')
            self._logger_sync_file_handler.setFormatter(self._logger_formatter)

            self.logger_sync.addHandler(self._logger_sync_file_handler)

            #log master
            self.to_log_syncer = to_log_syncer
            #create log header
            self.logger_sync.info("sync file")

class syncer(log_sync):
    def __init__(   self,
                    ntp_server_sync     : bool  = True          ,
                    set_deamon          : bool  = False         ,
                    sync_lock_precision : float = (10**(-5))    ,
                    sync_lock_upperbound: float = (10**(-3))    ,
                    ntp_sync_wait       : float = 1.0           ,
                    to_log_syncer       : bool  = True          ,
                    sync_logging_level  : str   = 'DEBUG'       
                ):
        log_sync.__init__(  self , 
                            to_log_syncer       = to_log_syncer , 
                            sync_logging_level  =sync_logging_level
                         )
        
        self.fast_sync_wait = float(0.1)
        self.slow_sync_wait = float(10.0)
        
        self.time_offset            = 0.0
        self.ntp_sync_wait          = ntp_sync_wait
        self.sync_lock_precision    = sync_lock_precision
        self.sync_lock_upperbound   = sync_lock_upperbound
        self.set_deamon = set_deamon
        if ntp_server_sync:
            self.sync_deamon()

    def get_time_offset (self):
        return self.time_offset

    def sync_func(self ):
        while( True ):
            actual_time_offset = time_sync(verbose=False)
        
            if(self.to_log_syncer):
                self.logger_sync.debug(' __sync_func__ actual_time_offset : {} '.format(actual_time_offset) )
            
            if ( -self.sync_lock_precision <= actual_time_offset <= self.sync_lock_precision ):
                self.ntp_sync_wait = 10
                self.time_offset = 0.0
                
                if(self.to_log_syncer):
                    self.logger_sync.debug(' __sync_func__ LOCKED actual , framed : {} - {}'.format(actual_time_offset,self.time_offset) )
            
            elif( self.sync_lock_upperbound <= abs(actual_time_offset) ):
                self.ntp_sync_wait = 0.1
                self.time_offset = actual_time_offset

                if(self.to_log_syncer):
                    self.logger_sync.debug(' __sync_func__ PASSED actual , framed : {} - {}'.format(actual_time_offset,self.time_offset) )
            
            else :
                self.ntp_sync_wait = 0.1
                self.time_offset = actual_time_offset
            #change this sleep pattern
            time_sleep(self.ntp_sync_wait)

    def sync_deamon(self):
        if (self.to_log_syncer):
            self.logger_sync.info('__sync_deamon__ : started')
        sync_deamon_TH = Thread( target = self.sync_func )
        sync_deamon_TH.setDaemon(self.set_deamon)
        sync_deamon_TH.start()

class Pmu_Client(syncer, log_trans):
    def __init__(   self ,
                    IP_to_send          : str   = '10.64.37.35' , 
                    port_to_send        : int   = 12345         , 
                    buffer              : int   = 1024          ,
                    trans_logging_level : str   = 'DEBUG'       ,
                    to_log_trans        : bool  = True          ,
                    ntp_server_sync     : bool  = True          ,
                    set_deamon          : bool  = False         , 
                    sync_lock_precision : float = (10 ** (-4))  ,
                    ntp_sync_wait       : float = 1.0           ,
                    to_log_syncer       : bool  = True          ,
                    sync_logging_level  : str   = 'DEBUG'        
                ):
        #inits
        log_trans.__init__( self, 
                            trans_logging_level =   trans_logging_level , 
                            to_log_trans        =   to_log_trans)
        
        syncer.__init__(    self,
                            ntp_server_sync     =   ntp_server_sync     , 
                            set_deamon          =   set_deamon          , 
                            sync_lock_precision =   sync_lock_precision ,
                            ntp_sync_wait       =   ntp_sync_wait       ,
                            to_log_syncer       =   to_log_syncer       ,
                            sync_logging_level  =   sync_logging_level
                        )

        self.logger_transaction.info("instancing client begin : " + str(self.get_name_from_ip()))          
        #client
        self.cl_sock    = socket.socket( family = socket.AF_INET , 
                                         type = socket.SOCK_DGRAM)

        self.PDC_IP         = IP_to_send
        self.PDC_port       = port_to_send
        self.BUFFER_SIZE    = buffer

        self.logger_transaction.info("IP_to_send    : " + str(self.PDC_IP))  
        self.logger_transaction.info("PDC_port      : " + str(self.PDC_port))  
        self.logger_transaction.info("buffer        : " + str(self.BUFFER_SIZE ))  

        self.logger_transaction.info("instancing client done  : " + str(self.get_name_from_ip()))
        self.logger_transaction.info("\n\n")

    def __del__(self):
        self.logger_transaction.info("closing client begin : " + str(self.get_name_from_ip()))          
        self.cl_sock.close()
        self.logger_transaction.info("closing client end : " + str(self.get_name_from_ip()))          

    def send_to_PDC (self , payload : bytes ):
        self.cl_sock.sendto( payload ,( self.PDC_IP , self.PDC_port ) )
        if (self.to_log_trans):
            self.logger_transaction.debug("payload - {}".format(payload) )

    def recv_frm_PDC(self) -> bytes:
        '''
        return bytes of data recvd
        '''
        data_recvd , server_addr = self.cl_sock.recvfrom(self.BUFFER_SIZE)
        if (self.to_log_trans):
            self.logger_transaction.debug("msg , addr - {} , {}".format(data_recvd,server_addr))
        return data_recvd

    def comm_debug(self):
        '''
        send recv in that order
        '''
        #send
        #recv
        pass

class PDC_server(syncer, log_trans):
    '''
        recv / send
    '''
    def __init__ (  self, 
                    ip_server_is_binding  : str   = '127.0.0.1' , 
                    port_opening          : int   = 12345       , 
                    buffer_size           : int   = 1024        ,
                    trans_logging_level   : str   = 'DEBUG'     ,
                    to_log_trans          : bool  = True        ,
                    ntp_server_sync       : bool  = True        , 
                    set_deamon            : bool  = True        ,
                    sync_lock_precision   : float = (10**(-4))  ,
                    ntp_sync_wait         : float = 1.0         ,
                    to_log_syncer         : bool  = True        ,
                    sync_logging_level    : str   = 'DEBUG'
                 ):
        log_trans.__init__( self , 
                            trans_logging_level =   trans_logging_level,
                            to_log_trans        =   to_log_trans
                          )
        
        syncer.__init__( self,
                         ntp_server_sync        = ntp_server_sync       , 
                         set_deamon             = set_deamon            ,
                         sync_lock_precision    = sync_lock_precision   ,
                         ntp_sync_wait          = ntp_sync_wait         ,
                         to_log_syncer          = to_log_syncer         ,
                         sync_logging_level     = sync_logging_level
                        )

        self.logger_transaction.info("instancing PDC_server @ {}".format( self.get_ip() ))
        #now server
        self.ip_server_is_binding   = ip_server_is_binding
        self.port_opening           = port_opening
        self.buffer_size            = buffer_size
       
        self.server_sock            = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        try:
            self.server_sock.bind((self.ip_server_is_binding,self.port_opening))
        except socket.error as err :
            self.logger_transaction.info( "server_sock bind error {}".format( (self.ip_server_is_binding,self.port_opening) ) )
            print("bind error " , str(err) )
            exit(-2)
        #logs
        self.logger_transaction.info( "ip_server_is_binding - {}".format( self.ip_server_is_binding ) )
        self.logger_transaction.info( "port_opening - {}".format( port_opening ) )
        self.logger_transaction.info( "buffer_size - {}".format( buffer_size ) )
        self.logger_transaction.info( "server_sock bind {}".format( (self.ip_server_is_binding,self.port_opening) ) )


    def __del__(self):
        self.logger_transaction.info( "server_sock close {}".format( (self.ip_server_is_binding,self.port_opening) ) )
        self.server_sock.close()

    def recv(self) -> bytes:
        ''' 
            returns data recvd in byes
        '''
        data_recvd , addr_of_client = self.server_sock.recvfrom(self.buffer_size)
        
        self.addr_of_client = addr_of_client
        if(self.to_log_trans):
            self.logger_transaction.debug(' msg recv : {} - {}'.format(data_recvd,addr_of_client) )
        return data_recvd , addr_of_client

    def send_to( self , payload  : bytes  , pmu_IP = '127.0.0.1',  pmu_port : int = 12345 ):
        '''sends bytes type data'''
        self.server_sock.sendto(payload,(pmu_IP , pmu_port))
        if(self.to_log_trans):
            self.logger_transaction.debug(' msg send_to : {}'.format(payload) )

    def base_comm(self):
        #recv
        #send
        pass