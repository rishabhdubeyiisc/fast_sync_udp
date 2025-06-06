#!/usr/bin/env python3
"""
Local Testing Configuration for Fast Sync UDP
Converts 5-computer lab setup to single PC with different ports
"""

# Original Lab IP Configuration
LAB_CONFIG = {
    'pmu_31': '10.64.37.31',
    'pmu_32': '10.64.37.32', 
    'pmu_33': '10.64.37.33',
    'pmu_34': '10.64.37.34',
    'pdc_35': '10.64.37.35'
}

# Local Testing Configuration - All on localhost with different ports
LOCAL_CONFIG = {
    'pmu_31': {'ip': '127.0.0.1', 'port': 9991},
    'pmu_32': {'ip': '127.0.0.1', 'port': 9992},
    'pmu_33': {'ip': '127.0.0.1', 'port': 9993}, 
    'pmu_34': {'ip': '127.0.0.1', 'port': 9994},
    'pdc_35': {'ip': '127.0.0.1', 'port': 9995}
}

# PMU ID to Local Port mapping (for server)
LOCAL_PMU_ID_PORT_MAP = {
    1000: {'ip': '127.0.0.1', 'port': 9991},  # PMU 31
    2000: {'ip': '127.0.0.1', 'port': 9992},  # PMU 32
    3000: {'ip': '127.0.0.1', 'port': 9993},  # PMU 33
    4000: {'ip': '127.0.0.1', 'port': 9994}   # PMU 34
}

# IP name mapping for local testing
LOCAL_IP_NAME_DICT = {
    '127.0.0.1': 'localhost_all_pmus'
}

def get_local_pmu_config(pmu_name):
    """Get local configuration for a specific PMU"""
    return LOCAL_CONFIG.get(pmu_name)

def get_pdc_config():
    """Get PDC server configuration for local testing"""
    return LOCAL_CONFIG['pdc_35']

def get_all_pmu_configs():
    """Get all PMU configurations"""
    return {k: v for k, v in LOCAL_CONFIG.items() if k.startswith('pmu_')}

def print_local_setup():
    """Print the local testing setup"""
    print("=== Local Testing Configuration ===")
    print("PDC Server:", LOCAL_CONFIG['pdc_35'])
    print("\nPMU Clients:")
    for pmu, config in get_all_pmu_configs().items():
        print(f"  {pmu}: {config}")
    print("\nAll running on localhost (127.0.0.1)")
    print("=====================================")

if __name__ == "__main__":
    print_local_setup() 