#!/usr/bin/env python3
"""
Enhanced PDC Server with Real Database and Frame Visualization
"""
import threading
import json
import sqlite3
import pandas as pd
from datetime import datetime
from time import time, sleep as time_sleep

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from comms import PDC_server
from config import LOCAL_PMU_ID_PORT_MAP, get_pdc_config

# Import frame classes from common
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from frame import ConfigFrame2, DataFrame

class EnhancedDatabase:
    """Real SQLite database for storing synchrophasor data"""
    
    def __init__(self, db_name='synchrophasor_data.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Synchrophasor measurements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                pmu_id INTEGER,
                pmu_name TEXT,
                
                -- Phasor data (voltage and current)
                va_mag REAL, va_angle REAL,
                vb_mag REAL, vb_angle REAL, 
                vc_mag REAL, vc_angle REAL,
                i1_mag REAL, i1_angle REAL,
                
                -- Frequency measurements
                frequency REAL,
                rocof REAL,
                
                -- Analog measurements
                analog1 REAL,
                analog2 REAL,
                analog3 REAL,
                
                -- Digital status
                digital_status INTEGER,
                
                -- Communication metrics
                comm_delay_us INTEGER,
                frame_size_bytes INTEGER
            )
        ''')
        
        # System events table for ML analysis
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                event_type TEXT,
                pmu_id INTEGER,
                severity INTEGER,
                description TEXT,
                ml_prediction REAL
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database initialized: {self.db_name}")
    
    def store_measurement(self, data):
        """Store synchrophasor measurement in database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO measurements (
                timestamp, pmu_id, pmu_name,
                va_mag, va_angle, vb_mag, vb_angle, vc_mag, vc_angle,
                i1_mag, i1_angle, frequency, rocof,
                analog1, analog2, analog3, digital_status,
                comm_delay_us, frame_size_bytes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        
        conn.commit()
        conn.close()
    
    def store_event(self, timestamp, event_type, pmu_id, severity, description, ml_prediction=None):
        """Store system event for ML analysis"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO system_events (timestamp, event_type, pmu_id, severity, description, ml_prediction)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, event_type, pmu_id, severity, description, ml_prediction))
        
        conn.commit()
        conn.close()
    
    def get_recent_data(self, limit=100):
        """Get recent measurements for ML analysis"""
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query(f'''
            SELECT * FROM measurements 
            ORDER BY timestamp DESC 
            LIMIT {limit}
        ''', conn)
        conn.close()
        return df

class FrameAnalyzer:
    """Analyze IEEE C37.118.2 frames and detect anomalies"""
    
    def __init__(self, db):
        self.db = db
        self.baseline_freq = 60.0  # 60 Hz baseline
        self.freq_tolerance = 0.1  # ±0.1 Hz tolerance
        
    def analyze_frame(self, frame_data, pmu_id, comm_delay):
        """Analyze a single frame and detect anomalies"""
        analysis = {
            'timestamp': time(),
            'pmu_id': pmu_id,
            'anomalies': [],
            'ml_score': 0.0
        }
        
        # Frequency analysis
        freq = frame_data.get('frequency', 60.0)
        if abs(freq - self.baseline_freq) > self.freq_tolerance:
            severity = min(int(abs(freq - self.baseline_freq) * 10), 5)
            analysis['anomalies'].append({
                'type': 'frequency_deviation',
                'value': freq,
                'severity': severity,
                'description': f'Frequency {freq:.2f} Hz outside normal range'
            })
        
        # Communication delay analysis
        if comm_delay > 2000:  # > 2ms
            analysis['anomalies'].append({
                'type': 'high_latency',
                'value': comm_delay,
                'severity': 3,
                'description': f'High communication delay: {comm_delay} μs'
            })
        
        # Voltage magnitude analysis
        voltages = [frame_data.get(f'v{phase}_mag', 1.0) for phase in ['a', 'b', 'c']]
        if any(v < 0.95 or v > 1.05 for v in voltages):  # ±5% tolerance
            analysis['anomalies'].append({
                'type': 'voltage_anomaly',
                'value': voltages,
                'severity': 4,
                'description': f'Voltage magnitudes outside normal range: {voltages}'
            })
        
        # Calculate ML risk score (simple example)
        analysis['ml_score'] = len(analysis['anomalies']) * 0.3
        
        return analysis

def display_frame_data(frame, pmu_id, comm_delay, frame_size):
    """Display detailed frame information"""
    try:
        # Extract phasor data
        phasors = frame.get_phasors(convert2polar=True)
        freq = frame.get_freq()
        dfreq = frame.get_dfreq() 
        analog = frame.get_analog()
        digital = frame.get_digital()
        stat = frame.get_stat()
        
        print(f"\n{'='*60}")
        print(f"PMU {pmu_id} - {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
        print(f"{'='*60}")
        
        # Phasor data (Voltage and Current)
        print("🔌 PHASOR MEASUREMENTS:")
        phasor_names = ["VA", "VB", "VC", "I1"]
        for i, (mag, angle) in enumerate(phasors):
            if i < 3:  # Voltage phasors
                unit = "V"
                scaled_mag = mag / 120  # Account for realistic scaling in client (mag*12/10)
            else:  # Current phasors
                unit = "A"
                scaled_mag = mag / 120  # Account for realistic scaling in client
            print(f"  {phasor_names[i]}: {scaled_mag:.3f} k{unit} ∠ {angle:.1f}°")
        
        # Frequency measurements
        print(f"\n⚡ FREQUENCY MEASUREMENTS:")
        print(f"  Frequency: {freq/40:.3f} Hz")  # Account for realistic scaling in client (freq*4/10)
        print(f"  ROCOF: {dfreq/10:.3f} Hz/s")  # Account for realistic scaling in client
        
        # Analog measurements
        print(f"\n📊 ANALOG MEASUREMENTS:")
        analog_names = ["Power", "RMS", "Peak"]
        for i, value in enumerate(analog):
            print(f"  {analog_names[i]}: {value}")
        
        # Digital status
        print(f"\n🔘 DIGITAL STATUS:")
        print(f"  Status Word: 0x{digital[0]:04X}")
        print(f"  Binary: {digital[0]:016b}")
        
        # System status
        print(f"\n📡 SYSTEM STATUS:")
        print(f"  Measurement: {stat[0]}")
        print(f"  Time Sync: {'OK' if stat[1] else 'ERROR'}")
        print(f"  Time Quality: {stat[7]}")
        
        # Communication metrics
        print(f"\n🌐 COMMUNICATION:")
        print(f"  Delay: {comm_delay} μs")
        print(f"  Frame Size: {frame_size} bytes")
        
        return {
            'va_mag': phasors[0][0]/120, 'va_angle': phasors[0][1],
            'vb_mag': phasors[1][0]/120, 'vb_angle': phasors[1][1],
            'vc_mag': phasors[2][0]/120, 'vc_angle': phasors[2][1],
            'i1_mag': phasors[3][0]/120, 'i1_angle': phasors[3][1],
            'frequency': freq/40,  # Account for realistic scaling in client
            'rocof': dfreq/10,     # Account for realistic scaling in client
            'analog1': analog[0], 'analog2': analog[1], 'analog3': analog[2],
            'digital_status': digital[0]
        }
        
    except Exception as e:
        print(f"Error displaying frame data: {e}")
        return {}

def enhanced_data_processing(db, analyzer, frame, pmu_id, comm_delay, frame_size):
    """Enhanced data processing with ML analysis"""
    
    # Display frame data
    frame_data = display_frame_data(frame, pmu_id, comm_delay, frame_size)
    
    if frame_data:
        # Store in database
        db_data = (
            time(), pmu_id, f"PMU_{pmu_id}",
            frame_data['va_mag'], frame_data['va_angle'],
            frame_data['vb_mag'], frame_data['vb_angle'], 
            frame_data['vc_mag'], frame_data['vc_angle'],
            frame_data['i1_mag'], frame_data['i1_angle'],
            frame_data['frequency'], frame_data['rocof'],
            frame_data['analog1'], frame_data['analog2'], frame_data['analog3'],
            frame_data['digital_status'],
            comm_delay, frame_size
        )
        db.store_measurement(db_data)
        
        # Analyze for anomalies
        analysis = analyzer.analyze_frame(frame_data, pmu_id, comm_delay)
        
        # Display anomalies
        if analysis['anomalies']:
            print(f"\n⚠️  ANOMALIES DETECTED:")
            for anomaly in analysis['anomalies']:
                print(f"  🚨 {anomaly['type'].upper()}: {anomaly['description']}")
                
                # Store anomaly event
                db.store_event(
                    analysis['timestamp'], 
                    anomaly['type'], 
                    pmu_id, 
                    anomaly['severity'],
                    anomaly['description'],
                    analysis['ml_score']
                )
        
        # ML Risk Assessment
        if analysis['ml_score'] > 0:
            print(f"\n🤖 ML RISK SCORE: {analysis['ml_score']:.2f}/5.0")
            if analysis['ml_score'] > 1.0:
                print("  📋 RECOMMENDATION: Increase monitoring frequency")
            if analysis['ml_score'] > 2.0:
                print("  📋 RECOMMENDATION: Check equipment status")

def main():
    """Enhanced PDC server main function"""
    
    print("🏭 Enhanced PDC Server with ML Analysis")
    print("="*50)
    
    # Initialize components
    db = EnhancedDatabase()
    analyzer = FrameAnalyzer(db)
    
    # Get PDC configuration
    pdc_config = get_pdc_config()
    
    print(f"🔗 Binding to: {pdc_config['ip']}:{pdc_config['port']}")
    print(f"📊 Database: {db.db_name}")
    print(f"🤖 ML Analysis: Enabled")
    print("="*50)
    
    # Create PDC server
    pdc = PDC_server(
        ip_server_is_binding=pdc_config['ip'],
        port_opening=pdc_config['port'],
        buffer_size=1024
    )
    
    # IEEE configuration
    ieee_cfg2_sample = ConfigFrame2(1000, 1000000, 1, "Station A", 7734, (False, False, True, False),
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
                                    60, 22, 30)
    
    print("\n🎯 Waiting for synchrophasor data...")
    
    packet_count = 0
    try:
        while True:
            # Receive data
            data_recvd, addr_of_client = pdc.recv()
            packet_count += 1
            
            # Server timestamp
            server_ct = time()
            SOC_server = int(server_ct)
            FRASEC_server = int((server_ct - SOC_server) * (10**6))
            
            try:
                # Parse IEEE frame
                frame = DataFrame.convert2frame(data_recvd, ieee_cfg2_sample)
                FRASEC_Client = frame.get_frasec()[0]
                pmu_id = frame.get_id_code()
                
                # Calculate metrics
                comm_delay = FRASEC_server - FRASEC_Client
                frame_size = len(data_recvd)
                
                # Enhanced processing with ML
                enhanced_data_processing(db, analyzer, frame, pmu_id, comm_delay, frame_size)
                
                # Send response
                response = f"ACK_{packet_count}"
                pdc.send_to(pmu_IP=addr_of_client[0], 
                          pmu_port=addr_of_client[1], 
                          payload=response.encode())
                
                # Show statistics every 10 packets
                if packet_count % 10 == 0:
                    print(f"\n📈 STATISTICS: {packet_count} frames processed")
                    
                    # Get recent data for trend analysis
                    recent_data = db.get_recent_data(limit=10)
                    if not recent_data.empty:
                        avg_freq = recent_data['frequency'].mean()
                        freq_std = recent_data['frequency'].std()
                        avg_delay = recent_data['comm_delay_us'].mean()
                        
                        print(f"  📊 Avg Frequency: {avg_freq:.3f} Hz (σ={freq_std:.4f})")
                        print(f"  📊 Avg Comm Delay: {avg_delay:.1f} μs")
                
            except Exception as e:
                print(f"\n❌ Frame parsing error: {e}")
                error_response = f"ERROR_{packet_count}"
                pdc.send_to(pmu_IP=addr_of_client[0], 
                          pmu_port=addr_of_client[1], 
                          payload=error_response.encode())
                
    except KeyboardInterrupt:
        print(f"\n\n🛑 PDC Server stopped. Processed {packet_count} frames.")
        print(f"💾 Data saved to: {db.db_name}")

if __name__ == "__main__":
    main() 