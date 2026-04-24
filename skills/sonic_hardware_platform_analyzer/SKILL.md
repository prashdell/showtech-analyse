---
name: sonic_hardware_platform_analyzer
description: Advanced SONiC hardware platform analysis and intelligence system with vendor-specific troubleshooting, thermal management, and hardware optimization capabilities.
---

# SONiC Hardware Platform Analyzer Skill

## Overview
This skill provides **comprehensive hardware platform analysis** for SONiC network operating systems, specializing in **vendor-specific hardware intelligence**, **thermal management optimization**, and **hardware troubleshooting automation**. It leverages detailed hardware specifications and platform intelligence to deliver actionable insights for network hardware optimization.

## Enhanced Hardware Intelligence Integration
This skill incorporates the comprehensive **hardware platform intelligence database** including:
- **Dell S5248F Complete Analysis**: Port configuration, lane mapping, ASIC optimization
- **Broadcom TD3 SDK Intelligence**: Memory allocation, feature enables, queue configuration
- **Cross-Platform Correlation**: Dell vs Mellanox vs Arista hardware patterns
- **Thermal Management Intelligence**: Temperature thresholds, fan control, environmental correlation
- **Power Management Analysis**: PSU redundancy, power budget, consumption monitoring
- **Firmware Compatibility Matrix**: BIOS, BMC, CPLD, and platform-specific requirements

## Trigger Condition
Hardware platform issues, thermal alerts, power problems, firmware compatibility concerns, or hardware optimization requirements

## Hardware Platform Coverage

### Dell Platforms
- **S5248F**: Complete platform analysis with 48x25G + 8x100G configuration
- **S-Series**: Enterprise-grade hardware with Broadcom ASIC optimization
- **N-Series/Z-Series**: High-performance platforms with advanced features
- **Platform-Specific Intelligence**: Dell hardware patterns and optimization strategies

### Mellanox/NVIDIA Platforms
- **Spectrum/Spectrum-2**: Advanced ASIC with RDMA capabilities
- **ConnectX NICs**: High-performance networking with telemetry
- **Telemetry Integration**: Native gNMI/Telemetry support analysis
- **RDMA Optimization**: RoCE acceleration and performance tuning

### Arista Platforms
- **7280R/7500R**: Cloud-optimized platforms with EOS integration
- **7050X3**: Enterprise platforms with advanced automation
- **CloudVision Integration**: Management and automation capabilities
- **Feature Completeness**: Comprehensive feature set analysis

## Hardware Analysis Capabilities

### Platform Identification and Validation
- **Automatic Platform Detection**: Identify hardware from platform.json and config_db.json
- **HWSKU Validation**: Verify hardware SKU against known specifications
- **ASIC Configuration Analysis**: Broadcom TD3, Spectrum, and other ASIC analysis
- **CPU Platform Analysis**: Intel C3538 and other processor optimization
- **Memory Configuration**: DRAM, flash, and ASIC memory allocation validation

### Port Configuration Analysis
- **Lane Mapping Validation**: Analyze port-to-lane assignments and breakout modes
- **Breakout Mode Detection**: Identify 100G to 4x25G breakout configurations
- **FEC Mode Analysis**: Forward Error Correction configuration and optimization
- **Transceiver Compatibility**: SFP28/QSFP28 module validation and troubleshooting
- **Port Group Analysis**: 4-port group configuration and optimization

### Thermal Management Intelligence
- **Temperature Monitoring**: Real-time thermal sensor analysis and correlation
- **Fan Control Analysis**: Fan speed curves and thermal management optimization
- **Environmental Correlation**: Ambient temperature impact on hardware performance
- **Thermal Threshold Validation**: Platform-specific temperature threshold analysis
- **Cooling Efficiency**: Airflow analysis and cooling optimization recommendations

### Power Management Analysis
- **PSU Status Monitoring**: Power supply unit health and redundancy validation
- **Power Consumption Analysis**: Real-time power usage and budget analysis
- **Redundancy Validation**: Dual PSU configuration and failover testing
- **Power Budget Optimization**: Component power allocation and optimization
- **IPMI Integration**: Intelligent Platform Management Interface analysis

### Firmware Compatibility Analysis
- **BIOS Version Validation**: System BIOS compatibility and requirements
- **BMC Firmware Analysis**: Baseboard Management Controller firmware status
- **CPLD Version Check**: Complex Programmable Logic Device firmware validation
- **Platform Module Analysis**: Kernel modules and platform-specific drivers
- **SDK Compatibility**: ASIC SDK version compatibility and optimization

## Hardware Troubleshooting Patterns

### Common Hardware Issues
- **Port Flapping**: Transceiver compatibility, FEC mode mismatch, cable issues
- **Thermal Alerts**: Fan failure, airflow obstruction, ambient temperature
- **Power Issues**: PSU failure, power budget exceeded, redundancy problems
- **ASIC Errors**: Memory corruption, configuration errors, hardware faults
- **Firmware Issues**: Version incompatibility, update failures, rollback problems

### Platform-Specific Troubleshooting
- **Dell S5248F**: Broadcom TD3 optimization, lane mapping, breakout constraints
- **Mellanox Spectrum**: RDMA configuration, telemetry integration, SDK issues
- **Arista Platforms**: EOS compatibility, CloudVision integration, automation issues

