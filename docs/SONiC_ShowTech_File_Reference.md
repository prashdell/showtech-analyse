# SONiC ShowTech File Reference - Complete Guide to Understanding Each File

## Overview

This guide provides comprehensive information about what each file in a SONiC showtech archive is for, its purpose, and how to interpret its contents for troubleshooting and analysis.

## How to Access File Information

### Method 1: Use the File Intelligence Analyzer
```bash
cd "C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse\skills"

# Run file intelligence analysis on your showtech
python .\sonic_file_intelligence_analyzer.py "C:\path\to\your\showtech.tar.gz"
```

### Method 2: Use the Comprehensive Analyzer
```bash
python .\sonic_comprehensive_deep_dive_analyzer.py "C:\path\to\your\showtech.tar.gz"
```

### Method 3: Manual File Reference (Below)
Use this guide as a quick reference for any showtech file you encounter.

---

## Complete SONiC ShowTech File Reference

### **A. Platform and System Information Files**

#### **`version`** or **`show version`**
- **Purpose**: SONiC OS version, build information, kernel version
- **Content**: SONiC version string, build date, kernel version, hardware platform
- **Used For**: Version compatibility checks, bug identification, feature support validation
- **Key Info**: `SONiC-OS-4.5.1-Enterprise_Standard`, kernel version, build timestamp

#### **`platform`** or **`show platform`**
- **Purpose**: Hardware platform identification and capabilities
- **Content**: Platform name, hardware SKU, ASIC type, serial number
- **Used For**: Platform-specific troubleshooting, hardware compatibility
- **Key Info**: `x86_64-dell_s5448f-r0`, product name, ASIC information

#### **`inventory`** or **`show inventory`**
- **Purpose**: Hardware component inventory and status
- **Content**: List of all hardware components with serial numbers and status
- **Used For**: Hardware tracking, warranty information, component replacement
- **Key Info**: Chassis, power supplies, fans, transceivers, ASIC modules

#### **`environment`** or **`show environment`**
- **Purpose**: Environmental monitoring (temperature, voltage, fans)
- **Content**: Temperature readings, voltage levels, fan speeds, PSU status
- **Used For**: Hardware health monitoring, thermal issues, power problems
- **Key Info**: Temperature sensors, fan RPM, PSU status, voltage levels

---

### **B. Interface and Data Plane Files**

#### **`interfaces`** or **`show interfaces`**
- **Purpose**: Interface configuration and operational status
- **Content**: All interfaces with admin/oper status, speed, duplex, MTU
- **Used For**: Interface troubleshooting, link status verification, connectivity issues
- **Key Info**: Interface names, admin/oper status, speed, error counters

#### **`interface counters`** or **`show interfaces counters`**
- **Purpose**: Detailed interface statistics and error counters
- **Content**: Packet/byte counts, error counters, discards, CRC errors
- **Used For**: Performance analysis, error detection, traffic monitoring
- **Key Info**: Rx/Tx packets, bytes, errors, discards, CRC, giants

#### **`lldp`** or **`show lldp`**
- **Purpose**: LLDP neighbor discovery and topology information
- **Content**: Connected devices, port descriptions, capability information
- **Used For**: Network topology mapping, physical connectivity verification
- **Key Info**: Neighbor device names, port IDs, system descriptions

#### **`mac address-table`** or **`show mac address-table`**
- **Purpose**: MAC address table and forwarding database
- **Content**: MAC addresses, VLANs, port associations, aging information
- **Used For**: Layer 2 troubleshooting, MAC learning issues, forwarding verification
- **Key Info**: MAC addresses, VLAN IDs, port numbers, entry types

---

### **C. Routing Protocol Files**

#### **`bgp`** or **`show bgp`**
- **Purpose**: BGP protocol status, neighbor information, routing tables
- **Content**: BGP neighbors, session status, advertised/received routes, AS paths
- **Used For**: BGP troubleshooting, routing policy verification, connectivity issues
- **Key Info**: Neighbor IPs, session state (Established/Active), prefix counts

#### **`ospf`** or **`show ospf`**
- **Purpose**: OSPF protocol status and routing information
- **Content**: OSPF neighbors, areas, LSAs, routing table entries
- **Used For**: OSPF troubleshooting, area configuration, route convergence
- **Key Info**: Router ID, neighbor IPs, area IDs, LSA types

#### **`ip route`** or **`show ip route`**
- **Purpose**: IP routing table and forwarding information
- **Content**: Routing entries, next hops, protocol sources, metric information
- **Used For**: Routing verification, reachability analysis, path troubleshooting
- **Key Info**: Destination networks, next hops, protocols, administrative distance

---

### **D. Container and Service Files**

#### **`docker ps`** or **`docker ps -a`**
- **Purpose**: Docker container status and runtime information
- **Content**: Container names, IDs, status, image information, resource limits
- **Used For**: Service health monitoring, container troubleshooting, resource analysis
- **Key Info**: Container names, status (Up/Down), image names, resource limits

