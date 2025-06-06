#!/usr/bin/env python3
"""
Enhanced Test Launcher with Real Data Visualization and ML Analysis
"""
import os
import sys
import time
import signal
import subprocess
import threading

# Add common directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from config import print_local_setup, get_all_pmu_configs

class EnhancedTestLauncher:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def start_enhanced_server(self):
        """Start the enhanced PDC server"""
        print("🏭 Starting Enhanced PDC Server...")
        try:
            pdc_process = subprocess.Popen([
                sys.executable, 'server.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.processes.append(('Enhanced_PDC_Server', pdc_process))
            print("✓ Enhanced PDC Server started")
            return True
        except Exception as e:
            print(f"✗ Failed to start Enhanced PDC Server: {e}")
            return False
    
    def start_enhanced_client(self, pmu_name, duration=60):
        """Start an enhanced PMU client"""
        print(f"🔌 Starting Enhanced {pmu_name.upper()}...")
        try:
            pmu_process = subprocess.Popen([
                sys.executable, 'client.py', pmu_name, str(duration)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.processes.append((f'Enhanced_{pmu_name.upper()}', pmu_process))
            print(f"✓ Enhanced {pmu_name.upper()} started")
            return True
        except Exception as e:
            print(f"✗ Failed to start Enhanced {pmu_name.upper()}: {e}")
            return False
    
    def start_ml_analyzer(self, interval=30):
        """Start periodic ML analysis"""
        print("🤖 Starting ML Analyzer...")
        try:
            def run_periodic_analysis():
                while self.running:
                    time.sleep(interval)
                    if self.running:
                        print(f"\n{'='*60}")
                        print("🤖 Running ML Analysis...")
                        try:
                            result = subprocess.run([
                                sys.executable, 'analyzer.py', '0.5'
                            ], capture_output=True, text=True)
                            if result.stdout:
                                print(result.stdout)
                        except Exception as e:
                            print(f"ML Analysis error: {e}")
            
            analysis_thread = threading.Thread(target=run_periodic_analysis, daemon=True)
            analysis_thread.start()
            print("✓ ML Analyzer started (periodic analysis every 30s)")
            return True
        except Exception as e:
            print(f"✗ Failed to start ML Analyzer: {e}")
            return False
    
    def monitor_processes(self):
        """Monitor running processes and print their output"""
        def print_output(name, process):
            while self.running and process.poll() is None:
                try:
                    output = process.stdout.readline()
                    if output and output.strip():
                        print(f"[{name}] {output.strip()}")
                    time.sleep(0.1)
                except:
                    break
        
        # Start monitoring threads for each process
        for name, process in self.processes:
            monitor_thread = threading.Thread(
                target=print_output, 
                args=(name, process),
                daemon=True
            )
            monitor_thread.start()
    
    def stop_all_processes(self):
        """Stop all running processes"""
        print(f"\n{'='*60}")
        print("🛑 Stopping all processes...")
        self.running = False
        
        for name, process in self.processes:
            try:
                if process.poll() is None:  # Process is still running
                    print(f"Stopping {name}...")
                    process.terminate()
                    time.sleep(1)
                    if process.poll() is None:
                        process.kill()
                    print(f"✓ {name} stopped")
            except Exception as e:
                print(f"Error stopping {name}: {e}")
        
        self.processes = []
    
    def run_enhanced_demo(self, duration=120):
        """Run enhanced demo with realistic power system simulation"""
        print("🎯 Enhanced Demo - Realistic Power System Simulation")
        print_local_setup()
        print(f"\n🕐 Demo Duration: {duration} seconds")
        print("📊 Features: Real database storage, ML analysis, event simulation")
        print("🤖 ML Analysis: Every 30 seconds")
        print("⚡ Events: Frequency excursions, voltage sags, load steps, breaker trips")
        print(f"\n{'='*60}")

        # Start enhanced PDC server
        if not self.start_enhanced_server():
            return

        time.sleep(3)  # Give server time to start

        # Start ML analyzer
        self.start_ml_analyzer()

        # Start multiple PMUs with staggered timing
        pmu_configs = get_all_pmu_configs()
        started_pmus = 0
        
        for i, pmu_name in enumerate(pmu_configs.keys()):
            if self.start_enhanced_client(pmu_name, duration):
                started_pmus += 1
                time.sleep(2)  # Stagger PMU starts

        if started_pmus == 0:
            print("❌ No PMUs started successfully")
            self.stop_all_processes()
            return

        print(f"\n✅ {started_pmus} Enhanced PMUs started successfully")
        print("🎭 Simulating realistic power system behavior...")

        # Monitor processes
        self.monitor_processes()

        try:
            # Wait for demo to complete
            print(f"\n⏳ Demo running... (Press Ctrl+C to stop early)")
            time.sleep(duration + 10)
        except KeyboardInterrupt:
            print("\n\n⚠️  Demo interrupted by user")
        finally:
            self.stop_all_processes()
            
            # Final ML analysis
            print(f"\n{'='*60}")
            print("📊 FINAL ML ANALYSIS REPORT")
            print("="*60)
            try:
                result = subprocess.run([
                    sys.executable, 'analyzer.py', '1'
                ], capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout)
            except Exception as e:
                print(f"Final analysis error: {e}")
            
            print("\n💾 Data saved to: synchrophasor_data.db")
            print("🔍 To view database: sqlite3 synchrophasor_data.db")
            print("📊 To run analysis: python3 analyzer.py [hours]")
    
    def run_single_pmu_demo(self, pmu_name='pmu_34', duration=60):
        """Run demo with single PMU for focused analysis"""
        print("🔍 Single PMU Enhanced Demo")
        print_local_setup()
        print(f"\n🎯 Testing: {pmu_name.upper()}")
        print(f"🕐 Duration: {duration} seconds") 
        print("📈 Features: Detailed frame visualization, real-time ML analysis")
        print(f"\n{'='*60}")

        # Start enhanced PDC server
        if not self.start_enhanced_server():
            return

        time.sleep(3)

        # Start ML analyzer
        self.start_ml_analyzer(interval=20)  # More frequent analysis

        # Start single PMU
        if not self.start_enhanced_client(pmu_name, duration):
            self.stop_all_processes()
            return

        print(f"\n✅ Enhanced {pmu_name.upper()} started")
        print("🔬 Running detailed analysis...")

        # Monitor processes
        self.monitor_processes()

        try:
            time.sleep(duration + 5)
        except KeyboardInterrupt:
            print("\n\n⚠️  Demo interrupted by user")
        finally:
            self.stop_all_processes()
            
            # Final analysis
            print(f"\n{'='*60}")
            print("📊 DETAILED ANALYSIS REPORT")
            print("="*60)
            try:
                result = subprocess.run([
                    sys.executable, 'analyzer.py', '0.5'
                ], capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout)
            except Exception as e:
                print(f"Analysis error: {e}")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n🛑 Received interrupt signal...")
    sys.exit(0)

def show_usage():
    """Show usage instructions"""
    print("Enhanced Test Launcher for Fast Sync UDP")
    print("="*50)
    print("Features:")
    print("  🏭 Real database storage (SQLite)")
    print("  🤖 Machine Learning analysis")
    print("  ⚡ Realistic power system events")
    print("  📊 Detailed frame visualization")
    print("  🔮 Event prediction")
    print("\nUsage:")
    print("  python3 run_enhanced_test.py [mode] [duration]")
    print("\nModes:")
    print("  demo     - Full demo with all 4 PMUs (default)")
    print("  single   - Single PMU detailed analysis")
    print("  config   - Show configuration only")
    print("\nDuration:")
    print("  Number of seconds to run (default: 120 for demo, 60 for single)")
    print("\nExamples:")
    print("  python3 run_enhanced_test.py demo 180")
    print("  python3 run_enhanced_test.py single 90")
    print("  python3 run_enhanced_test.py config")
    print("\nRequirements:")
    print("  pip install pandas numpy scikit-learn matplotlib")

def main():
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal_handler)
    
    # Parse arguments
    mode = 'demo'
    duration = 120
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    if len(sys.argv) > 2:
        try:
            duration = int(sys.argv[2])
        except ValueError:
            print("❌ Error: Duration must be a number")
            return
    
    # Adjust default duration for single mode
    if mode == 'single' and len(sys.argv) <= 2:
        duration = 60
    
    launcher = EnhancedTestLauncher()
    
    if mode == 'config':
        print_local_setup()
    elif mode == 'demo':
        launcher.run_enhanced_demo(duration)
    elif mode == 'single':
        pmu_name = 'pmu_34'  # Default PMU
        launcher.run_single_pmu_demo(pmu_name, duration)
    else:
        show_usage()

if __name__ == "__main__":
    main() 