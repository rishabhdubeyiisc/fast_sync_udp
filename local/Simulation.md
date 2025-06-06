# Synchrophasor System with Machine Learning Analysis

## 🎯 System Overview

This is a comprehensive IEEE C37.118.2 compliant synchrophasor system that transforms basic PMU-PDC communication into an intelligent power grid monitoring platform. The system features realistic power system simulation, production-grade database storage, and machine learning analysis for automated decision making.

**Key Capabilities:**
- IEEE C37.118.2 standard implementation
- Realistic power system behavior simulation
- Real-time database storage with ML analysis
- Anomaly detection and event prediction
- Scalable architecture supporting multiple PMUs
- Production-ready deployment options

## 📁 System Architecture & Files

### **Core System Components**

#### `server.py` - PDC Server with ML Integration
**Purpose:** The main Phasor Data Concentrator that receives, processes, and analyzes synchrophasor data.

**Key Features:**
- Real-time IEEE frame parsing and validation
- SQLite database integration for data persistence
- Live anomaly detection and risk assessment
- Detailed frame visualization with power system metrics
- ML-based event detection and classification
- Communication delay analysis and performance monitoring

**Implementation:**
- `EnhancedDatabase` class for SQLite operations
- `FrameAnalyzer` class for real-time ML analysis
- `display_frame_data()` for comprehensive data visualization
- Automatic risk scoring and operational recommendations

#### `client.py` - PMU Client with Power System Simulation
**Purpose:** Simulates realistic PMU behavior with authentic power system characteristics and events.

**Key Features:**
- Realistic 3-phase voltage and current phasor generation
- Dynamic frequency variations and ROCOF calculation
- Power system event simulation (frequency excursions, voltage sags, load steps, breaker trips)
- Configurable simulation parameters and duration
- IEEE frame generation with proper scaling and validation

**Implementation:**
- `PowerSystemSimulator` class for realistic data generation
- Event-driven simulation with probability-based triggers
- Proper IEEE data formatting and range validation
- Real-time status and measurement generation

#### `analyzer.py` - Machine Learning Analysis Engine
**Purpose:** Performs comprehensive ML analysis on stored synchrophasor data for power system intelligence.

**Key Features:**
- Frequency stability analysis with anomaly detection
- Voltage profile analysis and unbalance detection
- Power quality assessment and scoring
- Predictive analysis for system events
- Risk assessment with operational recommendations

**Implementation:**
- `SynchrophasorMLAnalyzer` class with multiple ML models
- Isolation Forest for anomaly detection
- DBSCAN for system state clustering
- Statistical analysis and trend detection
- Automated report generation

### **System Control & Configuration**

#### `run_test.py` - Test Orchestration & Demo Launcher
**Purpose:** Comprehensive test launcher that coordinates all system components for demonstrations and testing.

**Key Features:**
- Multiple test modes (demo, single PMU, configuration display)
- Process management and monitoring
- Automatic ML analysis scheduling
- Error handling and graceful shutdown
- Real-time output monitoring and logging

**Implementation:**
- `EnhancedTestLauncher` class for test coordination
- Subprocess management for parallel execution
- Automatic cleanup and process termination
- Configurable test duration and parameters

#### `config.py` - System Configuration Management
**Purpose:** Centralized configuration for all system components including network settings and PMU mappings.

**Key Features:**
- Local testing configuration with port mapping
- PMU ID and network address management
- Configuration validation and display utilities
- Support for both lab and local deployment modes

**Implementation:**
- Configuration dictionaries for different deployment scenarios
- Utility functions for configuration retrieval and validation
- Network topology management for multi-PMU setups

#### `comms.py` - Communication Infrastructure
**Purpose:** Low-level communication classes for PMU-PDC data exchange.

**Key Features:**
- UDP socket management for high-speed data transfer
- Local testing mode with bypass for system requirements
- Error handling and connection management
- Buffer management and data transmission utilities

**Implementation:**
- `PDC_server` class for server-side communication
- `Pmu_Client` class for client-side data transmission
- Socket configuration and error handling
- Local testing adaptations

### **Data Management & Utilities**

#### `synchrophasor_data.db` - Production Database
**Purpose:** SQLite database storing all synchrophasor measurements and system events.

**Schema:**
- **measurements** table: Complete synchrophasor data with timestamps
- **system_events** table: Detected anomalies and ML predictions
- Optimized for time-series analysis and ML training

