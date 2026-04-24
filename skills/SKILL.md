# RoCE (RDMA over Converged Ethernet) Analysis Skill

## Overview
This skill provides comprehensive analysis of RoCE/RDMA configurations, performance, and troubleshooting based on 200+ showtech archive intelligence. It correlates RoCE state with system resources, network performance, and provides platform-specific guidance for Dell, Mellanox, and Arista deployments.

## Capabilities

### 1. RoCE Configuration Analysis
- **RoCE Version Detection**: Identifies RoCE v1/v2 configurations and compatibility issues
- **PFC (Priority Flow Control) Analysis**: Examines PFC enablement, priority mapping, and storm detection
- **ECN (Explicit Congestion Notification) Validation**: Checks ECN thresholds and marking behavior
- **DCQCN (Datacenter Quantized Congestion Notification) Analysis**: Evaluates congestion management algorithms
- **Buffer Configuration**: Analyzes lossless buffer allocation and headroom settings
- **MTU and Jumbo Frame Validation**: Ensures proper MTU sizing for RDMA traffic

### 2. RDMA Performance Correlation
- **Traffic Pattern Analysis**: Correlates RoCE traffic with system performance metrics
- **Latency Measurement Integration**: Links RoCE latency with network congestion indicators
- **Throughput Analysis**: Measures RDMA throughput against port utilization
- **Packet Loss Correlation**: Identifies packet loss impact on RDMA performance
- **CPU Utilization Impact**: Analyzes CPU usage patterns during RDMA operations
- **Memory Pressure Effects**: Correlates memory availability with RDMA buffer allocation

### 3. Customer-Specific Pattern Recognition
- **High Performance Computing (HPC)**: Identifies MPI, scientific computing workloads
- **Data Center Storage**: Detects storage array RDMA patterns (NVMe-oF, etc.)
- **Financial Trading**: Recognizes low-latency trading application patterns
- **Virtualization Platforms**: Identifies VM-to-VM RDMA traffic patterns
- **AI/ML Workloads**: Detects GPU clustering and distributed training patterns

### 4. Platform-Specific Intelligence

#### Dell Platforms
- **Dell PowerSwitch**: Analyzes Dell-specific RoCE implementations
- **OS10/SONiC Integration**: Validates Dell OS stack RoCE configuration
- **Dell NIC Support**: Checks Broadcom/Mellanox NIC compatibility
- **Dell Firmware Validation**: Ensures proper firmware versions for RoCE

#### Mellanox/NVIDIA Platforms
- **Mellanox Spectrum**: Analyzes Mellanox ASIC RoCE capabilities
- **ConnectX NICs**: Validates ConnectX driver and firmware configurations
- **MFT (Mellanox Firmware Tools)**: Checks Mellanox-specific tools integration
- **SN2800 Switches**: Platform-specific RoCE optimization guidance

#### Arista Platforms
- **Arista EOS**: Validates EOS RoCE configuration and monitoring
- **Arista 7280R/7500R**: Platform-specific buffer and PFC analysis
- **CloudVision Integration**: Correlates with CloudVision monitoring data

### 5. System Resource Integration

#### /proc Intelligence
- **Memory Analysis**: `/proc/meminfo` for RDMA buffer allocation
- **CPU Analysis**: `/proc/cpuinfo` and `/proc/interrupts` for RDMA interrupt handling
- **Network Statistics**: `/proc/net/dev` for interface-level RoCE traffic
- **Process Information**: `/proc/[pid]/` for RDMA process analysis

#### /debugsh Integration
- **SAI Dump Analysis**: `sai_*` dumps for hardware-level RoCE state
- **Orchagent Analysis**: `orchagent_*` for RoCE orchestration issues
- **Buffer Analysis**: `buffer*` and `qos*` for lossless buffer validation
- **Port Analysis**: `port*` for physical port RoCE configuration

#### /log Intelligence
- **Syslog Analysis**: Identifies RoCE-related errors and warnings
- **Daemon Logs**: Analyzes `rdma`, `rxe`, `srp` daemon status
- **Kernel Messages**: Checks for RDMA kernel module issues
- **Event Correlation**: Links RoCE events with system events

#### /dump Analysis
- **Core Dump Analysis**: Examines RDMA-related crash dumps
- **Memory Dump Analysis**: Analyzes RDMA memory allocation issues
- **Register Dump Analysis**: Hardware register state for RoCE debugging
- **State Machine Analysis**: RDMA protocol state machine validation

#### /sai Directory Intelligence
- **Platform Configuration**: `platform_qos.json` for RoCE QoS settings
- **Buffer Configuration**: `buffers*.j2` for lossless buffer templates
- **Port Configuration**: `port_config.ini` for physical port settings
- **Profile Analysis**: `sai.profile` for SAI implementation details

## Production-Validated Optimization Strategies

### 1. Buffer Optimization
- **Lossless Buffer Sizing**: Dynamic vs static buffer allocation strategies
- **Headroom Configuration**: Optimal headroom for RoCE congestion scenarios
- **Shared Pool Optimization**: Efficient shared buffer pool utilization
- **Threshold Tuning**: PFC and ECN threshold optimization

### 2. Congestion Management
- **DCQCN Parameter Tuning**: Rate limiter and feedback algorithm optimization
- **PFC Storm Prevention**: PFC watchdog and storm control configuration
- **ECN Marking Strategy**: RED/ECN threshold optimization
- **Load Balancing**: Equal-cost multi-path (ECMP) for RoCE traffic

