#!/usr/bin/env python3
"""
Fixed Show Tech Extractor - Handles relative imports properly
"""

import os
import sys
import tarfile
import zipfile
import tempfile
import json
from pathlib import Path
from datetime import datetime

class FixedShowTechExtractor:
    """Fixed version of ShowTechExtractor that handles import issues"""
    
    def __init__(self):
        self.skill_path = Path(r"C:\Users\Prasanth_Sasidharan\.codeium\windsurf\skills\show_tech_extractor")
        self.parsers_path = self.skill_path / "parsers"
        
    def extract(self, archive_path):
        """Extract showtech archive with proper parsing"""
        # Extract archive
        temp_dir = tempfile.mkdtemp(prefix="showtech_extracted_")
        
        try:
            if archive_path.endswith('.tar.gz') or archive_path.endswith('.tgz'):
                with tarfile.open(archive_path, 'r:gz') as tar:
                    tar.extractall(temp_dir)
            elif archive_path.endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            else:
                raise ValueError(f"Unsupported archive format: {archive_path}")
            
            # Parse extracted data
            parsed_data = self._parse_extracted_data(temp_dir)
            
            return {
                'success': True,
                'temp_dir': temp_dir,
                'system_info': parsed_data.get('system_info', {}),
                'docker_containers': parsed_data.get('docker_containers', {}),
                'network_config': parsed_data.get('network_config', {}),
                'interface_stats': parsed_data.get('interface_stats', {}),
                'process_info': parsed_data.get('process_info', {}),
                'log_data': parsed_data.get('log_data', {}),
                'file_inventory': parsed_data.get('file_inventory', {}),
                'extraction_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            # Clean up on error
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            return {
                'success': False,
                'error': str(e),
                'extraction_time': datetime.now().isoformat()
            }
    
    def _parse_extracted_data(self, temp_dir):
        """Parse the extracted showtech data"""
        parsed_data = {
            'system_info': {},
            'docker_containers': {},
            'network_config': {},
            'interface_stats': {},
            'process_info': {},
            'log_data': {},
            'file_inventory': {}
        }
        
        # Create file inventory
        file_inventory = self._create_file_inventory(temp_dir)
        parsed_data['file_inventory'] = file_inventory
        
        # Parse system information
        parsed_data['system_info'] = self._parse_system_info(temp_dir, file_inventory)
        
        # Parse docker containers
        parsed_data['docker_containers'] = self._parse_docker_containers(temp_dir, file_inventory)
        
        # Parse network configuration
        parsed_data['network_config'] = self._parse_network_config(temp_dir, file_inventory)
        
        # Parse interface statistics
        parsed_data['interface_stats'] = self._parse_interface_stats(temp_dir, file_inventory)
        
        # Parse process information
        parsed_data['process_info'] = self._parse_process_info(temp_dir, file_inventory)
        
        # Parse log data
        parsed_data['log_data'] = self._parse_log_data(temp_dir, file_inventory)
        
        return parsed_data
    
    def _create_file_inventory(self, temp_dir):
        """Create inventory of extracted files"""
        inventory = {
            'total_files': 0,
            'directories': [],
            'files': [],
            'file_types': {},
            'key_files': {}
        }
        
        for root, dirs, files in os.walk(temp_dir):
            inventory['directories'].append(root)
            
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, temp_dir)
                
                inventory['total_files'] += 1
                inventory['files'].append(rel_path)
                
                # File type analysis
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext not in inventory['file_types']:
                    inventory['file_types'][file_ext] = []
                inventory['file_types'][file_ext].append(rel_path)
                
                # Identify key files
                if any(keyword in file.lower() for keyword in 
                      ['asic', 'memory', 'interface', 'bgp', 'docker', 'log', 'config', 'version']):
                    inventory['key_files'][file] = rel_path
        
        return inventory
    
    def _parse_system_info(self, temp_dir, file_inventory):
        """Parse system information"""
        system_info = {
            'hostname': 'Unknown',
            'sonic_version': 'Unknown',
            'platform': 'Unknown',
            'uptime': 'Unknown',
            'kernel_version': 'Unknown',
            'load_average': 'Unknown'
        }
        
        # Look for system information files
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_lower = file.lower()
                
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        content = f.read()
                        
                        # Parse hostname
                        if 'hostname' in file_lower and system_info['hostname'] == 'Unknown':
                            import re
                            hostname_match = re.search(r'hostname\s*[:=\s]+([^\s\n]+)', content, re.IGNORECASE)
                            if hostname_match:
                                system_info['hostname'] = hostname_match.group(1)
                        
                        # Parse SONiC version
                        if 'version' in file_lower and 'sonic' in content.lower() and system_info['sonic_version'] == 'Unknown':
                            import re
                            version_match = re.search(r'SONiC\s*([0-9]+\.[0-9]+)', content)
                            if version_match:
                                system_info['sonic_version'] = version_match.group(1)
                        
                        # Parse kernel version
                        if 'kernel' in file_lower or 'linux' in file_lower and system_info['kernel_version'] == 'Unknown':
                            import re
                            kernel_match = re.search(r'Linux\s+[^\s]+\s+([0-9]+\.[0-9]+\.[0-9]+)', content)
                            if kernel_match:
                                system_info['kernel_version'] = kernel_match.group(1)
                        
                        # Parse load average
                        if 'load' in file_lower and system_info['load_average'] == 'Unknown':
                            import re
                            load_match = re.search(r'load average[:\s]*([0-9.]+),\s*([0-9.]+),\s*([0-9.]+)', content)
                            if load_match:
                                system_info['load_average'] = f"{load_match.group(1)}, {load_match.group(2)}, {load_match.group(3)}"
                        
                        # Parse uptime
                        if 'uptime' in file_lower and system_info['uptime'] == 'Unknown':
                            import re
                            uptime_match = re.search(r'up\s+([^,]+)', content, re.IGNORECASE)
                            if uptime_match:
                                system_info['uptime'] = uptime_match.group(1).strip()
                        
                except Exception:
                    continue
        
        return system_info
    
    def _parse_docker_containers(self, temp_dir, file_inventory):
        """Parse docker container information"""
        containers = {
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
                            lines = content.split('\n')
                            
                            for line in lines:
                                if any(container in line for container in ['swss', 'syncd', 'bgp', 'teamd', 'snmp', 'lldp']):
                                    containers['total_containers'] += 1
                                    
                                    if 'up' in line.lower() or 'running' in line.lower():
                                        containers['running_containers'].append(line.strip())
                                    elif 'exit' in line.lower() or 'dead' in line.lower() or 'stopped' in line.lower():
                                        containers['stopped_containers'].append(line.strip())
                                    
                                    if 'unhealthy' in line.lower():
                                        containers['unhealthy_containers'].append(line.strip())
                                    
                                    # Store container details
                                    container_name = self._extract_container_name(line)
                                    if container_name:
                                        containers['container_details'][container_name] = {
                                            'status': line.strip(),
                                            'file': file
                                        }
                    
                    except Exception:
                        continue
        
        return containers
    
    def _parse_network_config(self, temp_dir, file_inventory):
        """Parse network configuration"""
        network_config = {
            'interfaces': {},
            'bgp_config': {},
            'routing_tables': {},
            'vlans': {}
        }
        
        # Parse interface configurations
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if 'interface' in file.lower() or 'network' in file.lower():
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            
                            # Parse interface configurations
                            if 'interface' in content.lower():
                                lines = content.split('\n')
                                current_interface = None
                                
                                for line in lines:
                                    line = line.strip()
                                    if line.startswith('interface') or line.startswith('Ethernet'):
                                        current_interface = line.split()[-1]
                                        network_config['interfaces'][current_interface] = {
                                            'status': 'unknown',
                                            'description': '',
                                            'config_lines': []
                                        }
                                    elif current_interface and line:
                                        network_config['interfaces'][current_interface]['config_lines'].append(line)
                                        
                                        if 'shutdown' in line.lower():
                                            network_config['interfaces'][current_interface]['status'] = 'down'
                                        elif 'no shutdown' in line.lower():
                                            network_config['interfaces'][current_interface]['status'] = 'up'
                    
                    except Exception:
                        continue
        
        return network_config
    
    def _parse_interface_stats(self, temp_dir, file_inventory):
        """Parse interface statistics"""
        interface_stats = {
            'interface_counters': {},
            'error_counts': {},
            'link_status': {}
        }
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if 'interface' in file.lower() or 'port' in file.lower() or 'counter' in file.lower():
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            
                            # Parse interface statistics
                            lines = content.split('\n')
                            for line in lines:
                                if 'Ethernet' in line or 'eth' in line.lower():
                                    parts = line.split()
                                    if len(parts) >= 3:
                                        interface_name = parts[0]
                                        status = parts[2] if len(parts) > 2 else 'unknown'
                                        
                                        interface_stats['link_status'][interface_name] = {
                                            'status': status,
                                            'raw_line': line.strip()
                                        }
                                        
                                        # Count errors
                                        if 'error' in line.lower() or 'crc' in line.lower():
                                            if interface_name not in interface_stats['error_counts']:
                                                interface_stats['error_counts'][interface_name] = 0
                                            interface_stats['error_counts'][interface_name] += 1
                    
                    except Exception:
                        continue
        
        return interface_stats
    
    def _parse_process_info(self, temp_dir, file_inventory):
        """Parse process information"""
        process_info = {
            'running_processes': [],
            'cpu_usage': {},
            'memory_usage': {},
            'high_memory_processes': []
        }
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if 'process' in file.lower() or 'ps' in file.lower() or 'top' in file.lower():
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            
                            # Parse process information
                            lines = content.split('\n')
                            for line in lines:
                                if '%' in line and ('CPU' in line or 'MEM' in line or 'memory' in line.lower()):
                                    process_info['running_processes'].append(line.strip())
                                    
                                    # Extract high memory processes
                                    import re
                                    mem_match = re.search(r'(\w+)\s+(\d+)%\s+memory', line, re.IGNORECASE)
                                    if mem_match:
                                        process_name, mem_usage = mem_match.groups()
                                        if int(mem_usage) > 80:
                                            process_info['high_memory_processes'].append({
                                                'process': process_name,
                                                'memory_usage': f"{mem_usage}%",
                                                'full_line': line.strip()
                                            })
                    
                    except Exception:
                        continue
        
        return process_info
    
    def _parse_log_data(self, temp_dir, file_inventory):
        """Parse log data"""
        log_data = {
            'critical_errors': [],
            'warnings': [],
            'reboot_events': [],
            'service_failures': [],
            'error_patterns': {},
            'log_summary': {
                'total_log_files': 0,
                'total_errors': 0,
                'total_warnings': 0
            }
        }
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.lower().endswith('.log'):
                    log_data['log_summary']['total_log_files'] += 1
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            lines = f.readlines()
                            
                            for i, line in enumerate(lines):
                                line_lower = line.lower()
                                
                                if 'critical' in line_lower or 'fatal' in line_lower:
                                    log_data['critical_errors'].append({
                                        'file': file,
                                        'line': i+1,
                                        'content': line.strip()
                                    })
                                    log_data['log_summary']['total_errors'] += 1
                                
                                if 'warning' in line_lower or 'warn' in line_lower:
                                    log_data['warnings'].append({
                                        'file': file,
                                        'line': i+1,
                                        'content': line.strip()
                                    })
                                    log_data['log_summary']['total_warnings'] += 1
                                
                                if 'reboot' in line_lower or 'restart' in line_lower:
                                    log_data['reboot_events'].append({
                                        'file': file,
                                        'line': i+1,
                                        'content': line.strip()
                                    })
                    
                    except Exception:
                        continue
        
        return log_data
    
    def _extract_container_name(self, line):
        """Extract container name from line"""
        import re
        # Look for common SONiC container names
        containers = ['swss', 'syncd', 'bgp', 'teamd', 'snmp', 'lldp', 'radv', 'pmon', 'dhcp_relay', 'telemetry']
        
        for container in containers:
            if container in line.lower():
                return container
        
        return None
    
    def get_system_info(self):
        """Get system information (compatibility method)"""
        return {}  # Will be populated after extraction
    
    def get_docker_containers(self):
        """Get docker containers (compatibility method)"""
        return {}  # Will be populated after extraction
    
    def get_network_config(self):
        """Get network configuration (compatibility method)"""
        return {}  # Will be populated after extraction

def main():
    """Main function for standalone execution"""
    if len(sys.argv) != 2:
        print("Usage: python fixed_showtech_extractor.py <showtech_archive>")
        print()
        print("Example: python fixed_showtech_extractor.py sonic_dump.tar.gz")
        sys.exit(1)
    
    archive_path = sys.argv[1]
    
    if not os.path.exists(archive_path):
        print(f"Error: Archive not found: {archive_path}")
        sys.exit(1)
    
    print("=== Fixed Show Tech Extractor ===")
    print(f"Processing: {archive_path}")
    print()
    
    # Initialize extractor
    extractor = FixedShowTechExtractor()
    
    try:
        # Extract and parse
        result = extractor.extract(archive_path)
        
        if result.get('success'):
            print("SUCCESS: Extraction completed!")
            print(f"Extraction Time: {result.get('extraction_time')}")
            print()
            
            # Display summary
            system_info = result.get('system_info', {})
            print("=== SYSTEM INFORMATION ===")
            for key, value in system_info.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            print()
            
            file_inventory = result.get('file_inventory', {})
            print("=== FILE INVENTORY ===")
            print(f"Total Files: {file_inventory.get('total_files', 0)}")
            print(f"File Types: {len(file_inventory.get('file_types', {}))}")
            print()
            
            containers = result.get('docker_containers', {})
            print("=== DOCKER CONTAINERS ===")
            print(f"Total: {containers.get('total_containers', 0)}")
            print(f"Running: {len(containers.get('running_containers', []))}")
            print(f"Stopped: {len(containers.get('stopped_containers', []))}")
            print()
            
            log_data = result.get('log_data', {})
            log_summary = log_data.get('log_summary', {})
            print("=== LOG ANALYSIS ===")
            print(f"Log Files: {log_summary.get('total_log_files', 0)}")
            print(f"Critical Errors: {log_summary.get('total_errors', 0)}")
            print(f"Warnings: {log_summary.get('total_warnings', 0)}")
            print(f"Reboot Events: {len(log_data.get('reboot_events', []))}")
            print()
            
            print("=== EXTRACTION COMPLETED SUCCESSFULLY ===")
            
        else:
            print(f"ERROR: Extraction failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()