#### `check_db.py` - Database Inspection Utility
**Purpose:** Simple utility for database content verification and summary statistics.

**Features:**
- Measurement and event count reporting
- Data span and PMU coverage analysis
- Recent data sample display
- Database health verification

#### `requirements.txt` - Dependency Management
**Purpose:** Python package requirements for ML and data analysis capabilities.

**Dependencies:**
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing and array operations
- **scikit-learn**: Machine learning algorithms and models
- **matplotlib**: Data visualization capabilities

## 🚀 Installation & Setup

### **Prerequisites**
```bash
# Install ML dependencies
pip install -r requirements.txt

# Verify installation
python3 -c "import pandas, numpy, sklearn, matplotlib; print('✓ All dependencies ready')"
```

### **System Verification**
```bash
# Check configuration
python3 run_test.py config

# Quick system test
python3 run_test.py single 10
```

## 🎮 Usage Instructions

### **Demonstration Modes**

#### **Full System Demo**
```bash
# Complete demo with all PMUs and ML analysis
python3 run_test.py demo [duration_seconds]

# Features:
# - All 4 PMUs transmitting simultaneously
# - Real-time ML analysis every 30 seconds
# - Comprehensive database storage
# - Event simulation and detection
```

#### **Single PMU Analysis**
```bash
# Focused single PMU testing with detailed analysis
python3 run_test.py single [duration_seconds]

# Features:
# - Detailed frame visualization
# - More frequent ML analysis
# - In-depth performance monitoring
# - Enhanced debugging output
```

#### **Configuration Display**
```bash
# Display system configuration
python3 run_test.py config

# Shows:
# - Network topology
# - PMU-PDC mappings
# - Port assignments
# - System parameters
```

### **Manual Component Operation**

#### **Direct Server Operation**
```bash
# Start PDC server independently
python3 server.py

# Features:
# - Real-time frame processing
# - Live ML analysis and visualization
# - Database storage
# - Performance monitoring
```

#### **Direct Client Operation**
```bash
# Start specific PMU client
python3 client.py [pmu_name] [duration]

# Examples:
python3 client.py pmu_34 60
python3 client.py pmu_31 120

# Features:
# - Realistic power system simulation
# - Event generation and modeling
# - IEEE frame transmission
# - Performance metrics
```

#### **Standalone ML Analysis**
```bash
# Analyze stored data
python3 analyzer.py [hours_back]

# Examples:
python3 analyzer.py 1    # Last hour
python3 analyzer.py 0.5  # Last 30 minutes
python3 analyzer.py 24   # Last day

# Provides:
# - Frequency stability analysis
# - Voltage profile assessment
# - Power quality evaluation
# - Event prediction
```

#### **Database Inspection**
```bash
# Quick database summary
python3 check_db.py

# Advanced database queries
sqlite3 synchrophasor_data.db
```

## 📊 Data Analysis Capabilities

### **Real-Time Analysis**
- **Frame-by-Frame Processing**: Complete IEEE data extraction and validation
- **Live Anomaly Detection**: Immediate identification of system irregularities
- **Performance Monitoring**: Communication delays, frame rates, data quality
- **Event Classification**: Automatic categorization of power system events

### **Historical Analysis**
- **Trend Analysis**: Long-term system behavior patterns
- **Statistical Modeling**: Frequency and voltage stability metrics
- **Predictive Analytics**: Future event probability assessment
- **Quality Assessment**: Overall power system health scoring

### **Machine Learning Models**

#### **Anomaly Detection**
- **Algorithm**: Isolation Forest with configurable contamination levels
- **Features**: Frequency deviation, voltage unbalance, communication metrics
- **Output**: Anomaly scores, risk classifications, operational recommendations

#### **System Clustering**
- **Algorithm**: DBSCAN for density-based state identification
- **Applications**: Operating mode classification, system state analysis
- **States**: Normal operation, emergency conditions, restoration phases

#### **Risk Assessment**
- **Multi-factor Analysis**: Frequency, voltage, communication, and operational metrics
- **Scoring System**: Numerical risk levels with automated thresholds
- **Recommendations**: Actionable guidance for system operators

## 🔬 Implementation Details

### **Power System Simulation**

#### **Voltage and Current Generation**
- Three-phase balanced/unbalanced voltage generation
- Load-dependent current calculation with realistic power factors
- Phase angle relationships and system impedance modeling
- Equipment behavior simulation (transformers, lines, loads)

