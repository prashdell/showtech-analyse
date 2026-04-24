#!/usr/bin/env python3
"""
Enhanced SONiC Analyzer for Deep Technical Consultants
Provides detailed, actionable insights for expert users
"""

import os
import sys
import json
import shutil
import re
from pathlib import Path
from datetime import datetime

# Import showtech extractor integration
sys.path.insert(0, str(Path(__file__).parent))
from showtech_extractor_integration import extract_showtech_archive

class EnhancedSONiCAnalyzer:
    """Deep analysis for technical consultants"""
    
    def __init__(self):
        self.workspace = Path(__file__).parent.parent
        self.skills_dir = self.workspace / "skills"
        self.data_dir = self.workspace / "data"
        self.knowledge_dir = self.workspace / "knowledge"
        
        # Load intelligence
        self.intelligence = self._load_intelligence()
        self.skill_registry = self._load_skill_registry()
        
    def analyze(self, showtech_file):
        """Deep technical analysis"""
        print("=== Enhanced SONiC Technical Analysis ===")
        print(f"Archive: {showtech_file}")
        print(f"Analysis Time: {datetime.now().isoformat()}")
        print()
        
        # Extract and analyze
        temp_dir = self._extract(showtech_file)
        file_inventory = self._inventory_files(temp_dir)
        
        # Deep analysis
        analysis_results = self._deep_analysis(temp_dir, file_inventory)
        
        # Generate detailed report
        self._generate_technical_report(analysis_results, showtech_file)
        
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
        
    def _load_intelligence(self):
        """Load SNC intelligence"""
        try:
            with open(self.data_dir / "sonic_persistent_memory.json", 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _load_skill_registry(self):
        """Load skill registry"""
        try:
            with open(self.skills_dir / "sonic_skill_registry.json", 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _extract(self, showtech_file):
        """Extract archive using show_tech_extractor skill"""
        print(f"Extracting {showtech_file} using show_tech_extractor skill...")
        
        # Use the showtech extractor integration
        extraction_result = extract_showtech_archive(showtech_file)
        
        if extraction_result['success']:
            self.temp_dir = extraction_result['output_dir']
            print(f"Extraction completed using {extraction_result['method']}")
            
            # Store extracted data properly - the actual extracted content is in 'extracted_data' key
            if 'extracted_data' in extraction_result:
                self.extracted_data = extraction_result['extracted_data']
            else:
                self.extracted_data = extraction_result  # Fallback to the result itself
            
            return self.temp_dir
        else:
            raise Exception(f"Extraction failed: {extraction_result.get('error', 'Unknown error')}")
    
    def _inventory_files(self, temp_dir):
        """Detailed file inventory"""
        inventory = {
            'total_files': 0,
            'file_types': {},
            'directories': [],
            'key_files': {}
        }
        
        for root, dirs, files in os.walk(temp_dir):
            inventory['directories'].append(root)
            
            for file in files:
                inventory['total_files'] += 1
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1]
                
                if file_ext not in inventory['file_types']:
                    inventory['file_types'][file_ext] = []
                inventory['file_types'][file_ext].append(file_path)
                
                # Identify key files
                if any(keyword in file.lower() for keyword in ['asic', 'memory', 'interface', 'bgp', 'docker']):
                    inventory['key_files'][file] = file_path
        
        return inventory
    
    def _deep_analysis(self, temp_dir, file_inventory):
        """Perform deep technical analysis"""
        results = {
            'system_overview': self._analyze_system_overview(temp_dir),
            'memory_analysis': self._deep_memory_analysis(temp_dir),
            'interface_analysis': self._deep_interface_analysis(temp_dir),
            'container_analysis': self._deep_container_analysis(temp_dir),
            'bgp_analysis': self._deep_bgp_analysis(temp_dir),
            'log_analysis': self._deep_log_analysis(temp_dir),
            'performance_indicators': self._analyze_performance_indicators(temp_dir),
            'configuration_review': self._analyze_configuration(temp_dir),
            'security_assessment': self._analyze_security(temp_dir),
            'recommendations': []
        }
        
        return results
    
    def _analyze_system_overview(self, temp_dir):
        """System overview analysis using show_tech_extractor skill data"""
        overview = {
            'hostname': 'Unknown',
            'sonic_version': 'Unknown',
            'platform': 'Unknown',
            'uptime': 'Unknown',
            'kernel_version': 'Unknown',
            'source': 'enhanced_analyzer_builtin'
        }
        
        # Try to use show_tech_extractor extracted data if available
        if hasattr(self, 'extracted_data') and self.extracted_data:
            try:
                # If extracted_data has system_info from fixed show_tech_extractor
                if isinstance(self.extracted_data, dict) and 'system_info' in self.extracted_data:
                    system_info = self.extracted_data['system_info']
                    overview.update({
                        'hostname': system_info.get('hostname', 'Unknown'),
                        'sonic_version': system_info.get('sonic_version', 'Unknown'),
                        'platform': system_info.get('platform', 'Unknown'),
                        'uptime': system_info.get('uptime', 'Unknown'),
                        'kernel_version': system_info.get('kernel_version', 'Unknown'),
                        'source': 'fixed_show_tech_extractor_system_parser'
                    })
                    return overview
                
                # If extracted_data is the full result from fixed extractor
                elif isinstance(self.extracted_data, dict) and 'extracted_data' in self.extracted_data:
                    extracted_content = self.extracted_data['extracted_data']
                    if 'system_info' in extracted_content:
                        system_info = extracted_content['system_info']
                        overview.update({
                            'hostname': system_info.get('hostname', 'Unknown'),
                            'sonic_version': system_info.get('sonic_version', 'Unknown'),
                            'platform': system_info.get('platform', 'Unknown'),
                            'uptime': system_info.get('uptime', 'Unknown'),
                            'kernel_version': system_info.get('kernel_version', 'Unknown'),
                            'load_average': system_info.get('load_average', 'Unknown'),
                            'source': 'fixed_show_tech_extractor_system_parser'
                        })
                        return overview
                
                # If extracted_data has get_system_info method (from original show_tech_extractor)
                elif hasattr(self.extracted_data, 'get_system_info'):
                    system_info = self.extracted_data.get_system_info()
                    overview.update({
                        'hostname': system_info.get('hostname', 'Unknown'),
                        'sonic_version': system_info.get('sonic_version', 'Unknown'),
                        'platform': system_info.get('platform', 'Unknown'),
                        'uptime': system_info.get('uptime', 'Unknown'),
                        'kernel_version': system_info.get('kernel_version', 'Unknown'),
                        'source': 'show_tech_extractor_system_parser'
                    })
                    return overview
                    
            except Exception as e:
                print(f"Warning: Could not use show_tech_extractor system data: {e}")
                print(f"Extracted data keys: {list(self.extracted_data.keys()) if isinstance(self.extracted_data, dict) else 'Not a dict'}")
        
        # Fallback to basic file parsing (current implementation)
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        content = f.read()
                        
                        # Extract system info
                        if 'version' in file.lower():
                            if 'SONiC' in content:
                                overview['sonic_version'] = self._extract_version(content)
                        
                        if 'hostname' in file.lower() or 'host' in file.lower():
                            hostname_match = re.search(r'hostname\s+([^\s\n]+)', content, re.IGNORECASE)
                            if hostname_match:
                                overview['hostname'] = hostname_match.group(1)
                        
                        if 'kernel' in file.lower():
                            kernel_match = re.search(r'Linux\s+[^\s]+\s+([0-9]+\.[0-9]+\.[0-9]+)', content)
                            if kernel_match:
                                overview['kernel_version'] = kernel_match.group(1)
                            
                except:
                    continue
        
        return overview
    
    def _deep_memory_analysis(self, temp_dir):
        """Detailed memory analysis"""
        memory_info = {
            'total_memory': 'Unknown',
            'available_memory': 'Unknown',
            'memory_usage': {},
            'oom_events': [],
            'high_memory_processes': [],
            'memory_pressure_indicators': []
        }
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if any(keyword in file.lower() for keyword in ['memory', 'meminfo', 'free', 'vmstat']):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            
                            # Parse memory info
                            if 'MemTotal' in content:
                                memtotal_match = re.search(r'MemTotal:\s+(\d+)', content)
                                if memtotal_match:
                                    memory_info['total_memory'] = f"{int(memtotal_match.group(1)) // 1024}MB"
                            
                            if 'MemAvailable' in content:
                                memavail_match = re.search(r'MemAvailable:\s+(\d+)', content)
                                if memavail_match:
                                    memory_info['available_memory'] = f"{int(memavail_match.group(1)) // 1024}MB"
                            
                            # Look for OOM events
                            if 'oom' in content.lower() or 'out of memory' in content.lower():
                                lines = content.split('\n')
                                for i, line in enumerate(lines):
                                    if 'oom' in line.lower():
                                        memory_info['oom_events'].append({
                                            'line': i+1,
                                            'content': line.strip()
                                        })
                            
                            # High memory processes
                            if '%' in content and 'memory' in content.lower():
                                proc_matches = re.findall(r'(\w+)\s+(\d+)%\s+memory', content, re.IGNORECASE)
                                for proc, usage in proc_matches:
                                    if int(usage) > 80:
                                        memory_info['high_memory_processes'].append({
                                            'process': proc,
                                            'usage': f"{usage}%"
                                        })
                    
                    except:
                        continue
        
        return memory_info
    
    def _deep_interface_analysis(self, temp_dir):
        """Detailed interface analysis"""
        interface_info = {
            'total_interfaces': 0,
            'up_interfaces': [],
            'down_interfaces': [],
            'flapping_interfaces': [],
            'error_interfaces': [],
            'interface_details': {}
        }
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if any(keyword in file.lower() for keyword in ['interface', 'port', 'ethernet', 'bgp']):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            
                            # Parse interface states
                            interface_lines = content.split('\n')
                            for line in interface_lines:
                                if 'Ethernet' in line or 'eth' in line.lower():
                                    interface_info['total_interfaces'] += 1
                                    
                                    if 'up' in line.lower() and 'down' not in line.lower():
                                        interface_info['up_interfaces'].append(line.strip())
                                    elif 'down' in line.lower():
                                        interface_info['down_interfaces'].append(line.strip())
                                    
                                    if 'error' in line.lower() or 'crc' in line.lower():
                                        interface_info['error_interfaces'].append(line.strip())
                                    
                                    if 'flap' in line.lower():
                                        interface_info['flapping_interfaces'].append(line.strip())
                    
                    except:
                        continue
        
        return interface_info
    
    def _deep_container_analysis(self, temp_dir):
        """Detailed container analysis"""
        container_info = {
            'total_containers': 0,
            'running_containers': [],
            'stopped_containers': [],
            'unhealthy_containers': [],
            'container_details': {}
        }
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if 'docker' in file.lower() or 'container' in file.lower():
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            
                            # Parse container states
                            lines = content.split('\n')
                            for line in lines:
                                if any(container in line for container in ['swss', 'syncd', 'bgp', 'teamd', 'snmp']):
                                    container_info['total_containers'] += 1
                                    
                                    if 'up' in line.lower() or 'running' in line.lower():
                                        container_info['running_containers'].append(line.strip())
                                    elif 'exit' in line.lower() or 'dead' in line.lower():
                                        container_info['stopped_containers'].append(line.strip())
                                    
                                    if 'unhealthy' in line.lower():
                                        container_info['unhealthy_containers'].append(line.strip())
                    
                    except:
                        continue
        
        return container_info
    
    def _deep_bgp_analysis(self, temp_dir):
        """Detailed BGP analysis"""
        bgp_info = {
            'bgp_neighbors': [],
            'established_sessions': [],
            'failed_sessions': [],
            'bgp_errors': []
        }
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if 'bgp' in file.lower():
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            
                            # Parse BGP neighbor info
                            if 'neighbor' in content.lower():
                                neighbor_matches = re.findall(r'(\d+\.\d+\.\d+\.\d+)', content)
                                bgp_info['bgp_neighbors'].extend(neighbor_matches)
                            
                            if 'established' in content.lower():
                                bgp_info['established_sessions'].append('BGP session established')
                            
                            if 'idle' in content.lower() or 'active' in content.lower():
                                bgp_info['failed_sessions'].append('BGP session not established')
                    
                    except:
                        continue
        
        return bgp_info
    
    def _deep_log_analysis(self, temp_dir):
        """Detailed log analysis"""
        log_info = {
            'critical_errors': [],
            'warning_messages': [],
            'reboot_events': [],
            'service_failures': [],
            'error_patterns': {}
        }
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.lower().endswith('.log'):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            lines = f.readlines()
                            
                            for i, line in enumerate(lines):
                                line_lower = line.lower()
                                
                                if 'critical' in line_lower or 'fatal' in line_lower:
                                    log_info['critical_errors'].append({
                                        'file': file,
                                        'line': i+1,
                                        'content': line.strip()
                                    })
                                
                                if 'warning' in line_lower or 'warn' in line_lower:
                                    log_info['warning_messages'].append({
                                        'file': file,
                                        'line': i+1,
                                        'content': line.strip()
                                    })
                                
                                if 'reboot' in line_lower or 'restart' in line_lower:
                                    log_info['reboot_events'].append({
                                        'file': file,
                                        'line': i+1,
                                        'content': line.strip()
                                    })
                    
                    except:
                        continue
        
        return log_info
    
    def _analyze_performance_indicators(self, temp_dir):
        """Analyze performance indicators"""
        performance = {
            'cpu_load': 'Unknown',
            'disk_usage': 'Unknown',
            'network_throughput': 'Unknown',
            'process_count': 'Unknown'
        }
        
        # Look for performance data
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if any(keyword in file.lower() for keyword in ['load', 'cpu', 'top', 'ps']):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            
                            # Parse load average
                            load_match = re.search(r'load average:\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)', content)
                            if load_match:
                                performance['cpu_load'] = f"{load_match.group(1)}, {load_match.group(2)}, {load_match.group(3)}"
                    
                    except:
                        continue
        
        return performance
    
    def _analyze_configuration(self, temp_dir):
        """Configuration analysis"""
        config = {
            'config_files': [],
            'potential_issues': [],
            'best_practices': []
        }
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if any(ext in file.lower() for ext in ['.conf', '.cfg', '.json', 'config']):
                    config['config_files'].append(file)
        
        return config
    
    def _analyze_security(self, temp_dir):
        """Security assessment"""
        security = {
            'open_ports': [],
            'user_accounts': [],
            'security_events': []
        }
        
        return security
    
    def _extract_version(self, content):
        """Extract SONiC version"""
        version_match = re.search(r'SONiC\s+([0-9]+\.[0-9]+)', content)
        return version_match.group(1) if version_match else 'Unknown'
    
    def _generate_technical_report(self, results, showtech_file):
        """Generate detailed technical report"""
        print("\n" + "="*80)
        print("TECHNICAL ANALYSIS REPORT")
        print("="*80)
        
        # System Overview
        print("\n1. SYSTEM OVERVIEW")
        print("-" * 40)
        overview = results['system_overview']
        for key, value in overview.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        # Memory Analysis
        print("\n2. MEMORY ANALYSIS")
        print("-" * 40)
        memory = results['memory_analysis']
        print(f"Total Memory: {memory['total_memory']}")
        print(f"Available Memory: {memory['available_memory']}")
        
        if memory['oom_events']:
            print(f"\nOOM Events ({len(memory['oom_events'])}):")
            for event in memory['oom_events'][:3]:
                print(f"  Line {event['line']}: {event['content']}")
        
        if memory['high_memory_processes']:
            print(f"\nHigh Memory Processes:")
            for proc in memory['high_memory_processes']:
                print(f"  {proc['process']}: {proc['usage']}")
        
        # Interface Analysis
        print("\n3. INTERFACE ANALYSIS")
        print("-" * 40)
        interfaces = results['interface_analysis']
        print(f"Total Interfaces: {interfaces['total_interfaces']}")
        print(f"Up Interfaces: {len(interfaces['up_interfaces'])}")
        print(f"Down Interfaces: {len(interfaces['down_interfaces'])}")
        
        if interfaces['down_interfaces']:
            print(f"\nDown Interfaces:")
            for intf in interfaces['down_interfaces'][:5]:
                print(f"  {intf}")
        
        if interfaces['error_interfaces']:
            print(f"\nInterfaces with Errors:")
            for intf in interfaces['error_interfaces'][:5]:
                print(f"  {intf}")
        
        # Container Analysis
        print("\n4. CONTAINER ANALYSIS")
        print("-" * 40)
        containers = results['container_analysis']
        print(f"Total Containers: {containers['total_containers']}")
        print(f"Running: {len(containers['running_containers'])}")
        print(f"Stopped: {len(containers['stopped_containers'])}")
        
        if containers['stopped_containers']:
            print(f"\nStopped Containers:")
            for container in containers['stopped_containers']:
                print(f"  {container}")
        
        # BGP Analysis
        print("\n5. BGP ANALYSIS")
        print("-" * 40)
        bgp = results['bgp_analysis']
        print(f"BGP Neighbors: {len(bgp['bgp_neighbors'])}")
        print(f"Established Sessions: {len(bgp['established_sessions'])}")
        print(f"Failed Sessions: {len(bgp['failed_sessions'])}")
        
        # Log Analysis
        print("\n6. LOG ANALYSIS")
        print("-" * 40)
        logs = results['log_analysis']
        print(f"Critical Errors: {len(logs['critical_errors'])}")
        print(f"Warnings: {len(logs['warning_messages'])}")
        print(f"Reboot Events: {len(logs['reboot_events'])}")
        
        if logs['critical_errors']:
            print(f"\nCritical Errors:")
            for error in logs['critical_errors'][:3]:
                print(f"  {error['file']}:{error['line']} - {error['content']}")
        
        # Performance Indicators
        print("\n7. PERFORMANCE INDICATORS")
        print("-" * 40)
        perf = results['performance_indicators']
        for key, value in perf.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        # Recommendations
        print("\n8. TECHNICAL RECOMMENDATIONS")
        print("-" * 40)
        recommendations = self._generate_recommendations(results)
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")
        else:
            print("No specific recommendations - system appears healthy")
        
        # COMPREHENSIVE DETAILS SECTION
        print("\n" + "="*80)
        print("COMPREHENSIVE TECHNICAL DETAILS")
        print("="*80)
        
        self._display_comprehensive_details(results)
        
        # Save detailed report
        self._save_detailed_report(results, showtech_file)
    
    def _display_comprehensive_details(self, results):
        """Display comprehensive technical details for consultants"""
        
        # Detailed Memory Analysis
        print("\n9.1 DETAILED MEMORY ANALYSIS")
        print("-" * 50)
        memory = results['memory_analysis']
        
        # Memory calculations
        if memory['total_memory'] != 'Unknown' and memory['available_memory'] != 'Unknown':
            try:
                total_mb = int(re.findall(r'\d+', memory['total_memory'])[0])
                avail_mb = int(re.findall(r'\d+', memory['available_memory'])[0])
                used_mb = total_mb - avail_mb
                usage_percent = (used_mb / total_mb) * 100
                
                print(f"Memory Utilization: {usage_percent:.1f}% ({used_mb}MB/{total_mb}MB)")
                print(f"Memory Pressure: {'HIGH' if usage_percent > 80 else 'MEDIUM' if usage_percent > 60 else 'LOW'}")
            except:
                print("Memory calculations: Unable to parse values")
        
        if memory['oom_events']:
            print(f"\nOOM Kill Analysis:")
            for event in memory['oom_events']:
                print(f"  Event: {event['content']}")
                print(f"  Location: Line {event['line']}")
        
        # Detailed Interface Analysis
        print("\n9.2 DETAILED INTERFACE ANALYSIS")
        print("-" * 50)
        interfaces = results['interface_analysis']
        
        if interfaces['total_interfaces'] > 0:
            up_count = len(interfaces['up_interfaces'])
            down_count = len(interfaces['down_interfaces'])
            health_percentage = (up_count / interfaces['total_interfaces']) * 100
            
            print(f"Interface Health: {health_percentage:.1f}% ({up_count}/{interfaces['total_interfaces']} up)")
            print(f"Interface Failure Rate: {(down_count/interfaces['total_interfaces'])*100:.1f}%")
            
            if interfaces['down_interfaces']:
                print(f"\nDown Interface Details:")
                for i, intf in enumerate(interfaces['down_interfaces'][:10], 1):
                    print(f"  {i}. {intf}")
                if len(interfaces['down_interfaces']) > 10:
                    print(f"  ... and {len(interfaces['down_interfaces']) - 10} more")
            
            if interfaces['error_interfaces']:
                print(f"\nInterface Error Details:")
                for i, error in enumerate(interfaces['error_interfaces'][:10], 1):
                    print(f"  {i}. {error}")
                if len(interfaces['error_interfaces']) > 10:
                    print(f"  ... and {len(interfaces['error_interfaces']) - 10} more")
        
        # Detailed Container Analysis
        print("\n9.3 DETAILED CONTAINER ANALYSIS")
        print("-" * 50)
        containers = results['container_analysis']
        
        if containers['total_containers'] > 0:
            running = len(containers['running_containers'])
            stopped = len(containers['stopped_containers'])
            health_percentage = (running / containers['total_containers']) * 100
            
            print(f"Container Health: {health_percentage:.1f}% ({running}/{containers['total_containers']} running)")
            print(f"Container Failure Rate: {(stopped/containers['total_containers'])*100:.1f}%")
            
            if containers['stopped_containers']:
                print(f"\nStopped Container Analysis:")
                for container in containers['stopped_containers']:
                    print(f"  Event: {container}")
        
        # Detailed BGP Analysis
        print("\n9.4 DETAILED BGP ANALYSIS")
        print("-" * 50)
        bgp = results['bgp_analysis']
        
        if bgp['bgp_neighbors']:
            print(f"BGP Neighbor Details:")
            for i, neighbor in enumerate(bgp['bgp_neighbors'], 1):
                print(f"  Neighbor {i}: {neighbor}")
        
        session_count = len(bgp['established_sessions']) + len(bgp['failed_sessions'])
        if session_count > 0:
            success_rate = (len(bgp['established_sessions']) / session_count) * 100
            print(f"BGP Session Success Rate: {success_rate:.1f}%")
        
        # Detailed Log Analysis
        print("\n9.5 DETAILED LOG ANALYSIS")
        print("-" * 50)
        logs = results['log_analysis']
        
        total_log_issues = len(logs['critical_errors']) + len(logs['warning_messages']) + len(logs['reboot_events'])
        print(f"Total Log Issues: {total_log_issues}")
        
        if logs['critical_errors']:
            print(f"\nCritical Error Analysis:")
            for error in logs['critical_errors'][:5]:
                print(f"  File: {error['file']}")
                print(f"  Line: {error['line']}")
                print(f"  Content: {error['content']}")
                print()
        
        if logs['reboot_events']:
            print(f"System Reboot Events: {len(logs['reboot_events'])}")
            print("System Stability: POOR" if len(logs['reboot_events']) > 10 else "MODERATE" if len(logs['reboot_events']) > 0 else "GOOD")
        
        # Performance Analysis
        print("\n9.6 DETAILED PERFORMANCE ANALYSIS")
        print("-" * 50)
        perf = results['performance_indicators']
        
        if perf['cpu_load'] != 'Unknown':
            load_parts = perf['cpu_load'].split(', ')
            if len(load_parts) >= 3:
                print(f"CPU Load Averages:")
                print(f"  1-minute: {load_parts[0]}")
                print(f"  5-minute: {load_parts[1]}")
                print(f"  15-minute: {load_parts[2]}")
                
                try:
                    load_1 = float(load_parts[0])
                    print(f"CPU Load Status: {'HIGH' if load_1 > 2.0 else 'MEDIUM' if load_1 > 1.0 else 'LOW'}")
                except:
                    pass
        
        # Configuration Analysis
        print("\n9.7 CONFIGURATION ANALYSIS")
        print("-" * 50)
        config = results['configuration_review']
        
        print(f"Configuration Files Found: {len(config['config_files'])}")
        if config['config_files']:
            print("Configuration Files:")
            for cfg in config['config_files'][:10]:
                print(f"  {cfg}")
            if len(config['config_files']) > 10:
                print(f"  ... and {len(config['config_files']) - 10} more")
        
        # Security Assessment
        print("\n9.8 SECURITY ASSESSMENT")
        print("-" * 50)
        security = results['security_assessment']
        
        print(f"Open Ports: {len(security['open_ports'])}")
        print(f"User Accounts: {len(security['user_accounts'])}")
        print(f"Security Events: {len(security['security_events'])}")
        
        # System Health Summary
        print("\n9.9 SYSTEM HEALTH SUMMARY")
        print("-" * 50)
        
        # Calculate overall health score
        health_factors = {
            'memory': self._calculate_memory_health(results['memory_analysis']),
            'interfaces': self._calculate_interface_health(results['interface_analysis']),
            'containers': self._calculate_container_health(results['container_analysis']),
            'bgp': self._calculate_bgp_health(results['bgp_analysis']),
            'logs': self._calculate_log_health(results['log_analysis'])
        }
        
        overall_health = sum(health_factors.values()) / len(health_factors)
        
        print(f"Component Health Scores:")
        for component, score in health_factors.items():
            status = "GOOD" if score >= 80 else "FAIR" if score >= 60 else "POOR"
            print(f"  {component.title()}: {score:.1f}% ({status})")
        
        print(f"\nOverall System Health: {overall_health:.1f}%")
        health_status = "HEALTHY" if overall_health >= 80 else "DEGRADED" if overall_health >= 60 else "CRITICAL"
        print(f"System Status: {health_status}")
    
    def _calculate_memory_health(self, memory_analysis):
        """Calculate memory health score"""
        if memory_analysis['oom_events']:
            return 30  # OOM events are critical
        # Simple heuristic - would be more sophisticated with real data
        return 70
    
    def _calculate_interface_health(self, interface_analysis):
        """Calculate interface health score"""
        total = interface_analysis['total_interfaces']
        if total == 0:
            return 100
        
        up = len(interface_analysis['up_interfaces'])
        return (up / total) * 100
    
    def _calculate_container_health(self, container_analysis):
        """Calculate container health score"""
        total = container_analysis['total_containers']
        if total == 0:
            return 100
        
        running = len(container_analysis['running_containers'])
        return (running / total) * 100
    
    def _calculate_bgp_health(self, bgp_analysis):
        """Calculate BGP health score"""
        total_sessions = len(bgp_analysis['established_sessions']) + len(bgp_analysis['failed_sessions'])
        if total_sessions == 0:
            return 100
        
        established = len(bgp_analysis['established_sessions'])
        return (established / total_sessions) * 100
    
    def _calculate_log_health(self, log_analysis):
        """Calculate log health score"""
        critical = len(log_analysis['critical_errors'])
        reboots = len(log_analysis['reboot_events'])
        
        if critical > 0:
            return 30
        elif reboots > 10:
            return 50
        elif reboots > 0:
            return 70
        else:
            return 90
    
    def _generate_recommendations(self, results):
        """Generate technical recommendations"""
        recommendations = []
        
        # Memory recommendations
        memory = results['memory_analysis']
        if memory['oom_events']:
            recommendations.append("CRITICAL: OOM events detected - investigate memory leaks and consider memory optimization")
        
        if memory['high_memory_processes']:
            recommendations.append("High memory usage detected - review process memory utilization")
        
        # Interface recommendations
        interfaces = results['interface_analysis']
        if interfaces['down_interfaces']:
            recommendations.append("Interface(s) down - check physical connections and configuration")
        
        if interfaces['error_interfaces']:
            recommendations.append("Interface errors detected - check for hardware issues or configuration problems")
        
        # Container recommendations
        containers = results['container_analysis']
        if containers['stopped_containers']:
            recommendations.append("Container(s) stopped - restart failed containers and check logs")
        
        # BGP recommendations
        bgp = results['bgp_analysis']
        if bgp['failed_sessions']:
            recommendations.append("BGP session issues - check BGP configuration and network connectivity")
        
        # Log recommendations
        logs = results['log_analysis']
        if logs['critical_errors']:
            recommendations.append("Critical errors in logs - immediate investigation required")
        
        return recommendations
    
    def _calculate_log_health(self, log_analysis):
        """Calculate log health score"""
        critical = len(log_analysis['critical_errors'])
        reboots = len(log_analysis['reboot_events'])
        
        if critical > 0:
            return 30
        elif reboots > 10:
            return 50
        elif reboots > 0:
            return 70
        else:
            return 90
        """Generate technical recommendations"""
        recommendations = []
        
        # Memory recommendations
        memory = results['memory_analysis']
        if memory['oom_events']:
            recommendations.append("CRITICAL: OOM events detected - investigate memory leaks and consider memory optimization")
        
        if memory['high_memory_processes']:
            recommendations.append("High memory usage detected - review process memory utilization")
        
        # Interface recommendations
        interfaces = results['interface_analysis']
        if interfaces['down_interfaces']:
            recommendations.append("Interface(s) down - check physical connections and configuration")
        
        if interfaces['error_interfaces']:
            recommendations.append("Interface errors detected - check for hardware issues or configuration problems")
        
        # Container recommendations
        containers = results['container_analysis']
        if containers['stopped_containers']:
            recommendations.append("Container(s) stopped - restart failed containers and check logs")
        
        # BGP recommendations
        bgp = results['bgp_analysis']
        if bgp['failed_sessions']:
            recommendations.append("BGP session issues - check BGP configuration and network connectivity")
        
        # Log recommendations
        logs = results['log_analysis']
        if logs['critical_errors']:
            recommendations.append("Critical errors in logs - immediate investigation required")
        
        return recommendations
    
    def _save_detailed_report(self, results, showtech_file):
        """Save detailed technical report"""
        # Create results directory
        archive_name = os.path.basename(showtech_file).replace('.tar.gz', '').replace('.tgz', '')
        results_dir = self.workspace / f"enhanced_analysis_{archive_name}"
        results_dir.mkdir(exist_ok=True)
        
        # Save comprehensive report
        report_file = results_dir / "enhanced_technical_report.json"
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save summary
        summary_file = results_dir / "technical_summary.md"
        with open(summary_file, 'w') as f:
            f.write("# Enhanced Technical Analysis Summary\n\n")
            f.write(f"Analysis Date: {datetime.now().isoformat()}\n")
            f.write(f"Archive: {showtech_file}\n\n")
            
            # Add key findings
            f.write("## Key Findings\n\n")
            
            memory = results['memory_analysis']
            if memory['oom_events']:
                f.write(f"- **CRITICAL**: {len(memory['oom_events'])} OOM events detected\n")
            
            interfaces = results['interface_analysis']
            if interfaces['down_interfaces']:
                f.write(f"- **WARNING**: {len(interfaces['down_interfaces'])} interfaces down\n")
            
            containers = results['container_analysis']
            if containers['stopped_containers']:
                f.write(f"- **WARNING**: {len(containers['stopped_containers'])} containers stopped\n")
        
        print(f"\nDetailed report saved: {report_file}")
        print(f"Technical summary saved: {summary_file}")
        print(f"All results in: {results_dir}")

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python enhanced_analyzer.py <showtech_file>")
        print()
        print("Example: python enhanced_analyzer.py sonic_dump.tar.gz")
        sys.exit(1)
    
    showtech_file = sys.argv[1]
    
    if not os.path.exists(showtech_file):
        print(f"File not found: {showtech_file}")
        sys.exit(1)
    
    analyzer = EnhancedSONiCAnalyzer()
    analyzer.analyze(showtech_file)

if __name__ == "__main__":
    main()