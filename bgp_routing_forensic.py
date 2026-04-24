#!/usr/bin/env python3
"""
Comprehensive BGP and Routing Forensic Analysis for NEE-13019
Detailed forensic review of BGP configuration, routing tables, and VxLAN overlay
"""

import tarfile
import tempfile
import os
import re
import json
from datetime import datetime

def main():
    print('=== COMPREHENSIVE BGP & ROUTING FORENSIC ANALYSIS ===')
    
    # Extract archive
    archive_path = 'C:/Users/Prasanth_Sasidharan/OneDrive - Dell Technologies/Documents/Customer Documents/2025/National Polite/NEE-13019/sonic_dump_trfols5304_20251219_104108.tar.gz'
    temp_dir = tempfile.mkdtemp(prefix='bgp_routing_forensic_')
    
    with tarfile.open(archive_path, 'r:gz') as tar:
        tar.extractall(temp_dir)
    
    print(f'Archive extracted to: {temp_dir}')
    
    # Find all BGP and routing related files
    bgp_routing_files = []
    routing_files = []
    bgp_files = []
    config_files = []
    
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_lower = file.lower()
            
            # BGP specific files
            if any(keyword in file_lower for keyword in ['bgp', 'border', 'neighbor', 'peer']):
                bgp_files.append(file_path)
                bgp_routing_files.append(file_path)
            
            # Routing specific files
            elif any(keyword in file_lower for keyword in ['route', 'routing', 'fib', 'rib', 'vrf']):
                routing_files.append(file_path)
                bgp_routing_files.append(file_path)
            
            # Configuration files
            elif any(keyword in file_lower for keyword in ['config', 'cfg', 'json', 'db']):
                config_files.append(file_path)
    
    print(f'Found {len(bgp_files)} BGP files')
    print(f'Found {len(routing_files)} routing files')
    print(f'Found {len(config_files)} config files')
    
    # Comprehensive BGP and routing data extraction
    forensic_data = {
        'bgp_neighbors': {},
        'bgp_statistics': {},
        'routing_table': {},
        'vni_information': {},
        'vxlan_configuration': {},
        'interface_mappings': {},
        'bgp_error_analysis': [],
        'routing_performance': {},
        'network_topology': {},
        'configuration_analysis': {}
    }
    
    # Analyze BGP files
    for bgp_file in bgp_files[:10]:
        try:
            with open(bgp_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Extract BGP neighbor information
                neighbor_pattern = r'BGP neighbor is ([\d\.]+),\s+remote AS (\d+)'
                neighbors = re.findall(neighbor_pattern, content)
                
                for neighbor_ip, asn in neighbors:
                    if neighbor_ip not in forensic_data['bgp_neighbors']:
                        forensic_data['bgp_neighbors'][neighbor_ip] = {
                            'remote_as': asn,
                            'state': 'unknown',
                            'uptime': 'unknown',
                            'prefixes_received': 0,
                            'prefixes_advertised': 0,
                            'messages_sent': 0,
                            'messages_received': 0
                        }
                
                # Extract BGP state information
                state_pattern = r'BGP state = (\w+)'
                states = re.findall(state_pattern, content)
                
                # Store file analysis
                forensic_data['bgp_statistics'][os.path.basename(bgp_file)] = {
                    'neighbors_found': len(neighbors),
                    'states_detected': states,
                    'file_size': len(content)
                }
                
        except Exception as e:
            forensic_data['bgp_error_analysis'].append({
                'file': os.path.basename(bgp_file),
                'error': str(e)
            })
    
    # Analyze routing files
    for routing_file in routing_files[:10]:
        try:
            with open(routing_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Extract VNI information
                vni_pattern = r'VNI\s+(\d+)'
                vni_matches = re.findall(vni_pattern, content)
                
                for vni in vni_matches:
                    if vni not in forensic_data['vni_information']:
                        forensic_data['vni_information'][vni] = {
                            'vni_id': vni,
                            'associated_interfaces': [],
                            'remote_vteps': [],
                            'arp_entries': 0
                        }
                
                # Extract IP addresses and routes
                ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                ip_matches = re.findall(ip_pattern, content)
                
                # Store routing analysis
                forensic_data['routing_table'][os.path.basename(routing_file)] = {
                    'vni_matches': vni_matches,
                    'ip_addresses': ip_matches[:20],
                    'file_size': len(content)
                }
                
        except Exception as e:
            forensic_data['bgp_error_analysis'].append({
                'file': os.path.basename(routing_file),
                'error': str(e)
            })
    
    # Analyze CONFIG_DB.json for detailed configuration
    config_db_path = None
    for config_file in config_files:
        if 'config_db.json' in config_file.lower():
            config_db_path = config_file
            break
    
    if config_db_path:
        try:
            with open(config_db_path, 'r', encoding='utf-8', errors='ignore') as f:
                config_data = json.load(f)
                
                # Analyze BGP configuration in CONFIG_DB
                if 'BGP_NEIGHBOR' in config_data:
                    bgp_neighbor_config = config_data['BGP_NEIGHBOR']
                    forensic_data['configuration_analysis']['bgp_neighbors'] = {
                        'total_neighbors': len(bgp_neighbor_config),
                        'neighbor_details': bgp_neighbor_config
                    }
                
                # Analyze VxLAN configuration
                if 'VXLAN_TUNNEL' in config_data:
                    vxlan_config = config_data['VXLAN_TUNNEL']
                    forensic_data['vxlan_configuration'] = vxlan_config
                
                # Analyze interface configurations
                if 'INTERFACE' in config_data:
                    interface_config = config_data['INTERFACE']
                    forensic_data['interface_mappings'] = interface_config
                    
        except Exception as e:
            forensic_data['bgp_error_analysis'].append({
                'file': 'CONFIG_DB.json',
                'error': str(e)
            })
    
    # Display comprehensive forensic results
    print()
    print('=== BGP FORENSIC ANALYSIS ===')
    print(f'BGP Neighbors Discovered: {len(forensic_data["bgp_neighbors"])}')
    for neighbor_ip, neighbor_data in forensic_data['bgp_neighbors'].items():
        print(f'  Neighbor: {neighbor_ip} (AS {neighbor_data["remote_as"]}) - State: {neighbor_data["state"]}')
    
    print()
    print('BGP Statistics Summary:')
    for file_name, stats in forensic_data['bgp_statistics'].items():
        print(f'  {file_name}: {stats["neighbors_found"]} neighbors, {len(stats["states_detected"])} states')
    
    print()
    print('=== ROUTING FORENSIC ANALYSIS ===')
    print(f'VNI Information Discovered: {len(forensic_data["vni_information"])}')
    for vni_id, vni_data in forensic_data['vni_information'].items():
        print(f'  VNI {vni_id}: {len(vni_data["associated_interfaces"])} interfaces')
    
    print()
    print('Routing Table Summary:')
    for file_name, routing_data in forensic_data['routing_table'].items():
        print(f'  {file_name}: {len(routing_data["ip_addresses"])} IPs')
    
    print()
    print('=== CONFIGURATION ANALYSIS ===')
    if 'bgp_neighbors' in forensic_data['configuration_analysis']:
        bgp_config = forensic_data['configuration_analysis']['bgp_neighbors']
        print(f'BGP Configuration: {bgp_config["total_neighbors"]} neighbors configured')
    
    if forensic_data['vxlan_configuration']:
        print(f'VxLAN Configuration: {len(forensic_data["vxlan_configuration"])} tunnels')
    
    if forensic_data['interface_mappings']:
        print(f'Interface Configuration: {len(forensic_data["interface_mappings"])} interfaces')
    
    print()
    print('=== DETAILED FORENSIC ANALYSIS ===')
    
    # Extract specific details from key files
    for bgp_file in bgp_files[:3]:
        try:
            with open(bgp_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                print(f'--- BGP File: {os.path.basename(bgp_file)} ---')
                for i, line in enumerate(lines[:15]):
                    if any(keyword in line.lower() for keyword in ['neighbor', 'bgp', 'state', 'prefix', 'route']):
                        print(f'  Line {i+1}: {line.strip()}')
        except:
            pass
    
    # Extract specific routing details from key files
    key_routing_files = [f for f in routing_files if any(keyword in f.lower() for keyword in ['vni', 'vxlan', 'evpn'])]
    for routing_file in key_routing_files[:3]:
        try:
            with open(routing_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                print(f'--- Routing File: {os.path.basename(routing_file)} ---')
                for i, line in enumerate(lines[:15]):
                    if any(keyword in line.lower() for keyword in ['vni', 'vtep', 'mac', 'ip', 'vlan']):
                        print(f'  Line {i+1}: {line.strip()}')
        except:
            pass
    
    # Extract CONFIG_DB details
    if config_db_path:
        try:
            with open(config_db_path, 'r', encoding='utf-8', errors='ignore') as f:
                config_data = json.load(f)
                
                print()
                print('=== CONFIG_DB DETAILED ANALYSIS ===')
                
                # BGP Configuration details
                if 'BGP_NEIGHBOR' in config_data:
                    print('BGP_NEIGHBOR Configuration:')
                    for neighbor_key, neighbor_config in config_data['BGP_NEIGHBOR'].items():
                        print(f'  {neighbor_key}: {neighbor_config}')
                
                # VxLAN Configuration details
                if 'VXLAN_TUNNEL' in config_data:
                    print('VXLAN_TUNNEL Configuration:')
                    for tunnel_key, tunnel_config in config_data['VXLAN_TUNNEL'].items():
                        print(f'  {tunnel_key}: {tunnel_config}')
                
                # Interface Configuration details
                if 'INTERFACE' in config_data:
                    print('INTERFACE Configuration (first 10):')
                    interface_count = 0
                    for interface_key, interface_config in config_data['INTERFACE'].items():
                        if interface_count < 10:
                            print(f'  {interface_key}: {interface_config}')
                            interface_count += 1
                
                # VLAN Configuration details
                if 'VLAN' in config_data:
                    print('VLAN Configuration:')
                    for vlan_key, vlan_config in config_data['VLAN'].items():
                        print(f'  {vlan_key}: {vlan_config}')
                        
        except Exception as e:
            print(f'CONFIG_DB analysis error: {e}')
    
    # Generate forensic summary
    print()
    print('=== FORENSIC SUMMARY ===')
    print(f'Total BGP Files Analyzed: {len(bgp_files)}')
    print(f'Total Routing Files Analyzed: {len(routing_files)}')
    print(f'BGP Neighbors Configured: {len(forensic_data["bgp_neighbors"])}')
    print(f'VNI Segments Detected: {len(forensic_data["vni_information"])}')
    print(f'Processing Errors: {len(forensic_data["bgp_error_analysis"])}')
    
    # Clean up
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    print()
    print('=== FORENSIC ANALYSIS COMPLETED ===')

if __name__ == "__main__":
    main()