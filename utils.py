#! /usr/bin/env python3
import os
import sys
import datetime
import time
import subprocess
import socket

def time_sync(verbose : bool = False , ntp_server : str = "10.64.37.35") -> float:
    '''
    return float 
    return offset after syncing with server lagging then will return a value so that after adding in FRACSEC we are syncyed with server
    '''
    cmd = "ntpdate " + ntp_server
    sync_status = run_cmd(cmd)
    
    is_server_avail = last_sys_call_status()
    if not is_server_avail:
        return 0.0

    offset = float(sync_status.split()[-2])

    if (offset < 0):
        if (verbose):
            print("unit is lagging in 0.1 microsec unit by : ", offset)
        return (-(offset))
    elif (offset > 0):
        if (verbose):
            print("unit is leading in 0.1 microsec unit by : ", offset)
        return (-(offset))
    else :
        if (verbose):
            print("exact sync is imposible")
        return 0

def last_sys_call_status()->bool:
    status = run_cmd("echo {$?}")
    try :
        value = int(status.split('\n')[0].split('{')[1].split('}')[0])
        if value == 0 :
            return True
    except :
        return False

def run_cmd (string : str = "pwd")->str:
    '''
    run a system command pass as string
    return status or error
    '''
    try: 
        stream = os.popen(string)
        return (stream.read())
    except OSError as error:
        print(error)
        return error

def check_sudo()->bool:
    '''
    check for root if not found ask for password
    '''
    if os.geteuid() == 0:
        print("root!")
        return True
    else:
        print("not root.")
        subprocess.call(['sudo', 'python3', *sys.argv])
        sys.exit()

def get_my_ipv4()->str:
    '''
    function to resolve ip
    '''
    IP = '127.0.0.1'
    ip_resolver = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    try :
        ip_resolver.connect(( '1.2.3.4' , 1 ))
        IP = ip_resolver.getsockname()[0]
    except Exception :
        IP = '127.0.0.1'
    finally :
        ip_resolver.close()
    return IP

def ping_time(ip : str = '10.64.37.34')->float:
    cmd = "ping -c 1 " + ip
    ret = run_cmd(cmd)
    value , unit = (ret.split('\n\n')[0].split('time=')[1]).split()
    if unit == 'us':
        return (float(value)) 
    elif unit == 'ms':
        return (float(value)) * 1000
    elif unit == 's' :
        print("ping time exceeded than a second")
        return (float(value)) * 1000 * 1000
    else :
        return float(0xDEAD)

class LogIt():
    def __init__(   self , 
                    logger_name     : str   = 'logger'      , 
                    logging_level   : str   = 'DEBUG'       , 
                    filename        : str   = 'logger.log'  , 
                    to_log          : bool  = True
                 ):
        import logging
        check_sudo()

        self._logger_dict = { 'CRITICAL' : 50 , 'ERROR' : 40 , 'WARNING' : 30 , 'INFO' : 20 , 'DEBUG' : 10}

        self._logger_formatter = logging.Formatter('%(asctime)s : %(module)s : %(threadName)s : %(levelname)s : %(funcName)s : %(message)s')

        #creating a logger for transactions
        self.logger_transaction = logging.getLogger(logger_name)
        self.logger_transaction.setLevel(self._logger_dict[logging_level])

        self._logger_transaction_file_handler = logging.FileHandler(filename = filename , mode='w')
        self._logger_transaction_file_handler.setFormatter(self._logger_formatter)

        self.logger_transaction.addHandler(self._logger_transaction_file_handler)

        #log master
        self.to_log = to_log
        #create log header
        self.logger_transaction.info("log file")

    def log(self ,msg : str):
        if self.to_log :
            self.logger_transaction.debug(msg)

def sync_me ( sync_lock_upperbound : float = (10 ** (-4) ) , verbose : bool = True ):
    offset = float(1000.0)
    while ( abs(offset) <= sync_lock_upperbound ) :
        offset = time_sync()
        if verbose :
            print(offset)
    

import inspect

class debugger_class:
    '''Creates a log folder in present dir, Takes 1st argument as verbose = True/ False , 2nd filename'''
    verbose_control = False
    use_debugger=False
    read = ""
    filename=""
    cmd="Generated_By_Debugger_own : RishabhDubey "
    bad_chars = [ '~' , '`' , '!' , '@' , '#' , '$' , '%' , '^' , '&' ,
                  '*' , '(' , ')' , '_' , '+' , '-' , '=' , '{' , '}' ,
                  '[' , ']' , '|' , ":" , ';' , "'" , ',' , '<' ,
                  '>' , ',' , '.' , '?' , '/']
    
    def __init__(self , use_debugger = True,verbose_control = False , create_dir = True , filename = "log_file"):
        self.use_debugger = use_debugger
        self.verbose_control = verbose_control
        if (self.verbose_control):
            print("\n\n VERBOSE MODE ON \n\n")
        self.filename=filename
        if (create_dir):
            self.run_cmd("rm -rf logs")
            self.run_cmd("mkdir logs")
        self.run_cmd("touch ./logs/"+str(self.filename))
        init_cmd = "echo " + "'This is a log file '" + self.filename + "> ./logs/" + self.filename
        self.run_cmd( init_cmd )
        init_cmd = "echo " + "'Path '" + sys.argv[0] + ">> ./logs/" + self.filename
        self.run_cmd( init_cmd )
        init_cmd = "echo " + "'    '" + ">> ./logs/" + self.filename
        self.run_cmd( init_cmd )
        init_cmd = "echo " + "'__FucntionName__  LOGS  '"  + ">> ./logs/" + self.filename
        self.run_cmd( init_cmd )
        init_cmd = "echo " + "'    '" + ">> ./logs/" + self.filename
        self.run_cmd( init_cmd )
        self.log( "debuggerClass init " , self.cmd)
        init_cmd = "echo " + "'    '" + ">> ./logs/" + self.filename
        self.run_cmd( init_cmd )

    def run_cmd (self ,string):
        if (self.use_debugger == False):
            return
        try: 
            stream = os.popen(string)
            self.read = stream.read()
        except OSError as error:
            print(error)
            
    def verbose(self , string):
        if (self.verbose_control):
            print(string)

    def log (self , function , string ):
        # ct stores current time 
        if (self.use_debugger == False):
            return
        current_time = datetime.datetime.now()
        self.cmd = " __ " + str(function) + " __  : " +string 
        self.verbose(self.cmd)
        self.cmd = self.cmd + " " +str(current_time)
        self.cmd +=  " >> ./logs/"+self.filename
        self.cmd = "echo " + self.cmd
        self.cmd = self.remove_slash_n(self.cmd)
        self.run_cmd(self.cmd)
    
    def function_name(self):
        function_name = inspect.stack()[1][3]
        function_name = self.remove_bad_chars(function_name)
        return str(function_name)

    def remove_bad_chars(self , string):
        string = ''.join((filter(lambda i: i not in self.bad_chars, string)))
        return str(string)
    
    def remove_slash_n(self , string):
        string = ''.join((filter(lambda i: i not in '\n', string)))
        return str(string)