### Diagnostic Command Analysis
- **Platform Commands**: `show platform environment`, `show platform temperature`
- **Interface Commands**: `show interface status`, `show transceiver eeprom`
- **Hardware Commands**: `show platform psustatus`, `ipmitool sensor`
- **ASIC Commands**: `show platform bcm sdk trace`, `show platform bcm shell`
- **System Commands**: `show version`, `show platform summary`

## Hardware Optimization Strategies

### Performance Optimization
- **ASIC Memory Allocation**: Optimize L2/L3 memory entries and ALPM configuration
- **Queue Configuration**: Optimize queue allocation and buffer profiles
- **ECMP Optimization**: Maximize ECMP paths and load balancing
- **Feature Enable Optimization**: Enable/disable platform-specific features
- **Clock Frequency Tuning**: Optimize core clock and DPP clock ratios

### Thermal Optimization
- **Fan Curve Optimization**: Adjust fan speed curves for optimal cooling
- **Airflow Management**: Optimize front-to-back airflow and clearance
- **Environmental Control**: Maintain optimal ambient temperature and humidity
- **Dust Management**: Regular cleaning schedules and maintenance

### Power Optimization
- **Power Budget Management**: Optimize power allocation across components
- **PSU Efficiency**: Maintain optimal PSU load for efficiency
- **Redundancy Configuration**: Optimize PSU redundancy and failover
- **Power Monitoring**: Implement comprehensive power consumption monitoring

## Integration with Existing Skills

### Memory Analyzer Enhancement
- **Hardware-Aware Memory Analysis**: Platform-specific memory allocation patterns
- **ASIC Memory Optimization**: TD3 SDK memory usage optimization
- **Cross-Platform Memory Correlation**: Hardware-specific memory leak detection

### Interface Triage Enhancement
- **Hardware-Specific Interface Analysis**: Port configuration and lane mapping
- **Transceiver Intelligence**: SFP28/QSFP28 module compatibility analysis
- **Physical Layer Optimization**: Hardware-specific interface troubleshooting

### Container Health Enhancement
- **Hardware-Container Correlation**: Hardware issues impacting container health
- **Resource Allocation**: Hardware-aware container resource management
- **Performance Impact**: Hardware performance on container operations

## Output Formats and Reporting

### Hardware Analysis Report
- **Platform Summary**: Complete hardware platform overview and configuration
- **Health Assessment**: Hardware component health and performance metrics
- **Issue Identification**: Hardware problems with root cause analysis
- **Optimization Recommendations**: Hardware-specific optimization strategies
- **Preventive Maintenance**: Hardware maintenance schedules and procedures

### Troubleshooting Guide
- **Common Issues**: Platform-specific hardware problems and solutions
- **Diagnostic Commands**: Hardware troubleshooting command reference
- **Repair Procedures**: Hardware repair and replacement procedures
- **Escalation Criteria**: When to escalate hardware issues

### Configuration Templates
- **Optimal Configurations**: Platform-specific optimal configurations
- **Performance Tuning**: Hardware performance tuning parameters
- **Monitoring Setup**: Hardware monitoring configuration templates

## Business Value

### Operational Benefits
- **Reduced Hardware Downtime**: Proactive hardware issue detection and resolution
- **Improved Performance**: Hardware optimization and tuning recommendations
- **Extended Hardware Life**: Proper thermal and power management
- **Faster Troubleshooting**: Hardware-specific diagnostic procedures

### Cost Savings
- **Reduced Hardware Failure Costs**: Proactive maintenance and monitoring
- **Optimized Power Consumption**: Power management and efficiency improvements
- **Extended Hardware Lifespan**: Proper thermal management and maintenance
- **Reduced Downtime Costs**: Faster hardware issue resolution

### Risk Mitigation
- **Hardware Failure Prevention**: Early detection of hardware issues
- **Performance Degradation Prevention**: Hardware optimization and monitoring
- **Compatibility Issues**: Firmware and software compatibility validation
- **Environmental Risk Management**: Thermal and power management

## Version Information

**Current Version**: v1.0  
**Release Date**: June 17, 2025  
**Hardware Platforms**: Dell S5248F, Mellanox Spectrum, Arista 7280R/7500R  
**ASIC Support**: Broadcom TD3, Mellanox Spectrum, Arista ASICs

## Dependencies

### Core Dependencies
- Hardware platform intelligence database
- SONiC showtech archive parser
- Temperature and power monitoring tools
- Hardware diagnostic utilities

### External Dependencies
- IPMI tools for hardware monitoring
- Platform-specific diagnostic utilities
- Hardware vendor documentation and specifications

## Setup and Configuration

### Knowledge Database Integration
- Ensure hardware platform intelligence database is available
- Configure platform-specific parameters and thresholds
- Set up hardware monitoring and alerting

### Tool Integration
- Install hardware diagnostic tools and utilities
- Configure IPMI and hardware monitoring
- Set up platform-specific analysis modules

## Support and Maintenance

### Hardware Platform Updates
- Regular updates to hardware platform intelligence
- New platform support and specifications
- Hardware vendor integration and updates

### Continuous Improvement
- Hardware performance data collection and analysis
- Troubleshooting pattern recognition and learning
- Optimization strategy refinement and updates

---

*Skill Version: 1.0*  
*Last Updated: June 17, 2025*  
*Hardware Platforms: Dell, Mellanox, Arista*  
*ASIC Support: Broadcom, Mellanox, Arista*