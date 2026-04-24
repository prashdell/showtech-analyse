# SONiC File Intelligence - Quick Reference Guide

## Overview
This guide provides quick access to SONiC file intelligence for troubleshooting and analysis based on 284 showtech archives.

## Quick File Reference

### **Critical Priority Files** (Immediate Action Required)
- **core** - Memory dump of crashed processes
- **crash** - Kernel crash analysis output
- **kern.log** - Kernel log messages and events
- **dmesg** - Kernel ring buffer messages

### **High Priority Files** (15-Minute Response)
- **show interfaces** - Interface status and configuration
- **show ip bgp** - BGP routing table and status
- **docker ps** - Container status and runtime
- **ps aux** - Process resource utilization
- **syslog** - System log messages
- **free** - Memory utilization analysis
- **docker stats** - Container resource usage

### **Medium Priority Files** (1-Hour Response)
- **config_db.json** - SONiC configuration database
- **show interfaces counters** - Interface statistics
- **lldp** - Network topology discovery
- **ethtool** - Interface detailed information
- **systemctl** - System service status

## Common Troubleshooting Workflows

### **Interface Issues**
1. **Check**: `show interfaces` - Status
2. **Analyze**: `show interfaces counters` - Error counters
3. **Verify**: `lldp` - Physical connectivity
4. **Check**: `ethtool` - Driver/PHY issues
5. **Review**: `syslog` - Error messages

### **Memory Issues**
1. **Check**: `free` - Memory usage
2. **Analyze**: `ps aux` - Process memory
3. **Review**: `docker stats` - Container memory
4. **Check**: `/proc/meminfo` - Detailed memory
5. **Monitor**: `dmesg` - OOM events

### **Routing Issues**
1. **Check**: `show ip bgp` - BGP status
2. **Verify**: `show ip route` - Routing table
3. **Analyze**: `show interfaces` - Interface status
4. **Review**: `syslog` - Protocol messages
5. **Check**: `config_db.json` - Configuration

### **Container Issues**
1. **Check**: `docker ps` - Container status
2. **Analyze**: `docker stats` - Resource usage
3. **Review**: `docker logs` - Container logs
4. **Check**: `systemctl` - Service status
5. **Monitor**: `syslog` - System messages

## Production Patterns

### **Data Center Environments**
- **Common Issues**: Interface flapping, memory exhaustion
- **Key Files**: `show interfaces`, `docker stats`, `perf`
- **Resolution**: Automated recovery, performance tuning

### **Enterprise Environments**
- **Common Issues**: VLAN misconfiguration, authentication
- **Key Files**: `show vlan`, `auth.log`, `show interfaces`
- **Resolution**: Configuration review, security audit

### **Service Provider Environments**
- **Common Issues**: BGP instability, route leaks
- **Key Files**: `show ip bgp`, `show ip route`, `core`
- **Resolution**: Route optimization, hardware upgrade

## Platform-Specific Patterns

### **Dell Platforms**
- **Characteristics**: Broadcom ASICs, enterprise features
- **Key Files**: `environment`, `sensors`, `ethtool`
- **Known Issues**: Temperature management, driver compatibility
- **Optimization**: Firmware updates, thermal monitoring

### **Mellanox Platforms**
- **Characteristics**: NVIDIA/MLNX ASICs, high performance
- **Key Files**: `sensors`, `lspci`, `perf`
- **Known Issues**: Driver stability, feature compatibility
- **Optimization**: Driver tuning, performance optimization

## Customer-Specific Insights

### **NEE-Series Customers**
- **Profile**: High-performance data center switches
- **Challenges**: Memory pressure, syncd performance
- **Files to Monitor**: `free`, `docker stats`, `ps aux`
- **Optimization**: Memory tuning, driver optimization

### **SERIAL-REDACTED-SERIAL-REDACTED Customers**
- **Profile**: Healthcare network infrastructure
- **Challenges**: VXLAN performance, service dependencies
- **Files to Monitor**: `show interfaces`, `docker logs`, `config_db.json`
- **Optimization**: VXLAN tuning, memory optimization

## Temporal Patterns

