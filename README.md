# 🚀 SONiC ShowTech Analysis System

A comprehensive technical analysis platform for SONiC (Software for Open Networking in the Cloud) network devices, featuring deep-dive analysis capabilities and automated reporting systems.

## 📊 **Project Overview**

This repository contains a sophisticated showtech analysis system designed to extract, analyze, and report on SONiC network device operational data. The system provides both executive-level summaries and detailed technical insights for network engineers.

## 🔍 **Key Features**

### **Comprehensive Analysis Capabilities**
- **24 Specialized Analysis Skills** covering all aspects of SONiC operations
- **Deep Technical Analysis** with actual extracted data from showtech archives
- **Executive Intelligence** with business impact assessments
- **Automated Reporting** with configurable output formats

### **Technical Analysis Components**
- **Hardware Performance Analysis** (CPU, Memory, Temperature, Power)
- **Network Interface Analysis** (Counters, Errors, Utilization)
- **BGP Routing Analysis** (Neighbors, Routes, Performance)
- **Service Health Monitoring** (Containers, Processes, Uptime)
- **ARP Table Analysis** (Topology Mapping, MAC Address Tracking)
- **Configuration Analysis** (CONFIG_DB.json, Interface Settings)

### **Analysis Modes**
- **Standard Analysis**: Comprehensive technical review
- **Escalation Czar**: Executive-level intelligence with business impact
- **Comprehensive Mode**: Combined technical and executive analysis

## 📁 **Project Structure**

```
showtech-analyse/
├── 📋 Analysis Reports/
│   ├── NEE-13019_technical_analysis_report.md
│   └── NEE-13019_comprehensive_technical_analysis.md
├── 🤖 Analysis Engine/
│   ├── sonic_analyzer.py (Main analysis orchestrator)
│   ├── enhanced_analyzer.py (Advanced analysis capabilities)
│   └── comprehensive_skill_analysis.py
├── 📚 Documentation/
│   ├── SONiC_ShowTech_Analysis_Guide.md
│   ├── SONiC_Auto_Analysis_Guide.md
│   └── docs/ (Detailed technical documentation)
├── 🔧 Skills & Components/
│   ├── .devin/skills/ (24 specialized analysis skills)
│   └── data/ (Configuration and knowledge bases)
└── 📦 Archive Processing/
    ├── extracted_enbd_archives/ (Processed showtech data)
    └── archive_scrubbing_workspace/ (Data sanitization)
```

## 🎯 **Recent Analysis: NEE-13019 Case Study**

### **Device Information**
- **Customer**: National Polite
- **Device**: TRFOLS5304 (Dell S4348T)
- **Platform**: SONiC 4.5.1
- **Analysis Date**: December 19, 2024

### **Key Technical Findings**
- **System Health**: 85/100 overall score
- **Interface Status**: 16/54 interfaces showing NO-LINK state
- **BGP Performance**: 8/8 neighbors established, ~1,792 EVPN routes
- **Hardware Metrics**: 144W power consumption, 38% memory utilization
- **Error Rates**: 0.00% across all interfaces

### **Critical Insights**
- **High Traffic Interface**: Eth1/50 handling 15.3B packets (41% utilization)
- **Physical Layer Issues**: AMPS_LOCK/AM_LOCK failures on multiple interfaces
- **ARP Topology**: 80 active entries with detailed MAC address mapping
- **Container Health**: 5/5 services operational with 99.9% uptime

## 🛠️ **Usage Instructions**

### **Basic Analysis**
```bash
python sonic_analyzer.py archive.tar.gz
```

### **Comprehensive Analysis**
```bash
python sonic_analyzer.py --comprehensive archive.tar.gz
```

### **Escalation Czar Analysis**
```bash
python sonic_analyzer.py --escalation-czar archive.tar.gz
```

### **Force All Skills**
```bash
python sonic_analyzer.py --force-all-skills archive.tar.gz
```

## 📈 **Analysis Capabilities**

### **Hardware Analysis**
- **CPU Performance**: Multi-core utilization and thermal monitoring
- **Memory Management**: RAM usage, swap activity, and cache analysis
- **Power Systems**: PSU efficiency, load distribution, and redundancy
- **Cooling Systems**: Fan speeds, temperature gradients, and airflow

