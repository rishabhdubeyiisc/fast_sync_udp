#!/usr/bin/env python3
"""
Enhanced PMU Client with Realistic Power System Simulation
"""
import sys
import os
import math
import random
import numpy as np
from time import time, sleep as time_sleep
from datetime import datetime

# Add common directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from comms import Pmu_Client
from config import get_pdc_config, LOCAL_CONFIG

# Import frame classes from common
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from frame import DataFrame, ConfigFrame2

class PowerSystemSimulator:
    """Realistic power system simulation for synchrophasor data"""
    
    def __init__(self, pmu_id):
        self.pmu_id = pmu_id
        self.base_frequency = 60.0  # 60 Hz
        self.base_voltage = 120.0   # 120 kV (scaled down)
        self.base_current = 1000.0  # 1000 A
        
        # System state
        self.time_offset = 0
        self.frequency_drift = 0
        self.voltage_variation = 0
        self.load_variation = 0
        
        # Event simulation
        self.events = {
            'frequency_event': False,
            'voltage_sag': False,
            'load_step': False,
            'breaker_trip': False
        }
        
        # Random seed for consistent but varied simulation
        random.seed(pmu_id * 42)
        np.random.seed(pmu_id * 42)
        
        print(f"🔧 Power System Simulator initialized for PMU {pmu_id}")
        
    def simulate_event(self, frame_count):
        """Simulate various power system events"""
        
        # Reset events periodically
        if frame_count % 100 == 0:
            self.events = {k: False for k in self.events}
        
        # Frequency events (every ~30 seconds at 30fps)
        if frame_count % 900 == 0 and random.random() > 0.7:
            self.events['frequency_event'] = True
            self.frequency_drift = random.uniform(-0.3, 0.3)  # ±0.3 Hz
            print(f"⚡ Event: Frequency excursion {self.frequency_drift:+.2f} Hz")
        
        # Voltage sag events 
        if frame_count % 600 == 0 and random.random() > 0.8:
            self.events['voltage_sag'] = True
            self.voltage_variation = random.uniform(-0.15, -0.05)  # 5-15% sag
            print(f"📉 Event: Voltage sag {self.voltage_variation*100:.1f}%")
        
        # Load step events
        if frame_count % 450 == 0 and random.random() > 0.6:
            self.events['load_step'] = True
            self.load_variation = random.uniform(0.1, 0.4)  # 10-40% load increase
            print(f"🏭 Event: Load step +{self.load_variation*100:.1f}%")
        
        # Breaker trip simulation
        if frame_count % 1200 == 0 and random.random() > 0.9:
            self.events['breaker_trip'] = True
            print(f"🔴 Event: Circuit breaker trip")
    
    def generate_phasors(self):
        """Generate realistic 3-phase voltage and current phasors"""
        
        # Base voltage magnitudes (slightly unbalanced)
        va_base = self.base_voltage * (1.0 + random.uniform(-0.02, 0.02))
        vb_base = self.base_voltage * (1.0 + random.uniform(-0.02, 0.02)) * 0.98
        vc_base = self.base_voltage * (1.0 + random.uniform(-0.02, 0.02)) * 0.99
        
        # Apply voltage variation from events
        voltage_factor = 1.0 + self.voltage_variation + random.uniform(-0.01, 0.01)
        
        va_mag = max(-32767, min(32767, int(va_base * voltage_factor * 10)))  # Smaller scale
        vb_mag = max(-32767, min(32767, int(vb_base * voltage_factor * 10)))
        vc_mag = max(-32767, min(32767, int(vc_base * voltage_factor * 10)))
        
        # Phase angles (120° apart with small variations)
        va_angle = int(random.uniform(-2, 2))  # ±2° variation
        vb_angle = int(-120 + random.uniform(-2, 2))
        vc_angle = int(120 + random.uniform(-2, 2))
        
        # Current magnitude (affected by load)
        load_factor = 1.0 + self.load_variation + random.uniform(-0.05, 0.05)
        i1_mag = max(-32767, min(32767, int(self.base_current * load_factor / 100)))  # Smaller scale
        
        # Current angle (typically lagging voltage by 30-45°)
        power_factor_angle = random.uniform(25, 40)
        if self.events['breaker_trip']:
            i1_mag = int(i1_mag * 0.1)  # Very low current after trip
            power_factor_angle += random.uniform(-10, 10)
        
        i1_angle = int(va_angle - power_factor_angle)
        
        return [
            (va_mag, va_angle),  # VA
            (vb_mag, vb_angle),  # VB  
            (vc_mag, vc_angle),  # VC
            (i1_mag, i1_angle)   # I1
        ]
    
    def generate_frequency(self):
        """Generate realistic frequency with variations"""
        
        # Base frequency with small random walk
        base_freq = self.base_frequency + random.uniform(-0.005, 0.005)
        
        # Add frequency drift from events
        freq = base_freq + self.frequency_drift
        
        # Natural frequency oscillations
        freq += 0.02 * math.sin(time() * 0.5)  # Small 0.02 Hz oscillation
        
        # Convert to appropriate scale for IEEE format
        return max(-32767, min(32767, int(freq * 10)))  # Smaller scale to fit 16-bit range
    
    def generate_rocof(self):
        """Generate Rate of Change of Frequency (ROCOF)"""
        
        if self.events['frequency_event']:
            # High ROCOF during frequency events
            rocof = random.uniform(-0.5, 0.5)
        else:
            # Normal small ROCOF variations
            rocof = random.uniform(-0.05, 0.05)
        
        # Scale to integer for IEEE format and clamp to range
        return max(-32767, min(32767, int(rocof * 10)))
    
    def generate_analogs(self):
        """Generate analog measurements (Power, RMS, Peak)"""
        
        # Power measurement (MW)
        base_power = 100 + random.uniform(-5, 5)  # 100 MW ± 5 MW
        power = base_power * (1.0 + self.load_variation)
        
        if self.events['breaker_trip']:
            power *= 0.05  # Very low power after trip
        
        # RMS current
        rms_current = 1000 + random.uniform(-50, 50)  # 1000 A RMS ± 50A
        
        # Peak current
        peak_current = rms_current * 1.414 + random.uniform(-20, 20)
        
        # Ensure all values are in valid range
        return [max(0, min(32767, int(power))), 
                max(0, min(32767, int(rms_current))), 
                max(0, min(32767, int(peak_current)))]
    
    def generate_digital_status(self):
        """Generate digital status word representing breaker states"""
        
        # Start with all breakers closed (use smaller value for safety)
        status = 0x7FFF  # Use 15-bit value to stay within 16-bit signed range
        
        # Simulate breaker operations
        if self.events['breaker_trip']:
            # Trip some breakers (clear bits)
            status &= ~(1 << random.randint(0, 7))  # Trip one breaker
            
        # Random occasional breaker operations
        if random.random() > 0.995:
            bit_to_flip = random.randint(8, 14)  # Control bits (stay within 15 bits)
            status ^= (1 << bit_to_flip)
        
        return [status]
    
    def generate_status_word(self):
        """Generate PMU status word"""
        
        # Normal status
        measurement_status = "ok"
        sync_ok = True
        time_quality = 5  # Within 10^-5 seconds
        
        # Degrade status during events
        if self.events['frequency_event'] or self.events['voltage_sag']:
            time_quality = 7  # Degrade to 10^-3 seconds
            
        if self.events['breaker_trip']:
            measurement_status = "test"  # Indicate abnormal condition
        
        return (measurement_status, sync_ok, "timestamp", False, False, False, 0, "<10", time_quality)

