# Fast Synced UDP - IEEE C37.118.2 Synchrophasor Implementation

A high-performance Python implementation of the IEEE C37.118.2 standard for synchrophasor data transfer in power systems. This project provides PMU (Phasor Measurement Unit) client and PDC (Phasor Data Concentrator) server functionality with precise time synchronization capabilities.

## Features

- **IEEE C37.118.2 Standard Compliance**: Complete implementation of synchrophasor data transfer protocol
- **PMU & PDC Communication**: UDP-based networking for real-time data exchange
- **Dual Time Synchronization**: Support for both NTP and PTP time synchronization
- **Real-time Database Integration**: Time series database storage with thread-safe queuing
- **Frame Types Support**: Data, Configuration (v1, v2, v3), Command, and Header frames
- **CRC Validation**: Frame integrity checking with CRC16-XMODEM
- **Comprehensive Logging**: Detailed transaction and synchronization logging
- **Multi-threaded Architecture**: Concurrent data processing and storage

## Project Structure

```
fast_sync_udp/
├── main_client.py          # PMU client implementation
├── main_server.py          # PDC server implementation
├── frame.py                # IEEE C37.118.2 frame implementations
├── cl_inherited_comms.py   # Communication classes (PMU_Client, PDC_server)
├── cl_utils.py             # Database client and threading utilities
├── utils.py                # System utilities and time synchronization
├── conf/                   # Configuration files
├── examples/               # Example implementations
└── backups/                # Backup files
```

## Quick Start

### Prerequisites

- Python 3.x
- Root/sudo privileges (required for time synchronization)
- Network access for NTP/PTP synchronization
- InfluxDB (optional, for database integration)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fast_sync_udp
```

2. Install dependencies:
```bash
pip install -r requirements.txt  # If requirements.txt exists
```

### Running PMU Client

```python
from cl_inherited_comms import Pmu_Client
from frame import DataFrame, ConfigFrame2

# Create PMU client with PTP synchronization
pmu_client = Pmu_Client(
    IP_to_send='10.64.37.35',        # PDC IP address
    port_to_send=9991,               # Communication port
    buffer=1024,                     # Buffer size
    trans_logging_level='DEBUG',     # Logging level
    to_log_trans=True,               # Enable transaction logging
    
    # PTP synchronization settings
    ptp_server_sync=True,
    ptp_sync_wait=0.5,
    to_log_ptp_syncer=False,
    ptp_sync_logging_level='DEBUG'
)

# Send synchrophasor data
pmu_client.send_to_PDC(data_payload)
```

### Running PDC Server

```python
from cl_inherited_comms import PDC_server

# Create PDC server
pdc_server = PDC_server(
    ip_server_is_binding='10.64.37.35',  # Server binding IP
    port_opening=9991,                   # Listening port
    buffer_size=1024,                    # Buffer size
    trans_logging_level='DEBUG',         # Logging level
    to_log_trans=True,                   # Enable logging
    
    # PTP synchronization
    ptp_server_sync=True,
    ptp_sync_wait=0.5,
    to_log_ptp_syncer=False,
    ptp_sync_logging_level='DEBUG'
)

# Receive and process data
while True:
    data, client_addr = pdc_server.recv()
    # Process received synchrophasor data
    pdc_server.send_to(response_data, client_ip, client_port)
```

## IEEE C37.118.2 Frame Types

### Data Frames
Real-time synchrophasor measurements including:
- Phasor data (voltage and current)
- Frequency and ROCOF (Rate of Change of Frequency)
- Analog measurements
- Digital status indicators

### Configuration Frames
- **Config v1**: Basic PMU configuration
- **Config v2**: Extended configuration with additional metadata
- **Config v3**: Advanced configuration options

### Command Frames
Control commands for PMU operations:
- Start/Stop data transmission
- Configuration requests
- Extended frame commands

### Header Frames
Human-readable information about the PMU station

## Time Synchronization

### NTP Synchronization
```python
# NTP client configuration
pmu_client = Pmu_Client(
    ntp_server="10.64.37.35",
    ntp_server_sync=True,
    sync_lock_precision=1e-3,
    ntp_sync_wait=30
)
```

### PTP Synchronization (Precision Time Protocol)
```python
# PTP client configuration
pmu_client = Pmu_Client(
    ptp_server_sync=True,
    ptp_sync_wait=0.5,
    to_log_ptp_syncer=True
)
```

## Database Integration

The project includes real-time time series database integration:

```python
from cl_utils import db_client_cls, Thread_safe_queue

# Create database client
db_client = db_client_cls(IFDbname='PMU_DATA')

# Thread-safe queue for data buffering
data_queue = Thread_safe_queue(BUF_SIZE=0, to_log_queue=True)

# Store measurement data
entry = db_client.create_me_json(
    measurement='comm_delay',
    tag_name='pmu_34',
    tag_field='fracsec_diff',
    field_name='pdc_pmu_diff',
    field_value=time_offset
)
data_queue.put_in_queue(entry)
```

## Configuration

### Network Configuration
Default IP mapping for PMUs and PDC:
- PMU 31: `10.64.37.31`
- PMU 32: `10.64.37.32`
- PMU 33: `10.64.37.33`
- PMU 34: `10.64.37.34`
- PDC 35: `10.64.37.35`

### Time Synchronization Settings
- **Sync Lock Precision**: 1ms (configurable)
- **NTP Sync Wait**: 30 seconds
- **PTP Sync Wait**: 0.5 seconds

## Logging

The system provides comprehensive logging for:
- **Transaction Logs**: Network communication details
- **Synchronization Logs**: Time sync status and offsets
- **Database Logs**: Storage operations and queue status

Log files are generated per PMU/PDC instance:
- `log_<device_name>_trans.log`
- `log_<device_name>_sync.log`

## Examples

See the `examples/` directory for:
- Database client usage
- Multi-threaded queue implementation
- Sample PMU and PDC configurations

## Performance Considerations

- **Data Rate**: Configurable (default: 30 samples/second)
- **Buffer Size**: Adjustable based on network conditions
- **Threading**: Multi-threaded architecture for concurrent operations
- **Queue Management**: Thread-safe data buffering for database operations

## Error Handling

The system includes comprehensive error handling for:
- Network communication failures
- Time synchronization issues
- Frame validation errors (CRC checking)
- Database connection problems

## Requirements

- Root privileges for time synchronization operations
- Network connectivity for NTP/PTP servers
- Ethernet interface for PTP synchronization
- Compatible with Linux systems (tested on WSL2)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🤝 Usage and Licensing

This fast synchronized UDP implementation for IEEE C37.118.2 synchrophasor data transfer is an educational/research project developed at IISC (Indian Institute of Science).

**Important**: Please contact the author (Rishabh Dubey) before using this code in any commercial or academic projects to ensure proper attribution and licensing compliance.

## 📧 Contact

**Engineer**: Rishabh Dubey  
**Institution**: Indian Institute of Science (IISC)  
**Project**: Fast Synced UDP - IEEE C37.118.2 Synchrophasor Implementation  
**Domain**: Power Systems & Real-time Communication  

For technical questions, collaboration requests, or licensing inquiries, please reach out to discuss proper usage and attribution.

---

*This implementation follows the IEEE Std C37.118.2-2011 standard for synchrophasor data transfer in power systems.*