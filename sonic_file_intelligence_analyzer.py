#!/usr/bin/env python3
"""
SONiC File Intelligence Analyzer - ShowTech File Reference Tool
Analyzes showtech archives and provides detailed information about each file's purpose
"""

import os
import sys
import tarfile
import tempfile
import shutil
import json
from datetime import datetime
# Import showtech extractor integration
sys.path.insert(0, str(Path(__file__).parent))
from showtech_extractor_integration import extract_showtech_archive
from pathlib import Path

class SONiCFileIntelligenceAnalyzer:
    """Analyzes showtech files and provides intelligence about their purpose"""
    
    def __init__(self):
        self.temp_dir = None
        self.file_intelligence = self.load_file_intelligence_database()
    
    def load_file_intelligence_database(self) -> dict:
        """Load comprehensive file intelligence database"""
        return {
            # Platform and System Information
            "version": {
                "purpose": "SONiC OS version, build information, kernel version",
                "used_for": "Version compatibility checks, bug identification, feature support validation",
                "key_info": "SONiC version string, kernel version, build timestamp, hardware platform",
                "category": "platform",
                "escalation": "MEDIUM",
                "correlation_targets": ["docker", "interfaces", "config"],
                "diagnostic_signals": "Normal: Complete version strings present. Fault: Missing/corrupted version data."
            },
            "platform": {
                "purpose": "Hardware platform identification and capabilities",
                "used_for": "Platform-specific troubleshooting, hardware compatibility",
                "key_info": "Platform name, hardware SKU, ASIC type, serial number",
                "category": "platform",
                "escalation": "MEDIUM",
                "correlation_targets": ["interfaces", "environment", "config"],
                "diagnostic_signals": "Normal: Platform info complete. Fault: Platform mismatch or missing data."
            },
            "inventory": {
                "purpose": "Hardware component inventory and status",
                "used_for": "Hardware tracking, warranty information, component replacement",
                "key_info": "Chassis, power supplies, fans, transceivers, ASIC modules",
                "category": "platform",
                "escalation": "MEDIUM",
                "correlation_targets": ["environment", "sensors", "interfaces"],
                "diagnostic_signals": "Normal: All components detected. Fault: Missing components or failure indicators."
            },
            "environment": {
                "purpose": "Environmental monitoring (temperature, voltage, fans)",
                "used_for": "Hardware health monitoring, thermal issues, power problems",
                "key_info": "Temperature sensors, fan RPM, PSU status, voltage levels",
                "category": "hardware",
                "escalation": "HIGH",
                "correlation_targets": ["inventory", "sensors", "syslog"],
                "diagnostic_signals": "Normal: All sensors within range. Fault: Temperature warnings or PSU failures."
            },
            
            # Interface and Data Plane
            "interfaces": {
                "purpose": "Interface configuration and operational status",
                "used_for": "Interface troubleshooting, link status verification, connectivity issues",
                "key_info": "Interface names, admin/oper status, speed, error counters",
                "category": "data-plane",
                "escalation": "HIGH",
                "correlation_targets": ["counters", "lldp", "bgp", "config"],
                "diagnostic_signals": "Normal: Interfaces admin=up, oper=up. Fault: Interfaces down or error counters."
            },
            "counters": {
                "purpose": "Detailed interface statistics and error counters",
                "used_for": "Performance analysis, error detection, traffic monitoring",
                "key_info": "Rx/Tx packets, bytes, errors, discards, CRC, giants",
                "category": "data-plane",
                "escalation": "HIGH",
                "correlation_targets": ["interfaces", "lldp", "bgp"],
                "diagnostic_signals": "Normal: Low error rates. Fault: High error counters or discards."
            },
            "lldp": {
                "purpose": "LLDP neighbor discovery and topology information",
                "used_for": "Network topology mapping, physical connectivity verification",
                "key_info": "Neighbor device names, port IDs, system descriptions",
                "category": "data-plane",
                "escalation": "MEDIUM",
                "correlation_targets": ["interfaces", "inventory", "mac"],
                "diagnostic_signals": "Normal: Neighbors discovered. Fault: No LLDP neighbors or topology issues."
            },
            "mac": {
                "purpose": "MAC address table and forwarding database",
                "used_for": "Layer 2 troubleshooting, MAC learning issues, forwarding verification",
                "key_info": "MAC addresses, VLAN IDs, port numbers, entry types",
                "category": "data-plane",
                "escalation": "MEDIUM",
                "correlation_targets": ["interfaces", "lldp", "vlan"],
                "diagnostic_signals": "Normal: MAC table populated. Fault: No MAC entries or learning issues."
            },
            
            # Routing Protocols
            "bgp": {
                "purpose": "BGP protocol status, neighbor information, routing tables",
                "used_for": "BGP troubleshooting, routing policy verification, connectivity issues",
                "key_info": "Neighbor IPs, session state, prefix counts, AS paths",
                "category": "protocol",
                "escalation": "HIGH",
                "correlation_targets": ["interfaces", "route", "config"],
                "diagnostic_signals": "Normal: All neighbors Established. Fault: Sessions in Active/Idle."
            },
            "ospf": {
                "purpose": "OSPF protocol status and routing information",
                "used_for": "OSPF troubleshooting, area configuration, route convergence",
                "key_info": "Router ID, neighbor IPs, area IDs, LSA types",
                "category": "protocol",
                "escalation": "HIGH",
                "correlation_targets": ["interfaces", "route", "config"],
                "diagnostic_signals": "Normal: OSPF neighbors up. Fault: Neighbor adjacency issues."
            },
            "route": {
                "purpose": "IP routing table and forwarding information",
                "used_for": "Routing verification, reachability analysis, path troubleshooting",
                "key_info": "Destination networks, next hops, protocols, administrative distance",
                "category": "protocol",
                "escalation": "HIGH",
                "correlation_targets": ["bgp", "ospf", "interfaces"],
                "diagnostic_signals": "Normal: Routing table populated. Fault: Missing routes or black holes."
            },
            
            # Container and Service Files
            "docker ps": {
                "purpose": "Docker container status and runtime information",
                "used_for": "Service health monitoring, container troubleshooting, resource analysis",
                "key_info": "Container names, status, image names, resource limits",
                "category": "control-plane",
                "escalation": "HIGH",
                "correlation_targets": ["docker stats", "docker logs", "systemctl"],
                "diagnostic_signals": "Normal: All containers Up. Fault: Containers Down/Restarting."
            },
            "docker stats": {
                "purpose": "Container resource utilization (CPU, memory, network, I/O)",
                "used_for": "Performance monitoring, resource exhaustion detection, capacity planning",
                "key_info": "CPU %, memory usage, network I/O, block I/O per container",
                "category": "control-plane",
                "escalation": "HIGH",
                "correlation_targets": ["docker ps", "free", "ps"],
                "diagnostic_signals": "Normal: Resource usage normal. Fault: High CPU/memory usage."
            },
            "docker logs": {
                "purpose": "Container application logs and service messages",
                "used_for": "Service troubleshooting, error analysis, operational monitoring",
                "key_info": "Service logs, error messages, timestamps, service events",
                "category": "logs",
                "escalation": "HIGH",
                "correlation_targets": ["docker ps", "syslog", "config"],
                "diagnostic_signals": "Normal: Normal service logs. Fault: Error messages or service failures."
            },
            "systemctl": {
                "purpose": "System service status and systemd information",
                "used_for": "Service management, startup troubleshooting, dependency analysis",
                "key_info": "Service names, status, PID, startup time",
                "category": "control-plane",
                "escalation": "MEDIUM",
                "correlation_targets": ["docker ps", "syslog", "config"],
                "diagnostic_signals": "Normal: All services active. Fault: Services failed or inactive."
            },
            
            # Process and System Resources
            "ps": {
                "purpose": "Process listing with resource utilization",
                "used_for": "Process monitoring, resource analysis, performance troubleshooting",
                "key_info": "Process names, PIDs, CPU %, MEM %, command arguments",
                "category": "process",
                "escalation": "HIGH",
                "correlation_targets": ["docker ps", "free", "top"],
                "diagnostic_signals": "Normal: Normal process load. Fault: High CPU/memory processes."
            },
            "top": {
                "purpose": "Real-time system resource monitoring",
                "used_for": "Performance monitoring, resource exhaustion, system health",
                "key_info": "Load average, memory usage, top CPU processes, system uptime",
                "category": "process",
                "escalation": "HIGH",
                "correlation_targets": ["ps", "free", "docker stats"],
                "diagnostic_signals": "Normal: Low system load. Fault: High load average or memory usage."
            },
            "free": {
                "purpose": "System memory utilization and availability",
                "used_for": "Memory analysis, resource planning, exhaustion detection",
                "key_info": "Total/used/free memory, swap usage, cached memory, available memory",
                "category": "process",
                "escalation": "HIGH",
                "correlation_targets": ["ps", "docker stats", "meminfo"],
                "diagnostic_signals": "Normal: Adequate free memory. Fault: Low available memory or high swap."
            },
            "meminfo": {
                "purpose": "Detailed system memory information",
                "used_for": "Deep memory analysis, kernel memory troubleshooting",
                "key_info": "MemTotal, MemFree, MemAvailable, Slab, PageTables, HugePages",
                "category": "process",
                "escalation": "MEDIUM",
                "correlation_targets": ["free", "ps", "slabinfo"],
                "diagnostic_signals": "Normal: Healthy memory distribution. Fault: Memory fragmentation or leaks."
            },
            
            # Configuration Files
            "config_db.json": {
                "purpose": "SONiC configuration database (running configuration)",
                "used_for": "Configuration analysis, change verification, backup/restore",
                "key_info": "Interface config, VLAN config, BGP config, system settings",
                "category": "config",
                "escalation": "MEDIUM",
                "correlation_targets": ["running-config", "interfaces", "bgp"],
                "diagnostic_signals": "Normal: Valid JSON structure. Fault: Syntax errors or missing sections."
            },
            "running-config": {
                "purpose": "Current running configuration in CLI format",
                "used_for": "Configuration review, change validation, documentation",
                "key_info": "Interface settings, routing config, service configuration",
                "category": "config",
                "escalation": "MEDIUM",
                "correlation_targets": ["config_db.json", "interfaces", "bgp"],
                "diagnostic_signals": "Normal: Complete configuration. Fault: Missing or invalid config."
            },
            "startup-config": {
                "purpose": "Startup configuration (boot configuration)",
                "used_for": "Configuration consistency, boot troubleshooting, change tracking",
                "key_info": "Saved configuration, boot settings, persistent config",
                "category": "config",
                "escalation": "LOW",
                "correlation_targets": ["running-config", "config_db.json"],
                "diagnostic_signals": "Normal: Valid startup config. Fault: Missing or corrupted startup config."
            },
            
            # Log Files
            "syslog": {
                "purpose": "System log messages and events",
                "used_for": "System troubleshooting, event correlation, security analysis",
                "key_info": "Timestamps, service names, error messages, system events",
                "category": "logs",
                "escalation": "HIGH",
                "correlation_targets": ["kern.log", "docker logs", "auth.log"],
                "diagnostic_signals": "Normal: Minimal warnings. Fault: High error count or critical messages."
            },
            "kern.log": {
                "purpose": "Kernel log messages and events",
                "used_for": "Kernel troubleshooting, hardware issues, system crashes",
                "key_info": "Kernel messages, hardware events, panic/crash information",
                "category": "logs",
                "escalation": "HIGH",
                "correlation_targets": ["dmesg", "syslog", "core"],
                "diagnostic_signals": "Normal: Normal kernel messages. Fault: Panic messages or hardware errors."
            },
            "dmesg": {
                "purpose": "Kernel ring buffer messages",
                "used_for": "Boot troubleshooting, hardware detection, memory issues",
                "key_info": "Boot sequence, hardware detection, OOM killer events, driver messages",
                "category": "logs",
                "escalation": "HIGH",
                "correlation_targets": ["kern.log", "syslog", "meminfo"],
                "diagnostic_signals": "Normal: Clean boot sequence. Fault: OOM events or driver errors."
            },
            "auth.log": {
                "purpose": "Authentication and authorization logs",
                "used_for": "Security analysis, access troubleshooting, audit trails",
                "key_info": "Login attempts, authentication success/failure, SSH sessions",
                "category": "logs",
                "escalation": "MEDIUM",
                "correlation_targets": ["syslog", "systemctl"],
                "diagnostic_signals": "Normal: Normal authentication. Fault: Failed login attempts or security issues."
            },
            
            # Hardware and Diagnostic Files
            "sensors": {
                "purpose": "Hardware sensor readings (temperature, voltage, fans)",
                "used_for": "Hardware monitoring, thermal analysis, power supply health",
                "key_info": "Temperature sensors, voltage readings, fan RPMs, alarm status",
                "category": "hardware",
                "escalation": "HIGH",
                "correlation_targets": ["environment", "inventory", "syslog"],
                "diagnostic_signals": "Normal: All sensors normal. Fault: Temperature warnings or voltage issues."
            },
            "ethtool": {
                "purpose": "Ethernet interface detailed information and statistics",
                "used_for": "Interface troubleshooting, PHY analysis, driver issues",
                "key_info": "Link speed, duplex, driver version, PHY settings, error counters",
                "category": "hardware",
                "escalation": "MEDIUM",
                "correlation_targets": ["interfaces", "counters", "lldp"],
                "diagnostic_signals": "Normal: Link up with normal stats. Fault: Link down or PHY errors."
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
            
            # Core Dump and Crash Files
            "core": {
                "purpose": "Memory dump of crashed processes",
                "used_for": "Crash analysis, debugging, root cause investigation",
                "key_info": "Process name, crash time, memory dump, stack trace",
                "category": "kernel",
                "escalation": "CRITICAL",
                "correlation_targets": ["kern.log", "syslog", "ps"],
                "diagnostic_signals": "Normal: No core dumps. Fault: Core dumps present indicating crashes."
            },
            "gdb": {
                "purpose": "Generated core dumps for debugging",
                "used_for": "Application debugging, crash analysis, memory leak detection",
                "key_info": "Stack traces, memory maps, register state, debugging info",
                "category": "kernel",
                "escalation": "HIGH",
                "correlation_targets": ["core", "kern.log", "ps"],
                "diagnostic_signals": "Normal: No debugging output. Fault: Debugging info indicating issues."
            },
            
            # Performance and Monitoring
            "perf": {
                "purpose": "Performance counters and statistics",
                "used_for": "Performance analysis, optimization, bottleneck identification",
                "key_info": "CPU cycles, instructions, cache hits/misses, branch predictions",
                "category": "debug",
                "escalation": "MEDIUM",
                "correlation_targets": ["top", "ps", "iostat"],
                "diagnostic_signals": "Normal: Normal performance counters. Fault: High cache miss rates or bottlenecks."
            },
            "netstat": {
                "purpose": "Network statistics and connection information",
                "used_for": "Network troubleshooting, connection analysis, performance monitoring",
                "key_info": "TCP/UDP connections, listening ports, network statistics",
                "category": "debug",
                "escalation": "MEDIUM",
                "correlation_targets": ["interfaces", "bgp", "ss"],
                "diagnostic_signals": "Normal: Normal connection states. Fault: High connection counts or errors."
            },
            "iostat": {
                "purpose": "I/O and virtual memory statistics",
                "used_for": "Performance monitoring, I/O analysis, memory paging analysis",
                "key_info": "Disk throughput, memory paging, CPU utilization, I/O wait",
                "category": "debug",
                "escalation": "MEDIUM",
                "correlation_targets": ["top", "free", "vmstat"],
                "diagnostic_signals": "Normal: Normal I/O patterns. Fault: High I/O wait or paging rates."
            }
        }
    
    def extract_archive(self, archive_path: str) -> str:
        """Extract showtech archive to temporary directory"""
        self.temp_dir = tempfile.mkdtemp(prefix="sonic_file_intelligence_")
        
        print(f"Extracting {archive_path} to {self.temp_dir}")
        
        try:
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(self.temp_dir)
            return self.temp_dir
        except Exception as e:
            print(f"Archive extraction failed: {e}")
            raise
    
    def match_file_intelligence(self, file_path: str) -> dict:
        """Match file path to intelligence database"""
        file_path_lower = file_path.lower()
        
        # Direct matches
        for key, intelligence in self.file_intelligence.items():
            if key in file_path_lower:
                return intelligence
        
        # Pattern matches
        patterns = {
            "version": ["version", "show version"],
            "platform": ["platform", "show platform", "chassis"],
            "inventory": ["inventory", "show inventory"],
            "environment": ["environment", "show environment", "temp", "fan", "psu"],
            "interfaces": ["interface", "show interface", "port"],
            "counters": ["counter", "show interface counter"],
            "lldp": ["lldp", "show lldp"],
            "mac": ["mac", "show mac", "address-table"],
            "bgp": ["bgp", "show bgp"],
            "ospf": ["ospf", "show ospf"],
            "route": ["route", "show ip route", "show route"],
            "docker ps": ["docker ps", "docker_ps"],
            "docker stats": ["docker stats", "docker_stats"],
            "docker logs": ["docker log", "docker_log"],
            "systemctl": ["systemctl", "service"],
            "ps": ["ps", "process"],
            "top": ["top"],
            "free": ["free", "memory"],
            "meminfo": ["meminfo", "proc/meminfo"],
            "config_db.json": ["config_db", "config.json"],
            "running-config": ["running-config", "running_config"],
            "startup-config": ["startup-config", "startup_config"],
            "syslog": ["syslog", "messages"],
            "kern.log": ["kern.log", "kernel"],
            "dmesg": ["dmesg"],
            "auth.log": ["auth.log", "secure"],
            "sensors": ["sensors", "temp", "thermal"],
            "ethtool": ["ethtool"],
            "lspci": ["lspci", "pci"],
            "core": ["core", "coredump"],
            "gdb": ["gdb", "debug"],
            "perf": ["perf"],
            "netstat": ["netstat", "ss"],
            "iostat": ["iostat", "vmstat"]
        }
        
        for pattern_key, pattern_list in patterns.items():
            for pattern in pattern_list:
                if pattern in file_path_lower:
                    return self.file_intelligence[pattern_key]
        
        # Default intelligence for unknown files
        return {
            "purpose": "Unknown file - requires manual analysis",
            "used_for": "General troubleshooting and analysis",
            "key_info": "File content analysis required",
            "category": "unknown",
            "escalation": "LOW",
            "correlation_targets": ["syslog", "config"],
            "diagnostic_signals": "Normal: Content readable. Fault: Empty or corrupted file."
        }
    
    def analyze_file_content(self, file_path: str, full_path: str) -> dict:
        """Analyze file content for additional intelligence"""
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1000)  # Read first 1000 chars
            
            content_lower = content.lower()
            
            # Detect issues in content
            issues = []
            if any(term in content_lower for term in ['error', 'fail', 'critical', 'panic']):
                issues.append("error_messages")
            if any(term in content_lower for term in ['down', 'offline', 'inactive']):
                issues.append("status_issues")
            if any(term in content_lower for term in ['warning', 'alert']):
                issues.append("warnings")
            if any(term in content_lower for term in ['timeout', 'slow', 'degraded']):
                issues.append("performance_issues")
            
            # Content summary
            lines = content.split('\n')
            return {
                "content_summary": f"{len(lines)} lines, {len(content)} characters",
                "issues_detected": issues,
                "has_errors": "error" in content_lower or "fail" in content_lower,
                "has_warnings": "warning" in content_lower or "alert" in content_lower
            }
            
        except Exception as e:
            return {
                "content_summary": f"Error reading file: {e}",
                "issues_detected": ["read_error"],
                "has_errors": True,
                "has_warnings": False
            }
    
    def generate_file_intelligence_report(self, archive_path: str) -> dict:
        """Generate comprehensive file intelligence report"""
        print("=== SONiC File Intelligence Analysis ===")
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
            
            print("Analyzing files...")
            
            for root, dirs, files in os.walk(extracted_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, extracted_path)
                    
                    # Get file intelligence
                    intelligence = self.match_file_intelligence(relative_path)
                    
                    # Analyze content
                    content_analysis = self.analyze_file_content(relative_path, file_path)
                    
                    # Create file entry
                    file_entry = {
                        "file_path": relative_path,
                        "intelligence": intelligence,
                        "content_analysis": content_analysis,
                        "priority": intelligence["escalation"]
                    }
                    
                    file_analysis.append(file_entry)
                    
                    # Update categories
                    category = intelligence["category"]
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(file_entry)
                    
                    # Update escalation summary
                    escalation_summary[intelligence["escalation"]] += 1
            
            # Sort files by priority
            file_analysis.sort(key=lambda x: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}[x["priority"]])
            
            print(f"Analysis complete: {len(file_analysis)} files analyzed")
            print()
            
            # Display summary
            print("=== FILE INTELLIGENCE SUMMARY ===")
            print(f"Total Files: {len(file_analysis)}")
            print(f"Categories: {len(categories)}")
            print()
            
            print("Priority Distribution:")
            for priority, count in escalation_summary.items():
                if count > 0:
                    print(f"  {priority}: {count} files")
            print()
            
            print("Categories:")
            for category, files in categories.items():
                print(f"  {category}: {len(files)} files")
            print()
            
            # Display high-priority files
            print("=== HIGH PRIORITY FILES ===")
            high_priority_files = [f for f in file_analysis if f["priority"] in ["CRITICAL", "HIGH"]]
            for file_entry in high_priority_files[:10]:  # Top 10
                intel = file_entry["intelligence"]
                content = file_entry["content_analysis"]
                
                print(f"File: {file_entry['file_path']}")
                print(f"  Purpose: {intel['purpose']}")
                print(f"  Priority: {file_entry['priority']}")
                print(f"  Used For: {intel['used_for']}")
                if content['issues_detected']:
                    print(f"  Issues: {', '.join(content['issues_detected'])}")
                print()
            
            # Save detailed report
            report = {
                "analysis_metadata": {
                    "archive_path": archive_path,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "total_files": len(file_analysis),
                    "categories": list(categories.keys()),
                    "escalation_summary": escalation_summary
                },
                "file_analysis": file_analysis,
                "categories": {k: [{"file_path": f["file_path"], "priority": f["priority"]} for f in v] for k, v in categories.items()},
                "high_priority_files": [f["file_path"] for f in high_priority_files],
                "correlation_matrix": self.generate_correlation_matrix(file_analysis)
            }
            
            # Save report
            self.save_intelligence_report(report, archive_path)
            
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
    
    def generate_correlation_matrix(self, file_analysis: list) -> dict:
        """Generate correlation matrix between files"""
        correlations = {}
        
        for file_entry in file_analysis:
            file_path = file_entry["file_path"]
            targets = file_entry["intelligence"]["correlation_targets"]
            correlations[file_path] = targets
        
        return correlations
    
    def save_intelligence_report(self, report: dict, archive_path: str):
        """Save intelligence report to files"""
        output_dir = os.path.dirname(os.path.abspath(__file__))
        archive_name = os.path.basename(archive_path).replace('.tar.gz', '')
        
        # Create analysis folder
        analysis_dir = os.path.join(output_dir, f"file_intelligence_{archive_name}")
        os.makedirs(analysis_dir, exist_ok=True)
        
        # Save JSON report
        json_file = os.path.join(analysis_dir, "file_intelligence_report.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print(f"Intelligence report saved: {json_file}")
        
        # Save markdown summary
        md_file = os.path.join(analysis_dir, "file_intelligence_summary.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# SONiC File Intelligence Analysis\n\n")
            f.write(f"**Archive:** {archive_name}\n")
            f.write(f"**Analysis Time:** {report['analysis_metadata']['analysis_timestamp']}\n")
            f.write(f"**Total Files:** {report['analysis_metadata']['total_files']}\n\n")
            
            f.write("## Priority Distribution\n\n")
            for priority, count in report['analysis_metadata']['escalation_summary'].items():
                if count > 0:
                    f.write(f"- **{priority}:** {count} files\n")
            f.write("\n")
            
            f.write("## Categories\n\n")
            for category in report['analysis_metadata']['categories']:
                f.write(f"- **{category}**\n")
            f.write("\n")
            
            f.write("## High Priority Files\n\n")
            for file_path in report['high_priority_files'][:20]:
                f.write(f"- `{file_path}`\n")
            f.write("\n")
            
            f.write("## Detailed File Analysis\n\n")
            for file_entry in report['file_analysis']:
                intel = file_entry["intelligence"]
                content = file_entry["content_analysis"]
                
                f.write(f"### {file_entry['file_path']}\n")
                f.write(f"**Purpose:** {intel['purpose']}\n")
                f.write(f"**Used For:** {intel['used_for']}\n")
                f.write(f"**Priority:** {file_entry['priority']}\n")
                f.write(f"**Category:** {intel['category']}\n")
                f.write(f"**Key Info:** {intel['key_info']}\n")
                f.write(f"**Content Summary:** {content['content_summary']}\n")
                
                if content['issues_detected']:
                    f.write(f"**Issues Detected:** {', '.join(content['issues_detected'])}\n")
                
                f.write(f"**Correlation Targets:** {', '.join(intel['correlation_targets'])}\n")
                f.write(f"**Diagnostic Signals:** {intel['diagnostic_signals']}\n\n")
        
        print(f"Intelligence summary saved: {md_file}")
        
        # Save correlation matrix
        correlation_file = os.path.join(analysis_dir, "correlation_matrix.json")
        with open(correlation_file, 'w', encoding='utf-8') as f:
            json.dump(report['correlation_matrix'], f, indent=2)
        print(f"Correlation matrix saved: {correlation_file}")
        
        print(f"\nAll intelligence reports saved in: {analysis_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sonic_file_intelligence_analyzer.py <showtech_archive.tar.gz>")
        sys.exit(1)
    
    archive_path = sys.argv[1]
    
    if not os.path.exists(archive_path):
        print(f"Error: Archive file not found: {archive_path}")
        sys.exit(1)
    
    # Run file intelligence analysis
    analyzer = SONiCFileIntelligenceAnalyzer()
    result = analyzer.generate_file_intelligence_report(archive_path)
    
    if result and 'error' not in result:
        print("\n=== FILE INTELLIGENCE ANALYSIS COMPLETE ===")
        print("File intelligence analysis completed successfully.")
        print("Reports generated:")
        print("  - file_intelligence_report.json")
        print("  - file_intelligence_summary.md")
        print("  - correlation_matrix.json")
    else:
        print("\n=== ANALYSIS FAILED ===")
        print("Please check the error message above.")