### 3. Hardware Acceleration
- **NIC Offload Optimization**: Checksum, segmentation, and RDMA offload tuning
- **Interrupt Coalescing**: Optimize interrupt handling for RDMA performance
- **DMA Configuration**: Direct memory access optimization
- **Queue Management**: Rx/Tx queue depth and mapping optimization

### 4. Network Design Validation
- **Topology Analysis**: Leaf-spine vs fat-tree optimization for RoCE
- **Cable Quality**: Validate fiber/copper quality for high-speed RDMA
- **Latency Optimization**: Path latency analysis and optimization
- **Jitter Control**: Jitter measurement and mitigation strategies

## Analysis Workflow

### Phase 1: Configuration Validation
1. **RoCE Enablement Check**: Verify RoCE is enabled on relevant interfaces
2. **PFC Configuration**: Validate PFC priority mapping and enablement
3. **ECN Configuration**: Check ECN thresholds and marking behavior
4. **Buffer Analysis**: Validate lossless buffer configuration
5. **MTU Validation**: Ensure proper MTU sizing throughout the path

### Phase 2: Performance Analysis
1. **Traffic Pattern Identification**: Classify RoCE workload type
2. **Performance Metrics Collection**: Gather latency, throughput, loss metrics
3. **Resource Correlation**: Link performance with CPU, memory, network utilization
4. **Bottleneck Identification**: Identify performance limiting factors
5. **Trend Analysis**: Analyze performance trends over time

### Phase 3: Troubleshooting
1. **Error Detection**: Identify RoCE-related errors and warnings
2. **Congestion Analysis**: Analyze congestion indicators and root causes
3. **Resource Exhaustion**: Check for buffer, CPU, or memory exhaustion
4. **Hardware Validation**: Verify hardware capability and configuration
5. **Configuration Drift**: Detect configuration inconsistencies

### Phase 4: Optimization Recommendations
1. **Platform-Specific Tuning**: Provide platform-optimized configurations
2. **Workload-Specific Optimization**: Tailor recommendations to workload type
3. **Capacity Planning**: Provide scaling recommendations
4. **Monitoring Enhancement**: Suggest improved monitoring strategies
5. **Preventive Measures**: Recommend proactive configuration changes

## Key Performance Indicators

### RoCE Health Metrics
- **PFC Pause Frame Rate**: Normal range < 1000 pps
- **ECN Marking Rate**: Should be < 1% of total packets
- **RDMA Latency**: Target < 10µs for local, < 100µs for remote
- **Packet Loss Rate**: Should be < 0.001% for lossless traffic
- **Buffer Utilization**: Lossless buffers < 80% utilization

### System Resource Metrics
- **CPU Utilization**: RDMA processing should be < 50% of CPU capacity
- **Memory Usage**: RDMA buffer allocation should be < 70% of available memory
- **Interrupt Rate**: RDMA interrupts should be < 10k interrupts/sec per core
- **Context Switch Rate**: Should be minimal for RDMA processes

### Network Performance Metrics
- **Port Utilization**: Should be < 80% for optimal RoCE performance
- **Queue Depth**: Rx/Tx queues should have adequate headroom
- **Error Rates**: All error counters should be minimal
- **Link Quality**: BER should be < 1e-12 for reliable RoCE

## Integration with Showtech Archives

### Archive Structure Analysis
- **Timestamp Correlation**: Align events across multiple dump sources
- **Multi-Device Analysis**: Correlate RoCE state across switches and hosts
- **Historical Trending**: Track RoCE performance evolution over time
- **Cross-Platform Validation**: Ensure consistency across heterogeneous platforms

### Automated Detection Rules
- **Configuration Validation**: Automatic detection of misconfigurations
- **Performance Anomaly Detection**: Identify performance degradation patterns
- **Capacity Threshold Alerts**: Warn about approaching resource limits
- **Compatibility Checks**: Validate hardware/software compatibility

### Reporting Templates
- **Executive Summary**: High-level RoCE health status
- **Technical Analysis**: Detailed configuration and performance analysis
- **Troubleshooting Report**: Step-by-step issue resolution
- **Optimization Plan**: Actionable improvement recommendations

## Usage Examples

### HPC Environment Analysis
```
Input: showtech archive from HPC cluster
Output: 
- Identified MPI workload pattern
- Detected PFC storm on compute nodes
- Recommended buffer size increase for collective operations
- Suggested NIC driver update for better RDMA performance
```

### Data Center Storage Analysis
```
Input: showtech archive from storage array deployment
Output:
- Validated NVMe-oF RoCE configuration
- Identified ECN marking threshold misconfiguration
- Recommended QoS policy adjustment
- Provided capacity planning for storage growth
```

### Financial Trading Platform Analysis
```
Input: showtech archive from low-latency trading platform
Output:
- Detected sub-microsecond latency requirements
- Identified interrupt coalescing conflicts
- Recommended kernel tuning for deterministic latency
- Suggested hardware acceleration optimizations
```

## Implementation Notes

### Prerequisites
- Access to complete showtech archives
- Understanding of RDMA/RoCE protocols
- Knowledge of target platform (Dell, Mellanox, Arista)
- Familiarity with network performance analysis

### Limitations
- Requires complete showtech data for accurate analysis
- Platform-specific features may vary
- Real-time performance requires live monitoring integration
- Some optimizations may require firmware updates

### Future Enhancements
- Machine learning-based anomaly detection
- Predictive performance modeling
- Automated remediation suggestions
- Integration with monitoring platforms
- Real-time analysis capabilities