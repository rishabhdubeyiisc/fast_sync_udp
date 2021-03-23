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

def sync_me ( sync_lock_upperbound : float = (10 ** (-4) ) , verbose : bool = True ):
    offset = float(1000.0)
    while ( abs(offset) > sync_lock_upperbound ) :
        offset = time_sync()
        if verbose :
            print("sync_lock_upperbound : {} , offset : {} ".format(sync_lock_upperbound , offset))
    return offset