#### **`docker stats`** or **`docker stats --no-stream`**
- **Purpose**: Container resource utilization (CPU, memory, network, I/O)
- **Content**: Real-time resource usage for all running containers
- **Used For**: Performance monitoring, resource exhaustion detection, capacity planning
- **Key Info**: CPU %, memory usage, network I/O, block I/O per container

#### **`docker logs`** or **`docker logs <container>`**
- **Purpose**: Container application logs and service messages
- **Content**: Service-specific logs, error messages, startup/shutdown events
- **Used For**: Service troubleshooting, error analysis, operational monitoring
- **Key Info**: Service logs, error messages, timestamps, service events

#### **`systemctl`** or **`systemctl status`**
- **Purpose**: System service status and systemd information
- **Content**: Service status, startup time, process IDs, dependency information
- **Used For**: Service management, startup troubleshooting, dependency analysis
- **Key Info**: Service names, status (active/inactive), PID, startup time

---

### **E. Process and System Resource Files**

#### **`ps aux`** or **`ps -ef`**
- **Purpose**: Process listing with resource utilization
- **Content**: All running processes, PID, CPU/memory usage, command lines
- **Used For**: Process monitoring, resource analysis, performance troubleshooting
- **Key Info**: Process names, PIDs, CPU %, MEM %, command arguments

#### **`top`** or **`htop`**
- **Purpose**: Real-time system resource monitoring
- **Content**: CPU usage, memory usage, process ranking, system load
- **Used For**: Performance monitoring, resource exhaustion, system health
- **Key Info**: Load average, memory usage, top CPU processes, system uptime

#### **`free -h`** or **`free -m`**
- **Purpose**: System memory utilization and availability
- **Content**: Total, used, free memory, swap usage, cache/buffer information
- **Used For**: Memory analysis, resource planning, exhaustion detection
- **Key Info**: Total/used/free memory, swap usage, cached memory, available memory

#### **`proc/meminfo`**
- **Purpose**: Detailed system memory information
- **Content**: Memory statistics, slab info, page tables, huge pages
- **Used For**: Deep memory analysis, kernel memory troubleshooting
- **Key Info**: MemTotal, MemFree, MemAvailable, Slab, PageTables, HugePages

---

### **F. Configuration Files**

#### **`config_db.json`**
- **Purpose**: SONiC configuration database (running configuration)
- **Content**: All device configuration in JSON format (interfaces, VLANs, BGP, etc.)
- **Used For**: Configuration analysis, change verification, backup/restore
- **Key Info**: Interface config, VLAN config, BGP config, system settings

#### **`running-config`** or **`show running-config`**
- **Purpose**: Current running configuration in CLI format
- **Content**: Complete device configuration in human-readable format
- **Used For**: Configuration review, change validation, documentation
- **Key Info**: Interface settings, routing config, service configuration

#### **`startup-config`** or **`show startup-config`**
- **Purpose**: Startup configuration (boot configuration)
- **Content**: Configuration that will be applied on next reboot
- **Used For**: Configuration consistency, boot troubleshooting, change tracking
- **Key Info**: Saved configuration, boot settings, persistent config

---

### **G. Log and System Message Files**

#### **`syslog`** or **`/var/log/syslog`**
- **Purpose**: System log messages and events
- **Content**: System messages, service logs, error messages, timestamps
- **Used For**: System troubleshooting, event correlation, security analysis
- **Key Info**: Timestamps, service names, error messages, system events

#### **`kern.log`** or **`/var/log/kern.log`**
- **Purpose**: Kernel log messages and events
- **Content**: Kernel messages, driver events, hardware events, panic messages
- **Used For**: Kernel troubleshooting, hardware issues, system crashes
- **Key Info**: Kernel messages, hardware events, panic/crash information

#### **`dmesg`** or **`dmesg -T`**
- **Purpose**: Kernel ring buffer messages
- **Content**: Boot messages, hardware detection, driver messages, OOM events
- **Used For**: Boot troubleshooting, hardware detection, memory issues
- **Key Info**: Boot sequence, hardware detection, OOM killer events, driver messages

#### **`auth.log`** or **`/var/log/auth.log`**
- **Purpose**: Authentication and authorization logs
- **Content**: Login attempts, authentication events, sudo usage, SSH sessions
- **Used For**: Security analysis, access troubleshooting, audit trails
- **Key Info**: Login attempts, authentication success/failure, SSH sessions

---

### **H. Hardware and Diagnostic Files**

#### **`sensors`** or **`sensors-detect`**
- **Purpose**: Hardware sensor readings (temperature, voltage, fans)
- **Content**: Sensor readings, temperature values, voltage levels, fan speeds
- **Used For**: Hardware monitoring, thermal analysis, power supply health
- **Key Info**: Temperature sensors, voltage readings, fan RPMs, alarm status

