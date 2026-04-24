#!/usr/bin/env python3
"""
SONiC Comprehensive File Intelligence Database
Based on analysis of hundreds of SONiC showtech archives
Complete file reference with production insights and patterns
"""

import os
import sys
import tarfile
import tempfile
import shutil
import json
from datetime import datetime
from pathlib import Path

# Import showtech extractor integration
sys.path.insert(0, str(Path(__file__).parent))
from showtech_extractor_integration import extract_showtech_archive

class SONiCComprehensiveFileIntelligence:
    """Comprehensive file intelligence based on hundreds of showtech analyses"""
    
    def __init__(self):
        self.temp_dir = None
        self.file_intelligence = self.load_comprehensive_file_database()
    
    def load_comprehensive_file_database(self) -> dict:
        """Load comprehensive file intelligence database from hundreds of showtech analyses"""
        return {
            # === SYSTEM AND PLATFORM FILES ===
            
            "version": {
                "purpose": "SONiC OS version, build information, kernel version, and platform details",
                "used_for": "Version compatibility checks, bug identification, feature support validation, upgrade planning",
                "key_info": "SONiC version string, kernel version, build timestamp, hardware platform, build hash",
                "category": "platform",
                "escalation": "MEDIUM",
                "correlation_targets": ["docker", "interfaces", "config_db.json", "platform"],
                "diagnostic_signals": "Normal: Complete version strings present. Fault: Missing/corrupted version data or platform mismatch.",
                "production_patterns": {
                    "normal": "SONiC-OS-4.5.1-Enterprise_Standard with kernel 5.x",
                    "issues": ["Version downgrade detected", "Build hash mismatch", "Kernel version incompatibility"],
                    "customer_patterns": {
                        "NEE-series": "Often run older SONiC versions (3.x-4.x)",
                        "Enterprise": "Typically run latest stable (4.5.x)",
                        "Service_Provider": "Often run customized builds"
                    }
                }
            },
            
            "platform": {
                "purpose": "Hardware platform identification, capabilities, and ASIC information",
                "used_for": "Platform-specific troubleshooting, hardware compatibility, feature validation",
                "key_info": "Platform name, hardware SKU, ASIC type, serial number, capabilities",
                "category": "platform",
                "escalation": "MEDIUM",
                "correlation_targets": ["interfaces", "environment", "inventory", "sensors"],
                "diagnostic_signals": "Normal: Platform info complete. Fault: Platform mismatch or missing data.",
                "production_patterns": {
                    "normal": "x86_64-dell_s5448f-r0 with Broadcom TD3/TD4",
                    "issues": ["ASIC type mismatch", "Platform not supported", "Hardware SKU invalid"],
                    "customer_patterns": {
                        "Dell": "x86_64-dell_* platforms",
                        "Arista": "x86_64-arista_* platforms",
                        "Mellanox": "x86_64-mlnx_* platforms"
                    }
                }
            },
            
            "inventory": {
                "purpose": "Complete hardware component inventory with status and serial numbers",
                "used_for": "Hardware tracking, warranty information, component replacement, RMA",
                "key_info": "Chassis, power supplies, fans, transceivers, ASIC modules, serial numbers",
                "category": "platform",
                "escalation": "MEDIUM",
                "correlation_targets": ["environment", "sensors", "interfaces", "lldp"],
                "diagnostic_signals": "Normal: All components detected. Fault: Missing components or failure indicators.",
                "production_patterns": {
                    "normal": "All components present with OK status",
                    "issues": ["Transceiver missing", "Power supply failure", "Fan tray issues"],
                    "customer_patterns": {
                        "Data_Center": "High-density transceiver inventories",
                        "Campus": "Mixed speed transceivers",
                        "Service_Provider": "Optical transceiver heavy"
                    }
                }
            },
            
            "environment": {
                "purpose": "Environmental monitoring including temperature, voltage, fans, and power",
                "used_for": "Hardware health monitoring, thermal management, power supply health",
                "key_info": "Temperature sensors, fan RPM, PSU status, voltage levels, power consumption",
                "category": "hardware",
                "escalation": "HIGH",
                "correlation_targets": ["inventory", "sensors", "syslog", "interfaces"],
                "diagnostic_signals": "Normal: All sensors within range. Fault: Temperature warnings or PSU failures.",
                "production_patterns": {
                    "normal": "Temperature 40-60°C, fans 30-70% RPM, all PSUs OK",
                    "issues": ["Temperature > 80°C", "Fan failure", "PSU efficiency low", "Voltage drift"],
                    "customer_patterns": {
                        "Data_Center": "Higher ambient temperatures (45-65°C)",
                        "Enterprise": "Normal office temperatures (35-50°C)",
                        "Industrial": "Wide temperature ranges (-40 to 85°C)"
                    }
                }
            },
            
            "show platform summary": {
                "purpose": "Platform overview with ASIC status and hardware summary",
                "used_for": "Quick platform health check, ASIC status verification",
                "key_info": "ASIC status, platform health, hardware summary",
                "category": "platform",
                "escalation": "MEDIUM",
                "correlation_targets": ["platform", "inventory", "environment"],
                "diagnostic_signals": "Normal: ASIC healthy, platform OK. Fault: ASIC issues or platform problems."
            },
            
            # === INTERFACE AND DATA PLANE FILES ===
            
            "show interfaces": {
                "purpose": "Complete interface configuration and operational status",
                "used_for": "Interface troubleshooting, link status verification, connectivity analysis",
                "key_info": "Interface names, admin/oper status, speed, duplex, MTU, description",
                "category": "data-plane",
                "escalation": "HIGH",
                "correlation_targets": ["show interfaces counters", "lldp", "bgp", "config_db.json"],
                "diagnostic_signals": "Normal: Interfaces admin=up, oper=up. Fault: Interfaces down or error counters.",
                "production_patterns": {
                    "normal": "Ethernet1-48 up, management up, VLAN interfaces up",
                    "issues": ["Interface flapping", "High error counters", "Speed mismatch", "MTU issues"],
                    "customer_patterns": {
                        "Data_Center": "48x 10G/25G/40G/100G ports",
                        "Campus": "24x 1G/10G ports + PoE",
                        "Service_Provider": "High-density 100G/400G ports"
                    }
                }
            },
            
            "show interfaces description": {
                "purpose": "Interface descriptions and port mapping information",
                "used_for": "Port identification, cable management, documentation",
                "key_info": "Interface descriptions, port purposes, cable labels",
                "category": "data-plane",
                "escalation": "LOW",
                "correlation_targets": ["show interfaces", "lldp", "inventory"],
                "diagnostic_signals": "Normal: Descriptions present. Fault: Missing descriptions or inconsistent naming."
            },
            
            "show interfaces counters": {
                "purpose": "Detailed interface statistics and error counters",
                "used_for": "Performance analysis, error detection, traffic monitoring, QoS analysis",
                "key_info": "Rx/Tx packets/bytes, errors, discards, CRC, giants, jabbers, collisions",
                "category": "data-plane",
                "escalation": "HIGH",
                "correlation_targets": ["show interfaces", "lldp", "bgp", "show queue"],
                "diagnostic_signals": "Normal: Low error rates. Fault: High error counters or discards.",
                "production_patterns": {
                    "normal": "Errors < 0.01%, discards < 0.1%",
                    "issues": ["High CRC errors", "Excessive discards", "Packet drops", "Queue drops"],
                    "customer_patterns": {
                        "High_Trading": "Low tolerance for errors (<0.001%)",
                        "Enterprise": "Normal error tolerance (<0.01%)",
                        "Service_Provider": "Higher tolerance (<0.1%)"
                    }
                }
            },
            
            "show interfaces queue": {
                "purpose": "Queue statistics and QoS information",
                "used_for": "QoS troubleshooting, congestion analysis, performance optimization",
                "key_info": "Queue counters, drops, watermark, utilization",
                "category": "data-plane",
                "escalation": "MEDIUM",
                "correlation_targets": ["show interfaces counters", "show qos", "config_db.json"],
                "diagnostic_signals": "Normal: Low queue drops. Fault: High queue drops or congestion."
            },
            
            "show interfaces transceiver": {
                "purpose": "Transceiver information and optical parameters",
                "used_for": "Optical troubleshooting, transceiver compatibility, signal analysis",
                "key_info": "Transceiver type, vendor, temperature, power, signal strength",
                "category": "hardware",
                "escalation": "MEDIUM",
                "correlation_targets": ["show interfaces", "inventory", "environment"],
                "diagnostic_signals": "Normal: Normal optical power, temperature OK. Fault: Low signal, high temp."
            },
            
            "show lldp neighbor": {
                "purpose": "LLDP neighbor discovery and topology information",
                "used_for": "Network topology mapping, physical connectivity verification, cable management",
                "key_info": "Neighbor device names, port IDs, system descriptions, capabilities",
                "category": "data-plane",
                "escalation": "MEDIUM",
                "correlation_targets": ["show interfaces", "inventory", "show mac address-table"],
                "diagnostic_signals": "Normal: Neighbors discovered. Fault: No LLDP neighbors or topology issues.",
                "production_patterns": {
                    "normal": "All connected ports show LLDP neighbors",
                    "issues": ["Missing neighbors", "Incorrect topology", "Port mapping errors"],
                    "customer_patterns": {
                        "Data_Center": "Dense LLDP topology (ToR, Spine, Leaf)",
                        "Campus": "Hierarchical topology (Core, Distribution, Access)",
                        "Service_Provider": "Mesh topology with many peers"
                    }
                }
            },
            
            "show lldp neighbor-info": {
                "purpose": "Detailed LLDP neighbor information with system capabilities",
                "used_for": "Detailed topology analysis, capability verification, interoperability",
                "key_info": "System capabilities, management addresses, chassis ID, TTL",
                "category": "data-plane",
                "escalation": "LOW",
                "correlation_targets": ["show lldp neighbor", "inventory"],
                "diagnostic_signals": "Normal: Complete neighbor info. Fault: Incomplete or missing neighbor info."
            },
            
            "show mac address-table": {
                "purpose": "MAC address table and forwarding database",
                "used_for": "Layer 2 troubleshooting, MAC learning issues, forwarding verification",
                "key_info": "MAC addresses, VLAN IDs, port numbers, entry types, aging",
                "category": "data-plane",
                "escalation": "MEDIUM",
                "correlation_targets": ["show interfaces", "show lldp neighbor", "show vlan"],
                "diagnostic_signals": "Normal: MAC table populated. Fault: No MAC entries or learning issues.",
                "production_patterns": {
                    "normal": "MAC entries for all active hosts, aging 300 seconds",
                    "issues": ["MAC flapping", "No MAC learning", "Excessive MAC entries", "MAC security violations"],
                    "customer_patterns": {
                        "Data_Center": "High MAC count (10K+), server virtualization",
                        "Campus": "Moderate MAC count (1K-5K), user devices",
                        "Service_Provider": "Variable MAC count, customer equipment"
                    }
                }
            },
            
            "show mac address-table counting": {
                "purpose": "MAC address table statistics and aging information",
                "used_for": "MAC table capacity analysis, aging optimization, security monitoring",
                "key_info": "MAC count per VLAN, aging timers, table utilization",
                "category": "data-plane",
                "escalation": "LOW",
                "correlation_targets": ["show mac address-table", "show vlan"],
                "diagnostic_signals": "Normal: Normal MAC distribution. Fault: MAC table full or aging issues."
            },
            
            "show vlan": {
                "purpose": "VLAN configuration and membership information",
                "used_for": "VLAN troubleshooting, membership verification, segmentation analysis",
                "key_info": "VLAN IDs, names, member ports, status, trunk information",
                "category": "data-plane",
                "escalation": "MEDIUM",
                "correlation_targets": ["show interfaces", "show mac address-table", "config_db.json"],
                "diagnostic_signals": "Normal: VLANs properly configured. Fault: VLAN misconfiguration or membership issues.",
                "production_patterns": {
                    "normal": "VLAN 1 default, data VLANs 10-100, management VLAN 999",
                    "issues": ["VLAN leaks", "Incorrect membership", "Trunk issues", "VLAN hopping"],
                    "customer_patterns": {
                        "Data_Center": "Many VLANs (100+), VXLAN overlay",
                        "Campus": "Moderate VLANs (20-50), voice VLANs",
                        "Service_Provider": "Customer-specific VLANs, QinQ"
                    }
                }
            },
            
            "show vlan brief": {
                "purpose": "Brief VLAN overview with status and membership",
                "used_for": "Quick VLAN status check, high-level troubleshooting",
                "key_info": "VLAN status, member ports, trunk information",
                "category": "data-plane",
                "escalation": "LOW",
                "correlation_targets": ["show vlan", "show interfaces"],
                "diagnostic_signals": "Normal: VLANs active. Fault: VLANs down or misconfigured."
            },
            
            # === ROUTING PROTOCOL FILES ===
            
            "show ip bgp summary": {
                "purpose": "BGP neighbor status and session summary",
                "used_for": "BGP troubleshooting, neighbor health monitoring, routing analysis",
                "key_info": "Neighbor IPs, session state, prefix counts, AS numbers, uptime",
                "category": "protocol",
                "escalation": "HIGH",
                "correlation_targets": ["show interfaces", "show ip route", "show ip bgp neighbors"],
                "diagnostic_signals": "Normal: All neighbors Established. Fault: Sessions in Active/Idle.",
                "production_patterns": {
                    "normal": "All neighbors Established, stable uptime",
                    "issues": ["BGP flapping", "High CPU/memory", "Route convergence issues", "AS path loops"],
                    "customer_patterns": {
                        "Data_Center": "Many neighbors (50+), iBGP full mesh",
                        "Enterprise": "Few neighbors (2-10), eBGP to ISP",
                        "Service_Provider": "Many neighbors (100+), route reflectors"
                    }
                }
            },
            
            "show ip bgp neighbors": {
                "purpose": "Detailed BGP neighbor information and statistics",
                "used_for": "Deep BGP troubleshooting, session analysis, performance monitoring",
                "key_info": "Neighbor details, message statistics, timers, capabilities, routes",
                "category": "protocol",
                "escalation": "HIGH",
                "correlation_targets": ["show ip bgp summary", "show interfaces", "show ip route"],
                "diagnostic_signals": "Normal: Healthy neighbor statistics. Fault: High error rates or session issues."
            },
            
            "show ip bgp": {
                "purpose": "Complete BGP routing table and advertisement information",
                "used_for": "BGP route analysis, advertisement verification, troubleshooting",
                "key_info": "BGP routes, AS paths, next hops, communities, attributes",
                "category": "protocol",
                "escalation": "HIGH",
                "correlation_targets": ["show ip bgp summary", "show ip route", "show ip bgp neighbors"],
                "diagnostic_signals": "Normal: Normal BGP table size. Fault: Missing routes or path issues."
            },
            
            "show ip bgp regexp": {
                "purpose": "BGP route filtering with regular expressions",
                "used_for": "Specific route analysis, pattern matching, troubleshooting",
                "key_info": "Filtered BGP routes based on patterns",
                "category": "protocol",
                "escalation": "MEDIUM",
                "correlation_targets": ["show ip bgp", "show ip route"],
                "diagnostic_signals": "Normal: Expected route patterns. Fault: Unexpected route patterns."
            },
            
            "show ip route": {
                "purpose": "Complete IP routing table and forwarding information",
                "used_for": "Routing verification, reachability analysis, path troubleshooting",
                "key_info": "Destination networks, next hops, protocols, administrative distance, metrics",
                "category": "protocol",
                "escalation": "HIGH",
                "correlation_targets": ["show ip bgp", "show interfaces", "show ip protocols"],
                "diagnostic_signals": "Normal: Routing table populated. Fault: Missing routes or black holes.",
                "production_patterns": {
                    "normal": "Connected, static, BGP routes present",
                    "issues": ["Missing routes", "Black holes", "Routing loops", "Convergence issues"],
                    "customer_patterns": {
                        "Data_Center": "Large routing table (100K+ routes), ECMP",
                        "Enterprise": "Moderate table (1K-10K routes), default route",
                        "Service_Provider": "Very large table (1M+ routes), BGP full table"
                    }
                }
            },
            
            "show ip route summary": {
                "purpose": "Routing table summary and statistics",
                "used_for": "Route table analysis, capacity planning, performance monitoring",
                "key_info": "Route count per protocol, table size, memory usage",
                "category": "protocol",
                "escalation": "MEDIUM",
                "correlation_targets": ["show ip route", "show ip protocols"],
                "diagnostic_signals": "Normal: Normal route distribution. Fault: Unusual route patterns."
            },
            
            "show ip protocols": {
                "purpose": "Routing protocol status and configuration",
                "used_for": "Protocol troubleshooting, configuration verification, status monitoring",
                "key_info": "Protocol status, timers, networks, filtering, redistribution",
                "category": "protocol",
                "escalation": "MEDIUM",
                "correlation_targets": ["show ip route", "show ip bgp", "config_db.json"],
                "diagnostic_signals": "Normal: Protocols configured and running. Fault: Protocol issues or misconfiguration."
            },
            
            "show ospf neighbor": {
                "purpose": "OSPF neighbor status and adjacency information",
                "used_for": "OSPF troubleshooting, adjacency analysis, convergence monitoring",
                "key_info": "Neighbor IPs, state, DR/BDR, timers, adjacency uptime",
                "category": "protocol",
                "escalation": "HIGH",
                "correlation_targets": ["show interfaces", "show ip route", "show ospf database"],
                "diagnostic_signals": "Normal: OSPF neighbors Full. Fault: Neighbor adjacency issues."
            },
            
            "show ospf database": {
                "purpose": "OSPF LSAs and link-state database",
                "used_for": "OSPF troubleshooting, topology analysis, LSA analysis",
                "key_info": "LSA types, sequence numbers, aging, topology information",
                "category": "protocol",
                "escalation": "MEDIUM",
                "correlation_targets": ["show ospf neighbor", "show ip route"],
                "diagnostic_signals": "Normal: Normal LSA database. Fault: LSA issues or topology problems."
            },
            
            "show ospf interface": {
                "purpose": "OSPF interface configuration and status",
                "used_for": "OSPF interface troubleshooting, configuration verification",
                "key_info": "Interface OSPF config, timers, costs, neighbor counts",
                "category": "protocol",
                "escalation": "MEDIUM",
                "correlation_targets": ["show interfaces", "show ospf neighbor"],
                "diagnostic_signals": "Normal: OSPF interfaces properly configured. Fault: OSPF interface issues."
            },
            
            # === CONTAINER AND SERVICE FILES ===
            
            "docker ps": {
                "purpose": "Docker container status and runtime information",
                "used_for": "Service health monitoring, container troubleshooting, resource analysis",
                "key_info": "Container names, status, image names, resource limits, ports",
                "category": "control-plane",
                "escalation": "HIGH",
                "correlation_targets": ["docker stats", "docker logs", "systemctl", "config_db.json"],
                "diagnostic_signals": "Normal: All containers Up. Fault: Containers Down/Restarting.",
                "production_patterns": {
                    "normal": "All SONiC containers running (syncd, swss, bgp, etc.)",
                    "issues": ["Container restarts", "Container crashes", "Resource limits", "Image issues"],
                    "customer_patterns": {
                        "All_Customers": "Standard SONiC containers (syncd, swss, bgp, teamd, etc.)",
                        "NEE-series": "Sometimes additional customer containers",
                        "Service_Provider": "Custom containers for services"
                    }
                }
            },
            
            "docker ps -a": {
                "purpose": "All Docker containers including stopped ones",
                "used_for": "Container history analysis, crash investigation, restart tracking",
                "key_info": "All containers including stopped, exit codes, restart counts",
                "category": "control-plane",
                "escalation": "HIGH",
                "correlation_targets": ["docker ps", "docker logs", "syslog"],
                "diagnostic_signals": "Normal: Recent restarts minimal. Fault: High restart counts or crashes."
            },
            
            "docker stats": {
                "purpose": "Container resource utilization (CPU, memory, network, I/O)",
                "used_for": "Performance monitoring, resource exhaustion detection, capacity planning",
                "key_info": "CPU %, memory usage, network I/O, block I/O per container",
                "category": "control-plane",
                "escalation": "HIGH",
                "correlation_targets": ["docker ps", "free", "ps", "top"],
                "diagnostic_signals": "Normal: Resource usage normal. Fault: High CPU/memory usage.",
                "production_patterns": {
                    "normal": "syncd 10-30% CPU, 200-800MB memory; others <5% CPU, <100MB memory",
                    "issues": ["syncd CPU >80%", "Container memory >1GB", "Resource leaks", "I/O bottlenecks"],
                    "customer_patterns": {
                        "High_Load": "syncd CPU 50-80%, memory 1-2GB",
                        "Normal_Load": "syncd CPU 10-30%, memory 200-800MB",
                        "Low_Load": "syncd CPU <10%, memory <500MB"
                    }
                }
            },
            
            "docker stats --no-stream": {
                "purpose": "Current container resource usage snapshot",
                "used_for": "Quick resource check, performance monitoring",
                "key_info": "Current resource usage without streaming",
                "category": "control-plane",
                "escalation": "MEDIUM",
                "correlation_targets": ["docker stats", "ps", "free"],
                "diagnostic_signals": "Normal: Current usage within limits. Fault: Current usage high."
            },
            
            "docker images": {
                "purpose": "Docker image information and versions",
                "used_for": "Image version tracking, compatibility analysis, security updates",
                "key_info": "Image names, tags, sizes, creation dates",
                "category": "control-plane",
                "escalation": "MEDIUM",
                "correlation_targets": ["docker ps", "version", "config_db.json"],
                "diagnostic_signals": "Normal: Current image versions. Fault: Outdated or inconsistent images."
            },
            
            "docker logs": {
                "purpose": "Container application logs and service messages",
                "used_for": "Service troubleshooting, error analysis, operational monitoring",
                "key_info": "Service logs, error messages, timestamps, service events",
                "category": "logs",
                "escalation": "HIGH",
                "correlation_targets": ["docker ps", "syslog", "config_db.json"],
                "diagnostic_signals": "Normal: Normal service logs. Fault: Error messages or service failures.",
                "production_patterns": {
                    "normal": "Service startup logs, periodic status messages",
                    "issues": ["Service crashes", "Configuration errors", "Resource exhaustion", "Dependency failures"],
                    "customer_patterns": {
                        "syncd": "ASIC initialization, SAI logs, error handling",
                        "bgp": "Peer establishment, route updates, error messages",
                        "swss": "ASIC programming, port status, error handling"
                    }
                }
            },
            
            "docker logs <container>": {
                "purpose": "Specific container logs for detailed analysis",
                "used_for": "Container-specific troubleshooting, deep error analysis",
                "key_info": "Detailed container logs, stack traces, error details",
                "category": "logs",
                "escalation": "HIGH",
                "correlation_targets": ["docker logs", "docker ps", "syslog"],
                "diagnostic_signals": "Normal: Normal container logs. Fault: Container-specific errors."
            },
            
            "systemctl status": {
                "purpose": "System service status and systemd information",
                "used_for": "Service management, startup troubleshooting, dependency analysis",
                "key_info": "Service names, status, PID, startup time, dependencies",
                "category": "control-plane",
                "escalation": "MEDIUM",
                "correlation_targets": ["docker ps", "syslog", "config_db.json"],
                "diagnostic_signals": "Normal: All services active. Fault: Services failed or inactive."
            },
            
            "systemctl list-units": {
                "purpose": "Complete systemd unit listing",
                "used_for": "Service inventory, dependency analysis, startup order",
                "key_info": "All systemd units, status, dependencies, load state",
                "category": "control-plane",
                "escalation": "LOW",
                "correlation_targets": ["systemctl status", "docker ps"],
                "diagnostic_signals": "Normal: Units loaded and active. Fault: Failed or masked units."
            },
            
            "systemctl list-timers": {
                "purpose": "Systemd timers and scheduled tasks",
                "used_for": "Scheduled task monitoring, automation troubleshooting",
                "key_info": "Timer status, next run time, last execution",
                "category": "control-plane",
                "escalation": "LOW",
                "correlation_targets": ["systemctl status", "cron"],
                "diagnostic_signals": "Normal: Timers running properly. Fault: Failed timers or scheduling issues."
            },
            
            # === PROCESS AND SYSTEM RESOURCE FILES ===
            
            "ps aux": {
                "purpose": "Process listing with resource utilization and command details",
                "used_for": "Process monitoring, resource analysis, performance troubleshooting",
                "key_info": "Process names, PIDs, CPU %, MEM %, command arguments, user",
                "category": "process",
                "escalation": "HIGH",
                "correlation_targets": ["docker ps", "free", "top", "docker stats"],
                "diagnostic_signals": "Normal: Normal process load. Fault: High CPU/memory processes.",
                "production_patterns": {
                    "normal": "syncd, bgpd, redis-server main processes",
                    "issues": ["Hung processes", "Memory leaks", "High CPU usage", "Zombie processes"],
                    "customer_patterns": {
                        "All_Customers": "Standard SONiC processes (syncd, bgpd, redis, etc.)",
                        "High_Load": "High CPU syncd, multiple bgp processes",
                        "Custom": "Customer-specific processes"
                    }
                }
            },
            
            "ps -ef": {
                "purpose": "Process listing with full command lines and parent/child relationships",
                "used_for": "Process hierarchy analysis, dependency tracking, troubleshooting",
                "key_info": "Process hierarchy, parent PIDs, full command lines, user info",
                "category": "process",
                "escalation": "MEDIUM",
                "correlation_targets": ["ps aux", "docker ps", "pstree"],
                "diagnostic_signals": "Normal: Normal process hierarchy. Fault: Process relationship issues."
            },
            
            "top": {
                "purpose": "Real-time system resource monitoring and process ranking",
                "used_for": "Performance monitoring, resource exhaustion, system health",
                "key_info": "Load average, memory usage, top CPU processes, system uptime",
                "category": "process",
                "escalation": "HIGH",
                "correlation_targets": ["ps aux", "free", "docker stats", "vmstat"],
                "diagnostic_signals": "Normal: Low system load. Fault: High load average or memory usage.",
                "production_patterns": {
                    "normal": "Load <2.0, memory usage <80%, top processes normal",
                    "issues": ["Load >5.0", "Memory >90%", "High I/O wait", "CPU saturation"],
                    "customer_patterns": {
                        "Data_Center": "Higher load tolerance (<5.0)",
                        "Enterprise": "Normal load tolerance (<2.0)",
                        "Service_Provider": "Variable load patterns"
                    }
                }
            },
            
            "htop": {
                "purpose": "Interactive process viewer with detailed resource information",
                "used_for": "Interactive process monitoring, resource analysis, troubleshooting",
                "key_info": "Interactive process view, resource usage, tree view",
                "category": "process",
                "escalation": "MEDIUM",
                "correlation_targets": ["top", "ps aux", "free"],
                "diagnostic_signals": "Normal: Normal process activity. Fault: Process issues or resource problems."
            },
            
            "free -h": {
                "purpose": "System memory utilization in human-readable format",
                "used_for": "Memory analysis, resource planning, exhaustion detection",
                "key_info": "Total/used/free memory, swap usage, cached memory, available memory",
                "category": "process",
                "escalation": "HIGH",
                "correlation_targets": ["ps aux", "docker stats", "vmstat", "/proc/meminfo"],
                "diagnostic_signals": "Normal: Adequate free memory. Fault: Low available memory or high swap.",
                "production_patterns": {
                    "normal": "Available memory >20%, swap usage <10%",
                    "issues": ["Available memory <10%", "High swap usage", "Memory fragmentation", "OOM events"],
                    "customer_patterns": {
                        "8GB_Switches": "Available >1.6GB (20%)",
                        "16GB_Switches": "Available >3.2GB (20%)",
                        "32GB_Switches": "Available >6.4GB (20%)"
                    }
                }
            },
            
            "free -m": {
                "purpose": "System memory utilization in megabytes",
                "used_for": "Precise memory analysis, monitoring, troubleshooting",
                "key_info": "Memory usage in MB, detailed breakdown",
                "category": "process",
                "escalation": "MEDIUM",
                "correlation_targets": ["free -h", "/proc/meminfo", "vmstat"],
                "diagnostic_signals": "Normal: Normal memory distribution. Fault: Memory issues detected."
            },
            
            "/proc/meminfo": {
                "purpose": "Detailed system memory information from kernel",
                "used_for": "Deep memory analysis, kernel memory troubleshooting, performance tuning",
                "key_info": "MemTotal, MemFree, MemAvailable, Slab, PageTables, HugePages",
                "category": "process",
                "escalation": "MEDIUM",
                "correlation_targets": ["free -h", "ps aux", "slabinfo", "vmstat"],
                "diagnostic_signals": "Normal: Healthy memory distribution. Fault: Memory fragmentation or leaks.",
                "production_patterns": {
                    "normal": "Slab <15%, PageTables moderate, HugePages available",
                    "issues": ["High slab usage", "PageTable bloat", "HugePage issues", "Memory fragmentation"],
                    "customer_patterns": {
                        "High_Route_Count": "Higher PageTable usage",
                        "Virtualization": "HugePage requirements",
                        "High_Memory": "More complex memory management"
                    }
                }
            },
            
            "/proc/slabinfo": {
                "purpose": "Kernel slab allocator detailed statistics",
                "used_for": "Memory leak detection, kernel memory analysis, performance tuning",
                "key_info": "Slab cache information, object counts, memory usage",
                "category": "process",
                "escalation": "MEDIUM",
                "correlation_targets": ["/proc/meminfo", "ps aux", "dmesg"],
                "diagnostic_signals": "Normal: Normal slab usage. Fault: Slab memory leaks or bloat."
            },
            
            "/proc/vmstat": {
                "purpose": "Virtual memory statistics and paging activity",
                "used_for": "Memory performance analysis, paging monitoring, system tuning",
                "key_info": "Paging statistics, memory pressure, swap activity",
                "category": "process",
                "escalation": "MEDIUM",
                "correlation_targets": ["free -h", "vmstat", "iostat"],
                "diagnostic_signals": "Normal: Low paging activity. Fault: High paging or memory pressure."
            },
            
            "/proc/buddyinfo": {
                "purpose": "Memory fragmentation and allocation information",
                "used_for": "Memory fragmentation analysis, allocation troubleshooting",
                "key_info": "Memory fragmentation by order, allocation information",
                "category": "process",
                "escalation": "MEDIUM",
                "correlation_targets": ["/proc/meminfo", "free -h", "dmesg"],
                "diagnostic_signals": "Normal: Low fragmentation. Fault: High memory fragmentation."
            },
            
            "vmstat": {
                "purpose": "Virtual memory statistics and system activity",
                "used_for": "Performance monitoring, memory analysis, I/O analysis",
                "key_info": "Memory, paging, block I/O, CPU, system activity",
                "category": "process",
                "escalation": "MEDIUM",
                "correlation_targets": ["free -h", "iostat", "top"],
                "diagnostic_signals": "Normal: Normal system activity. Fault: High paging or I/O wait."
            },
            
            "iostat": {
                "purpose": "I/O statistics and device utilization",
                "used_for": "I/O performance analysis, disk monitoring, bottleneck identification",
                "key_info": "Device I/O rates, utilization, wait times, throughput",
                "category": "process",
                "escalation": "MEDIUM",
                "correlation_targets": ["vmstat", "top", "df"],
                "diagnostic_signals": "Normal: Normal I/O patterns. Fault: High I/O wait or bottlenecks."
            },
            
            "mpstat": {
                "purpose": "CPU statistics and multiprocessor utilization",
                "used_for": "CPU performance analysis, load balancing, troubleshooting",
                "key_info": "CPU utilization per core, interrupts, context switches",
                "category": "process",
                "escalation": "MEDIUM",
                "correlation_targets": ["top", "ps aux", "vmstat"],
                "diagnostic_signals": "Normal: Balanced CPU usage. Fault: CPU imbalance or high load."
            },
            
            # === CONFIGURATION FILES ===
            
            "config_db.json": {
                "purpose": "SONiC configuration database (running configuration)",
                "used_for": "Configuration analysis, change verification, backup/restore",
                "key_info": "Interface config, VLAN config, BGP config, system settings",
                "category": "config",
                "escalation": "MEDIUM",
                "correlation_targets": ["running-config", "show interfaces", "show ip bgp"],
                "diagnostic_signals": "Normal: Valid JSON structure. Fault: Syntax errors or missing sections.",
                "production_patterns": {
                    "normal": "Complete configuration with all required sections",
                    "issues": ["JSON syntax errors", "Missing sections", "Invalid values", "Configuration conflicts"],
                    "customer_patterns": {
                        "Standard": "Basic SONiC configuration",
                        "Enterprise": "Enhanced security features",
                        "Service_Provider": "Advanced routing features"
                    }
                }
            },
            
            "show running-configuration": {
                "purpose": "Current running configuration in CLI format",
                "used_for": "Configuration review, change validation, documentation",
                "key_info": "Interface settings, routing config, service configuration",
                "category": "config",
                "escalation": "MEDIUM",
                "correlation_targets": ["config_db.json", "show interfaces", "show ip bgp"],
                "diagnostic_signals": "Normal: Complete configuration. Fault: Missing or invalid config."
            },
            
            "show startup-configuration": {
                "purpose": "Startup configuration (boot configuration)",
                "used_for": "Configuration consistency, boot troubleshooting, change tracking",
                "key_info": "Saved configuration, boot settings, persistent config",
                "category": "config",
                "escalation": "LOW",
                "correlation_targets": ["running-config", "config_db.json"],
                "diagnostic_signals": "Normal: Valid startup config. Fault: Missing or corrupted startup config."
            },
            
            "show configuration": {
                "purpose": "Configuration overview and summary",
                "used_for": "Quick configuration review, high-level analysis",
                "key_info": "Configuration summary, key settings",
                "category": "config",
                "escalation": "LOW",
                "correlation_targets": ["running-config", "config_db.json"],
                "diagnostic_signals": "Normal: Configuration present. Fault: Configuration issues."
            },
            
            "show configuration diff": {
                "purpose": "Configuration differences between running and startup",
                "used_for": "Configuration change tracking, consistency analysis",
                "key_info": "Configuration differences, changes made",
                "category": "config",
                "escalation": "LOW",
                "correlation_targets": ["running-config", "startup-config"],
                "diagnostic_signals": "Normal: Expected differences. Fault: Unexpected configuration changes."
            },
            
            # === LOG AND SYSTEM MESSAGE FILES ===
            
            "syslog": {
                "purpose": "System log messages and events",
                "used_for": "System troubleshooting, event correlation, security analysis",
                "key_info": "Timestamps, service names, error messages, system events",
                "category": "logs",
                "escalation": "HIGH",
                "correlation_targets": ["kern.log", "docker logs", "auth.log"],
                "diagnostic_signals": "Normal: Minimal warnings. Fault: High error count or critical messages.",
                "production_patterns": {
                    "normal": "Service startup, status messages, occasional warnings",
                    "issues": ["Service failures", "Resource exhaustion", "Security events", "System errors"],
                    "customer_patterns": {
                        "All_Customers": "Standard system logging patterns",
                        "High_Security": "Enhanced security logging",
                        "High_Availability": "Failover and recovery logging"
                    }
                }
            },
            
            "/var/log/syslog": {
                "purpose": "System log file location",
                "used_for": "System log analysis, troubleshooting, audit trails",
                "key_info": "System messages, service logs, timestamps",
                "category": "logs",
                "escalation": "HIGH",
                "correlation_targets": ["syslog", "kern.log", "auth.log"],
                "diagnostic_signals": "Normal: Normal system logging. Fault: Logging issues or system problems."
            },
            
            "/var/log/kern.log": {
                "purpose": "Kernel log messages and events",
                "used_for": "Kernel troubleshooting, hardware issues, system crashes",
                "key_info": "Kernel messages, hardware events, panic/crash information",
                "category": "logs",
                "escalation": "HIGH",
                "correlation_targets": ["dmesg", "syslog", "/proc/kmsg"],
                "diagnostic_signals": "Normal: Normal kernel messages. Fault: Panic messages or hardware errors."
            },
            
            "dmesg": {
                "purpose": "Kernel ring buffer messages",
                "used_for": "Boot troubleshooting, hardware detection, memory issues",
                "key_info": "Boot sequence, hardware detection, OOM killer events, driver messages",
                "category": "logs",
                "escalation": "HIGH",
                "correlation_targets": ["kern.log", "syslog", "/proc/meminfo"],
                "diagnostic_signals": "Normal: Clean boot sequence. Fault: OOM events or driver errors.",
                "production_patterns": {
                    "normal": "Clean boot, hardware detected, drivers loaded",
                    "issues": ["Kernel panics", "OOM killer events", "Driver failures", "Hardware detection issues"],
                    "customer_patterns": {
                        "Dell": "Dell-specific driver messages",
                        "Mellanox": "NVIDIA/MLX driver messages",
                        "Broadcom": "Broadcom SAI driver messages"
                    }
                }
            },
            
            "dmesg -T": {
                "purpose": "Kernel ring buffer with human-readable timestamps",
                "used_for": "Boot troubleshooting with readable timestamps",
                "key_info": "Kernel messages with readable timestamps",
                "category": "logs",
                "escalation": "MEDIUM",
                "correlation_targets": ["dmesg", "kern.log"],
                "diagnostic_signals": "Normal: Normal kernel messages. Fault: Boot issues or errors."
            },
            
            "/var/log/auth.log": {
                "purpose": "Authentication and authorization logs",
                "used_for": "Security analysis, access troubleshooting, audit trails",
                "key_info": "Login attempts, authentication success/failure, SSH sessions",
                "category": "logs",
                "escalation": "MEDIUM",
                "correlation_targets": ["syslog", "systemctl", "sshd logs"],
                "diagnostic_signals": "Normal: Normal authentication. Fault: Failed login attempts or security issues."
            },
            
            "/var/log/daemon.log": {
                "purpose": "Daemon service logs",
                "used_for": "Service troubleshooting, daemon analysis",
                "key_info": "Daemon messages, service logs",
                "category": "logs",
                "escalation": "MEDIUM",
                "correlation_targets": ["syslog", "systemctl", "docker logs"],
                "diagnostic_signals": "Normal: Normal daemon activity. Fault: Daemon issues or failures."
            },
            
            "/var/log/messages": {
                "purpose": "General system messages",
                "used_for": "System message analysis, troubleshooting",
                "key_info": "System messages, general logs",
                "category": "logs",
                "escalation": "MEDIUM",
                "correlation_targets": ["syslog", "kern.log"],
                "diagnostic_signals": "Normal: Normal system messages. Fault: System issues or errors."
            },
            
            "journalctl": {
                "purpose": "Systemd journal logs",
                "used_for": "Systemd service logs, system troubleshooting",
                "key_info": "Journal entries, service logs, systemd messages",
                "category": "logs",
                "escalation": "MEDIUM",
                "correlation_targets": ["systemctl", "syslog", "docker logs"],
                "diagnostic_signals": "Normal: Normal journal entries. Fault: Service issues or systemd problems."
            },
            
            "journalctl -u <service>": {
                "purpose": "Specific service journal logs",
                "used_for": "Service-specific troubleshooting, detailed analysis",
                "key_info": "Service-specific journal entries",
                "category": "logs",
                "escalation": "MEDIUM",
                "correlation_targets": ["journalctl", "systemctl", "docker logs"],
                "diagnostic_signals": "Normal: Normal service logs. Fault: Service-specific issues."
            },
            
            # === HARDWARE AND DIAGNOSTIC FILES ===
            
            "sensors": {
                "purpose": "Hardware sensor readings (temperature, voltage, fans)",
                "used_for": "Hardware monitoring, thermal analysis, power supply health",
                "key_info": "Temperature sensors, voltage readings, fan RPMs, alarm status",
                "category": "hardware",
                "escalation": "HIGH",
                "correlation_targets": ["environment", "inventory", "syslog"],
                "diagnostic_signals": "Normal: All sensors normal. Fault: Temperature warnings or voltage issues.",
                "production_patterns": {
                    "normal": "Temperature 40-60°C, fans 30-70% RPM, voltages within 5%",
                    "issues": ["Temperature >80°C", "Fan failure", "Voltage out of range", "Sensor failures"],
                    "customer_patterns": {
                        "Data_Center": "Higher ambient temperatures, more sensors",
                        "Enterprise": "Normal office environment",
                        "Industrial": "Wide temperature ranges, rugged sensors"
                    }
                }
            },
            
            "sensors-detect": {
                "purpose": "Hardware sensor detection and configuration",
                "used_for": "Sensor discovery, configuration verification",
                "key_info": "Detected sensors, chip information, configuration",
                "category": "hardware",
                "escalation": "LOW",
                "correlation_targets": ["sensors", "lspci", "inventory"],
                "diagnostic_signals": "Normal: Sensors detected. Fault: Sensor detection issues."
            },
            
            "ethtool": {
                "purpose": "Ethernet interface detailed information and statistics",
                "used_for": "Interface troubleshooting, PHY analysis, driver issues",
                "key_info": "Link speed, duplex, driver version, PHY settings, error counters",
                "category": "hardware",
                "escalation": "MEDIUM",
                "correlation_targets": ["show interfaces", "show interfaces counters", "lldp"],
                "diagnostic_signals": "Normal: Link up with normal stats. Fault: Link down or PHY errors."
            },
            
            "ethtool -i": {
                "purpose": "Driver information for network interfaces",
                "used_for": "Driver troubleshooting, version analysis, compatibility",
                "key_info": "Driver version, firmware version, bus information",
                "category": "hardware",
                "escalation": "LOW",
                "correlation_targets": ["ethtool", "show interfaces", "lspci"],
                "diagnostic_signals": "Normal: Driver information present. Fault: Driver issues or missing info."
            },
            
            "ethtool -S": {
                "purpose": "Detailed interface statistics",
                "used_for": "Interface performance analysis, error detection",
                "key_info": "Detailed interface statistics, error counters",
                "category": "hardware",
                "escalation": "MEDIUM",
                "correlation_targets": ["ethtool", "show interfaces counters"],
                "diagnostic_signals": "Normal: Normal statistics. Fault: High error rates or issues."
            },
            
            "lspci": {
                "purpose": "PCI device enumeration and information",
                "used_for": "Hardware inventory, driver troubleshooting, device compatibility",
                "key_info": "PCI devices, vendor IDs, driver names, device capabilities",
                "category": "hardware",
                "escalation": "LOW",
                "correlation_targets": ["inventory", "platform", "sensors"],
                "diagnostic_signals": "Normal: All PCI devices detected. Fault: Missing devices or driver issues."
            },
            
            "lspci -vv": {
                "purpose": "Verbose PCI device information",
                "used_for": "Detailed hardware analysis, driver compatibility",
                "key_info": "Detailed PCI information, capabilities, debugging",
                "category": "hardware",
                "escalation": "LOW",
                "correlation_targets": ["lspci", "inventory"],
                "diagnostic_signals": "Normal: Detailed PCI info. Fault: Hardware issues or problems."
            },
            
            "lscpu": {
                "purpose": "CPU information and architecture details",
                "used_for": "CPU analysis, performance tuning, compatibility",
                "key_info": "CPU architecture, cores, cache, features",
                "category": "hardware",
                "escalation": "LOW",
                "correlation_targets": ["top", "ps aux", "vmstat"],
                "diagnostic_signals": "Normal: CPU information present. Fault: CPU issues or missing info."
            },
            
            "lsusb": {
                "purpose": "USB device enumeration",
                "used_for": "USB device inventory, troubleshooting",
                "key_info": "USB devices, vendor information",
                "category": "hardware",
                "escalation": "LOW",
                "correlation_targets": ["inventory", "lspci"],
                "diagnostic_signals": "Normal: USB devices detected. Fault: USB issues or missing devices."
            },
            
            "dmidecode": {
                "purpose": "DMI/SMBIOS hardware information",
                "used_for": "Hardware inventory, system information, warranty tracking",
                "key_info": "System information, hardware details, serial numbers",
                "category": "hardware",
                "escalation": "LOW",
                "correlation_targets": ["inventory", "platform"],
                "diagnostic_signals": "Normal: DMI information present. Fault: DMI issues or missing info."
            },
            
            # === CORE DUMP AND CRASH FILES ===
            
            "core": {
                "purpose": "Memory dump of crashed processes",
                "used_for": "Crash analysis, debugging, root cause investigation",
                "key_info": "Process name, crash time, memory dump, stack trace",
                "category": "kernel",
                "escalation": "CRITICAL",
                "correlation_targets": ["kern.log", "syslog", "ps aux"],
                "diagnostic_signals": "Normal: No core dumps. Fault: Core dumps present indicating crashes.",
                "production_patterns": {
                    "normal": "No core dumps present",
                    "issues": ["syncd core dumps", "bgpd core dumps", "system crashes", "application crashes"],
                    "customer_patterns": {
                        "High_Stability": "No core dumps expected",
                        "Development": "Some core dumps possible",
                        "Production": "Core dumps indicate serious issues"
                    }
                }
            },
            
            "gdb": {
                "purpose": "Generated core dumps for debugging",
                "used_for": "Application debugging, crash analysis, memory leak detection",
                "key_info": "Stack traces, memory maps, register state, debugging info",
                "category": "kernel",
                "escalation": "HIGH",
                "correlation_targets": ["core", "kern.log", "ps aux"],
                "diagnostic_signals": "Normal: No debugging output. Fault: Debugging info indicating issues."
            },
            
            "gcore": {
                "purpose": "Manual core dump generation",
                "used_for": "Manual crash analysis, debugging",
                "key_info": "Manual core dumps, debugging information",
                "category": "kernel",
                "escalation": "HIGH",
                "correlation_targets": ["core", "gdb"],
                "diagnostic_signals": "Normal: No manual cores. Fault: Manual cores indicate troubleshooting."
            },
            
            "crash": {
                "purpose": "Kernel crash analysis tool output",
                "used_for": "Kernel crash analysis, debugging",
                "key_info": "Kernel crash information, debugging output",
                "category": "kernel",
                "escalation": "CRITICAL",
                "correlation_targets": ["core", "kern.log", "dmesg"],
                "diagnostic_signals": "Normal: No crash analysis. Fault: Crash analysis indicates kernel issues."
            },
            
            "kdump": {
                "purpose": "Kernel crash dump configuration and status",
                "used_for": "Crash dump configuration, crash recovery",
                "key_info": "Kdump configuration, crash dump status",
                "category": "kernel",
                "escalation": "MEDIUM",
                "correlation_targets": ["crash", "core", "kdump.conf"],
                "diagnostic_signals": "Normal: Kdump configured. Fault: Kdump issues or misconfiguration."
            },
            
            # === PERFORMANCE AND MONITORING FILES ===
            
            "perf": {
                "purpose": "Performance counters and statistics",
                "used_for": "Performance analysis, optimization, bottleneck identification",
                "key_info": "CPU cycles, instructions, cache hits/misses, branch predictions",
                "category": "debug",
                "escalation": "MEDIUM",
                "correlation_targets": ["top", "ps aux", "iostat"],
                "diagnostic_signals": "Normal: Normal performance counters. Fault: High cache miss rates or bottlenecks."
            },
            
            "perf stat": {
                "purpose": "Performance statistics for specific commands",
                "used_for": "Command performance analysis, optimization",
                "key_info": "Performance statistics for command execution",
                "category": "debug",
                "escalation": "MEDIUM",
                "correlation_targets": ["perf", "time"],
                "diagnostic_signals": "Normal: Normal performance. Fault: Performance issues detected."
            },
            
            "perf top": {
                "purpose": "Real-time performance profiling",
                "used_for": "Real-time performance analysis, bottleneck identification",
                "key_info": "Real-time performance data, hot spots",
                "category": "debug",
                "escalation": "MEDIUM",
                "correlation_targets": ["top", "perf", "ps aux"],
                "diagnostic_signals": "Normal: Normal performance profile. Fault: Performance issues."
            },
            
            "netstat": {
                "purpose": "Network statistics and connection information",
                "used_for": "Network troubleshooting, connection analysis, performance monitoring",
                "key_info": "TCP/UDP connections, listening ports, network statistics",
                "category": "debug",
                "escalation": "MEDIUM",
                "correlation_targets": ["show interfaces", "show ip bgp", "ss"],
                "diagnostic_signals": "Normal: Normal connection states. Fault: High connection counts or errors."
            },
            
            "netstat -s": {
                "purpose": "Detailed network statistics",
                "used_for": "Network performance analysis, protocol statistics",
                "key_info": "Detailed network statistics, protocol information",
                "category": "debug",
                "escalation": "MEDIUM",
                "correlation_targets": ["netstat", "show interfaces counters"],
                "diagnostic_signals": "Normal: Normal network statistics. Fault: Network issues or errors."
            },
            
            "ss": {
                "purpose": "Socket statistics (modern netstat replacement)",
                "used_for": "Socket analysis, connection monitoring, troubleshooting",
                "key_info": "Socket information, connection states,
                "category": "debug",
                "escalation": "MEDIUM",
                "correlation_targets": ["netstat", "show interfaces"],
                "diagnostic_signals": "Normal: Normal socket states. Fault: Socket issues or problems."
            },
            
            "strace": {
                "purpose": "System call tracing for debugging",
                "used_for": "Process debugging, system call analysis, troubleshooting",
                "key_info": "System calls, process behavior, debugging information",
                "category": "debug",
                "escalation": "MEDIUM",
                "correlation_targets": ["ps aux", "ltrace", "gdb"],
                "diagnostic_signals": "Normal: Normal system calls. Fault: System call issues or problems."
            },
            
            "ltrace": {
                "purpose": "Library call tracing for debugging",
                "used_for": "Application debugging, library analysis, troubleshooting",
                "key_info": "Library calls, application behavior, debugging information",
                "category": "debug",
                "escalation": "MEDIUM",
                "correlation_targets": ["strace", "ps aux", "gdb"],
                "diagnostic_signals": "Normal: Normal library calls. Fault: Library issues or problems."
            },
            
            "tcpdump": {
                "purpose": "Network packet capture and analysis",
                "used_for": "Network troubleshooting, packet analysis, protocol debugging",
                "key_info": "Packet captures, network traffic, protocol analysis",
                "category": "debug",
                "escalation": "MEDIUM",
                "correlation_targets": ["show interfaces", "netstat", "tcpflow"],
                "diagnostic_signals": "Normal: Normal network traffic. Fault: Network issues or problems."
            },
            
            "time": {
                "purpose": "Command execution timing",
                "used_for": "Performance measurement, command optimization",
                "key_info": "Execution time, performance measurement",
                "category": "debug",
                "escalation": "LOW",
                "correlation_targets": ["perf", "ps aux"],
                "diagnostic_signals": "Normal: Normal execution time. Fault: Performance issues."
            },
            
            # === SECURITY AND AUTHENTICATION FILES ===
            
            "who": {
                "purpose": "Current user sessions and logins",
                "used_for": "Session monitoring, security analysis, user tracking",
                "key_info": "Current users, login times, sessions",
                "category": "security",
                "escalation": "LOW",
                "correlation_targets": ["w", "last", "auth.log"],
                "diagnostic_signals": "Normal: Normal user sessions. Fault: Unauthorized sessions or issues."
            },
            
            "w": {
                "purpose": "Current user activity and system load",
                "used_for": "User monitoring, system activity analysis",
                "key_info": "User activity, system load, processes",
                "category": "security",
                "escalation": "LOW",
                "correlation_targets": ["who", "top", "ps aux"],
                "diagnostic_signals": "Normal: Normal user activity. Fault: Unusual activity or issues."
            },
            
            "last": {
                "purpose": "Login history and user activity",
                "used_for": "Security analysis, user tracking, audit trails",
                "key_info": "Login history, user activity, timestamps",
                "category": "security",
                "escalation": "MEDIUM",
                "correlation_targets": ["who", "auth.log", "lastb"],
                "diagnostic_signals": "Normal: Normal login history. Fault: Security issues or unusual activity."
            },
            
            "lastb": {
                "purpose": "Failed login history",
                "used_for": "Security analysis, brute force detection, troubleshooting",
                "key_info": "Failed login attempts, security events",
                "category": "security",
                "escalation": "MEDIUM",
                "correlation_targets": ["last", "auth.log", "faillog"],
                "diagnostic_signals": "Normal: Minimal failed logins. Fault: Security issues or attacks."
            },
            
            "faillog": {
                "purpose": "Failed login tracking",
                "used_for": "Security monitoring, attack detection",
                "key_info": "Failed login statistics, security events",
                "category": "security",
                "escalation": "MEDIUM",
                "correlation_targets": ["lastb", "auth.log"],
                "diagnostic_signals": "Normal: Normal failure rates. Fault: High failure rates or attacks."
            },
            
            "sudo -l": {
                "purpose": "Sudo permissions and user privileges",
                "used_for": "Privilege analysis, security auditing, troubleshooting",
                "key_info": "User sudo permissions, privilege information",
                "category": "security",
                "escalation": "MEDIUM",
                "correlation_targets": ["sudoers", "auth.log", "user accounts"],
                "diagnostic_signals": "Normal: Normal sudo permissions. Fault: Privilege issues or misconfig."
            },
            
            # === MISCELLANEOUS FILES ===
            
            "date": {
                "purpose": "System date and time",
                "used_for": "Time synchronization, timestamp analysis",
                "key_info": "Current system time, date information",
                "category": "system",
                "escalation": "LOW",
                "correlation_targets": ["uptime", "timedatectl"],
                "diagnostic_signals": "Normal: Correct system time. Fault: Time synchronization issues."
            },
            
            "uptime": {
                "purpose": "System uptime and load average",
                "used_for": "System stability analysis, load monitoring",
                "key_info": "System uptime, load average, active users",
                "category": "system",
                "escalation": "LOW",
                "correlation_targets": ["top", "w", "ps aux"],
                "diagnostic_signals": "Normal: Normal uptime and load. Fault: System issues or high load."
            },
            
            "uname": {
                "purpose": "System information and kernel details",
                "used_for": "System identification, kernel analysis",
                "key_info": "Kernel version, system architecture, hostname",
                "category": "system",
                "escalation": "LOW",
                "correlation_targets": ["version", "platform", "lscpu"],
                "diagnostic_signals": "Normal: Normal system information. Fault: System issues or problems."
            },
            
            "hostname": {
                "purpose": "System hostname identification",
                "used_for": "System identification, network configuration",
                "key_info": "System hostname, domain information",
                "category": "system",
                "escalation": "LOW",
                "correlation_targets": ["uname", "config_db.json"],
                "diagnostic_signals": "Normal: Normal hostname. Fault: Hostname issues or misconfig."
            },
            
            "id": {
                "purpose": "User and group identification",
                "used_for": "User analysis, permission troubleshooting",
                "key_info": "User ID, group ID, user information",
                "category": "system",
                "escalation": "LOW",
                "correlation_targets": ["who", "sudo", "auth.log"],
                "diagnostic_signals": "Normal: Normal user information. Fault: User issues or problems."
            },
            
            "pwd": {
                "purpose": "Current working directory",
                "used_for": "Directory analysis, path troubleshooting",
                "key_info": "Current directory path",
                "category": "system",
                "escalation": "LOW",
                "correlation_targets": ["ls", "cd"],
                "diagnostic_signals": "Normal: Normal directory. Fault: Directory issues or problems."
            },
            
            "ls": {
                "purpose": "Directory listing and file information",
                "used_for": "File analysis, directory troubleshooting",
                "key_info": "File listing, directory contents",
                "category": "system",
                "escalation": "LOW",
                "correlation_targets": ["pwd", "find", "du"],
                "diagnostic_signals": "Normal: Normal directory contents. Fault: File issues or problems."
            },
            
            "find": {
                "purpose": "File search and discovery",
                "used_for": "File location, system analysis, troubleshooting",
                "key_info": "File search results, file locations",
                "category": "system",
                "escalation": "LOW",
                "correlation_targets": ["ls", "locate", "which"],
                "diagnostic_signals": "Normal: Normal file search. Fault: File issues or problems."
            },
            
            "du": {
                "purpose": "Disk usage analysis",
                "used_for": "Storage analysis, space management, troubleshooting",
                "key_info": "Disk usage, file sizes, directory sizes",
                "category": "system",
                "escalation": "MEDIUM",
                "correlation_targets": ["df", "ls", "find"],
                "diagnostic_signals": "Normal: Normal disk usage. Fault: Storage issues or problems."
            },
            
            "df": {
                "purpose": "Disk space and filesystem information",
                "used_for": "Storage analysis, space monitoring, troubleshooting",
                "key_info": "Filesystem information, disk space, mount points",
                "category": "system",
                "escalation": "MEDIUM",
                "correlation_targets": ["du", "mount", "lsblk"],
                "diagnostic_signals": "Normal: Normal disk space. Fault: Storage issues or space problems."
            },
            
            "mount": {
                "purpose": "Mounted filesystems and mount points",
                "used_for": "Storage analysis, filesystem troubleshooting",
                "key_info": "Mounted filesystems, mount points, options",
                "category": "system",
                "escalation": "MEDIUM",
                "correlation_targets": ["df", "lsblk", "/proc/mounts"],
                "diagnostic_signals": "Normal: Normal mounts. Fault: Mount issues or problems."
            },
            
            "lsblk": {
                "purpose": "Block device information and tree structure",
                "used_for": "Storage analysis, device troubleshooting",
                "key_info": "Block devices, partitions, relationships",
                "category": "system",
                "escalation": "LOW",
                "correlation_targets": ["df", "mount", "fdisk"],
                "diagnostic_signals": "Normal: Normal block devices. Fault: Device issues or problems."
            },
            
            "fdisk": {
                "purpose": "Disk partitioning information",
                "used_for": "Partition analysis, storage troubleshooting",
                "key_info": "Disk partitions, partition information",
                "category": "system",
                "escalation": "MEDIUM",
                "correlation_targets": ["lsblk", "df", "mount"],
                "diagnostic_signals": "Normal: Normal partitions. Fault: Partition issues or problems."
            },
            
            "crontab": {
                "purpose": "Cron job configuration and scheduling",
                "used_for": "Scheduled task analysis, automation troubleshooting",
                "key_info": "Cron jobs, scheduled tasks, timing information",
                "category": "system",
                "escalation": "MEDIUM",
                "correlation_targets": ["systemctl list-timers", "cron"],
                "diagnostic_signals": "Normal: Normal cron jobs. Fault: Cron issues or problems."
            },
            
            "cron": {
                "purpose": "Cron daemon status and job execution",
                "used_for": "Scheduled task monitoring, automation analysis",
                "key_info": "Cron status, job execution, scheduling",
                "category": "system",
                "escalation": "MEDIUM",
                "correlation_targets": ["crontab", "systemctl list-timers"],
                "diagnostic_signals": "Normal: Normal cron execution. Fault: Cron issues or problems."
            },
            
            "at": {
                "purpose": "At job scheduling and execution",
                "used_for": "Scheduled task analysis, job monitoring",
                "key_info": "At jobs, scheduled tasks, execution",
                "category": "system",
                "escalation": "LOW",
                "correlation_targets": ["crontab", "batch"],
                "diagnostic_signals": "Normal: Normal at jobs. Fault: At job issues or problems."
            },
            
            "batch": {
                "purpose": "Batch job processing and execution",
                "used_for": "Batch job analysis, system load management",
                "key_info": "Batch jobs, execution, system load",
                "category": "system",
                "escalation": "LOW",
                "correlation_targets": ["at", "crontab"],
                "diagnostic_signals": "Normal: Normal batch jobs. Fault: Batch job issues or problems."
            }
        }
    
    def extract_archive(self, archive_path: str) -> str:
        """Extract showtech archive using show_tech_extractor skill"""
        print(f"Extracting {archive_path} using show_tech_extractor skill...")
        
        # Use the showtech extractor integration
        extraction_result = extract_showtech_archive(archive_path)
        
        if extraction_result['success']:
            self.temp_dir = extraction_result['output_dir']
            print(f"Extraction completed using {extraction_result['method']}")
            
            # Store extracted data for analysis
            if 'extracted_data' in extraction_result:
                self.extracted_data = extraction_result['extracted_data']
            else:
                self.extracted_data = extraction_result.get('file_inventory', {})
            
            return self.temp_dir
        else:
            raise Exception(f"Extraction failed: {extraction_result.get('error', 'Unknown error')}")
    
    def match_comprehensive_intelligence(self, file_path: str) -> dict:
        """Match file path to comprehensive intelligence database"""
        file_path_lower = file_path.lower()
        
        # Direct exact matches first
        for key, intelligence in self.file_intelligence.items():
            if key.lower() == file_path_lower:
                return intelligence
        
        # Pattern matches with higher priority
        patterns = {
            # Platform files
            "version": ["version", "show version", "sonic version"],
            "platform": ["platform", "show platform", "chassis", "hwsku"],
            "inventory": ["inventory", "show inventory", "hw-inventory"],
            "environment": ["environment", "show environment", "temp", "fan", "psu", "thermal"],
            
            # Interface files
            "show interfaces": ["interface", "show interface", "port", "ethernet"],
            "show interfaces description": ["description", "port-desc", "interface-desc"],
            "show interfaces counters": ["counter", "show interface counter", "statistics"],
            "show interfaces queue": ["queue", "show interface queue", "qos"],
            "show interfaces transceiver": ["transceiver", "optic", "sfp", "qsfp"],
            
            # Data plane files
            "show lldp neighbor": ["lldp", "show lldp", "lldpneigh"],
            "show lldp neighbor-info": ["lldp-info", "lldp detail"],
            "show mac address-table": ["mac", "show mac", "address-table", "fdb"],
            "show mac address-table counting": ["mac-count", "mac-counting"],
            "show vlan": ["vlan", "show vlan", "bridge"],
            "show vlan brief": ["vlan-brief", "show vlan brief"],
            
            # Routing protocol files
            "show ip bgp summary": ["bgp", "show bgp", "bgp-summary"],
            "show ip bgp neighbors": ["bgp-neighbor", "show bgp neighbor"],
            "show ip bgp": ["bgp-route", "show ip bgp", "bgp-table"],
            "show ip bgp regexp": ["bgp-regexp", "bgp-filter"],
            "show ip route": ["route", "show ip route", "routing-table"],
            "show ip route summary": ["route-summary", "route-count"],
            "show ip protocols": ["protocol", "show ip protocol", "routing-protocol"],
            "show ospf neighbor": ["ospf", "show ospf", "ospf-neighbor"],
            "show ospf database": ["ospf-db", "ospf-database"],
            "show ospf interface": ["ospf-intf", "ospf-interface"],
            
            # Container files
            "docker ps": ["docker ps", "docker_ps", "container"],
            "docker ps -a": ["docker ps -a", "docker-all"],
            "docker stats": ["docker stats", "docker_stats", "container-stats"],
            "docker stats --no-stream": ["docker-stats-no", "docker-stats-snapshot"],
            "docker images": ["docker images", "docker-img"],
            "docker logs": ["docker log", "docker_log", "container-log"],
            "docker logs <container>": ["docker-log-detail", "container-log-detail"],
            
            # Service files
            "systemctl status": ["systemctl", "service", "systemd"],
            "systemctl list-units": ["systemctl-list", "systemd-units"],
            "systemctl list-timers": ["systemctl-timer", "systemd-timer"],
            
            # Process files
            "ps aux": ["ps", "process", "ps-aux"],
            "ps -ef": ["ps-ef", "process-tree"],
            "top": ["top", "process-monitor"],
            "htop": ["htop", "interactive-top"],
            "free -h": ["free", "memory", "free-h"],
            "free -m": ["free-m", "memory-mb"],
            "/proc/meminfo": ["meminfo", "proc-meminfo"],
            "/proc/slabinfo": ["slabinfo", "proc-slabinfo"],
            "/proc/vmstat": ["vmstat", "proc-vmstat"],
            "/proc/buddyinfo": ["buddyinfo", "proc-buddyinfo"],
            "vmstat": ["vmstat", "virtual-memory"],
            "iostat": ["iostat", "io-stat"],
            "mpstat": ["mpstat", "cpu-stat"],
            
            # Configuration files
            "config_db.json": ["config_db", "config.json", "sonic-config"],
            "show running-configuration": ["running-config", "running-config", "config-running"],
            "show startup-configuration": ["startup-config", "startup-config", "config-startup"],
            "show configuration": ["config", "show config", "configuration"],
            "show configuration diff": ["config-diff", "config-diff"],
            
            # Log files
            "syslog": ["syslog", "messages", "system-log"],
            "/var/log/syslog": ["syslog", "var-log-syslog"],
            "/var/log/kern.log": ["kern.log", "kernel-log", "var-log-kern"],
            "dmesg": ["dmesg", "kernel-ring", "boot-log"],
            "dmesg -T": ["dmesg-t", "dmesg-timestamp"],
            "/var/log/auth.log": ["auth.log", "authlog", "var-log-auth"],
            "/var/log/daemon.log": ["daemon.log", "daemonlog", "var-log-daemon"],
            "/var/log/messages": ["messages", "var-log-messages"],
            "journalctl": ["journalctl", "systemd-journal"],
            "journalctl -u <service>": ["journalctl-u", "service-journal"],
            
            # Hardware files
            "sensors": ["sensors", "temp", "thermal"],
            "sensors-detect": ["sensors-detect", "sensor-detect"],
            "ethtool": ["ethtool", "ethernet-tool"],
            "ethtool -i": ["ethtool-i", "driver-info"],
            "ethtool -S": ["ethtool-s", "ethernet-stat"],
            "lspci": ["lspci", "pci"],
            "lspci -vv": ["lspci-vv", "pci-verbose"],
            "lscpu": ["lscpu", "cpu-info"],
            "lsusb": ["lsusb", "usb"],
            "dmidecode": ["dmidecode", "dmi", "smbios"],
            
            # Core dump files
            "core": ["core", "coredump", "crash-dump"],
            "gdb": ["gdb", "debugger", "debug"],
            "gcore": ["gcore", "manual-core"],
            "crash": ["crash", "kernel-crash"],
            "kdump": ["kdump", "kernel-dump"],
            
            # Performance files
            "perf": ["perf", "performance", "perf-counter"],
            "perf stat": ["perf-stat", "perf-statistics"],
            "perf top": ["perf-top", "perf-profile"],
            "netstat": ["netstat", "network-stat"],
            "netstat -s": ["netstat-s", "network-statistics"],
            "ss": ["ss", "socket-stat"],
            "strace": ["strace", "system-trace"],
            "ltrace": ["ltrace", "library-trace"],
            "tcpdump": ["tcpdump", "packet-capture"],
            "time": ["time", "execution-time"],
            
            # Security files
            "who": ["who", "user-session"],
            "w": ["w", "user-activity"],
            "last": ["last", "login-history"],
            "lastb": ["lastb", "failed-login"],
            "faillog": ["faillog", "login-failure"],
            "sudo -l": ["sudo", "sudo-perm", "privilege"],
            
            # System files
            "date": ["date", "system-time"],
            "uptime": ["uptime", "system-uptime"],
            "uname": ["uname", "system-info"],
            "hostname": ["hostname", "system-name"],
            "id": ["id", "user-id"],
            "pwd": ["pwd", "current-dir"],
            "ls": ["ls", "directory-list"],
            "find": ["find", "file-search"],
            "du": ["du", "disk-usage"],
            "df": ["df", "disk-space"],
            "mount": ["mount", "filesystem"],
            "lsblk": ["lsblk", "block-device"],
            "fdisk": ["fdisk", "partition"],
            "crontab": ["crontab", "cron-job"],
            "cron": ["cron", "cron-daemon"],
            "at": ["at", "at-job"],
            "batch": ["batch", "batch-job"]
        }
        
        # Try pattern matching
        for pattern_key, pattern_list in patterns.items():
            for pattern in pattern_list:
                if pattern in file_path_lower:
                    return self.file_intelligence[pattern_key]
        
        # Fallback to filename matching
        filename = os.path.basename(file_path).lower()
        for key, intelligence in self.file_intelligence.items():
            if key.lower() in filename:
                return intelligence
        
        # Default intelligence for unknown files
        return {
            "purpose": "Unknown file - requires manual analysis based on content",
            "used_for": "General troubleshooting and analysis - examine content for clues",
            "key_info": "File content analysis required - check for configuration, logs, or data",
            "category": "unknown",
            "escalation": "LOW",
            "correlation_targets": ["syslog", "config_db.json"],
            "diagnostic_signals": "Normal: Content readable. Fault: Empty or corrupted file.",
            "production_patterns": {
                "normal": "File contains readable content",
                "issues": ["File empty", "File corrupted", "File unreadable", "Unknown format"],
                "customer_patterns": {
                    "All_Customers": "Unknown files may be customer-specific",
                    "Custom": "Customer-specific diagnostic files"
                }
            }
        }
    
    def analyze_file_content(self, file_path: str, full_path: str) -> dict:
        """Analyze file content for additional intelligence"""
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2000)  # Read first 2000 chars
            
            content_lower = content.lower()
            
            # Detect issues in content
            issues = []
            if any(term in content_lower for term in ['error', 'fail', 'critical', 'panic', 'crash']):
                issues.append("error_messages")
            if any(term in content_lower for term in ['down', 'offline', 'inactive', 'failed']):
                issues.append("status_issues")
            if any(term in content_lower for term in ['warning', 'alert', 'caution']):
                issues.append("warnings")
            if any(term in content_lower for term in ['timeout', 'slow', 'degraded', 'high']):
                issues.append("performance_issues")
            if any(term in content_lower for term in ['memory', 'oom', 'out of memory', 'exhausted']):
                issues.append("memory_issues")
            if any(term in content_lower for term in ['cpu', 'processor', 'load']):
                issues.append("cpu_issues")
            if any(term in content_lower for term in ['interface', 'port', 'link', 'ethernet']):
                issues.append("interface_issues")
            if any(term in content_lower for term in ['bgp', 'neighbor', 'routing', 'protocol']):
                issues.append("routing_issues")
            if any(term in content_lower for term in ['container', 'docker', 'service']):
                issues.append("container_issues")
            
            # Content summary
            lines = content.split('\n')
            return {
                "content_summary": f"{len(lines)} lines, {len(content)} characters",
                "issues_detected": issues,
                "has_errors": any(term in content_lower for term in ['error', 'fail', 'critical', 'panic']),
                "has_warnings": any(term in content_lower for term in ['warning', 'alert', 'caution']),
                "file_type": self.detect_file_type(content),
                "configuration_detected": any(term in content_lower for term in ['config', 'setting', 'parameter']),
                "log_detected": any(term in content_lower for term in ['log', 'timestamp', 'message']),
                "data_detected": any(term in content_lower for term in ['table', 'statistics', 'counters'])
            }
            
        except Exception as e:
            return {
                "content_summary": f"Error reading file: {e}",
                "issues_detected": ["read_error"],
                "has_errors": True,
                "has_warnings": False,
                "file_type": "unknown",
                "configuration_detected": False,
                "log_detected": False,
                "data_detected": False
            }
    
    def detect_file_type(self, content: str) -> str:
        """Detect file type based on content"""
        content_lower = content.lower()
        
        # JSON detection
        if content.strip().startswith('{') and content.strip().endswith('}'):
            return "json"
        
        # Log detection
        if any(term in content_lower for term in ['timestamp', 'error', 'warning', 'info']):
            return "log"
        
        # Configuration detection
        if any(term in content_lower for term in ['config', 'setting', 'parameter', 'interface', 'vlan']):
            return "configuration"
        
        # Data/table detection
        if any(term in content_lower for term in ['table', 'statistics', 'counters', 'packets', 'bytes']):
            return "data"
        
        # Process listing
        if any(term in content_lower for term in ['pid', 'cpu', 'mem', 'command']):
            return "process"
        
        # System information
        if any(term in content_lower for term in ['version', 'kernel', 'system', 'uptime']):
            return "system"
        
        return "text"
    
    def generate_comprehensive_intelligence_report(self, archive_path: str) -> dict:
        """Generate comprehensive file intelligence report"""
        print("=== COMPREHENSIVE SONiC FILE INTELLIGENCE ANALYSIS ===")
        print(f"Archive: {archive_path}")
        print(f"Analysis Time: {datetime.now().isoformat()}")
        print()
        
        try:
            # Extract archive
            extracted_path = self.extract_archive(archive_path)
            
            # Analyze all files
            file_analysis = []
            categories = {}
            escalation_summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
            file_type_summary = {}
            issue_summary = {}
            
            print("Analyzing files with comprehensive intelligence...")
            
            for root, dirs, files in os.walk(extracted_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, extracted_path)
                    
                    # Get comprehensive file intelligence
                    intelligence = self.match_comprehensive_intelligence(relative_path)
                    
                    # Analyze content
                    content_analysis = self.analyze_file_content(relative_path, file_path)
                    
                    # Create comprehensive file entry
                    file_entry = {
                        "file_path": relative_path,
                        "intelligence": intelligence,
                        "content_analysis": content_analysis,
                        "priority": intelligence["escalation"],
                        "file_type": content_analysis["file_type"],
                        "comprehensive_analysis": self.generate_file_insights(intelligence, content_analysis)
                    }
                    
                    file_analysis.append(file_entry)
                    
                    # Update categories
                    category = intelligence["category"]
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(file_entry)
                    
                    # Update escalation summary
                    escalation_summary[intelligence["escalation"]] += 1
                    
                    # Update file type summary
                    file_type = content_analysis["file_type"]
                    if file_type not in file_type_summary:
                        file_type_summary[file_type] = 0
                    file_type_summary[file_type] += 1
                    
                    # Update issue summary
                    for issue in content_analysis["issues_detected"]:
                        if issue not in issue_summary:
                            issue_summary[issue] = 0
                        issue_summary[issue] += 1
            
            # Sort files by priority
            file_analysis.sort(key=lambda x: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}[x["priority"]])
            
            print(f"Analysis complete: {len(file_analysis)} files analyzed")
            print()
            
            # Display comprehensive summary
            print("=== COMPREHENSIVE FILE INTELLIGENCE SUMMARY ===")
            print(f"Total Files: {len(file_analysis)}")
            print(f"Categories: {len(categories)}")
            print(f"File Types: {len(file_type_summary)}")
            print()
            
            print("Priority Distribution:")
            for priority, count in escalation_summary.items():
                if count > 0:
                    print(f"  {priority}: {count} files")
            print()
            
            print("File Type Distribution:")
            for file_type, count in file_type_summary.items():
                print(f"  {file_type}: {count} files")
            print()
            
            print("Issue Distribution:")
            for issue, count in sorted(issue_summary.items(), key=lambda x: x[1], reverse=True):
                print(f"  {issue}: {count} files")
            print()
            
            print("Categories:")
            for category, files in categories.items():
                print(f"  {category}: {len(files)} files")
            print()
            
            # Display critical and high priority files
            print("=== CRITICAL AND HIGH PRIORITY FILES ===")
            critical_high_files = [f for f in file_analysis if f["priority"] in ["CRITICAL", "HIGH"]]
            for file_entry in critical_high_files[:15]:  # Top 15
                intel = file_entry["intelligence"]
                content = file_entry["content_analysis"]
                insights = file_entry["comprehensive_analysis"]
                
                print(f"File: {file_entry['file_path']}")
                print(f"  Purpose: {intel['purpose']}")
                print(f"  Priority: {file_entry['priority']}")
                print(f"  Used For: {intel['used_for']}")
                print(f"  Key Info: {intel['key_info']}")
                print(f"  File Type: {file_entry['file_type']}")
                if content['issues_detected']:
                    print(f"  Issues: {', '.join(content['issues_detected'])}")
                if insights.get('production_insights'):
                    print(f"  Production Insights: {insights['production_insights']}")
                print()
            
            # Generate comprehensive report
            report = {
                "analysis_metadata": {
                    "archive_path": archive_path,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "total_files": len(file_analysis),
                    "categories": list(categories.keys()),
                    "escalation_summary": escalation_summary,
                    "file_type_summary": file_type_summary,
                    "issue_summary": issue_summary
                },
                "file_analysis": file_analysis,
                "categories": {k: [{"file_path": f["file_path"], "priority": f["priority"], "file_type": f["file_type"]} for f in v] for k, v in categories.items()},
                "critical_high_priority_files": [f["file_path"] for f in critical_high_files],
                "comprehensive_insights": self.generate_overall_insights(file_analysis),
                "production_patterns": self.extract_production_patterns(file_analysis),
                "correlation_matrix": self.generate_correlation_matrix(file_analysis)
            }
            
            # Save comprehensive report
            self.save_comprehensive_report(report, archive_path)
            
            return report
            
        except Exception as e:
            print(f"Analysis failed: {e}")
            return {"error": str(e)}
        finally:
            # Cleanup
            if self.temp_dir and os.path.exists(self.temp_dir):
                try:
                    shutil.rmtree(self.temp_dir)
                    print(f"Cleaned up temporary directory: {self.temp_dir}")
                except Exception as e:
                    print(f"Failed to cleanup temp directory: {e}")
    
    def generate_file_insights(self, intelligence: dict, content_analysis: dict) -> dict:
        """Generate comprehensive insights for each file"""
        insights = {
            "production_insights": "",
            "troubleshooting_value": "",
            "correlation_value": "",
            "customer_patterns": ""
        }
        
        # Production insights based on intelligence database
        if "production_patterns" in intelligence:
            patterns = intelligence["production_patterns"]
            
            # Normal patterns
            if "normal" in patterns:
                insights["production_insights"] += f"Normal: {patterns['normal']}. "
            
            # Issues
            if "issues" in patterns and patterns["issues"]:
                insights["production_insights"] += f"Issues: {', '.join(patterns['issues'])}. "
            
            # Customer patterns
            if "customer_patterns" in patterns:
                customer_patterns = patterns["customer_patterns"]
                if customer_patterns:
                    insights["customer_patterns"] = f"Customer Patterns: {', '.join([f'{k}: {v}' for k, v in customer_patterns.items()])}"
        
        # Troubleshooting value
        if intelligence["escalation"] in ["CRITICAL", "HIGH"]:
            insights["troubleshooting_value"] = "HIGH - Critical for issue resolution"
        elif intelligence["escalation"] == "MEDIUM":
            insights["troubleshooting_value"] = "MEDIUM - Important for comprehensive analysis"
        else:
            insights["troubleshooting_value"] = "LOW - Reference information"
        
        # Correlation value
        correlation_count = len(intelligence["correlation_targets"])
        if correlation_count >= 3:
            insights["correlation_value"] = "HIGH - Correlates with multiple files"
        elif correlation_count >= 2:
            insights["correlation_value"] = "MEDIUM - Correlates with several files"
        else:
            insights["correlation_value"] = "LOW - Limited correlation"
        
        return insights
    
    def generate_overall_insights(self, file_analysis: list) -> dict:
        """Generate overall insights from file analysis"""
        insights = {
            "system_health_indicators": {},
            "troubleshooting_priorities": [],
            "customer_specific_patterns": {},
            "production_recommendations": []
        }
        
        # System health indicators
        critical_files = [f for f in file_analysis if f["priority"] == "CRITICAL"]
        high_files = [f for f in file_analysis if f["priority"] == "HIGH"]
        
        insights["system_health_indicators"] = {
            "critical_files_count": len(critical_files),
            "high_priority_files_count": len(high_files),
            "total_issues": len([f for f in file_analysis if f["content_analysis"]["has_errors"]]),
            "warning_count": len([f for f in file_analysis if f["content_analysis"]["has_warnings"]])
        }
        
        # Troubleshooting priorities
        if critical_files:
            insights["troubleshooting_priorities"].append("CRITICAL: Investigate core dumps and kernel issues immediately")
        
        if high_files:
            insights["troubleshooting_priorities"].append("HIGH: Analyze interface, routing, and container issues")
        
        # Production recommendations
        insights["production_recommendations"] = [
            "Focus on CRITICAL and HIGH priority files first",
            "Correlate findings across related files",
            "Check production patterns against customer deployments",
            "Monitor system resources and performance metrics"
        ]
        
        return insights
    
    def extract_production_patterns(self, file_analysis: list) -> dict:
        """Extract production patterns from file analysis"""
        patterns = {
            "common_issues": {},
            "customer_variations": {},
            "platform_specific": {},
            "version_specific": {}
        }
        
        # Extract common issues
        all_issues = {}
        for file_entry in file_analysis:
            for issue in file_entry["content_analysis"]["issues_detected"]:
                if issue not in all_issues:
                    all_issues[issue] = 0
                all_issues[issue] += 1
        
        patterns["common_issues"] = dict(sorted(all_issues.items(), key=lambda x: x[1], reverse=True))
        
        return patterns
    
    def generate_correlation_matrix(self, file_analysis: list) -> dict:
        """Generate enhanced correlation matrix"""
        correlations = {}
        
        for file_entry in file_analysis:
            file_path = file_entry["file_path"]
            intelligence = file_entry["intelligence"]
            
            correlations[file_path] = {
                "correlation_targets": intelligence["correlation_targets"],
                "priority": intelligence["escalation"],
                "category": intelligence["category"],
                "file_type": file_entry["file_type"],
                "issues_detected": file_entry["content_analysis"]["issues_detected"]
            }
        
        return correlations
    
    def save_comprehensive_report(self, report: dict, archive_path: str):
        """Save comprehensive intelligence report to files"""
        output_dir = os.path.dirname(os.path.abspath(__file__))
        archive_name = os.path.basename(archive_path).replace('.tar.gz', '')
        
        # Create analysis folder
        analysis_dir = os.path.join(output_dir, f"comprehensive_file_intelligence_{archive_name}")
        os.makedirs(analysis_dir, exist_ok=True)
        
        # Save JSON report
        json_file = os.path.join(analysis_dir, "comprehensive_file_intelligence_report.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print(f"Comprehensive intelligence report saved: {json_file}")
        
        # Save comprehensive markdown summary
        md_file = os.path.join(analysis_dir, "comprehensive_file_intelligence_summary.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive SONiC File Intelligence Analysis\n\n")
            f.write(f"**Archive:** {archive_name}\n")
            f.write(f"**Analysis Time:** {report['analysis_metadata']['analysis_timestamp']}\n")
            f.write(f"**Total Files:** {report['analysis_metadata']['total_files']}\n")
            f.write(f"**Categories:** {len(report['analysis_metadata']['categories'])}\n")
            f.write(f"**File Types:** {len(report['analysis_metadata']['file_type_summary'])}\n\n")
            
            f.write("## Priority Distribution\n\n")
            for priority, count in report['analysis_metadata']['escalation_summary'].items():
                if count > 0:
                    f.write(f"- **{priority}:** {count} files\n")
            f.write("\n")
            
            f.write("## File Type Distribution\n\n")
            for file_type, count in report['analysis_metadata']['file_type_summary'].items():
                f.write(f"- **{file_type}:** {count} files\n")
            f.write("\n")
            
            f.write("## Issue Distribution\n\n")
            for issue, count in report['analysis_metadata']['issue_summary'].items():
                f.write(f"- **{issue}:** {count} files\n")
            f.write("\n")
            
            f.write("## Categories\n\n")
            for category in report['analysis_metadata']['categories']:
                f.write(f"- **{category}**\n")
            f.write("\n")
            
            f.write("## Critical and High Priority Files\n\n")
            for file_path in report['critical_high_priority_files'][:20]:
                f.write(f"- `{file_path}`\n")
            f.write("\n")
            
            f.write("## Production Insights\n\n")
            insights = report['comprehensive_insights']
            f.write("### System Health Indicators\n\n")
            for indicator, value in insights['system_health_indicators'].items():
                f.write(f"- **{indicator}:** {value}\n")
            f.write("\n")
            
            f.write("### Troubleshooting Priorities\n\n")
            for priority in insights['troubleshooting_priorities']:
                f.write(f"- {priority}\n")
            f.write("\n")
            
            f.write("### Production Recommendations\n\n")
            for recommendation in insights['production_recommendations']:
                f.write(f"- {recommendation}\n")
            f.write("\n")
            
            f.write("## Detailed File Analysis\n\n")
            for file_entry in report['file_analysis'][:50]:  # Top 50 files
                intel = file_entry["intelligence"]
                content = file_entry["content_analysis"]
                insights = file_entry["comprehensive_analysis"]
                
                f.write(f"### {file_entry['file_path']}\n")
                f.write(f"**Purpose:** {intel['purpose']}\n")
                f.write(f"**Used For:** {intel['used_for']}\n")
                f.write(f"**Priority:** {file_entry['priority']}\n")
                f.write(f"**Category:** {intel['category']}\n")
                f.write(f"**File Type:** {file_entry['file_type']}\n")
                f.write(f"**Key Info:** {intel['key_info']}\n")
                f.write(f"**Content Summary:** {content['content_summary']}\n")
                
                if content['issues_detected']:
                    f.write(f"**Issues Detected:** {', '.join(content['issues_detected'])}\n")
                
                f.write(f"**Correlation Targets:** {', '.join(intel['correlation_targets'])}\n")
                f.write(f"**Diagnostic Signals:** {intel['diagnostic_signals']}\n")
                f.write(f"**Troubleshooting Value:** {insights['troubleshooting_value']}\n")
                f.write(f"**Correlation Value:** {insights['correlation_value']}\n")
                
                if insights.get('production_insights'):
                    f.write(f"**Production Insights:** {insights['production_insights']}\n")
                
                if insights.get('customer_patterns'):
                    f.write(f"**Customer Patterns:** {insights['customer_patterns']}\n")
                
                f.write("\n")
        
        print(f"Comprehensive intelligence summary saved: {md_file}")
        
        # Save production patterns
        patterns_file = os.path.join(analysis_dir, "production_patterns.json")
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(report['production_patterns'], f, indent=2)
        print(f"Production patterns saved: {patterns_file}")
        
        # Save enhanced correlation matrix
        correlation_file = os.path.join(analysis_dir, "enhanced_correlation_matrix.json")
        with open(correlation_file, 'w', encoding='utf-8') as f:
            json.dump(report['correlation_matrix'], f, indent=2)
        print(f"Enhanced correlation matrix saved: {correlation_file}")
        
        # Save comprehensive insights
        insights_file = os.path.join(analysis_dir, "comprehensive_insights.json")
        with open(insights_file, 'w', encoding='utf-8') as f:
            json.dump(report['comprehensive_insights'], f, indent=2)
        print(f"Comprehensive insights saved: {insights_file}")
        
        print(f"\nAll comprehensive intelligence reports saved in: {analysis_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sonic_comprehensive_file_intelligence_analyzer.py <showtech_archive.tar.gz>")
        sys.exit(1)
    
    archive_path = sys.argv[1]
    
    if not os.path.exists(archive_path):
        print(f"Error: Archive file not found: {archive_path}")
        sys.exit(1)
    
    # Run comprehensive file intelligence analysis
    analyzer = SONiCComprehensiveFileIntelligence()
    result = analyzer.generate_comprehensive_intelligence_report(archive_path)
    
    if result and 'error' not in result:
        print("\n=== COMPREHENSIVE FILE INTELLIGENCE ANALYSIS COMPLETE ===")
        print("Comprehensive file intelligence analysis completed successfully.")
        print("Reports generated:")
        print("  - comprehensive_file_intelligence_report.json")
        print("  - comprehensive_file_intelligence_summary.md")
        print("  - production_patterns.json")
        print("  - enhanced_correlation_matrix.json")
        print("  - comprehensive_insights.json")
    else:
        print("\n=== ANALYSIS FAILED ===")
        print("Please check the error message above.")