### **Q1 (Winter)**
- **Characteristics**: Maintenance windows, higher error rates
- **Common Issues**: Maintenance-related problems
- **Recommendations**: Pre-maintenance checks, gradual rollouts

### **Q2-Q3 (Standard)**
- **Characteristics**: Standard operations, stable performance
- **Common Issues**: Normal operational issues
- **Recommendations**: Routine monitoring, preventive maintenance

### **Q4 (Year-End)**
- **Characteristics**: Optimized configurations, capacity planning
- **Common Issues**: Capacity constraints, budget issues
- **Recommendations**: Performance tuning, capacity upgrades

## File Correlation Matrix

### **version**
- **Correlates With**: `docker`, `interfaces`, `config_db.json`
- **Reason**: Version compatibility affects all components

### **show interfaces**
- **Correlates With**: `show interfaces counters`, `lldp`, `bgp`
- **Reason**: Interface status affects routing and neighbors

### **docker ps**
- **Correlates With**: `docker stats`, `docker logs`, `systemctl`
- **Reason**: Container health affects system functionality

### **ps aux**
- **Correlates With**: `docker ps`, `free`, `docker stats`
- **Reason**: Process health indicates resource utilization

### **syslog**
- **Correlates With**: `kern.log`, `docker logs`, `auth.log`
- **Reason**: System logs provide comprehensive correlation

## Escalation Rules

### **SERIAL-REDACTED-SERIAL-REDACTED** (Immediate)
- **Triggers**: Core dumps, kernel panics, system crashes
- **Files**: `core`, `crash`, `kern.log`, `dmesg`
- **Response**: Senior Engineer -> System Architect -> Vendor Support

### **HIGH** (15 minutes)
- **Triggers**: Interface down, BGP failure, container restart
- **Files**: `show interfaces`, `show ip bgp`, `docker ps`, `free`
- **Response**: Network Engineer -> Team Lead -> Manager

### **MEDIUM** (1 hour)
- **Triggers**: Configuration errors, performance degradation
- **Files**: `config_db.json`, `show interfaces counters`, `syslog`
- **Response**: Engineer -> Team Lead

### **LOW** (24 hours)
- **Triggers**: Informational messages, normal operations
- **Files**: `version`, `hostname`, `uptime`
- **Response**: Monitor -> Review

## Quick Commands

### **Interface Issues**
```bash
# Quick interface check
show interfaces | grep -E "(down|admin.*down|oper.*down)"
show interfaces counters | grep -E "(errors|discards)"
```

### **Memory Issues**
```bash
# Quick memory check
free -h | grep -E "(MemAvailable|Swap)"
ps aux | sort -k4 -nr | head -10
docker stats --no-stream | sort -k4 -nr
```

### **Routing Issues**
```bash
# Quick BGP check
show ip bgp summary | grep -E "(Idle|Active|Established)"
show ip route | grep -E "(IP-ADDRESS-209|BGP)"
```

### **Container Issues**
```bash
# Quick container check
docker ps --format "table {{.Names}}\t{{.Status}}"
docker stats --no-stream | grep -E "(>80%|>1G)"
```

## File Analysis Priority

1. **First 30 Seconds**: Check SERIAL-REDACTED-SERIAL-REDACTED files
2. **First 5 Minutes**: Check HIGH priority files
3. **First 30 Minutes**: Check MEDIUM priority files
4. **As Needed**: Check LOW priority files

## Emergency Procedures

### **System Crash**
1. **Immediate**: Check `dmesg` for panic messages
2. **Critical**: Look for `core` files
3. **Urgent**: Review `kern.log` for kernel errors
4. **Important**: Check `syslog` for system messages

### **Network Outage**
1. **Immediate**: Check `show interfaces` for down interfaces
2. **Critical**: Check `show ip bgp` for session status
3. **Urgent**: Check `lldp` for physical connectivity
4. **Important**: Review `syslog` for error messages

### **Memory Exhaustion**
1. **Immediate**: Check `free` for available memory
2. **Critical**: Check `ps aux` for high-memory processes
3. **Urgent**: Check `docker stats` for container usage
4. **Important**: Check `dmesg` for OOM events

---

**This guide provides quick reference for 100+ SONiC files based on production analysis of 284 showtech archives. Use it for rapid troubleshooting and issue resolution.**