#### **Frequency Modeling**
- Base frequency with natural oscillations and random walk
- Grid inertia simulation and frequency response characteristics
- Generator and load impact on system frequency
- ROCOF calculation for stability analysis

#### **Event Simulation**
- **Frequency Events**: Generator trips, load rejection, interconnection issues
- **Voltage Events**: Transmission faults, voltage regulation problems
- **Load Events**: Motor starting, load switching, demand variations
- **Protection Events**: Circuit breaker operations, relay actions

### **Database Design**

#### **Measurements Table Structure**
- **Temporal Data**: High-resolution timestamps for trend analysis
- **Phasor Data**: Magnitude and angle for all voltage and current measurements
- **Frequency Data**: Instantaneous frequency and rate of change
- **Operational Data**: Analog measurements, digital status, communication metrics

#### **Events Table Structure**
- **Event Classification**: Type, severity, and description fields
- **ML Integration**: Prediction confidence and model outputs
- **Correlation**: Links to measurement data for root cause analysis

### **Communication Architecture**

#### **Network Design**
- **Local Testing**: Localhost with port-based PMU differentiation
- **Production Ready**: Configurable IP addresses and network topologies
- **Protocol Compliance**: Full IEEE C37.118.2 implementation
- **Error Handling**: Robust communication with automatic recovery

#### **Data Flow**
1. **PMU Simulation**: Generate realistic measurements
2. **IEEE Encoding**: Format data according to standard
3. **Network Transmission**: UDP-based high-speed delivery
4. **PDC Processing**: Frame parsing and validation
5. **Database Storage**: Persistent data storage
6. **ML Analysis**: Real-time and batch processing
7. **Reporting**: Automated analysis and recommendations

## 🏗️ System Architecture Benefits

### **Scalability**
- **Multi-PMU Support**: Easily expandable to hundreds of PMUs
- **Database Performance**: Optimized for large-scale data storage
- **ML Processing**: Efficient algorithms for real-time analysis
- **Network Architecture**: Designed for wide-area monitoring

### **Flexibility**
- **Configurable Parameters**: Adjustable simulation and analysis settings
- **Modular Design**: Independent components for custom deployments
- **Multiple Deployment Modes**: Lab testing and production operation
- **Extensible Framework**: Easy integration of new features and models

### **Reliability**
- **Error Handling**: Comprehensive exception management
- **Data Validation**: Multiple levels of data integrity checking
- **Graceful Degradation**: System continues operation during component failures
- **Recovery Mechanisms**: Automatic restart and state restoration

## 🔧 Troubleshooting & Maintenance

### **Common Issues**
- **Dependency Problems**: Use requirements.txt for consistent package versions
- **Network Configuration**: Verify port availability and network settings
- **Database Issues**: Check file permissions and disk space
- **Performance Problems**: Monitor system resources and adjust parameters

### **Maintenance Tasks**
- **Database Cleanup**: Periodic removal of old data for storage management
- **Configuration Updates**: Adjustment of thresholds and parameters
- **Model Retraining**: Update ML models with new data patterns
- **Performance Optimization**: Monitor and tune system performance

## 🚀 Future Development Opportunities

### **Enhanced Visualization**
- Real-time plotting and dashboard development
- Geographic information system (GIS) integration
- Web-based monitoring interfaces
- Mobile application development

### **Advanced Analytics**
- Deep learning models for complex pattern recognition
- Time series forecasting for predictive maintenance
- Correlation analysis across multiple grid locations
- Integration with weather and market data

### **Integration Capabilities**
- SCADA system connectivity
- Energy management system integration
- Protection system coordination
- Market operation interfaces

### **Deployment Options**
- Cloud-based processing and storage
- Edge computing for local analysis
- Hybrid architectures for scalability
- Industrial IoT platform integration

## 📞 Support & Documentation

### **Getting Help**
- **Code Documentation**: Comprehensive inline comments and docstrings
- **Configuration Guide**: Detailed setup and configuration instructions
- **Troubleshooting Guide**: Common issues and solutions
- **API Reference**: Function and class documentation

### **Contributing**
- **Code Standards**: Python PEP 8 compliance and documentation requirements
- **Testing**: Comprehensive test coverage for new features
- **Documentation**: Update documentation for all changes
- **Performance**: Benchmark new features for scalability impact

This system represents a complete transformation from basic communication testing to an intelligent, production-ready power grid monitoring platform with advanced analytics and machine learning capabilities. 