### **Network Analysis**
- **Interface Counters**: Packet counts, error rates, and utilization
- **Port Channel Analysis**: LACP bundles and load balancing
- **BGP Routing**: Neighbor states, route tables, and performance
- **ARP Topology**: Network mapping and MAC address tracking

### **Service Analysis**
- **Container Health**: Docker service status and resource usage
- **Process Monitoring**: System processes and resource consumption
- **Service Dependencies**: Inter-service relationships and health
- **Configuration Analysis**: CONFIG_DB.json and interface settings

## 🔧 **Technical Architecture**

### **Analysis Engine**
- **Python-based** with modular skill architecture
- **Multi-threaded** processing for performance
- **Extensible** skill system for custom analysis
- **Automated** knowledge integration and updates

### **Data Processing**
- **Archive Extraction**: Automated showtech archive processing
- **Data Sanitization**: PII removal and security compliance
- **Knowledge Integration**: Automatic learning from analysis results
- **Report Generation**: Multiple output formats and customization

### **Skill System**
- **24 Specialized Skills** covering all SONiC components
- **Automatic Discovery** of available analysis capabilities
- **Knowledge Sharing** between analysis components
- **Continuous Learning** from analysis results

## 📊 **Sample Analysis Output**

### **Executive Summary**
```
SYSTEM HEALTH: 85/100 ✅
- Interface Health: 70/100 (16/54 interfaces down)
- BGP Health: 100/100 (8/8 neighbors established)
- Memory Health: 95/100 (38% utilization, healthy)
- Error Health: 100/100 (Zero errors)
- Service Health: 100/100 (All services running)
```

### **Technical Metrics**
```
Hardware Performance:
- CPU: Intel Atom C3558R @ 2.40GHz (4 cores)
- Memory: 15.3 GB total, 38% utilized
- Power: 144W consumption (19% of capacity)
- Temperature: 35-49°C (Normal operating range)

Network Performance:
- Total Traffic: 25.3 TB processed
- Error Rate: 0.00% (Zero errors)
- BGP Routes: ~1,792 EVPN routes
- ARP Entries: 80 active mappings
```

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.8+ with required dependencies
- SONiC showtech archive files
- Sufficient disk space for archive processing

### **Installation**
1. Clone this repository
2. Install Python dependencies
3. Configure analysis parameters
4. Run analysis on your showtech archives

### **Configuration**
- Edit `.devin/config.json` for analysis settings
- Customize skill parameters in `.devin/skills/`
- Configure output formats and reporting options

## 📚 **Documentation**

### **Technical Guides**
- [SONiC ShowTech Analysis Guide](docs/SONiC_ShowTech_Analysis_Guide.md)
- [Auto Analysis Guide](docs/SONiC_Auto_Analysis_Guide.md)
- [Complete Skills Documentation](docs/COMPLETE_SKILLS_DOCUMENTATION_V6.md)

### **API Reference**
- [Skill Invocation Best Practices](SKILL_INVOCATION_BEST_PRACTICES.md)
- [Hardware Platform Analysis](HARDWARE_PLATFORM_ANALYSIS_LEARNINGS.md)
- [Master Documentation](MASTER_DOCUMENTATION.md)

## 🤝 **Contributing**

This project is actively developed with continuous improvements:
- **Automated Knowledge Integration**: Learning from each analysis
- **Skill Enhancement**: Expanding analysis capabilities
- **Performance Optimization**: Improving analysis speed and accuracy
- **Documentation Updates**: Maintaining comprehensive guides

## 📄 **License**

This project is proprietary to Dell Technologies and contains confidential analysis methodologies and technical insights.

## 🔗 **Repository Information**

- **Repository**: https://github.com/prashdell/showtech-analyse
- **Created**: April 24, 2026
- **Last Updated**: Continuous development
- **Analysis Reports**: NEE-13019 comprehensive technical analysis
- **Skills Count**: 24 specialized analysis capabilities

---

**Note**: This system is designed for professional network analysis and requires understanding of SONiC architecture and network operations. The analysis reports contain sensitive technical data and should be handled according to your organization's security policies.