#### **`ethtool`** or **`ethtool <interface>`**
- **Purpose**: Ethernet interface detailed information and statistics
- **Content**: Link settings, driver information, PHY settings, detailed statistics
- **Used For**: Interface troubleshooting, PHY analysis, driver issues
- **Key Info**: Link speed, duplex, driver version, PHY settings, error counters

#### **`lspci`** or **`lspci -vv`**
- **Purpose**: PCI device enumeration and information
- **Content**: PCI devices, vendor/device IDs, driver information, capabilities
- **Used For**: Hardware inventory, driver troubleshooting, device compatibility
- **Key Info**: PCI devices, vendor IDs, driver names, device capabilities

---

### **I. Core Dump and Crash Files**

#### **`core`** files
- **Purpose**: Memory dump of crashed processes
- **Content**: Process memory image at time of crash
- **Used For**: Crash analysis, debugging, root cause investigation
- **Key Info**: Process name, crash time, memory dump, stack trace

#### **`gcore`** or **`gdb`** output
- **Purpose**: Generated core dumps for debugging
- **Content**: Process memory state, stack traces, debugging information
- **Used For**: Application debugging, crash analysis, memory leak detection
- **Key Info**: Stack traces, memory maps, register state, debugging info

---

### **J. Performance and Monitoring Files**

#### **`perf`** or **`perf stat`**
- **Purpose**: Performance counters and statistics
- **Content**: CPU performance counters, cache statistics, branch prediction
- **Used For**: Performance analysis, optimization, bottleneck identification
- **Key Info**: CPU cycles, instructions, cache hits/misses, branch predictions

#### **`netstat`** or **`ss`**
- **Purpose**: Network statistics and connection information
- **Content**: Network connections, listening sockets, network statistics
- **Used For**: Network troubleshooting, connection analysis, performance monitoring
- **Key Info**: TCP/UDP connections, listening ports, network statistics

#### **`iostat`** or **`vmstat`**
- **Purpose**: I/O and virtual memory statistics
- **Content**: Disk I/O statistics, virtual memory paging, system activity
- **Used For**: Performance monitoring, I/O analysis, memory paging analysis
- **Key Info**: Disk throughput, memory paging, CPU utilization, I/O wait

---

## How to Use This Information

### **1. Quick File Lookup**
- Use this guide to understand any file you encounter in a showtech
- Look up the file name to understand its purpose and key information

### **2. Troubleshooting Workflow**
1. **Start with Overview**: Check `version`, `platform`, `interfaces`
2. **Identify Issues**: Look at relevant logs and error files
3. **Deep Dive**: Use detailed files for specific problem areas
4. **Correlate**: Cross-reference information across multiple files

### **3. Analysis Best Practices**
- **Check timestamps** to correlate events across files
- **Look for error patterns** in log files first
- **Verify configuration** against running state
- **Compare normal vs. problem states** if available

### **4. Common Troubleshooting Paths**

#### **Interface Issues**:
1. `show interfaces` - Check status
2. `show interfaces counters` - Look for errors
3. `lldp` - Verify physical connectivity
4. `ethtool` - Check PHY/driver issues

#### **Routing Issues**:
1. `show ip route` - Verify routing table
2. `show bgp` - Check BGP status
3. `show ospf` - Verify OSPF if applicable
4. Configuration files - Check routing config

#### **Performance Issues**:
1. `top`/`ps` - Check CPU/memory
2. `free -h` - Check memory usage
3. `docker stats` - Check container resources
4. `perf` - Deep performance analysis

#### **Service Issues**:
1. `docker ps` - Check container status
2. `docker logs` - Check service logs
3. `systemctl` - Check service status
4. `syslog` - Check system messages

---

## File Intelligence Tool

For automatic file analysis and intelligence, use the built-in file intelligence analyzer:

```bash
python .\sonic_file_intelligence_analyzer.py "your_showtech.tar.gz"
```

This tool will:
- Automatically categorize all files
- Provide purpose and diagnostic information
- Suggest correlation targets
- Identify escalation priorities
- Generate comprehensive file inventory

---

## Quick Reference Summary

| File Category | Key Files | Primary Purpose |
|---------------|-----------|-----------------|
| **System Info** | `version`, `platform`, `inventory` | Hardware/OS identification |
| **Interfaces** | `interfaces`, `counters`, `lldp` | Network connectivity |
| **Routing** | `bgp`, `ospf`, `ip route` | Routing protocols |
| **Containers** | `docker ps`, `docker stats`, `logs` | Service health |
| **Resources** | `ps`, `top`, `free`, `meminfo` | System resources |
| **Configuration** | `config_db.json`, `running-config` | Device configuration |
| **Logs** | `syslog`, `kern.log`, `dmesg` | Event analysis |
| **Hardware** | `sensors`, `ethtool`, `lspci` | Hardware monitoring |
| **Crash** | `core`, `gdb` output | Crash analysis |
| **Performance** | `perf`, `netstat`, `iostat` | Performance monitoring |

This comprehensive reference should help you understand any file you encounter in a SONiC showtech archive and guide your troubleshooting efforts effectively.