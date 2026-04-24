#!/usr/bin/env python3
"""
Advanced Data Extraction and Parsing System for SONiC Showtech Analysis
Comprehensive data extraction with expert-level technical detail extraction
"""

import os
import re
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime
import logging

# ============================================================================
# ADVANCED DATA EXTRACTION FRAMEWORK
# ============================================================================

@dataclass
class ExtractionMetrics:
    """Metrics for data extraction process"""
    files_processed: int = 0
    data_points_extracted: int = 0
    parsing_errors: int = 0
    extraction_time: float = 0.0
    data_quality_score: float = 0.0

class AdvancedDataExtractor:
    """Advanced data extraction with comprehensive parsing capabilities"""
    
    def __init__(self):
        self.extraction_patterns = self._initialize_extraction_patterns()
        self.parsing_rules = self._initialize_parsing_rules()
        self.data_validators = self._initialize_data_validators()
        self.extraction_metrics = ExtractionMetrics()
        
    def extract_comprehensive_data(self, temp_dir: str) -> Dict[str, Any]:
        """Extract comprehensive data with expert-level detail"""
        
        print(f"[EXTRACTION] Starting comprehensive data extraction from: {temp_dir}")
        start_time = datetime.now()
        
        extracted_data = {
            "extraction_metadata": {
                "start_time": start_time.isoformat(),
                "extraction_depth": "comprehensive",
                "technical_detail_level": "expert"
            },
            "hardware_data": self._extract_hardware_data_comprehensive(temp_dir),
            "network_data": self._extract_network_data_comprehensive(temp_dir),
            "service_data": self._extract_service_data_comprehensive(temp_dir),
            "configuration_data": self._extract_configuration_data_comprehensive(temp_dir),
            "performance_data": self._extract_performance_data_comprehensive(temp_dir),
            "log_data": self._extract_log_data_comprehensive(temp_dir),
            "error_data": self._extract_error_data_comprehensive(temp_dir),
            "security_data": self._extract_security_data_comprehensive(temp_dir),
            "capacity_data": self._extract_capacity_data_comprehensive(temp_dir)
        }
        
        # Calculate extraction metrics
        end_time = datetime.now()
        self.extraction_metrics.extraction_time = (end_time - start_time).total_seconds()
        self.extraction_metrics.data_quality_score = self._calculate_data_quality_score(extracted_data)
        
        extracted_data["extraction_metrics"] = asdict(self.extraction_metrics)
        
        print(f"[EXTRACTION] Completed: {self.extraction_metrics.files_processed} files, "
              f"{self.extraction_metrics.data_points_extracted} data points")
        
        return extracted_data
    
    def _extract_hardware_data_comprehensive(self, temp_dir: str) -> Dict[str, Any]:
        """Extract comprehensive hardware data"""
        
        hardware_data = {
            "cpu_data": self._extract_cpu_data_detailed(temp_dir),
            "memory_data": self._extract_memory_data_detailed(temp_dir),
            "temperature_data": self._extract_temperature_data_detailed(temp_dir),
            "power_data": self._extract_power_data_detailed(temp_dir),
            "cooling_data": self._extract_cooling_data_detailed(temp_dir),
            "pci_data": self._extract_pci_data_detailed(temp_dir),
            "platform_data": self._extract_platform_data_detailed(temp_dir),
            "sensor_data": self._extract_sensor_data_detailed(temp_dir)
        }
        
        return hardware_data
    
    def _extract_cpu_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed CPU data"""
        
        cpu_data = {
            "processor_info": {},
            "core_analysis": {},
            "architecture_details": {},
            "performance_metrics": {},
            "cache_analysis": {},
            "feature_flags": []
        }
        
        # Extract from /proc/cpuinfo
        cpuinfo_files = self._find_files_by_pattern(temp_dir, ["cpuinfo"])
        for cpuinfo_file in cpuinfo_files:
            try:
                cpu_data["processor_info"] = self._parse_cpuinfo_detailed(cpuinfo_file)
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing cpuinfo: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        # Extract from lscpu
        lscpu_files = self._find_files_by_pattern(temp_dir, ["lscpu"])
        for lscpu_file in lscpu_files:
            try:
                cpu_data["architecture_details"] = self._parse_lscpu_detailed(lscpu_file)
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing lscpu: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        # Extract CPU performance metrics
        cpu_perf_files = self._find_files_by_pattern(temp_dir, ["cpu", "perf", "stat"])
        for perf_file in cpu_perf_files:
            try:
                perf_data = self._parse_cpu_performance_detailed(perf_file)
                cpu_data["performance_metrics"].update(perf_data)
                self.extraction_metrics.data_points_extracted += len(perf_data)
            except Exception as e:
                logging.error(f"Error parsing CPU performance: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return cpu_data
    
    def _parse_cpuinfo_detailed(self, cpuinfo_path: str) -> Dict[str, Any]:
        """Parse /proc/cpuinfo with detailed extraction"""
        
        processor_info = {
            "processors": [],
            "total_cores": 0,
            "total_threads": 0,
            "socket_count": 0,
            "vendor_id": "",
            "model_name": "",
            "cpu_family": "",
            "model": "",
            "stepping": "",
            "cpu_mhz": "",
            "cache_size": "",
            "flags": [],
            "bogomips": "",
            "clflush_size": "",
            "cache_alignment": "",
            "address_sizes": "",
            "power_management": []
        }
        
        try:
            with open(cpuinfo_path, 'r', encoding='utf-8', errors='ignore') as f:
                processor_data = {}
                for line in f:
                    line = line.strip()
                    if not line:
                        if processor_data:
                            processor_info["processors"].append(processor_data.copy())
                            processor_data.clear()
                        continue
                    
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        processor_data[key] = value
                        
                        # Extract key information
                        if key == "processor":
                            processor_info["total_threads"] += 1
                        elif key == "model name":
                            processor_info["model_name"] = value
                        elif key == "vendor_id":
                            processor_info["vendor_id"] = value
                        elif key == "cpu family":
                            processor_info["cpu_family"] = value
                        elif key == "model":
                            processor_info["model"] = value
                        elif key == "stepping":
                            processor_info["stepping"] = value
                        elif key == "cpu MHz":
                            processor_info["cpu_mhz"] = value
                        elif key == "cache size":
                            processor_info["cache_size"] = value
                        elif key == "flags":
                            processor_info["flags"] = value.split()
                        elif key == "bogomips":
                            processor_info["bogomips"] = value
                        elif key == "clflush size":
                            processor_info["clflush_size"] = value
                        elif key == "cache_alignment":
                            processor_info["cache_alignment"] = value
                        elif key == "address sizes":
                            processor_info["address_sizes"] = value
                
                # Add last processor if exists
                if processor_data:
                    processor_info["processors"].append(processor_data)
                
                # Calculate cores and sockets
                processor_info["total_cores"] = len(set(p.get("processor", "0") for p in processor_info["processors"]))
                processor_info["socket_count"] = len(set(p.get("physical id", "0") for p in processor_info["processors"]))
                
                # Extract power management features
                for processor in processor_info["processors"]:
                    if "power management" in processor:
                        pm_features = [f.strip() for f in processor["power management"].split(',')]
                        processor_info["power_management"].extend(pm_features)
                
                processor_info["power_management"] = list(set(processor_info["power_management"]))
                
        except Exception as e:
            processor_info["parse_error"] = str(e)
        
        return processor_info
    
    def _parse_lscpu_detailed(self, lscpu_path: str) -> Dict[str, Any]:
        """Parse lscpu output with detailed extraction"""
        
        architecture_details = {
            "architecture": "",
            "cpu_op_modes": [],
            "byte_order": "",
            "cpu_sizes": {},
            "vendor_id": "",
            "cpu_family": "",
            "model": "",
            "model_name": "",
            "stepping": "",
            "cpu_mhz": "",
            "bogomips": "",
            "virtualization": "",
            "l1d_cache": "",
            "l1i_cache": "",
            "l2_cache": "",
            "l3_cache": "",
            "numa_config": {},
            "thread_config": {},
            "feature_flags": []
        }
        
        try:
            with open(lscpu_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower().replace(' ', '_')
                        value = value.strip()
                        
                        if key == "architecture":
                            architecture_details["architecture"] = value
                        elif key == "cpu_op-mode(s)":
                            architecture_details["cpu_op_modes"] = [mode.strip() for mode in value.split(',')]
                        elif key == "byte_order":
                            architecture_details["byte_order"] = value
                        elif key == "cpu(s)":
                            architecture_details["cpu_sizes"]["total_cpus"] = value
                        elif key == "on-line_cpu(s)_list":
                            architecture_details["cpu_sizes"]["online_cpus"] = value
                        elif key == "thread(s)_per_core":
                            architecture_details["thread_config"]["threads_per_core"] = value
                        elif key == "core(s)_per_socket":
                            architecture_details["thread_config"]["cores_per_socket"] = value
                        elif key == "socket(s)":
                            architecture_details["thread_config"]["sockets"] = value
                        elif key == "numa_node(s)":
                            architecture_details["numa_config"]["numa_nodes"] = value
                        elif key == "numa_node0_cpu(s)":
                            architecture_details["numa_config"]["node0_cpus"] = value
                        elif key == "virtualization":
                            architecture_details["virtualization"] = value
                        elif key.startswith("l1") or key.startswith("l2") or key.startswith("l3"):
                            cache_key = key.replace('_cache', '_cache')
                            architecture_details[cache_key] = value
                        elif key == "flags":
                            architecture_details["feature_flags"] = value.split()
                        
                        # Update other fields
                        if key in ["vendor_id", "cpu_family", "model", "model_name", "stepping", "cpu_mhz", "bogomips"]:
                            architecture_details[key] = value
                
        except Exception as e:
            architecture_details["parse_error"] = str(e)
        
        return architecture_details
    
    def _parse_cpu_performance_detailed(self, perf_file_path: str) -> Dict[str, Any]:
        """Parse CPU performance data with detailed metrics"""
        
        performance_metrics = {
            "cpu_utilization": {},
            "context_switches": 0,
            "interrupts": 0,
            "cpu_time": {},
            "load_average": {},
            "process_stats": {}
        }
        
        try:
            with open(perf_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Parse CPU utilization
                cpu_util_match = re.search(r'cpu\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', content)
                if cpu_util_match:
                    performance_metrics["cpu_utilization"] = {
                        "user": int(cpu_util_match.group(1)),
                        "nice": int(cpu_util_match.group(2)),
                        "system": int(cpu_util_match.group(3)),
                        "idle": int(cpu_util_match.group(4)),
                        "iowait": int(cpu_util_match.group(5)),
                        "irq": int(cpu_util_match.group(6)),
                        "softirq": int(cpu_util_match.group(7)),
                        "steal": int(cpu_util_match.group(8))
                    }
                
                # Parse context switches
                ctxt_match = re.search(r'ctxt\s+(\d+)', content)
                if ctxt_match:
                    performance_metrics["context_switches"] = int(ctxt_match.group(1))
                
                # Parse interrupts
                intr_match = re.search(r'intr\s+(\d+)', content)
                if intr_match:
                    performance_metrics["interrupts"] = int(intr_match.group(1))
                
                # Parse load average
                load_match = re.search(r'load average:\s+([\d.]+),\s+([\d.]+),\s+([\d.]+)', content)
                if load_match:
                    performance_metrics["load_average"] = {
                        "1min": float(load_match.group(1)),
                        "5min": float(load_match.group(2)),
                        "15min": float(load_match.group(3))
                    }
                
                # Parse process statistics
                processes_match = re.search(r'processes\s+(\d+)', content)
                if processes_match:
                    performance_metrics["process_stats"]["total_processes"] = int(processes_match.group(1))
                
                procs_running_match = re.search(r'procs_running\s+(\d+)', content)
                if procs_running_match:
                    performance_metrics["process_stats"]["running_processes"] = int(procs_running_match.group(1))
                
                procs_blocked_match = re.search(r'procs_blocked\s+(\d+)', content)
                if procs_blocked_match:
                    performance_metrics["process_stats"]["blocked_processes"] = int(procs_blocked_match.group(1))
                
        except Exception as e:
            performance_metrics["parse_error"] = str(e)
        
        return performance_metrics
    
    def _extract_memory_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed memory data"""
        
        memory_data = {
            "memory_info": {},
            "utilization_analysis": {},
            "cache_analysis": {},
            "swap_analysis": {},
            "numa_analysis": {},
            "performance_metrics": {}
        }
        
        # Extract from /proc/meminfo
        meminfo_files = self._find_files_by_pattern(temp_dir, ["meminfo"])
        for meminfo_file in meminfo_files:
            try:
                memory_data["memory_info"] = self._parse_meminfo_detailed(meminfo_file)
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing meminfo: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        # Extract from free command
        free_files = self._find_files_by_pattern(temp_dir, ["free"])
        for free_file in free_files:
            try:
                free_data = self._parse_free_detailed(free_file)
                memory_data["utilization_analysis"].update(free_data)
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing free output: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        # Extract NUMA information
        numa_files = self._find_files_by_pattern(temp_dir, ["numa"])
        for numa_file in numa_files:
            try:
                numa_data = self._parse_numa_detailed(numa_file)
                memory_data["numa_analysis"] = numa_data
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing NUMA info: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return memory_data
    
    def _parse_meminfo_detailed(self, meminfo_path: str) -> Dict[str, Any]:
        """Parse /proc/meminfo with comprehensive extraction"""
        
        memory_info = {
            "total_memory_kb": 0,
            "free_memory_kb": 0,
            "available_memory_kb": 0,
            "buffers_kb": 0,
            "cached_kb": 0,
            "swap_cached_kb": 0,
            "active_kb": 0,
            "inactive_kb": 0,
            "unevictable_kb": 0,
            "mlocked_kb": 0,
            "swap_total_kb": 0,
            "swap_free_kb": 0,
            "dirty_kb": 0,
            "writeback_kb": 0,
            "anonpages_kb": 0,
            "mapped_kb": 0,
            "shmem_kb": 0,
            "slab_kb": 0,
            "sreclaimable_kb": 0,
            "sunreclaimable_kb": 0,
            "kernelstack_kb": 0,
            "pagetables_kb": 0,
            "nfs_unstable_kb": 0,
            "bounce_kb": 0,
            "writebacktmp_kb": 0,
            "commitlimit_kb": 0,
            "committedas_kb": 0,
            "vmalloctotal_kb": 0,
            "vmallocused_kb": 0,
            "vmallocchunk_kb": 0,
            "hardwarecorrupted_kb": 0,
            "anonhugepages_kb": 0,
            "shmemhugepages_kb": 0,
            "cmemall_kb": 0,
            "hugepages_total": 0,
            "hugepages_free": 0,
            "hugepages_rsvd": 0,
            "hugepages_surp": 0,
            "hugepagesize_kb": 0,
            "directmap4k_kb": 0,
            "directmap2m_kb": 0,
            "directmap1g_kb": 0,
            "detailed_breakdown": {},
            "memory_zones": {}
        }
        
        try:
            with open(meminfo_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower().replace(' ', '_')
                        value = value.strip().split()[0]  # Remove "kB" suffix
                        
                        try:
                            value_kb = int(value)
                            memory_info["detailed_breakdown"][key] = value_kb
                            
                            # Map to specific fields
                            if key == "memtotal":
                                memory_info["total_memory_kb"] = value_kb
                            elif key == "memfree":
                                memory_info["free_memory_kb"] = value_kb
                            elif key == "memavailable":
                                memory_info["available_memory_kb"] = value_kb
                            elif key == "buffers":
                                memory_info["buffers_kb"] = value_kb
                            elif key == "cached":
                                memory_info["cached_kb"] = value_kb
                            elif key == "swaptotal":
                                memory_info["swap_total_kb"] = value_kb
                            elif key == "swapfree":
                                memory_info["swap_free_kb"] = value_kb
                            elif key == "active":
                                memory_info["active_kb"] = value_kb
                            elif key == "inactive":
                                memory_info["inactive_kb"] = value_kb
                            elif key == "unevictable":
                                memory_info["unevictable_kb"] = value_kb
                            elif key == "mlocked":
                                memory_info["mlocked_kb"] = value_kb
                            elif key == "dirty":
                                memory_info["dirty_kb"] = value_kb
                            elif key == "writeback":
                                memory_info["writeback_kb"] = value_kb
                            elif key == "anonpages":
                                memory_info["anonpages_kb"] = value_kb
                            elif key == "mapped":
                                memory_info["mapped_kb"] = value_kb
                            elif key == "shmem":
                                memory_info["shmem_kb"] = value_kb
                            elif key == "slab":
                                memory_info["slab_kb"] = value_kb
                            elif key == "sreclaimable":
                                memory_info["sreclaimable_kb"] = value_kb
                            elif key == "sunreclaim":
                                memory_info["sunreclaimable_kb"] = value_kb
                            elif key == "kernelstack":
                                memory_info["kernelstack_kb"] = value_kb
                            elif key == "pagetables":
                                memory_info["pagetables_kb"] = value_kb
                            elif key == "commitlimit":
                                memory_info["commitlimit_kb"] = value_kb
                            elif key == "committedas":
                                memory_info["committedas_kb"] = value_kb
                            elif key == "vmalloctotal":
                                memory_info["vmalloctotal_kb"] = value_kb
                            elif key == "vmallocused":
                                memory_info["vmallocused_kb"] = value_kb
                            elif key == "vmallocchunk":
                                memory_info["vmallocchunk_kb"] = value_kb
                            elif key == "hardwarecorrupted":
                                memory_info["hardwarecorrupted_kb"] = value_kb
                            elif key == "hugepages_total":
                                memory_info["hugepages_total"] = value_kb
                            elif key == "hugepages_free":
                                memory_info["hugepages_free"] = value_kb
                            elif key == "hugepages_rsvd":
                                memory_info["hugepages_rsvd"] = value_kb
                            elif key == "hugepages_surp":
                                memory_info["hugepages_surp"] = value_kb
                            elif key == "hugepagesize":
                                memory_info["hugepagesize_kb"] = value_kb
                            elif key == "directmap4k":
                                memory_info["directmap4k_kb"] = value_kb
                            elif key == "directmap2m":
                                memory_info["directmap2m_kb"] = value_kb
                            elif key == "directmap1g":
                                memory_info["directmap1g_kb"] = value_kb
                            
                            # Extract memory zones
                            if key.startswith("dma") or key.startswith("normal") or key.startswith("highmem"):
                                zone_name = key.split('_')[0]
                                if zone_name not in memory_info["memory_zones"]:
                                    memory_info["memory_zones"][zone_name] = {}
                                memory_info["memory_zones"][zone_name][key] = value_kb
                            
                        except ValueError:
                            continue
                            
        except Exception as e:
            memory_info["parse_error"] = str(e)
        
        return memory_info
    
    def _parse_free_detailed(self, free_path: str) -> Dict[str, Any]:
        """Parse free command output with detailed analysis"""
        
        free_data = {
            "memory": {
                "total_kb": 0,
                "used_kb": 0,
                "free_kb": 0,
                "shared_kb": 0,
                "buff_cache_kb": 0,
                "available_kb": 0
            },
            "swap": {
                "total_kb": 0,
                "used_kb": 0,
                "free_kb": 0
            },
            "utilization_percent": 0.0,
            "swap_utilization_percent": 0.0
        }
        
        try:
            with open(free_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("total"):
                        continue
                    
                    parts = line.split()
                    if len(parts) >= 6:
                        memory_type = parts[0].lower()
                        
                        if memory_type == "mem:":
                            free_data["memory"]["total_kb"] = self._parse_memory_value(parts[1])
                            free_data["memory"]["used_kb"] = self._parse_memory_value(parts[2])
                            free_data["memory"]["free_kb"] = self._parse_memory_value(parts[3])
                            free_data["memory"]["shared_kb"] = self._parse_memory_value(parts[4])
                            free_data["memory"]["buff_cache_kb"] = self._parse_memory_value(parts[5])
                            if len(parts) > 6:
                                free_data["memory"]["available_kb"] = self._parse_memory_value(parts[6])
                            
                            # Calculate utilization
                            if free_data["memory"]["total_kb"] > 0:
                                free_data["utilization_percent"] = (
                                    free_data["memory"]["used_kb"] / free_data["memory"]["total_kb"]
                                ) * 100
                        
                        elif memory_type == "swap:":
                            free_data["swap"]["total_kb"] = self._parse_memory_value(parts[1])
                            free_data["swap"]["used_kb"] = self._parse_memory_value(parts[2])
                            free_data["swap"]["free_kb"] = self._parse_memory_value(parts[3])
                            
                            # Calculate swap utilization
                            if free_data["swap"]["total_kb"] > 0:
                                free_data["swap_utilization_percent"] = (
                                    free_data["swap"]["used_kb"] / free_data["swap"]["total_kb"]
                                ) * 100
                
        except Exception as e:
            free_data["parse_error"] = str(e)
        
        return free_data
    
    def _parse_memory_value(self, value_str: str) -> int:
        """Parse memory value with unit conversion"""
        value_str = value_str.upper()
        
        if value_str.endswith('G'):
            return int(float(value_str[:-1]) * 1024 * 1024)
        elif value_str.endswith('M'):
            return int(float(value_str[:-1]) * 1024)
        elif value_str.endswith('K'):
            return int(float(value_str[:-1]))
        else:
            return int(float(value_str))
    
    def _parse_numa_detailed(self, numa_path: str) -> Dict[str, Any]:
        """Parse NUMA information with detailed analysis"""
        
        numa_data = {
            "numa_nodes": {},
            "node_distances": {},
            "memory_allocation": {},
            "cpu_binding": {}
        }
        
        try:
            with open(numa_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Parse NUMA node information
                node_matches = re.findall(r'node(\d+)\s+size:\s+(\d+)MB', content)
                for node_match in node_matches:
                    node_id = int(node_match[0])
                    size_mb = int(node_match[1])
                    
                    numa_data["numa_nodes"][f"node{node_id}"] = {
                        "node_id": node_id,
                        "size_mb": size_mb,
                        "size_kb": size_mb * 1024,
                        "cpus": []
                    }
                
                # Parse CPU to NUMA node mapping
                cpu_matches = re.findall(r'node(\d+)\s+cpus:\s+([0-9\s-]+)', content)
                for cpu_match in cpu_matches:
                    node_id = int(cpu_match[0])
                    cpu_list = cpu_match[1].strip()
                    
                    if f"node{node_id}" in numa_data["numa_nodes"]:
                        cpus = []
                        for cpu_range in cpu_list.split():
                            if '-' in cpu_range:
                                start, end = map(int, cpu_range.split('-'))
                                cpus.extend(range(start, end + 1))
                            else:
                                cpus.append(int(cpu_range))
                        
                        numa_data["numa_nodes"][f"node{node_id}"]["cpus"] = cpus
                
                # Parse node distances
                distance_matches = re.findall(r'node(\d+)\s+distance:\s+([0-9\s]+)', content)
                for distance_match in distance_matches:
                    node_id = int(distance_match[0])
                    distances = [int(d) for d in distance_match[1].split()]
                    
                    numa_data["node_distances"][f"node{node_id}"] = {
                        "node_id": node_id,
                        "distances": distances
                    }
                
        except Exception as e:
            numa_data["parse_error"] = str(e)
        
        return numa_data
    
    def _extract_network_data_comprehensive(self, temp_dir: str) -> Dict[str, Any]:
        """Extract comprehensive network data"""
        
        network_data = {
            "interface_data": self._extract_interface_data_detailed(temp_dir),
            "port_channel_data": self._extract_port_channel_data_detailed(temp_dir),
            "bgp_data": self._extract_bgp_data_detailed(temp_dir),
            "arp_data": self._extract_arp_data_detailed(temp_dir),
            "routing_data": self._extract_routing_data_detailed(temp_dir),
            "hardware_counter_data": self._extract_hardware_counter_data_detailed(temp_dir),
            "qos_data": self._extract_qos_data_detailed(temp_dir)
        }
        
        return network_data
    
    def _extract_interface_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed interface data"""
        
        interface_data = {
            "interface_status": {},
            "interface_counters": {},
            "physical_layer": {},
            "error_counters": {},
            "queue_counters": {},
            "utilization_metrics": {},
            "configuration_data": {}
        }
        
        # Extract interface counters
        counter_files = self._find_files_by_pattern(temp_dir, ["interface_counters", "show_interface_counters"])
        for counter_file in counter_files:
            try:
                counter_data = self._parse_interface_counters_detailed(counter_file)
                interface_data["interface_counters"].update(counter_data)
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing interface counters: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        # Extract physical status
        phy_files = self._find_files_by_pattern(temp_dir, ["phy_status", "show_interface_phy_status"])
        for phy_file in phy_files:
            try:
                phy_data = self._parse_phy_status_detailed(phy_file)
                interface_data["physical_layer"].update(phy_data)
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing physical status: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        # Extract error counters
        error_files = self._find_files_by_pattern(temp_dir, ["dropcounters", "show_interface_dropcounters"])
        for error_file in error_files:
            try:
                error_data = self._parse_error_counters_detailed(error_file)
                interface_data["error_counters"].update(error_data)
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing error counters: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        # Extract queue counters
        queue_files = self._find_files_by_pattern(temp_dir, ["queue_counters", "show_queue_counters"])
        for queue_file in queue_files:
            try:
                queue_data = self._parse_queue_counters_detailed(queue_file)
                interface_data["queue_counters"].update(queue_data)
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing queue counters: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return interface_data
    
    def _parse_interface_counters_detailed(self, counter_file_path: str) -> Dict[str, Any]:
        """Parse interface counters with comprehensive detail"""
        
        interface_counters = {
            "interfaces": {},
            "summary": {
                "total_interfaces": 0,
                "active_interfaces": 0,
                "inactive_interfaces": 0,
                "total_rx_packets": 0,
                "total_tx_packets": 0,
                "total_rx_bytes": 0,
                "total_tx_bytes": 0,
                "total_rx_errors": 0,
                "total_tx_errors": 0,
                "total_rx_drops": 0,
                "total_tx_drops": 0,
                "total_rx_overruns": 0,
                "total_tx_overruns": 0,
                "total_collisions": 0,
                "high_utilization_interfaces": [],
                "error_prone_interfaces": []
            }
        }
        
        try:
            with open(counter_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                current_interface = None
                
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Detect interface name
                    if self._is_interface_line(line):
                        current_interface = self._extract_interface_name(line)
                        if current_interface:
                            interface_counters["interfaces"][current_interface] = {
                                "rx_packets": 0,
                                "tx_packets": 0,
                                "rx_bytes": 0,
                                "tx_bytes": 0,
                                "rx_errors": 0,
                                "tx_errors": 0,
                                "rx_drops": 0,
                                "tx_drops": 0,
                                "rx_overruns": 0,
                                "tx_overruns": 0,
                                "collisions": 0,
                                "rx_frame": 0,
                                "tx_carrier": 0,
                                "tx_heartbeat": 0,
                                "rx_length": 0,
                                "rx_missed": 0,
                                "tx_aborted": 0,
                                "utilization_rx": 0.0,
                                "utilization_tx": 0.0,
                                "utilization_total": 0.0,
                                "error_rate": 0.0,
                                "drop_rate": 0.0
                            }
                            interface_counters["summary"]["total_interfaces"] += 1
                    
                    elif current_interface and ':' in line:
                        # Parse counter values
                        key, value = line.split(':', 1)
                        key = key.strip().lower().replace(' ', '_')
                        value = value.strip()
                        
                        try:
                            # Extract numeric value
                            numeric_value = re.search(r'[\d,]+', value)
                            if numeric_value:
                                num_val = int(numeric_value.group().replace(',', ''))
                                
                                if current_interface in interface_counters["interfaces"]:
                                    # Map counters to fields
                                    if "rx" in key and "packet" in key:
                                        interface_counters["interfaces"][current_interface]["rx_packets"] = num_val
                                        interface_counters["summary"]["total_rx_packets"] += num_val
                                    elif "tx" in key and "packet" in key:
                                        interface_counters["interfaces"][current_interface]["tx_packets"] = num_val
                                        interface_counters["summary"]["total_tx_packets"] += num_val
                                    elif "rx" in key and "byte" in key:
                                        interface_counters["interfaces"][current_interface]["rx_bytes"] = num_val
                                        interface_counters["summary"]["total_rx_bytes"] += num_val
                                    elif "tx" in key and "byte" in key:
                                        interface_counters["interfaces"][current_interface]["tx_bytes"] = num_val
                                        interface_counters["summary"]["total_tx_bytes"] += num_val
                                    elif "error" in key and "rx" in key:
                                        interface_counters["interfaces"][current_interface]["rx_errors"] = num_val
                                        interface_counters["summary"]["total_rx_errors"] += num_val
                                    elif "error" in key and "tx" in key:
                                        interface_counters["interfaces"][current_interface]["tx_errors"] = num_val
                                        interface_counters["summary"]["total_tx_errors"] += num_val
                                    elif "drop" in key and "rx" in key:
                                        interface_counters["interfaces"][current_interface]["rx_drops"] = num_val
                                        interface_counters["summary"]["total_rx_drops"] += num_val
                                    elif "drop" in key and "tx" in key:
                                        interface_counters["interfaces"][current_interface]["tx_drops"] = num_val
                                        interface_counters["summary"]["total_tx_drops"] += num_val
                                    elif "overrun" in key and "rx" in key:
                                        interface_counters["interfaces"][current_interface]["rx_overruns"] = num_val
                                        interface_counters["summary"]["total_rx_overruns"] += num_val
                                    elif "overrun" in key and "tx" in key:
                                        interface_counters["interfaces"][current_interface]["tx_overruns"] = num_val
                                        interface_counters["summary"]["total_tx_overruns"] += num_val
                                    elif "collision" in key:
                                        interface_counters["interfaces"][current_interface]["collisions"] = num_val
                                        interface_counters["summary"]["total_collisions"] += num_val
                                    elif "frame" in key and "rx" in key:
                                        interface_counters["interfaces"][current_interface]["rx_frame"] = num_val
                                    elif "carrier" in key and "tx" in key:
                                        interface_counters["interfaces"][current_interface]["tx_carrier"] = num_val
                                    elif "heartbeat" in key and "tx" in key:
                                        interface_counters["interfaces"][current_interface]["tx_heartbeat"] = num_val
                                    elif "length" in key and "rx" in key:
                                        interface_counters["interfaces"][current_interface]["rx_length"] = num_val
                                    elif "missed" in key and "rx" in key:
                                        interface_counters["interfaces"][current_interface]["rx_missed"] = num_val
                                    elif "aborted" in key and "tx" in key:
                                        interface_counters["interfaces"][current_interface]["tx_aborted"] = num_val
                                    
                        except ValueError:
                            continue
                
                # Calculate derived metrics for each interface
                for interface, data in interface_counters["interfaces"].items():
                    total_packets = data["rx_packets"] + data["tx_packets"]
                    total_bytes = data["rx_bytes"] + data["tx_bytes"]
                    total_errors = data["rx_errors"] + data["tx_errors"]
                    total_drops = data["rx_drops"] + data["tx_drops"]
                    
                    if total_packets > 0:
                        data["error_rate"] = (total_errors / total_packets) * 100
                        data["drop_rate"] = (total_drops / total_packets) * 100
                    
                    if total_bytes > 0:
                        # Simplified utilization calculation (would need time interval for accurate calculation)
                        data["utilization_total"] = min(100.0, (total_bytes / (1024 * 1024 * 1024)) * 0.1)  # Rough estimate
                    
                    # Classify interface status
                    if total_packets > 0:
                        interface_counters["summary"]["active_interfaces"] += 1
                        if data["utilization_total"] > 70:
                            interface_counters["summary"]["high_utilization_interfaces"].append(interface)
                        if data["error_rate"] > 1.0 or data["drop_rate"] > 1.0:
                            interface_counters["summary"]["error_prone_interfaces"].append(interface)
                    else:
                        interface_counters["summary"]["inactive_interfaces"] += 1
                
                self.extraction_metrics.data_points_extracted += len(interface_counters["interfaces"]) * 20  # Approximate data points
                
        except Exception as e:
            interface_counters["parse_error"] = str(e)
        
        return interface_counters
    
    def _parse_phy_status_detailed(self, phy_file_path: str) -> Dict[str, Any]:
        """Parse physical interface status with comprehensive detail"""
        
        phy_status = {
            "interfaces": {},
            "summary": {
                "total_interfaces": 0,
                "link_up": 0,
                "link_down": 0,
                "signal_detect_ok": 0,
                "signal_detect_nok": 0,
                "cdr_lock_ok": 0,
                "cdr_lock_nok": 0,
                "block_lock_ok": 0,
                "block_lock_nok": 0,
                "amps_lock_ok": 0,
                "amps_lock_nok": 0,
                "am_lock_ok": 0,
                "am_lock_nok": 0,
                "problematic_interfaces": []
            }
        }
        
        try:
            with open(phy_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                current_interface = None
                
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Detect interface line
                    if self._is_interface_line(line):
                        current_interface = self._extract_interface_name(line)
                        if current_interface:
                            phy_status["interfaces"][current_interface] = {
                                "link_status": "unknown",
                                "signal_detect": "unknown",
                                "cdr_lock": "unknown",
                                "block_lock": "unknown",
                                "amps_lock": "unknown",
                                "am_lock": "unknown",
                                "timestamp": "",
                                "status_flags": [],
                                "health_score": 100
                            }
                            phy_status["summary"]["total_interfaces"] += 1
                    
                    elif current_interface and ':' in line:
                        # Parse physical status
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if current_interface in phy_status["interfaces"]:
                            if "link" in key:
                                phy_status["interfaces"][current_interface]["link_status"] = value
                                if value.lower() == "ok":
                                    phy_status["summary"]["link_up"] += 1
                                elif value.lower() == "nok":
                                    phy_status["summary"]["link_down"] += 1
                                    phy_status["interfaces"][current_interface]["health_score"] -= 25
                            elif "signal" in key and "detect" in key:
                                phy_status["interfaces"][current_interface]["signal_detect"] = value
                                if value.lower() == "ok":
                                    phy_status["summary"]["signal_detect_ok"] += 1
                                elif value.lower() == "nok":
                                    phy_status["summary"]["signal_detect_nok"] += 1
                                    phy_status["interfaces"][current_interface]["health_score"] -= 20
                            elif "cdr" in key and "lock" in key:
                                phy_status["interfaces"][current_interface]["cdr_lock"] = value
                                if value.lower() == "ok":
                                    phy_status["summary"]["cdr_lock_ok"] += 1
                                elif value.lower() == "nok":
                                    phy_status["summary"]["cdr_lock_nok"] += 1
                                    phy_status["interfaces"][current_interface]["health_score"] -= 15
                            elif "block" in key and "lock" in key:
                                phy_status["interfaces"][current_interface]["block_lock"] = value
                                if value.lower() == "ok":
                                    phy_status["summary"]["block_lock_ok"] += 1
                                elif value.lower() == "nok":
                                    phy_status["summary"]["block_lock_nok"] += 1
                                    phy_status["interfaces"][current_interface]["health_score"] -= 10
                            elif "amps" in key and "lock" in key:
                                phy_status["interfaces"][current_interface]["amps_lock"] = value
                                if value.lower() == "ok":
                                    phy_status["summary"]["amps_lock_ok"] += 1
                                elif value.lower() == "nok":
                                    phy_status["summary"]["amps_lock_nok"] += 1
                                    phy_status["interfaces"][current_interface]["health_score"] -= 5
                            elif "am" in key and "lock" in key:
                                phy_status["interfaces"][current_interface]["am_lock"] = value
                                if value.lower() == "ok":
                                    phy_status["summary"]["am_lock_ok"] += 1
                                elif value.lower() == "nok":
                                    phy_status["summary"]["am_lock_nok"] += 1
                                    phy_status["interfaces"][current_interface]["health_score"] -= 5
                            elif "timestamp" in key:
                                phy_status["interfaces"][current_interface]["timestamp"] = value
                            
                            # Add status flags
                            if value.lower() == "nok":
                                phy_status["interfaces"][current_interface]["status_flags"].append(key)
                
                # Identify problematic interfaces
                for interface, data in phy_status["interfaces"].items():
                    if data["health_score"] < 80:
                        phy_status["summary"]["problematic_interfaces"].append(interface)
                
                self.extraction_metrics.data_points_extracted += len(phy_status["interfaces"]) * 8
                
        except Exception as e:
            phy_status["parse_error"] = str(e)
        
        return phy_status
    
    def _parse_error_counters_detailed(self, error_file_path: str) -> Dict[str, Any]:
        """Parse error counters with comprehensive detail"""
        
        error_counters = {
            "interfaces": {},
            "summary": {
                "total_rx_drops": 0,
                "total_tx_drops": 0,
                "total_rx_overruns": 0,
                "total_tx_overruns": 0,
                "total_rx_frame_errors": 0,
                "total_tx_carrier_errors": 0,
                "total_collisions": 0,
                "interfaces_with_errors": 0,
                "interfaces_with_drops": 0,
                "critical_error_interfaces": []
            }
        }
        
        try:
            with open(error_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                current_interface = None
                
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Detect interface line
                    if self._is_interface_line(line):
                        current_interface = self._extract_interface_name(line)
                        if current_interface:
                            error_counters["interfaces"][current_interface] = {
                                "rx_drops": 0,
                                "tx_drops": 0,
                                "rx_overruns": 0,
                                "tx_overruns": 0,
                                "rx_frame_errors": 0,
                                "tx_carrier_errors": 0,
                                "tx_heartbeat_errors": 0,
                                "rx_length_errors": 0,
                                "rx_missed_errors": 0,
                                "tx_aborted_errors": 0,
                                "total_errors": 0,
                                "total_drops": 0,
                                "error_rate": 0.0,
                                "drop_rate": 0.0,
                                "severity": "normal"
                            }
                    
                    elif current_interface and ':' in line:
                        # Parse error counters
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if current_interface in error_counters["interfaces"]:
                            try:
                                numeric_value = int(re.search(r'[\d,]+', value).group().replace(',', ''))
                                
                                if "rx" in key and "drop" in key:
                                    error_counters["interfaces"][current_interface]["rx_drops"] = numeric_value
                                    error_counters["summary"]["total_rx_drops"] += numeric_value
                                elif "tx" in key and "drop" in key:
                                    error_counters["interfaces"][current_interface]["tx_drops"] = numeric_value
                                    error_counters["summary"]["total_tx_drops"] += numeric_value
                                elif "rx" in key and "overrun" in key:
                                    error_counters["interfaces"][current_interface]["rx_overruns"] = numeric_value
                                    error_counters["summary"]["total_rx_overruns"] += numeric_value
                                elif "tx" in key and "overrun" in key:
                                    error_counters["interfaces"][current_interface]["tx_overruns"] = numeric_value
                                    error_counters["summary"]["total_tx_overruns"] += numeric_value
                                elif "frame" in key and "rx" in key:
                                    error_counters["interfaces"][current_interface]["rx_frame_errors"] = numeric_value
                                    error_counters["summary"]["total_rx_frame_errors"] += numeric_value
                                elif "carrier" in key and "tx" in key:
                                    error_counters["interfaces"][current_interface]["tx_carrier_errors"] = numeric_value
                                    error_counters["summary"]["total_tx_carrier_errors"] += numeric_value
                                elif "collision" in key:
                                    error_counters["interfaces"][current_interface]["collisions"] = numeric_value
                                    error_counters["summary"]["total_collisions"] += numeric_value
                                
                                # Calculate totals and rates
                                interface_data = error_counters["interfaces"][current_interface]
                                interface_data["total_drops"] = interface_data["rx_drops"] + interface_data["tx_drops"]
                                interface_data["total_errors"] = (
                                    interface_data["rx_overruns"] + interface_data["tx_overruns"] +
                                    interface_data["rx_frame_errors"] + interface_data["tx_carrier_errors"] +
                                    interface_data["collisions"]
                                )
                                
                                if interface_data["total_drops"] > 0:
                                    error_counters["summary"]["interfaces_with_drops"] += 1
                                
                                if interface_data["total_errors"] > 0:
                                    error_counters["summary"]["interfaces_with_errors"] += 1
                                
                                # Classify severity
                                if interface_data["total_drops"] > 1000 or interface_data["total_errors"] > 100:
                                    interface_data["severity"] = "critical"
                                    error_counters["summary"]["critical_error_interfaces"].append(current_interface)
                                elif interface_data["total_drops"] > 100 or interface_data["total_errors"] > 10:
                                    interface_data["severity"] = "warning"
                                else:
                                    interface_data["severity"] = "normal"
                                    
                            except (ValueError, AttributeError):
                                continue
                
                self.extraction_metrics.data_points_extracted += len(error_counters["interfaces"]) * 15
                
        except Exception as e:
            error_counters["parse_error"] = str(e)
        
        return error_counters
    
    def _parse_queue_counters_detailed(self, queue_file_path: str) -> Dict[str, Any]:
        """Parse queue counters with comprehensive detail"""
        
        queue_counters = {
            "queues": {},
            "summary": {
                "total_queues": 0,
                "active_queues": 0,
                "total_drops": 0,
                "total_overflows": 0,
                "total_packets": 0,
                "congested_queues": []
            }
        }
        
        try:
            with open(queue_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                current_queue = None
                
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Detect queue line
                    if "queue" in line.lower() or "uc" in line.lower():
                        queue_match = re.search(r'(queue|uc)(\d+)', line, re.IGNORECASE)
                        if queue_match:
                            queue_type = queue_match.group(1).lower()
                            queue_id = queue_match.group(2)
                            current_queue = f"{queue_type}_{queue_id}"
                            
                            queue_counters["queues"][current_queue] = {
                                "drops": 0,
                                "overflows": 0,
                                "packets": 0,
                                "bytes": 0,
                                "utilization": 0.0,
                                "drop_rate": 0.0,
                                "status": "normal"
                            }
                            queue_counters["summary"]["total_queues"] += 1
                    
                    elif current_queue and ':' in line:
                        # Parse queue counters
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if current_queue in queue_counters["queues"]:
                            try:
                                numeric_value = int(re.search(r'[\d,]+', value).group().replace(',', ''))
                                
                                if "drop" in key:
                                    queue_counters["queues"][current_queue]["drops"] = numeric_value
                                    queue_counters["summary"]["total_drops"] += numeric_value
                                elif "overflow" in key:
                                    queue_counters["queues"][current_queue]["overflows"] = numeric_value
                                    queue_counters["summary"]["total_overflows"] += numeric_value
                                elif "packet" in key:
                                    queue_counters["queues"][current_queue]["packets"] = numeric_value
                                    queue_counters["summary"]["total_packets"] += numeric_value
                                elif "byte" in key:
                                    queue_counters["queues"][current_queue]["bytes"] = numeric_value
                                
                                # Calculate queue metrics
                                queue_data = queue_counters["queues"][current_queue]
                                if queue_data["packets"] > 0:
                                    queue_data["drop_rate"] = (queue_data["drops"] / queue_data["packets"]) * 100
                                    queue_data["utilization"] = min(100.0, queue_data["packets"] / 100000)  # Rough estimate
                                    queue_counters["summary"]["active_queues"] += 1
                                    
                                    # Classify queue status
                                    if queue_data["drop_rate"] > 5.0:
                                        queue_data["status"] = "critical"
                                        queue_counters["summary"]["congested_queues"].append(current_queue)
                                    elif queue_data["drop_rate"] > 1.0:
                                        queue_data["status"] = "warning"
                                    elif queue_data["utilization"] > 80:
                                        queue_data["status"] = "busy"
                                    else:
                                        queue_data["status"] = "normal"
                                        
                            except (ValueError, AttributeError):
                                continue
                
                self.extraction_metrics.data_points_extracted += len(queue_counters["queues"]) * 8
                
        except Exception as e:
            queue_counters["parse_error"] = str(e)
        
        return queue_counters
    
    def _extract_bgp_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed BGP data"""
        
        bgp_data = {
            "neighbor_status": {},
            "route_information": {},
            "message_statistics": {},
            "configuration_data": {},
            "performance_metrics": {}
        }
        
        # Extract BGP summary
        bgp_summary_files = self._find_files_by_pattern(temp_dir, ["bgp_summary", "bgp"])
        for bgp_file in bgp_summary_files:
            try:
                bgp_data["neighbor_status"] = self._parse_bgp_summary_detailed(bgp_file)
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing BGP summary: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        # Extract BGP routes
        bgp_route_files = self._find_files_by_pattern(temp_dir, ["bgp_routes", "route"])
        for route_file in bgp_route_files:
            try:
                route_data = self._parse_bgp_routes_detailed(route_file)
                bgp_data["route_information"].update(route_data)
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing BGP routes: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return bgp_data
    
    def _parse_bgp_summary_detailed(self, bgp_file_path: str) -> Dict[str, Any]:
        """Parse BGP summary with comprehensive detail"""
        
        bgp_summary = {
            "neighbors": {},
            "summary": {
                "total_neighbors": 0,
                "established_neighbors": 0,
                "active_neighbors": 0,
                "idle_neighbors": 0,
                "connecting_neighbors": 0,
                "total_routes_received": 0,
                "total_routes_advertised": 0,
                "total_messages_sent": 0,
                "total_messages_received": 0,
                "total_updates_sent": 0,
                "total_updates_received": 0,
                "total_keepalives_sent": 0,
                "total_keepalives_received": 0,
                "neighbor_uptime_stats": {},
                "as_path_analysis": {},
                "problematic_neighbors": []
            }
        }
        
        try:
            with open(bgp_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                current_neighbor = None
                
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Detect neighbor line
                    if re.match(r'^\d+\.\d+\.\d+\.\d+', line):
                        parts = line.split()
                        if len(parts) >= 8:
                            neighbor_ip = parts[0]
                            vrf = parts[1] if len(parts) > 1 else "default"
                            as_number = parts[2] if len(parts) > 2 else ""
                            msg_rcvd = parts[3] if len(parts) > 3 else "0"
                            msg_sent = parts[4] if len(parts) > 4 else "0"
                            tbl_ver = parts[5] if len(parts) > 5 else "0"
                            in_queue = parts[6] if len(parts) > 6 else "0"
                            out_queue = parts[7] if len(parts) > 7 else "0"
                            up_down = parts[8] if len(parts) > 8 else ""
                            state_pfxrcd = parts[9] if len(parts) > 9 else ""
                            
                            # Parse state and prefix count
                            state = "unknown"
                            prefixes_received = 0
                            
                            if "/" in state_pfxrcd:
                                state, prefixes_str = state_pfxrcd.split('/', 1)
                                try:
                                    prefixes_received = int(prefixes_str)
                                except ValueError:
                                    prefixes_received = 0
                            else:
                                state = state_pfxrcd
                            
                            bgp_summary["neighbors"][neighbor_ip] = {
                                "vrf": vrf,
                                "as_number": as_number,
                                "state": state,
                                "uptime": up_down,
                                "prefixes_received": prefixes_received,
                                "messages_received": self._parse_number(msg_rcvd),
                                "messages_sent": self._parse_number(msg_sent),
                                "table_version": self._parse_number(tbl_ver),
                                "in_queue": self._parse_number(in_queue),
                                "out_queue": self._parse_number(out_queue),
                                "prefixes_advertised": 0,
                                "updates_received": 0,
                                "updates_sent": 0,
                                "keepalives_received": 0,
                                "keepalives_sent": 0,
                                "notifications_sent": 0,
                                "notifications_received": 0,
                                "connection_attempts": 0,
                                "last_reset": "",
                                "reset_reason": "",
                                "health_score": 100,
                                "performance_metrics": {}
                            }
                            
                            bgp_summary["summary"]["total_neighbors"] += 1
                            bgp_summary["summary"]["total_routes_received"] += prefixes_received
                            bgp_summary["summary"]["total_messages_received"] += self._parse_number(msg_rcvd)
                            bgp_summary["summary"]["total_messages_sent"] += self._parse_number(msg_sent)
                            
                            # Classify neighbor state
                            if state.lower() == "established":
                                bgp_summary["summary"]["established_neighbors"] += 1
                            elif state.lower() == "active":
                                bgp_summary["summary"]["active_neighbors"] += 1
                                bgp_summary["neighbors"][neighbor_ip]["health_score"] -= 30
                            elif state.lower() == "idle":
                                bgp_summary["summary"]["idle_neighbors"] += 1
                                bgp_summary["neighbors"][neighbor_ip]["health_score"] -= 50
                            elif state.lower() == "connecting":
                                bgp_summary["summary"]["connecting_neighbors"] += 1
                                bgp_summary["neighbors"][neighbor_ip]["health_score"] -= 20
                            
                            current_neighbor = neighbor_ip
                    
                    elif current_neighbor and ":" in line:
                        # Parse neighbor details
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if current_neighbor in bgp_summary["neighbors"]:
                            if "route" in key and "received" in key:
                                try:
                                    routes = int(re.search(r'\d+', value).group())
                                    bgp_summary["neighbors"][current_neighbor]["prefixes_received"] = routes
                                except:
                                    pass
                            elif "route" in key and "advertised" in key:
                                try:
                                    routes = int(re.search(r'\d+', value).group())
                                    bgp_summary["neighbors"][current_neighbor]["prefixes_advertised"] = routes
                                    bgp_summary["summary"]["total_routes_advertised"] += routes
                                except:
                                    pass
                            elif "uptime" in key:
                                bgp_summary["neighbors"][current_neighbor]["uptime"] = value
                            elif "message" in key and "sent" in key:
                                try:
                                    messages = int(re.search(r'\d+', value).group())
                                    bgp_summary["neighbors"][current_neighbor]["messages_sent"] = messages
                                except:
                                    pass
                            elif "message" in key and "received" in key:
                                try:
                                    messages = int(re.search(r'\d+', value).group())
                                    bgp_summary["neighbors"][current_neighbor]["messages_received"] = messages
                                except:
                                    pass
                            elif "update" in key and "sent" in key:
                                try:
                                    updates = int(re.search(r'\d+', value).group())
                                    bgp_summary["neighbors"][current_neighbor]["updates_sent"] = updates
                                    bgp_summary["summary"]["total_updates_sent"] += updates
                                except:
                                    pass
                            elif "update" in key and "received" in key:
                                try:
                                    updates = int(re.search(r'\d+', value).group())
                                    bgp_summary["neighbors"][current_neighbor]["updates_received"] = updates
                                    bgp_summary["summary"]["total_updates_received"] += updates
                                except:
                                    pass
                            elif "keepalive" in key and "sent" in key:
                                try:
                                    keepalives = int(re.search(r'\d+', value).group())
                                    bgp_summary["neighbors"][current_neighbor]["keepalives_sent"] = keepalives
                                    bgp_summary["summary"]["total_keepalives_sent"] += keepalives
                                except:
                                    pass
                            elif "keepalive" in key and "received" in key:
                                try:
                                    keepalives = int(re.search(r'\d+', value).group())
                                    bgp_summary["neighbors"][current_neighbor]["keepalives_received"] = keepalives
                                    bgp_summary["summary"]["total_keepalives_received"] += keepalives
                                except:
                                    pass
                            elif "notification" in key and "sent" in key:
                                try:
                                    notifications = int(re.search(r'\d+', value).group())
                                    bgp_summary["neighbors"][current_neighbor]["notifications_sent"] = notifications
                                except:
                                    pass
                            elif "notification" in key and "received" in key:
                                try:
                                    notifications = int(re.search(r'\d+', value).group())
                                    bgp_summary["neighbors"][current_neighbor]["notifications_received"] = notifications
                                except:
                                    pass
                            elif "reset" in key and "reason" in key:
                                bgp_summary["neighbors"][current_neighbor]["reset_reason"] = value
                                bgp_summary["neighbors"][current_neighbor]["health_score"] -= 40
                
                # Calculate neighbor health scores and identify problematic neighbors
                for neighbor_ip, neighbor_data in bgp_summary["neighbors"].items():
                    # Calculate message ratio
                    total_messages = neighbor_data["messages_sent"] + neighbor_data["messages_received"]
                    if total_messages > 0:
                        update_ratio = (neighbor_data["updates_sent"] + neighbor_data["updates_received"]) / total_messages
                        if update_ratio < 0.1:
                            neighbor_data["health_score"] -= 10
                    
                    # Check for notifications
                    if neighbor_data["notifications_sent"] > 0 or neighbor_data["notifications_received"] > 0:
                        neighbor_data["health_score"] -= 20
                    
                    # Identify problematic neighbors
                    if neighbor_data["health_score"] < 70:
                        bgp_summary["summary"]["problematic_neighbors"].append(neighbor_ip)
                
                self.extraction_metrics.data_points_extracted += len(bgp_summary["neighbors"]) * 20
                
        except Exception as e:
            bgp_summary["parse_error"] = str(e)
        
        return bgp_summary
    
    def _parse_bgp_routes_detailed(self, route_file_path: str) -> Dict[str, Any]:
        """Parse BGP route information with comprehensive detail"""
        
        bgp_routes = {
            "routes": {},
            "summary": {
                "total_routes": 0,
                "ipv4_routes": 0,
                "ipv6_routes": 0,
                "best_routes": 0,
                "backup_routes": 0,
                "as_path_analysis": {},
                "origin_distribution": {},
                "med_distribution": {},
                "local_pref_distribution": {}
            }
        }
        
        try:
            with open(route_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                current_route = None
                
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parse route entry
                    if re.match(r'^[Bb]\s+', line) or re.match(r'^\*\s+', line):
                        parts = line.split()
                        if len(parts) >= 5:
                            route_type = parts[0] if parts[0] in ['B', 'R', 'S', 'C', 'i', 'e', '?', '*'] else "B"
                            network = parts[1] if re.match(r'^\d+\.\d+\.\d+\.\d+', parts[1]) else parts[2] if len(parts) > 2 else ""
                            next_hop = parts[2] if len(parts) > 2 and re.match(r'^\d+\.\d+\.\d+\.\d+', parts[2]) else parts[3] if len(parts) > 3 else ""
                            metric = parts[3] if len(parts) > 3 and not re.match(r'^\d+\.\d+\.\d+\.\d+', parts[3]) else "0"
                            locprf = parts[4] if len(parts) > 4 else "100"
                            weight = parts[5] if len(parts) > 5 else "0"
                            path = " ".join(parts[6:]) if len(parts) > 6 else ""
                            
                            current_route = network
                            bgp_routes["routes"][current_route] = {
                                "route_type": route_type,
                                "network": network,
                                "next_hop": next_hop,
                                "metric": self._parse_number(metric),
                                "local_pref": self._parse_number(locprf),
                                "weight": self._parse_number(weight),
                                "as_path": path,
                                "origin": "IGP",
                                "med": 0,
                                "community": "",
                                "is_best": route_type == "*",
                                "is_backup": False,
                                "age": "",
                                "received_from": ""
                            }
                            
                            bgp_routes["summary"]["total_routes"] += 1
                            
                            if ":" in network:  # IPv6 route
                                bgp_routes["summary"]["ipv6_routes"] += 1
                            else:  # IPv4 route
                                bgp_routes["summary"]["ipv4_routes"] += 1
                            
                            if route_type == "*":
                                bgp_routes["summary"]["best_routes"] += 1
                            else:
                                bgp_routes["summary"]["backup_routes"] += 1
                    
                    elif current_route and ":" in line:
                        # Parse route attributes
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if current_route in bgp_routes["routes"]:
                            if "origin" in key:
                                bgp_routes["routes"][current_route]["origin"] = value
                            elif "med" in key:
                                try:
                                    bgp_routes["routes"][current_route]["med"] = int(re.search(r'\d+', value).group())
                                except:
                                    pass
                            elif "community" in key:
                                bgp_routes["routes"][current_route]["community"] = value
                            elif "age" in key:
                                bgp_routes["routes"][current_route]["age"] = value
                            elif "received" in key and "from" in key:
                                bgp_routes["routes"][current_route]["received_from"] = value
                
                # Analyze AS path distribution
                as_path_counts = {}
                for route_data in bgp_routes["routes"].values():
                    as_path = route_data["as_path"]
                    if as_path:
                        as_path_counts[as_path] = as_path_counts.get(as_path, 0) + 1
                
                bgp_routes["summary"]["as_path_analysis"] = dict(sorted(as_path_counts.items(), key=lambda x: x[1], reverse=True)[:10])
                
                # Analyze origin distribution
                origin_counts = {}
                for route_data in bgp_routes["routes"].values():
                    origin = route_data["origin"]
                    origin_counts[origin] = origin_counts.get(origin, 0) + 1
                
                bgp_routes["summary"]["origin_distribution"] = origin_counts
                
                self.extraction_metrics.data_points_extracted += len(bgp_routes["routes"]) * 12
                
        except Exception as e:
            bgp_routes["parse_error"] = str(e)
        
        return bgp_routes
    
    def _extract_arp_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed ARP data"""
        
        arp_data = {
            "arp_table": {},
            "mac_analysis": {},
            "network_topology": {},
            "vendor_analysis": {}
        }
        
        # Extract ARP table
        arp_files = self._find_files_by_pattern(temp_dir, ["arp"])
        for arp_file in arp_files:
            try:
                arp_table = self._parse_arp_table_detailed(arp_file)
                arp_data["arp_table"].update(arp_table)
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing ARP table: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return arp_data
    
    def _parse_arp_table_detailed(self, arp_file_path: str) -> Dict[str, Any]:
        """Parse ARP table with comprehensive detail"""
        
        arp_table = {
            "entries": [],
            "summary": {
                "total_entries": 0,
                "unique_macs": set(),
                "unique_ips": set(),
                "interfaces": set(),
                "mac_vendors": {},
                "ip_ranges": {},
                "incomplete_entries": 0,
                "permanent_entries": 0,
                "dynamic_entries": 0
            }
        }
        
        try:
            with open(arp_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('IP address') or line.startswith('Address'):
                        continue
                    
                    parts = line.split()
                    if len(parts) >= 4:
                        ip = parts[0]
                        mac = parts[1] if len(parts) > 1 else ""
                        interface = parts[2] if len(parts) > 2 else ""
                        flags = parts[3] if len(parts) > 3 else ""
                        mask = parts[4] if len(parts) > 4 else ""
                        hw_type = parts[5] if len(parts) > 5 else ""
                        
                        # Validate MAC address format
                        if mac and (mac == "(incomplete)" or re.match(r'^[0-9a-fA-F:]{17}$', mac)):
                            entry = {
                                "ip_address": ip,
                                "mac_address": mac,
                                "interface": interface,
                                "flags": flags,
                                "mask": mask,
                                "hw_type": hw_type,
                                "vendor": self._identify_mac_vendor(mac) if mac != "(incomplete)" else "incomplete",
                                "is_permanent": "C" in flags,
                                "is_dynamic": "D" in flags,
                                "is_incomplete": mac == "(incomplete)",
                                "ip_type": self._classify_ip_address(ip),
                                "mac_type": self._classify_mac_address(mac) if mac != "(incomplete)" else "incomplete"
                            }
                            
                            arp_table["entries"].append(entry)
                            arp_table["summary"]["total_entries"] += 1
                            arp_table["summary"]["unique_macs"].add(mac)
                            arp_table["summary"]["unique_ips"].add(ip)
                            arp_table["summary"]["interfaces"].add(interface)
                            
                            # Count entry types
                            if entry["is_incomplete"]:
                                arp_table["summary"]["incomplete_entries"] += 1
                            elif entry["is_permanent"]:
                                arp_table["summary"]["permanent_entries"] += 1
                            elif entry["is_dynamic"]:
                                arp_table["summary"]["dynamic_entries"] += 1
                            
                            # Count MAC vendors
                            vendor = entry["vendor"]
                            if vendor != "incomplete":
                                arp_table["summary"]["mac_vendors"][vendor] = arp_table["summary"]["mac_vendors"].get(vendor, 0) + 1
                
                # Convert sets to counts
                arp_table["summary"]["unique_macs"] = len(arp_table["summary"]["unique_macs"])
                arp_table["summary"]["unique_ips"] = len(arp_table["summary"]["unique_ips"])
                arp_table["summary"]["interfaces"] = len(arp_table["summary"]["interfaces"])
                
                # Analyze IP ranges
                ip_ranges = {}
                for entry in arp_table["entries"]:
                    if entry["ip_address"] and entry["ip_address"] != "(incomplete)":
                        ip_class = self._get_ip_class(entry["ip_address"])
                        ip_ranges[ip_class] = ip_ranges.get(ip_class, 0) + 1
                
                arp_table["summary"]["ip_ranges"] = ip_ranges
                
                self.extraction_metrics.data_points_extracted += len(arp_table["entries"]) * 10
                
        except Exception as e:
            arp_table["parse_error"] = str(e)
        
        return arp_table
    
    def _identify_mac_vendor(self, mac: str) -> str:
        """Identify MAC address vendor with comprehensive database"""
        if not mac or mac == "(incomplete)":
            return "incomplete"
        
        mac_prefix = mac[:8].upper()  # First 3 octets
        
        vendor_map = {
            "00:11:22": "Dell Technologies",
            "9C:6B:00": "Dell Technologies",
            "C4:CB:E1": "Cisco Systems",
            "D0:C1:B5": "Hewlett Packard",
            "00:1B:21": "Juniper Networks",
            "00:07:E9": "Cisco Systems",
            "00:1C:F0": "Cisco Systems",
            "00:23:04": "Juniper Networks",
            "00:26:98": "Juniper Networks",
            "00:27:0E": "Juniper Networks",
            "00:90:0B": "Cisco Systems",
            "00:0F:B5": "Netgear",
            "00:13:02": "Intel Corporation",
            "00:15:5D": "Microsoft",
            "08:00:27": "Oracle VirtualBox",
            "00:0C:29": "VMware",
            "00:50:56": "VMware",
            "00:05:69": "VMware",
            "00:1C:42": "Parallels",
            "00:03:FF": "Xensource",
            "00:16:3E": "Xensource",
            "B8:27:EB": "Raspberry Pi",
            "DC:A6:32": "Raspberry Pi",
            "E8:94:F6": "Raspberry Pi",
            "B8:AE:ED": "Raspberry Pi"
        }
        
        return vendor_map.get(mac_prefix, "unknown")
    
    def _classify_mac_address(self, mac: str) -> str:
        """Classify MAC address type"""
        if not mac or mac == "(incomplete)":
            return "incomplete"
        
        first_byte = mac[:2].upper()
        
        # Check for multicast/broadcast
        first_byte_int = int(first_byte, 16)
        if first_byte_int & 0x01:  # Least significant bit of first byte
            return "multicast"
        elif first_byte_int == 0xFF:
            return "broadcast"
        elif first_byte_int & 0x02:  # Locally administered
            return "local"
        else:
            return "universal"
    
    def _classify_ip_address(self, ip: str) -> str:
        """Classify IP address type"""
        if not ip or ip == "(incomplete)":
            return "incomplete"
        
        try:
            parts = list(map(int, ip.split('.')))
            if parts[0] == 10:
                return "private_a"
            elif parts[0] == 172 and 16 <= parts[1] <= 31:
                return "private_b"
            elif parts[0] == 192 and parts[1] == 168:
                return "private_c"
            elif parts[0] == 169 and parts[1] == 254:
                return "link_local"
            elif parts[0] == 127:
                return "loopback"
            elif parts[0] >= 224:
                return "multicast"
            else:
                return "public"
        except:
            return "invalid"
    
    def _get_ip_class(self, ip: str) -> str:
        """Get IP address class"""
        try:
            first_octet = int(ip.split('.')[0])
            if 1 <= first_octet <= 126:
                return "Class A"
            elif 128 <= first_octet <= 191:
                return "Class B"
            elif 192 <= first_octet <= 223:
                return "Class C"
            elif 224 <= first_octet <= 239:
                return "Class D"
            elif 240 <= first_octet <= 255:
                return "Class E"
        except:
            pass
        return "Unknown"
    
    def _extract_service_data_comprehensive(self, temp_dir: str) -> Dict[str, Any]:
        """Extract comprehensive service data"""
        
        service_data = {
            "container_data": self._extract_container_data_detailed(temp_dir),
            "process_data": self._extract_process_data_detailed(temp_dir),
            "dependency_data": self._extract_dependency_data_detailed(temp_dir),
            "resource_data": self._extract_resource_data_detailed(temp_dir),
            "error_data": self._extract_service_error_data_detailed(temp_dir),
            "startup_data": self._extract_startup_data_detailed(temp_dir)
        }
        
        return service_data
    
    def _extract_container_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed container data"""
        
        container_data = {
            "containers": {},
            "summary": {
                "total_containers": 0,
                "running_containers": 0,
                "stopped_containers": 0,
                "healthy_containers": 0,
                "unhealthy_containers": 0,
                "total_memory_usage": 0,
                "total_cpu_usage": 0.0,
                "container_types": {},
                "resource_utilization": {}
            }
        }
        
        # Extract docker ps output
        docker_ps_files = self._find_files_by_pattern(temp_dir, ["docker_ps", "docker"])
        for docker_file in docker_ps_files:
            try:
                docker_data = self._parse_docker_ps_detailed(docker_file)
                container_data["containers"].update(docker_data["containers"])
                container_data["summary"].update(docker_data["summary"])
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing docker ps: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        # Extract services summary
        services_files = self._find_files_by_pattern(temp_dir, ["services.summary", "services"])
        for services_file in services_files:
            try:
                services_data = self._parse_services_summary_detailed(services_file)
                container_data["containers"].update(services_data["containers"])
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing services summary: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return container_data
    
    def _parse_docker_ps_detailed(self, docker_file_path: str) -> Dict[str, Any]:
        """Parse docker ps output with comprehensive detail"""
        
        docker_data = {
            "containers": {},
            "summary": {
                "total_containers": 0,
                "running_containers": 0,
                "stopped_containers": 0,
                "healthy_containers": 0,
                "unhealthy_containers": 0,
                "total_memory_usage": 0,
                "total_cpu_usage": 0.0,
                "container_types": {},
                "resource_utilization": {}
            }
        }
        
        try:
            with open(docker_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
                # Skip header line
                for line in lines[1:]:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split()
                    if len(parts) >= 7:
                        container_id = parts[0]
                        image = parts[1]
                        command = parts[2]
                        created = parts[3]
                        status = parts[4]
                        ports = parts[5] if len(parts) > 5 else ""
                        names = parts[6] if len(parts) > 6 else ""
                        
                        # Parse status for detailed information
                        status_details = self._parse_container_status(status)
                        
                        docker_data["containers"][container_id] = {
                            "container_id": container_id,
                            "image": image,
                            "command": command,
                            "created": created,
                            "status": status,
                            "status_details": status_details,
                            "ports": ports,
                            "names": names,
                            "health_status": "healthy" if "Up" in status else "unhealthy",
                            "memory_usage": 0,
                            "cpu_usage": 0.0,
                            "network_usage": {},
                            "restart_count": 0,
                            "start_time": "",
                            "container_type": self._classify_container_image(image),
                            "resource_limits": {},
                            "mounts": [],
                            "environment": []
                        }
                        
                        docker_data["summary"]["total_containers"] += 1
                        
                        if "Up" in status:
                            docker_data["summary"]["running_containers"] += 1
                            docker_data["summary"]["healthy_containers"] += 1
                        else:
                            docker_data["summary"]["stopped_containers"] += 1
                            docker_data["summary"]["unhealthy_containers"] += 1
                        
                        # Count container types
                        container_type = docker_data["containers"][container_id]["container_type"]
                        docker_data["summary"]["container_types"][container_type] = docker_data["summary"]["container_types"].get(container_type, 0) + 1
                
                self.extraction_metrics.data_points_extracted += len(docker_data["containers"]) * 15
                
        except Exception as e:
            docker_data["parse_error"] = str(e)
        
        return docker_data
    
    def _parse_container_status(self, status: str) -> Dict[str, Any]:
        """Parse container status for detailed information"""
        status_details = {
            "state": "unknown",
            "health": "unknown",
            "uptime": "",
            "exit_code": 0,
            "error": ""
        }
        
        if "Up" in status:
            status_details["state"] = "running"
            # Extract uptime
            uptime_match = re.search(r'Up\s+([\w\s]+)', status)
            if uptime_match:
                status_details["uptime"] = uptime_match.group(1).strip()
        elif "Exited" in status:
            status_details["state"] = "exited"
            # Extract exit code
            exit_match = re.search(r'Exited\s+\((\d+)\)', status)
            if exit_match:
                status_details["exit_code"] = int(exit_match.group(1))
        elif "Created" in status:
            status_details["state"] = "created"
        elif "Restarting" in status:
            status_details["state"] = "restarting"
        elif "Removing" in status:
            status_details["state"] = "removing"
        elif "Paused" in status:
            status_details["state"] = "paused"
        
        # Check for health status
        if "healthy" in status.lower():
            status_details["health"] = "healthy"
        elif "unhealthy" in status.lower():
            status_details["health"] = "unhealthy"
        elif "starting" in status.lower():
            status_details["health"] = "starting"
        
        return status_details
    
    def _classify_container_image(self, image: str) -> str:
        """Classify container image type"""
        image_lower = image.lower()
        
        if "sonic" in image_lower:
            if "swss" in image_lower:
                return "sonic_swss"
            elif "syncd" in image_lower:
                return "sonic_syncd"
            elif "bgp" in image_lower:
                return "sonic_bgp"
            elif "snmp" in image_lower:
                return "sonic_snmp"
            elif "lldp" in image_lower:
                return "sonic_lldp"
            elif "telemetry" in image_lower:
                return "sonic_telemetry"
            elif "teamd" in image_lower:
                return "sonic_teamd"
            else:
                return "sonic_other"
        elif "redis" in image_lower:
            return "redis"
        elif "database" in image_lower:
            return "database"
        elif "web" in image_lower or "nginx" in image_lower or "apache" in image_lower:
            return "web"
        elif "app" in image_lower or "application" in image_lower:
            return "application"
        else:
            return "other"
    
    def _parse_services_summary_detailed(self, services_file_path: str) -> Dict[str, Any]:
        """Parse services summary with comprehensive detail"""
        
        services_data = {
            "containers": {},
            "summary": {
                "total_services": 0,
                "running_services": 0,
                "stopped_services": 0,
                "failed_services": 0,
                "service_types": {},
                "resource_usage": {}
            }
        }
        
        try:
            with open(services_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parse service information
                    if ':' in line:
                        service_name, status = line.split(':', 1)
                        service_name = service_name.strip()
                        status = status.strip()
                        
                        services_data["containers"][service_name] = {
                            "container_id": service_name,
                            "names": service_name,
                            "status": status,
                            "health_status": "healthy" if "running" in status.lower() else "unhealthy",
                            "container_type": self._classify_service_name(service_name),
                            "memory_usage": 0,
                            "cpu_usage": 0.0
                        }
                        
                        services_data["summary"]["total_services"] += 1
                        
                        if "running" in status.lower():
                            services_data["summary"]["running_services"] += 1
                        elif "stopped" in status.lower():
                            services_data["summary"]["stopped_services"] += 1
                        elif "failed" in status.lower():
                            services_data["summary"]["failed_services"] += 1
                        
                        # Count service types
                        service_type = services_data["containers"][service_name]["container_type"]
                        services_data["summary"]["service_types"][service_type] = services_data["summary"]["service_types"].get(service_type, 0) + 1
                
                self.extraction_metrics.data_points_extracted += len(services_data["containers"]) * 8
                
        except Exception as e:
            services_data["parse_error"] = str(e)
        
        return services_data
    
    def _classify_service_name(self, service_name: str) -> str:
        """Classify service name type"""
        name_lower = service_name.lower()
        
        if "swss" in name_lower:
            return "sonic_swss"
        elif "syncd" in name_lower:
            return "sonic_syncd"
        elif "bgp" in name_lower:
            return "sonic_bgp"
        elif "snmp" in name_lower:
            return "sonic_snmp"
        elif "lldp" in name_lower:
            return "sonic_lldp"
        elif "telemetry" in name_lower:
            return "sonic_telemetry"
        elif "teamd" in name_lower:
            return "sonic_teamd"
        elif "redis" in name_lower:
            return "redis"
        elif "database" in name_lower:
            return "database"
        else:
            return "other"
    
    def _extract_configuration_data_comprehensive(self, temp_dir: str) -> Dict[str, Any]:
        """Extract comprehensive configuration data"""
        
        config_data = {
            "config_db": {},
            "interface_config": {},
            "bgp_config": {},
            "vlan_config": {},
            "system_config": {},
            "acl_config": {},
            "qos_config": {}
        }
        
        # Look for CONFIG_DB.json
        config_db_files = self._find_files_by_pattern(temp_dir, ["config_db.json"])
        for config_file in config_db_files:
            try:
                with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
                    config_data["config_db"] = json.load(f)
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing CONFIG_DB.json: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        # Look for other config files
        config_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if "config" in file.lower() and file.endswith(".json"):
                    config_files.append(os.path.join(root, file))
        
        for config_file in config_files:
            try:
                with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = json.load(f)
                    config_data[os.path.basename(config_file)] = content
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing config file {config_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return config_data
    
    def _extract_performance_data_comprehensive(self, temp_dir: str) -> Dict[str, Any]:
        """Extract comprehensive performance data"""
        
        perf_data = {
            "cpu_performance": {},
            "memory_performance": {},
            "network_performance": {},
            "storage_performance": {},
            "system_performance": {}
        }
        
        # Look for performance files
        perf_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if "performance" in file.lower() or "perf" in file.lower() or "stat" in file.lower():
                    perf_files.append(os.path.join(root, file))
        
        for perf_file in perf_files:
            try:
                with open(perf_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    perf_data["system_performance"][os.path.basename(perf_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing performance file {perf_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return perf_data
    
    def _extract_log_data_comprehensive(self, temp_dir: str) -> Dict[str, Any]:
        """Extract comprehensive log data"""
        
        log_data = {
            "system_logs": {},
            "service_logs": {},
            "error_logs": {},
            "debug_logs": {}
        }
        
        # Look for log files
        log_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if "log" in file.lower():
                    log_files.append(os.path.join(root, file))
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    log_data["system_logs"][os.path.basename(log_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing log file {log_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return log_data
    
    def _extract_error_data_comprehensive(self, temp_dir: str) -> Dict[str, Any]:
        """Extract comprehensive error data"""
        
        error_data = {
            "error_logs": {},
            "error_patterns": {},
            "error_statistics": {},
            "critical_errors": []
        }
        
        # Look for error files
        error_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if "error" in file.lower() or "fail" in file.lower():
                    error_files.append(os.path.join(root, file))
        
        for error_file in error_files:
            try:
                with open(error_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    error_data["error_logs"][os.path.basename(error_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing error file {error_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return error_data
    
    def _extract_security_data_comprehensive(self, temp_dir: str) -> Dict[str, Any]:
        """Extract comprehensive security data"""
        
        security_data = {
            "access_control": {},
            "authentication": {},
            "encryption": {},
            "firewall_rules": {},
            "security_policies": {}
        }
        
        # Look for security files
        security_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if "security" in file.lower() or "acl" in file.lower() or "auth" in file.lower():
                    security_files.append(os.path.join(root, file))
        
        for security_file in security_files:
            try:
                with open(security_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    security_data["security_policies"][os.path.basename(security_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing security file {security_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return security_data
    
    def _extract_capacity_data_comprehensive(self, temp_dir: str) -> Dict[str, Any]:
        """Extract comprehensive capacity data"""
        
        capacity_data = {
            "interface_capacity": {},
            "memory_capacity": {},
            "storage_capacity": {},
            "power_capacity": {},
            "cooling_capacity": {}
        }
        
        # Look for capacity files
        capacity_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if "capacity" in file.lower() or "usage" in file.lower():
                    capacity_files.append(os.path.join(root, file))
        
        for capacity_file in capacity_files:
            try:
                with open(capacity_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    capacity_data["interface_capacity"][os.path.basename(capacity_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing capacity file {capacity_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return capacity_data
    
    def _extract_process_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed process data"""
        
        process_data = {
            "processes": {},
            "summary": {
                "total_processes": 0,
                "running_processes": 0,
                "sleeping_processes": 0,
                "zombie_processes": 0,
                "total_memory_usage": 0,
                "total_cpu_usage": 0.0
            }
        }
        
        # Look for process files
        process_files = self._find_files_by_pattern(temp_dir, ["process", "ps"])
        for process_file in process_files:
            try:
                with open(process_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    process_data["processes"][os.path.basename(process_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing process file {process_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return process_data
    
    def _extract_dependency_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed dependency data"""
        
        dependency_data = {
            "dependencies": {},
            "startup_order": {},
            "service_graph": {}
        }
        
        # Look for dependency files
        dependency_files = self._find_files_by_pattern(temp_dir, ["depend", "service"])
        for dependency_file in dependency_files:
            try:
                with open(dependency_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    dependency_data["dependencies"][os.path.basename(dependency_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing dependency file {dependency_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return dependency_data
    
    def _extract_resource_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed resource data"""
        
        resource_data = {
            "cpu_resources": {},
            "memory_resources": {},
            "disk_resources": {},
            "network_resources": {}
        }
        
        # Look for resource files
        resource_files = self._find_files_by_pattern(temp_dir, ["usage", "resource"])
        for resource_file in resource_files:
            try:
                with open(resource_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    resource_data["cpu_resources"][os.path.basename(resource_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing resource file {resource_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return resource_data
    
    def _extract_service_error_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed service error data"""
        
        error_data = {
            "service_errors": {},
            "error_patterns": {},
            "error_counts": {}
        }
        
        # Look for service error files
        error_files = self._find_files_by_pattern(temp_dir, ["error", "fail"])
        for error_file in error_files:
            try:
                with open(error_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    error_data["service_errors"][os.path.basename(error_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing service error file {error_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return error_data
    
    def _extract_startup_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed startup data"""
        
        startup_data = {
            "startup_sequence": {},
            "startup_times": {},
            "boot_timeline": {}
        }
        
        # Look for startup files
        startup_files = self._find_files_by_pattern(temp_dir, ["startup", "boot"])
        for startup_file in startup_files:
            try:
                with open(startup_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    startup_data["startup_sequence"][os.path.basename(startup_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing startup file {startup_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return startup_data
    
    def _extract_port_channel_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed port channel data"""
        
        port_channel_data = {
            "port_channels": {},
            "lacp_status": {},
            "member_interfaces": {}
        }
        
        # Look for port channel files
        pc_files = self._find_files_by_pattern(temp_dir, ["portchannel", "lag", "port_channel"])
        for pc_file in pc_files:
            try:
                with open(pc_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    port_channel_data["port_channels"][os.path.basename(pc_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing port channel file {pc_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return port_channel_data
    
    def _extract_routing_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed routing data"""
        
        routing_data = {
            "routing_tables": {},
            "route_statistics": {}
        }
        
        # Look for routing files
        routing_files = self._find_files_by_pattern(temp_dir, ["route", "rib", "routing"])
        for routing_file in routing_files:
            try:
                with open(routing_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    routing_data["routing_tables"][os.path.basename(routing_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing routing file {routing_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return routing_data
    
    def _extract_hardware_counter_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed hardware counter data"""
        
        hw_counter_data = {
            "counters": {},
            "statistics": {}
        }
        
        # Look for counter files
        counter_files = self._find_files_by_pattern(temp_dir, ["counter", "statistic"])
        for counter_file in counter_files:
            try:
                with open(counter_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    hw_counter_data["counters"][os.path.basename(counter_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing counter file {counter_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return hw_counter_data
    
    def _extract_qos_data_detailed(self, temp_dir: str) -> Dict[str, Any]:
        """Extract detailed QoS data"""
        
        qos_data = {
            "qos_policies": {},
            "queue_config": {}
        }
        
        # Look for QoS files
        qos_files = self._find_files_by_pattern(temp_dir, ["qos", "queue"])
        for qos_file in qos_files:
            try:
                with open(qos_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    qos_data["qos_policies"][os.path.basename(qos_file)] = content.strip()
                self.extraction_metrics.files_processed += 1
            except Exception as e:
                logging.error(f"Error parsing QoS file {qos_file}: {e}")
                self.extraction_metrics.parsing_errors += 1
        
        return qos_data
    
    # Helper methods
    def _find_files_by_pattern(self, temp_dir: str, patterns: List[str]) -> List[str]:
        """Find files by pattern"""
        found_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_lower = file.lower()
                for pattern in patterns:
                    if pattern in file_lower:
                        found_files.append(os.path.join(root, file))
                        break
        return found_files
    
    def _is_interface_line(self, line: str) -> bool:
        """Check if line contains interface name"""
        return re.match(r'^[Ee]thernet\d+|^[Pp]ort[Cc]hannel\d+|^[Vv]lan\d+', line.strip())
    
    def _extract_interface_name(self, line: str) -> Optional[str]:
        """Extract interface name from line"""
        match = re.search(r'([Ee]thernet\d+|[Pp]ort[Cc]hannel\d+|[Vv]lan\d+)', line)
        return match.group(1) if match else None
    
    def _parse_number(self, value_str: str) -> int:
        """Parse number from string"""
        try:
            # Remove commas and convert to int
            clean_value = re.sub(r'[,\s]', '', value_str)
            return int(clean_value)
        except (ValueError, AttributeError):
            return 0
    
    def _initialize_extraction_patterns(self) -> Dict[str, Any]:
        """Initialize extraction patterns"""
        return {
            "cpu_patterns": {
                "processor_info": r"processor\s*:\s*(\d+)",
                "vendor_id": r"vendor_id\s*:\s*(.+)",
                "model_name": r"model name\s*:\s*(.+)",
                "cpu_mhz": r"cpu mhz\s*:\s*([\d.]+)"
            },
            "memory_patterns": {
                "memtotal": r"memtotal\s*:\s*(\d+)",
                "memfree": r"memfree\s*:\s*(\d+)",
                "memavailable": r"memavailable\s*:\s*(\d+)"
            },
            "network_patterns": {
                "interface": r"([Ee]thernet\d+|[Pp]ort[Cc]hannel\d+)",
                "rx_packets": r"rx[_\s]*packets\s*:\s*(\d+)",
                "tx_packets": r"tx[_\s]*packets\s*:\s*(\d+)"
            }
        }
    
    def _initialize_parsing_rules(self) -> Dict[str, Any]:
        """Initialize parsing rules"""
        return {
            "numeric_extraction": r"[\d,]+",
            "mac_address": r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}",
            "ip_address": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
            "timestamp": r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}"
        }
    
    def _initialize_data_validators(self) -> Dict[str, Any]:
        """Initialize data validators"""
        return {
            "mac_validator": lambda x: re.match(r"^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$", x) is not None,
            "ip_validator": lambda x: re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", x) is not None,
            "numeric_validator": lambda x: isinstance(x, (int, float)) or str(x).replace(',', '').isdigit()
        }
    
    def _calculate_data_quality_score(self, extracted_data: Dict[str, Any]) -> float:
        """Calculate data quality score"""
        total_files = self.extraction_metrics.files_processed
        total_data_points = self.extraction_metrics.data_points_extracted
        parsing_errors = self.extraction_metrics.parsing_errors
        
        if total_files == 0:
            return 0.0
        
        # Base score from successful files
        file_success_rate = (total_files - parsing_errors) / total_files
        
        # Bonus for data points extracted
        data_point_bonus = min(1.0, total_data_points / (total_files * 10))  # Expect at least 10 data points per file
        
        # Penalty for parsing errors
        error_penalty = parsing_errors / max(1, total_files)
        
        quality_score = (file_success_rate * 0.6) + (data_point_bonus * 0.4) - (error_penalty * 0.2)
        
        return max(0.0, min(1.0, quality_score))

# ============================================================================
# MAIN EXECUTION FOR TESTING
# ============================================================================

if __name__ == "__main__":
    # Test the advanced data extractor
    extractor = AdvancedDataExtractor()
    
    # Example usage (would need actual temp_dir path)
    # extracted_data = extractor.extract_comprehensive_data("/path/to/extracted/archive")
    # print(json.dumps(extracted_data, indent=2, default=str))
    
    print("Advanced Data Extractor initialized successfully")
    print(f"Extraction patterns: {len(extractor.extraction_patterns)}")
    print(f"Parsing rules: {len(extractor.parsing_rules)}")
    print(f"Data validators: {len(extractor.data_validators)}")