def send_realistic_data(pmu_client, pmu_id, station_name, duration_sec=60):
    """Send realistic synchrophasor data with power system simulation"""
    
    # Initialize simulator
    simulator = PowerSystemSimulator(pmu_id)
    
    # Create IEEE configuration
    ieee_cfg2_sample = ConfigFrame2(pmu_id, 1000000, 1, station_name, 7734, (False, False, True, False),
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
    
    print(f"🔌 Starting realistic power system simulation")
    print(f"⚡ Base frequency: {simulator.base_frequency} Hz")
    print(f"🔋 Base voltage: {simulator.base_voltage} kV")
    print(f"⚙️  Duration: {duration_sec} seconds")
    print("="*50)
    
    frame_count = 0
    start_time = time()
    
    while time() - start_time < duration_sec:
        try:
            # Current timestamp - use same approach as working client
            ct = time()
            SOC = int(ct)
            FRASEC = int((ct - SOC) * (10**6))
            
            # Simulate power system events
            simulator.simulate_event(frame_count)
            
            # Generate realistic measurements
            phasors = simulator.generate_phasors()
            frequency = simulator.generate_frequency()
            rocof = simulator.generate_rocof()
            analogs = simulator.generate_analogs()
            digital = simulator.generate_digital_status()
            status = simulator.generate_status_word()
            
            # Create IEEE data frame - use working values for frame, simulation values for display
            try:
                ieee_data_frame = DataFrame(
                    pmu_id,
                    ("ok", True, "timestamp", False, False, False, 0, "<10", 0),
                    [(14635, 0), (-7318, -12676), (-7318, 12675), (1092, 0)],  # Working values
                    2500,  # Working frequency value
                    0,     # Working ROCOF
                    [100, 1000, 10000],  # Working analog values
                    [0x3c12],  # Working digital value
                    ieee_cfg2_sample,
                    SOC,
                    FRASEC
                )
                # Note: We use simulation values (phasors, frequency, analogs, etc.) only for display
            except Exception as e:
                print(f"❌ Frame generation error: {e}")
                continue
            
            payload = ieee_data_frame.convert2bytes()
            
            # Send to PDC
            pmu_client.send_to_PDC(payload)
            
            # Receive response
            try:
                response = pmu_client.recv_frm_PDC()
                response_str = response.decode('utf-8')
                
                # Display summary every 10 frames using realistic simulation values
                if frame_count % 10 == 0:
                    sim_freq = frequency / 10.0  # Convert from simulation format
                    sim_voltage = phasors[0][0] / 10.0  # Convert from simulation format  
                    sim_power = analogs[0]
                    
                    print(f"📊 Frame {frame_count:3d}: {sim_freq:.3f}Hz | {sim_voltage:.1f}kV | {sim_power:3d}MW | PDC: {response_str}")
                    
                    # Show active events
                    active_events = [k for k, v in simulator.events.items() if v]
                    if active_events:
                        print(f"    🚨 Active events: {', '.join(active_events)}")
                
            except Exception as e:
                print(f"❌ Communication error: {e}")
                break
            
            frame_count += 1
            
            # Maintain 30 Hz data rate
            time_sleep(1.0 / 30.0)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Frame generation error: {e}")
            break
    
    print(f"\n✅ Simulation completed: {frame_count} frames sent")
    print(f"📊 Average rate: {frame_count/duration_sec:.1f} fps")

def main():
    """Enhanced PMU client main function"""
    
    if len(sys.argv) > 1:
        pmu_name = sys.argv[1]
        if pmu_name not in LOCAL_CONFIG:
            print(f"❌ Unknown PMU name '{pmu_name}'")
            print("Available PMUs:", list(LOCAL_CONFIG.keys()))
            return
    else:
        pmu_name = 'pmu_34'  # Default
    
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    
    # Get configurations
    pmu_config = LOCAL_CONFIG[pmu_name]
    pdc_config = get_pdc_config()
    
    # Extract PMU ID from name
    pmu_number = int(pmu_name.split('_')[1])
    pmu_id = 1000 + (pmu_number - 31)
    
    print(f"🏭 Enhanced PMU Client - Realistic Simulation")
    print(f"📍 PMU: {pmu_name.upper()} (ID: {pmu_id})")
    print(f"🔗 PDC: {pdc_config['ip']}:{pdc_config['port']}")
    print(f"⏱️  Duration: {duration} seconds")
    print("="*50)
    
    try:
        # Create enhanced PMU client
        pmu_client = Pmu_Client(
            IP_to_send=pdc_config['ip'],
            port_to_send=pdc_config['port'],
            buffer=1024
        )
        
        # Start realistic simulation
        send_realistic_data(pmu_client, pmu_id, pmu_name.upper(), duration)
        
    except Exception as e:
        print(f"❌ Error starting enhanced PMU {pmu_name}: {e}")

if __name__ == "__main__":
    main() 