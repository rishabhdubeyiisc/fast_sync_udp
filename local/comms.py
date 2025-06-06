#!/usr/bin/env python3
"""
Local communication classes for testing - no sudo required
"""
import socket
import threading
import logging
import sys
import os
from time import time, sleep as time_sleep

# Add common directory to path for shared utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from local_utils import get_my_ipv4, check_sudo

class LocalPmuClient:
    """Simplified PMU Client for local testing"""
    
    def __init__(self, IP_to_send='127.0.0.1', port_to_send=9995, buffer=1024):
        # Mock sudo check (always passes)
        check_sudo()
        
        self.PDC_IP = IP_to_send
        self.PDC_port = port_to_send
        self.BUFFER_SIZE = buffer
        self._time_offset = 0.0
        
        # Create UDP socket
        self.cl_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.cl_sock.settimeout(10.0)  # 10 second timeout
        
        print(f"Local PMU Client created: {IP_to_send}:{port_to_send}")
    
    def send_to_PDC(self, payload: bytes):
        """Send data to PDC"""
        try:
            self.cl_sock.sendto(payload, (self.PDC_IP, self.PDC_port))
        except Exception as e:
            print(f"Send error: {e}")
            raise
    
    def recv_frm_PDC(self) -> bytes:
        """Receive data from PDC"""
        try:
            data_recvd, server_addr = self.cl_sock.recvfrom(self.BUFFER_SIZE)
            return data_recvd
        except Exception as e:
            print(f"Receive error: {e}")
            raise
    
    def get_time_offset(self):
        """Mock time offset for local testing"""
        return self._time_offset
    
    def __del__(self):
        try:
            self.cl_sock.close()
        except:
            pass

class LocalPdcServer:
    """Simplified PDC Server for local testing"""
    
    def __init__(self, ip_server_is_binding='127.0.0.1', port_opening=9995, buffer_size=1024):
        # Mock sudo check (always passes)
        check_sudo()
        
        self.ip_server_is_binding = ip_server_is_binding
        self.port_opening = port_opening
        self.buffer_size = buffer_size
        self._time_offset = 0.0
        
        # Create UDP socket
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_sock.bind((self.ip_server_is_binding, self.port_opening))
            print(f"Local PDC Server bound to: {ip_server_is_binding}:{port_opening}")
        except socket.error as err:
            print(f"Bind error: {err}")
            raise
    
    def recv(self):
        """Receive data from PMU"""
        try:
            data_recvd, addr_of_client = self.server_sock.recvfrom(self.buffer_size)
            return data_recvd, addr_of_client
        except Exception as e:
            print(f"Receive error: {e}")
            raise
    
    def send_to(self, payload: bytes, pmu_IP='127.0.0.1', pmu_port=9991):
        """Send response to PMU"""
        try:
            self.server_sock.sendto(payload, (pmu_IP, pmu_port))
        except Exception as e:
            print(f"Send error: {e}")
            raise
    
    def get_time_offset(self):
        """Mock time offset for local testing"""
        return self._time_offset
    
    def __del__(self):
        try:
            self.server_sock.close()
        except:
            pass

# Aliases to match original class names
Pmu_Client = LocalPmuClient
PDC_server = LocalPdcServer 