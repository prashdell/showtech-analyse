#!/usr/bin/env python3
"""
Comprehensive Technical Analysis Templates and Frameworks
Expert-level analysis templates with consistent technical detail extraction
"""

import json
import re
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# ============================================================================
# ANALYSIS FRAMEWORK ENUMS AND DATA STRUCTURES
# ============================================================================

class AnalysisDepth(Enum):
    """Analysis depth levels"""
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"
    EXPERT = "expert"

class SeverityLevel(Enum):
    """Severity classification levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class HealthStatus(Enum):
    """Health status classifications"""
    HEALTHY = "healthy"
    WARNING = "warning"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

@dataclass
class TechnicalMetric:
    """Technical metric with context and analysis"""
    name: str
    value: Union[int, float, str]
    unit: str
    threshold: Optional[float] = None
    status: Optional[HealthStatus] = None
    trend: Optional[str] = None
    analysis: Optional[str] = None
    recommendations: List[str] = None
    
    def __post_init__(self):
        if self.recommendations is None:
            self.recommendations = []

@dataclass
class SystemComponent:
    """System component with comprehensive analysis"""
    name: str
    type: str
    status: HealthStatus
    metrics: List[TechnicalMetric]
    configuration: Dict[str, Any]
    dependencies: List[str]
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    
    def __post_init__(self):
        if self.issues is None:
            self.issues = []
        if self.recommendations is None:
            self.recommendations = []

# ============================================================================
# COMPREHENSIVE ANALYSIS FRAMEWORKS
# ============================================================================

class HardwareAnalysisFramework:
    """Comprehensive hardware analysis framework"""
    
    def __init__(self):
        self.cpu_analysis_template = self._create_cpu_analysis_template()
        self.memory_analysis_template = self._create_memory_analysis_template()
        self.temperature_analysis_template = self._create_temperature_analysis_template()
        self.power_analysis_template = self._create_power_analysis_template()
        self.cooling_analysis_template = self._create_cooling_analysis_template()
        self.pci_analysis_template = self._create_pci_analysis_template()
    
    def analyze_cpu_comprehensive(self, cpu_data: Dict[str, Any]) -> SystemComponent:
        """Comprehensive CPU analysis with expert-level detail"""
        
        metrics = []
        issues = []
        recommendations = []
        
        # Extract CPU information
        processor_info = cpu_data.get("processor_info", {})
        core_analysis = cpu_data.get("core_analysis", {})
        architecture_details = cpu_data.get("architecture_details", {})
        performance_metrics = cpu_data.get("performance_metrics", {})
        
        # Create technical metrics
        metrics.append(TechnicalMetric(
            name="Total Cores",
            value=core_analysis.get("total_cores", 0),
            unit="cores",
            threshold=4,
            analysis="CPU core count for parallel processing capability"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total Threads",
            value=core_analysis.get("total_threads", 0),
            unit="threads",
            threshold=8,
            analysis="Total logical threads for concurrent processing"
        ))
        
        metrics.append(TechnicalMetric(
            name="CPU Frequency",
            value=float(processor_info.get("cpu_mhz", "0")),
            unit="MHz",
            threshold=2000,
            analysis="Processor clock speed affecting performance"
        ))
        
        # Analyze CPU utilization
        cpu_util = performance_metrics.get("cpu_utilization", {})
        if cpu_util:
            user_percent = cpu_util.get("user", 0)
            system_percent = cpu_util.get("system", 0)
            idle_percent = cpu_util.get("idle", 0)
            total_util = user_percent + system_percent
            
            metrics.append(TechnicalMetric(
                name="CPU Utilization",
                value=total_util,
                unit="%",
                threshold=80,
                status=self._classify_health_status(total_util, 80, 90),
                analysis="Combined user and system CPU utilization"
            ))
            
            metrics.append(TechnicalMetric(
                name="Idle Percentage",
                value=idle_percent,
                unit="%",
                threshold=20,
                status=self._classify_health_status(100 - idle_percent, 80, 90),
                analysis="CPU idle time indicating available capacity"
            ))
        
        # Analyze load average
        load_avg = performance_metrics.get("load_average", {})
        if load_avg:
            load_1min = load_avg.get("1min", 0)
            load_5min = load_avg.get("5min", 0)
            load_15min = load_avg.get("15min", 0)
            
            metrics.append(TechnicalMetric(
                name="Load Average (1min)",
                value=load_1min,
                unit="load",
                threshold=core_analysis.get("total_cores", 1),
                analysis="1-minute load average compared to CPU cores"
            ))
            
            metrics.append(TechnicalMetric(
                name="Load Average (5min)",
                value=load_5min,
                unit="load",
                threshold=core_analysis.get("total_cores", 1),
                analysis="5-minute load average indicating sustained load"
            ))
        
        # Analyze context switches
        context_switches = performance_metrics.get("context_switches", 0)
        metrics.append(TechnicalMetric(
            name="Context Switches",
            value=context_switches,
            unit="switches",
            threshold=1000000,
            analysis="Number of context switches indicating system activity"
        ))
        
        # Identify issues
        if total_util > 90:
            issues.append({
                "severity": SeverityLevel.CRITICAL.value,
                "category": "performance",
                "description": "CPU utilization critically high",
                "impact": "System performance severely degraded",
                "evidence": f"CPU utilization at {total_util}%"
            })
            recommendations.append("Investigate high CPU utilization processes")
            recommendations.append("Consider CPU upgrade or load balancing")
        elif total_util > 80:
            issues.append({
                "severity": SeverityLevel.HIGH.value,
                "category": "performance",
                "description": "CPU utilization high",
                "impact": "System performance degraded",
                "evidence": f"CPU utilization at {total_util}%"
            })
            recommendations.append("Monitor CPU utilization trends")
            recommendations.append("Optimize CPU-intensive processes")
        
        if load_1min > core_analysis.get("total_cores", 1) * 2:
            issues.append({
                "severity": SeverityLevel.HIGH.value,
                "category": "performance",
                "description": "Load average exceeds CPU capacity",
                "impact": "System overload possible",
                "evidence": f"Load average {load_1min} vs {core_analysis.get('total_cores', 1)} cores"
            })
            recommendations.append("Investigate processes causing high load")
            recommendations.append("Consider horizontal scaling")
        
        # Analyze CPU features and capabilities
        cpu_flags = processor_info.get("flags", [])
        virtualization_support = "vmx" in cpu_flags or "svm" in cpu_flags
        aes_support = "aes" in cpu_flags
        avx_support = "avx" in cpu_flags
        
        metrics.append(TechnicalMetric(
            name="Virtualization Support",
            value="Yes" if virtualization_support else "No",
            unit="boolean",
            analysis="CPU virtualization capability for container workloads"
        ))
        
        metrics.append(TechnicalMetric(
            name="AES Encryption Support",
            value="Yes" if aes_support else "No",
            unit="boolean",
            analysis="Hardware acceleration for encryption operations"
        ))
        
        metrics.append(TechnicalMetric(
            name="AVX Vector Operations",
            value="Yes" if avx_support else "No",
            unit="boolean",
            analysis="Advanced vector extensions for parallel processing"
        ))
        
        # Generate recommendations based on analysis
        if not virtualization_support:
            recommendations.append("Consider CPU upgrade with virtualization support for container workloads")
        
        if not aes_support:
            recommendations.append("CPU lacks AES support - encryption operations may be slower")
        
        if core_analysis.get("total_cores", 0) < 4:
            recommendations.append("Consider CPU upgrade for better parallel processing")
        
        if float(processor_info.get("cpu_mhz", "0")) < 2000:
            recommendations.append("CPU frequency below 2GHz may impact performance")
        
        return SystemComponent(
            name="CPU Subsystem",
            type="hardware",
            status=self._calculate_component_status(issues),
            metrics=metrics,
            configuration=processor_info,
            dependencies=["memory", "power", "cooling"],
            issues=issues,
            recommendations=recommendations
        )
    
    def analyze_memory_comprehensive(self, memory_data: Dict[str, Any]) -> SystemComponent:
        """Comprehensive memory analysis with expert-level detail"""
        
        metrics = []
        issues = []
        recommendations = []
        
        # Extract memory information
        memory_info = memory_data.get("memory_info", {})
        utilization_analysis = memory_data.get("utilization_analysis", {})
        cache_analysis = memory_data.get("cache_analysis", {})
        slab_analysis = memory_data.get("slab_analysis", {})
        swap_analysis = utilization_analysis.get("swap_utilization", {})
        
        # Create technical metrics
        total_memory_mb = memory_info.get("total_memory_kb", 0) // 1024
        used_memory_mb = utilization_analysis.get("used_memory_mb", 0)
        free_memory_mb = utilization_analysis.get("free_memory_mb", 0)
        available_memory_mb = utilization_analysis.get("available_memory_mb", 0)
        utilization_percent = utilization_analysis.get("utilization_percent", 0)
        
        metrics.append(TechnicalMetric(
            name="Total Memory",
            value=total_memory_mb,
            unit="MB",
            threshold=4096,
            analysis="Total physical memory available to system"
        ))
        
        metrics.append(TechnicalMetric(
            name="Used Memory",
            value=used_memory_mb,
            unit="MB",
            threshold=total_memory_mb * 0.8,
            status=self._classify_health_status(utilization_percent, 75, 90),
            analysis="Memory currently in use by processes and system"
        ))
        
        metrics.append(TechnicalMetric(
            name="Available Memory",
            value=available_memory_mb,
            unit="MB",
            threshold=1024,
            status=self._classify_health_status(100 - utilization_percent, 25, 10),
            analysis="Memory available for new processes"
        ))
        
        metrics.append(TechnicalMetric(
            name="Memory Utilization",
            value=utilization_percent,
            unit="%",
            threshold=80,
            status=self._classify_health_status(utilization_percent, 75, 90),
            analysis="Percentage of total memory currently utilized"
        ))
        
        # Analyze swap utilization
        swap_total_mb = swap_analysis.get("swap_total_mb", 0)
        swap_used_mb = swap_analysis.get("swap_used_mb", 0)
        swap_utilization_percent = swap_analysis.get("swap_utilization_percent", 0)
        
        if swap_total_mb > 0:
            metrics.append(TechnicalMetric(
                name="Swap Total",
                value=swap_total_mb,
                unit="MB",
                analysis="Total swap space available for memory overflow"
            ))
            
            metrics.append(TechnicalMetric(
                name="Swap Used",
                value=swap_used_mb,
                unit="MB",
                threshold=swap_total_mb * 0.5,
                status=self._classify_health_status(swap_utilization_percent, 50, 80),
                analysis="Swap space currently in use"
            ))
            
            metrics.append(TechnicalMetric(
                name="Swap Utilization",
                value=swap_utilization_percent,
                unit="%",
                threshold=50,
                status=self._classify_health_status(swap_utilization_percent, 50, 80),
                analysis="Percentage of swap space utilized"
            ))
        
        # Analyze cache efficiency
        cache_memory_mb = cache_analysis.get("cached_memory_mb", 0)
        cache_percentage = cache_analysis.get("cache_percentage", 0)
        cache_efficiency = cache_analysis.get("cache_efficiency", "unknown")
        
        metrics.append(TechnicalMetric(
            name="Cached Memory",
            value=cache_memory_mb,
            unit="MB",
            analysis="Memory used for file system caching"
        ))
        
        metrics.append(TechnicalMetric(
            name="Cache Percentage",
            value=cache_percentage,
            unit="%",
            analysis="Percentage of total memory used for caching"
        ))
        
        metrics.append(TechnicalMetric(
            name="Cache Efficiency",
            value=cache_efficiency,
            unit="rating",
            analysis="Efficiency of memory caching system"
        ))
        
        # Analyze buffer usage
        buffer_memory_mb = cache_analysis.get("buffer_memory_mb", 0)
        buffer_percentage = cache_analysis.get("buffer_percentage", 0)
        buffer_status = cache_analysis.get("buffer_status", "unknown")
        
        metrics.append(TechnicalMetric(
            name="Buffer Memory",
            value=buffer_memory_mb,
            unit="MB",
            analysis="Memory used for block device buffers"
        ))
        
        metrics.append(TechnicalMetric(
            name="Buffer Percentage",
            value=buffer_percentage,
            unit="%",
            analysis="Percentage of total memory used for buffers"
        ))
        
        # Analyze slab usage
        slab_memory_mb = slab_analysis.get("slab_memory_mb", 0)
        slab_reclaimable_mb = slab_analysis.get("slab_reclaimable_mb", 0)
        slab_unreclaimable_mb = slab_analysis.get("slab_unreclaimable_mb", 0)
        reclaimable_percentage = slab_analysis.get("reclaimable_percentage", 0)
        slab_efficiency = slab_analysis.get("slab_efficiency", "unknown")
        
        metrics.append(TechnicalMetric(
            name="Slab Memory",
            value=slab_memory_mb,
            unit="MB",
            analysis="Memory used for kernel slab allocator"
        ))
        
        metrics.append(TechnicalMetric(
            name="Reclaimable Slab",
            value=slab_reclaimable_mb,
            unit="MB",
            analysis="Slab memory that can be reclaimed by kernel"
        ))
        
        metrics.append(TechnicalMetric(
            name="Unreclaimable Slab",
            value=slab_unreclaimable_mb,
            unit="MB",
            threshold=512,
            analysis="Slab memory that cannot be reclaimed"
        ))
        
        metrics.append(TechnicalMetric(
            name="Slab Reclaimable Percentage",
            value=reclaimable_percentage,
            unit="%",
            threshold=50,
            analysis="Percentage of slab memory that is reclaimable"
        ))
        
        # Identify issues
        if utilization_percent > 90:
            issues.append({
                "severity": SeverityLevel.CRITICAL.value,
                "category": "resource",
                "description": "Memory utilization critically high",
                "impact": "System may experience memory exhaustion and OOM kills",
                "evidence": f"Memory utilization at {utilization_percent}%"
            })
            recommendations.append("Immediate memory upgrade required")
            recommendations.append("Identify and terminate memory-intensive processes")
        elif utilization_percent > 80:
            issues.append({
                "severity": SeverityLevel.HIGH.value,
                "category": "resource",
                "description": "Memory utilization high",
                "impact": "System performance degraded, risk of OOM",
                "evidence": f"Memory utilization at {utilization_percent}%"
            })
            recommendations.append("Monitor memory usage trends")
            recommendations.append("Plan memory upgrade")
        
        if available_memory_mb < 512:
            issues.append({
                "severity": SeverityLevel.HIGH.value,
                "category": "resource",
                "description": "Low available memory",
                "impact": "Limited capacity for new processes",
                "evidence": f"Only {available_memory_mb}MB available"
            })
            recommendations.append("Free up memory or add more RAM")
        
        if swap_utilization_percent > 50:
            issues.append({
                "severity": SeverityLevel.HIGH.value,
                "category": "performance",
                "description": "High swap utilization",
                "impact": "System performance degraded due to swapping",
                "evidence": f"Swap utilization at {swap_utilization_percent}%"
            })
            recommendations.append("Investigate memory leaks")
            recommendations.append("Add more physical memory")
        
        if slab_unreclaimable_mb > 512:
            issues.append({
                "severity": SeverityLevel.MEDIUM.value,
                "category": "performance",
                "description": "High unreclaimable slab usage",
                "impact": "Memory fragmentation and waste",
                "evidence": f"Unreclaimable slab at {slab_unreclaimable_mb}MB"
            })
            recommendations.append("Consider kernel tuning")
            recommendations.append("Monitor slab usage patterns")
        
        if reclaimable_percentage < 50:
            issues.append({
                "severity": SeverityLevel.MEDIUM.value,
                "category": "performance",
                "description": "Poor slab reclaim efficiency",
                "impact": "Inefficient memory management",
                "evidence": f"Only {reclaimable_percentage}% reclaimable"
            })
            recommendations.append("Optimize kernel memory management")
        
        # Generate recommendations based on analysis
        if total_memory_mb < 4096:
            recommendations.append("Consider upgrading to at least 4GB RAM for optimal performance")
        
        if cache_efficiency == "poor":
            recommendations.append("Optimize file system caching policies")
        
        if buffer_status == "high":
            recommendations.append("Monitor buffer usage patterns")
        
        if swap_analysis.get("swap_status") == "active" and swap_used_mb > 0:
            recommendations.append("Monitor swap usage - consider memory upgrade")
        
        return SystemComponent(
            name="Memory Subsystem",
            type="hardware",
            status=self._calculate_component_status(issues),
            metrics=metrics,
            configuration=memory_info,
            dependencies=["cpu", "storage"],
            issues=issues,
            recommendations=recommendations
        )
    
    def analyze_temperature_comprehensive(self, temp_data: Dict[str, Any]) -> SystemComponent:
        """Comprehensive temperature analysis with expert-level detail"""
        
        metrics = []
        issues = []
        recommendations = []
        
        # Extract temperature information
        cpu_temps = temp_data.get("cpu_temperatures", {})
        system_temps = temp_data.get("system_temperatures", {})
        thermal_zones = temp_data.get("thermal_zones", {})
        
        # Analyze CPU temperatures
        for zone_name, temp_value in thermal_zones.items():
            if "cpu" in zone_name.lower():
                try:
                    temp_celsius = float(temp_value)
                    metrics.append(TechnicalMetric(
                        name=f"CPU Temperature ({zone_name})",
                        value=temp_celsius,
                        unit="°C",
                        threshold=80,
                        status=self._classify_health_status(temp_celsius, 70, 85),
                        analysis=f"CPU temperature in {zone_name}"
                    ))
                    
                    if temp_celsius > 85:
                        issues.append({
                            "severity": SeverityLevel.CRITICAL.value,
                            "category": "thermal",
                            "description": "CPU temperature critically high",
                            "impact": "Risk of CPU damage and thermal throttling",
                            "evidence": f"CPU temperature at {temp_celsius}°C"
                        })
                        recommendations.append("Check cooling system immediately")
                        recommendations.append("Reduce CPU load or improve cooling")
                    elif temp_celsius > 70:
                        issues.append({
                            "severity": SeverityLevel.HIGH.value,
                            "category": "thermal",
                            "description": "CPU temperature elevated",
                            "impact": "Potential thermal throttling",
                            "evidence": f"CPU temperature at {temp_celsius}°C"
                        })
                        recommendations.append("Monitor temperature trends")
                        recommendations.append("Check airflow and cooling")
                except ValueError:
                    continue
        
        # Analyze system temperatures
        for zone_name, temp_value in thermal_zones.items():
            if "system" in zone_name.lower() or "ambient" in zone_name.lower():
                try:
                    temp_celsius = float(temp_value)
                    metrics.append(TechnicalMetric(
                        name=f"System Temperature ({zone_name})",
                        value=temp_celsius,
                        unit="°C",
                        threshold=50,
                        status=self._classify_health_status(temp_celsius, 40, 55),
                        analysis=f"System temperature in {zone_name}"
                    ))
                    
                    if temp_celsius > 55:
                        issues.append({
                            "severity": SeverityLevel.HIGH.value,
                            "category": "thermal",
                            "description": "System temperature high",
                            "impact": "Environmental cooling inadequate",
                            "evidence": f"System temperature at {temp_celsius}°C"
                        })
                        recommendations.append("Check environmental cooling")
                        recommendations.append("Improve system airflow")
                except ValueError:
                    continue
        
        # Generate general thermal recommendations
        if not metrics:
            recommendations.append("Temperature monitoring not available - consider implementing thermal sensors")
        else:
            recommendations.append("Continue monitoring temperature trends")
            recommendations.append("Maintain adequate cooling and airflow")
        
        return SystemComponent(
            name="Thermal Management",
            type="hardware",
            status=self._calculate_component_status(issues),
            metrics=metrics,
            configuration=thermal_zones,
            dependencies=["cooling", "power"],
            issues=issues,
            recommendations=recommendations
        )
    
    def analyze_power_comprehensive(self, power_data: Dict[str, Any]) -> SystemComponent:
        """Comprehensive power analysis with expert-level detail"""
        
        metrics = []
        issues = []
        recommendations = []
        
        # Extract power information
        power_supplies = power_data.get("power_supplies", {})
        power_consumption = power_data.get("power_consumption", {})
        power_efficiency = power_data.get("power_efficiency", {})
        
        # Analyze power supplies
        for psu_name, psu_data in power_supplies.items():
            if isinstance(psu_data, dict):
                # Extract PSU metrics
                input_voltage = psu_data.get("input_voltage", "0")
                output_voltage = psu_data.get("output_voltage", "0")
                input_current = psu_data.get("input_current", "0")
                output_current = psu_data.get("output_current", "0")
                efficiency = psu_data.get("efficiency", "0")
                temperature = psu_data.get("temperature", "0")
                
                try:
                    input_v = float(input_voltage)
                    output_v = float(output_voltage)
                    input_c = float(input_current)
                    output_c = float(output_current)
                    eff = float(efficiency)
                    temp = float(temperature)
                    
                    # Calculate power values
                    input_power = input_v * input_c
                    output_power = output_v * output_c
                    
                    metrics.append(TechnicalMetric(
                        name=f"{psu_name} Input Power",
                        value=input_power,
                        unit="W",
                        threshold=750,
                        analysis=f"Input power consumption for {psu_name}"
                    ))
                    
                    metrics.append(TechnicalMetric(
                        name=f"{psu_name} Output Power",
                        value=output_power,
                        unit="W",
                        threshold=600,
                        analysis=f"Output power delivered by {psu_name}"
                    ))
                    
                    metrics.append(TechnicalMetric(
                        name=f"{psu_name} Efficiency",
                        value=eff,
                        unit="%",
                        threshold=85,
                        status=self._classify_health_status(eff, 80, 70),
                        analysis=f"Power conversion efficiency for {psu_name}"
                    ))
                    
                    metrics.append(TechnicalMetric(
                        name=f"{psu_name} Temperature",
                        value=temp,
                        unit="°C",
                        threshold=60,
                        status=self._classify_health_status(temp, 50, 65),
                        analysis=f"Operating temperature of {psu_name}"
                    ))
                    
                    # Check for issues
                    if eff < 70:
                        issues.append({
                            "severity": SeverityLevel.HIGH.value,
                            "category": "power",
                            "description": f"Low PSU efficiency on {psu_name}",
                            "impact": "Increased power consumption and heat generation",
                            "evidence": f"Efficiency at {eff}%"
                        })
                        recommendations.append(f"Check {psu_name} for aging or load issues")
                    
                    if temp > 65:
                        issues.append({
                            "severity": SeverityLevel.HIGH.value,
                            "category": "thermal",
                            "description": f"PSU temperature high on {psu_name}",
                            "impact": "Reduced PSU lifespan and reliability",
                            "evidence": f"Temperature at {temp}°C"
                        })
                        recommendations.append(f"Check cooling for {psu_name}")
                    
                    if input_v < 200 or input_v > 240:
                        issues.append({
                            "severity": SeverityLevel.MEDIUM.value,
                            "category": "power",
                            "description": f"Input voltage out of range on {psu_name}",
                            "impact": "Potential power quality issues",
                            "evidence": f"Input voltage at {input_v}V"
                        })
                        recommendations.append("Check input power quality")
                
                except (ValueError, TypeError):
                    continue
        
        # Generate power recommendations
        if not metrics:
            recommendations.append("Power monitoring not available - consider implementing power sensors")
        else:
            recommendations.append("Monitor power consumption trends")
            recommendations.append("Maintain redundant power supplies")
            recommendations.append("Regular PSU maintenance and replacement")
        
        return SystemComponent(
            name="Power Management",
            type="hardware",
            status=self._calculate_component_status(issues),
            metrics=metrics,
            configuration=power_supplies,
            dependencies=["cooling", "thermal"],
            issues=issues,
            recommendations=recommendations
        )
    
    def analyze_cooling_comprehensive(self, cooling_data: Dict[str, Any]) -> SystemComponent:
        """Comprehensive cooling analysis with expert-level detail"""
        
        metrics = []
        issues = []
        recommendations = []
        
        # Extract cooling information
        fan_speeds = cooling_data.get("fan_speeds", {})
        cooling_zones = cooling_data.get("cooling_zones", {})
        airflow_analysis = cooling_data.get("airflow_analysis", {})
        
        # Analyze fan speeds
        for fan_name, fan_data in fan_speeds.items():
            if isinstance(fan_data, dict):
                speed = fan_data.get("speed", "0")
                speed_percent = fan_data.get("speed_percent", "0")
                status = fan_data.get("status", "unknown")
                
                try:
                    rpm = float(speed)
                    percent = float(speed_percent)
                    
                    metrics.append(TechnicalMetric(
                        name=f"Fan Speed ({fan_name})",
                        value=rpm,
                        unit="RPM",
                        threshold=10000,
                        analysis=f"Rotational speed of {fan_name}"
                    ))
                    
                    metrics.append(TechnicalMetric(
                        name=f"Fan Speed Percent ({fan_name})",
                        value=percent,
                        unit="%",
                        threshold=80,
                        status=self._classify_health_status(percent, 70, 90),
                        analysis=f"Speed percentage of {fan_name}"
                    ))
                    
                    # Check for issues
                    if rpm == 0:
                        issues.append({
                            "severity": SeverityLevel.CRITICAL.value,
                            "category": "cooling",
                            "description": f"Fan {fan_name} not operating",
                            "impact": "Risk of overheating",
                            "evidence": f"Fan speed at {rpm} RPM"
                        })
                        recommendations.append(f"Replace or repair {fan_name} immediately")
                    elif percent > 90:
                        issues.append({
                            "severity": SeverityLevel.HIGH.value,
                            "category": "cooling",
                            "description": f"Fan {fan_name} running at high speed",
                            "impact": "High cooling demand or fan issues",
                            "evidence": f"Fan speed at {percent}%"
                        })
                        recommendations.append(f"Check {fan_name} and cooling demand")
                    elif percent < 20:
                        issues.append({
                            "severity": SeverityLevel.MEDIUM.value,
                            "category": "cooling",
                            "description": f"Fan {fan_name} running at low speed",
                            "impact": "Potential cooling issues",
                            "evidence": f"Fan speed at {percent}%"
                        })
                        recommendations.append(f"Check {fan_name} operation")
                
                except (ValueError, TypeError):
                    continue
        
        # Generate cooling recommendations
        if not metrics:
            recommendations.append("Cooling monitoring not available - consider implementing fan sensors")
        else:
            recommendations.append("Monitor fan speed trends")
            recommendations.append("Maintain proper airflow and ventilation")
            recommendations.append("Regular fan cleaning and maintenance")
        
        return SystemComponent(
            name="Cooling System",
            type="hardware",
            status=self._calculate_component_status(issues),
            metrics=metrics,
            configuration=cooling_zones,
            dependencies=["thermal", "power"],
            issues=issues,
            recommendations=recommendations
        )
    
    def analyze_pci_comprehensive(self, pci_data: Dict[str, Any]) -> SystemComponent:
        """Comprehensive PCI analysis with expert-level detail"""
        
        metrics = []
        issues = []
        recommendations = []
        
        # Extract PCI information
        pci_devices = pci_data.get("pci_devices", [])
        
        # Analyze PCI devices
        network_devices = 0
        storage_devices = 0
        bridge_devices = 0
        unknown_devices = 0
        
        for device in pci_devices:
            if isinstance(device, dict):
                address = device.get("address", "")
                description = device.get("description", "")
                device_type = device.get("type", "unknown")
                
                metrics.append(TechnicalMetric(
                    name=f"PCI Device ({address})",
                    value=description,
                    unit="device",
                    analysis=f"PCI device at {address}"
                ))
                
                # Count device types
                if device_type == "network":
                    network_devices += 1
                elif device_type == "storage":
                    storage_devices += 1
                elif device_type == "bridge":
                    bridge_devices += 1
                else:
                    unknown_devices += 1
                
                # Check for issues
                if device_type == "unknown":
                    issues.append({
                        "severity": SeverityLevel.INFO.value,
                        "category": "hardware",
                        "description": f"Unknown PCI device at {address}",
                        "impact": "Device may not be properly recognized",
                        "evidence": f"Device: {description}"
                    })
                    recommendations.append(f"Investigate unknown PCI device {address}")
        
        # Add summary metrics
        metrics.append(TechnicalMetric(
            name="Network Devices",
            value=network_devices,
            unit="devices",
            analysis="Number of network interface PCI devices"
        ))
        
        metrics.append(TechnicalMetric(
            name="Storage Devices",
            value=storage_devices,
            unit="devices",
            analysis="Number of storage controller PCI devices"
        ))
        
        metrics.append(TechnicalMetric(
            name="Bridge Devices",
            value=bridge_devices,
            unit="devices",
            analysis="Number of PCI bridge devices"
        ))
        
        metrics.append(TechnicalMetric(
            name="Unknown Devices",
            value=unknown_devices,
            unit="devices",
            analysis="Number of unrecognized PCI devices"
        ))
        
        # Generate PCI recommendations
        if unknown_devices > 0:
            recommendations.append("Investigate unknown PCI devices for proper driver support")
        
        if network_devices == 0:
            recommendations.append("No network interfaces detected - check PCI configuration")
        
        recommendations.append("Monitor PCI device health and performance")
        recommendations.append("Keep PCI device drivers updated")
        
        return SystemComponent(
            name="PCI Subsystem",
            type="hardware",
            status=self._calculate_component_status(issues),
            metrics=metrics,
            configuration={"pci_devices": pci_devices},
            dependencies=["power", "cooling"],
            issues=issues,
            recommendations=recommendations
        )
    
    # Helper methods
    def _classify_health_status(self, value: float, warning_threshold: float, critical_threshold: float) -> HealthStatus:
        """Classify health status based on thresholds"""
        if value >= critical_threshold:
            return HealthStatus.CRITICAL
        elif value >= warning_threshold:
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY
    
    def _calculate_component_status(self, issues: List[Dict[str, Any]]) -> HealthStatus:
        """Calculate overall component status based on issues"""
        if not issues:
            return HealthStatus.HEALTHY
        
        critical_issues = [issue for issue in issues if issue.get("severity") == SeverityLevel.CRITICAL.value]
        high_issues = [issue for issue in issues if issue.get("severity") == SeverityLevel.HIGH.value]
        
        if critical_issues:
            return HealthStatus.CRITICAL
        elif high_issues:
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY
    
    def _create_cpu_analysis_template(self) -> Dict[str, Any]:
        """Create CPU analysis template"""
        return {
            "name": "CPU Analysis",
            "description": "Comprehensive CPU subsystem analysis",
            "metrics": [
                "core_count", "thread_count", "frequency", "utilization",
                "load_average", "context_switches", "cache_performance"
            ],
            "thresholds": {
                "utilization_warning": 80,
                "utilization_critical": 90,
                "load_warning": 2.0,
                "load_critical": 4.0
            }
        }
    
    def _create_memory_analysis_template(self) -> Dict[str, Any]:
        """Create memory analysis template"""
        return {
            "name": "Memory Analysis",
            "description": "Comprehensive memory subsystem analysis",
            "metrics": [
                "total_memory", "used_memory", "available_memory",
                "cache_efficiency", "swap_usage", "slab_usage"
            ],
            "thresholds": {
                "utilization_warning": 80,
                "utilization_critical": 90,
                "swap_warning": 50,
                "swap_critical": 80
            }
        }
    
    def _create_temperature_analysis_template(self) -> Dict[str, Any]:
        """Create temperature analysis template"""
        return {
            "name": "Temperature Analysis",
            "description": "Comprehensive thermal analysis",
            "metrics": [
                "cpu_temperature", "system_temperature", "ambient_temperature"
            ],
            "thresholds": {
                "cpu_warning": 70,
                "cpu_critical": 85,
                "system_warning": 40,
                "system_critical": 55
            }
        }
    
    def _create_power_analysis_template(self) -> Dict[str, Any]:
        """Create power analysis template"""
        return {
            "name": "Power Analysis",
            "description": "Comprehensive power system analysis",
            "metrics": [
                "power_consumption", "efficiency", "voltage_levels", "current_draw"
            ],
            "thresholds": {
                "efficiency_warning": 80,
                "efficiency_critical": 70,
                "temperature_warning": 50,
                "temperature_critical": 65
            }
        }
    
    def _create_cooling_analysis_template(self) -> Dict[str, Any]:
        """Create cooling analysis template"""
        return {
            "name": "Cooling Analysis",
            "description": "Comprehensive cooling system analysis",
            "metrics": [
                "fan_speeds", "airflow", "cooling_capacity", "temperature_differentials"
            ],
            "thresholds": {
                "fan_speed_warning": 70,
                "fan_speed_critical": 90,
                "airflow_warning": 50,
                "airflow_critical": 80
            }
        }
    
    def _create_pci_analysis_template(self) -> Dict[str, Any]:
        """Create PCI analysis template"""
        return {
            "name": "PCI Analysis",
            "description": "Comprehensive PCI subsystem analysis",
            "metrics": [
                "device_count", "device_types", "bandwidth_utilization", "error_rates"
            ],
            "thresholds": {
                "error_rate_warning": 0.01,
                "error_rate_critical": 0.05,
                "bandwidth_warning": 80,
                "bandwidth_critical": 95
            }
        }

# ============================================================================
# NETWORK ANALYSIS FRAMEWORK
# ============================================================================

class NetworkAnalysisFramework:
    """Comprehensive network analysis framework"""
    
    def __init__(self):
        self.interface_analysis_template = self._create_interface_analysis_template()
        self.bgp_analysis_template = self._create_bgp_analysis_template()
        self.arp_analysis_template = self._create_arp_analysis_template()
    
    def analyze_interfaces_comprehensive(self, interface_data: Dict[str, Any]) -> SystemComponent:
        """Comprehensive interface analysis with expert-level detail"""
        
        metrics = []
        issues = []
        recommendations = []
        
        # Extract interface information
        interface_counters = interface_data.get("interface_counters", {})
        physical_layer = interface_data.get("physical_layer", {})
        error_counters = interface_data.get("error_counters", {})
        queue_counters = interface_data.get("queue_counters", {})
        
        # Analyze interface summary
        summary = interface_counters.get("summary", {})
        total_interfaces = summary.get("total_interfaces", 0)
        active_interfaces = summary.get("active_interfaces", 0)
        inactive_interfaces = summary.get("inactive_interfaces", 0)
        total_rx_packets = summary.get("total_rx_packets", 0)
        total_tx_packets = summary.get("total_tx_packets", 0)
        total_rx_bytes = summary.get("total_rx_bytes", 0)
        total_tx_bytes = summary.get("total_tx_bytes", 0)
        total_rx_errors = summary.get("total_rx_errors", 0)
        total_tx_errors = summary.get("total_tx_errors", 0)
        total_rx_drops = summary.get("total_rx_drops", 0)
        total_tx_drops = summary.get("total_tx_drops", 0)
        high_utilization_interfaces = summary.get("high_utilization_interfaces", [])
        error_prone_interfaces = summary.get("error_prone_interfaces", [])
        
        # Create summary metrics
        metrics.append(TechnicalMetric(
            name="Total Interfaces",
            value=total_interfaces,
            unit="interfaces",
            analysis="Total number of network interfaces"
        ))
        
        metrics.append(TechnicalMetric(
            name="Active Interfaces",
            value=active_interfaces,
            unit="interfaces",
            threshold=1,
            analysis="Number of interfaces with traffic"
        ))
        
        metrics.append(TechnicalMetric(
            name="Inactive Interfaces",
            value=inactive_interfaces,
            unit="interfaces",
            threshold=total_interfaces * 0.1,
            analysis="Number of interfaces without traffic"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total RX Packets",
            value=total_rx_packets,
            unit="packets",
            analysis="Total received packets across all interfaces"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total TX Packets",
            value=total_tx_packets,
            unit="packets",
            analysis="Total transmitted packets across all interfaces"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total RX Bytes",
            value=total_rx_bytes,
            unit="bytes",
            analysis="Total received bytes across all interfaces"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total TX Bytes",
            value=total_tx_bytes,
            unit="bytes",
            analysis="Total transmitted bytes across all interfaces"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total RX Errors",
            value=total_rx_errors,
            unit="errors",
            threshold=100,
            analysis="Total receive errors across all interfaces"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total TX Errors",
            value=total_tx_errors,
            unit="errors",
            threshold=100,
            analysis="Total transmit errors across all interfaces"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total RX Drops",
            value=total_rx_drops,
            unit="drops",
            threshold=1000,
            analysis="Total receive drops across all interfaces"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total TX Drops",
            value=total_tx_drops,
            unit="drops",
            threshold=1000,
            analysis="Total transmit drops across all interfaces"
        ))
        
        # Analyze individual interfaces
        interfaces = interface_counters.get("interfaces", {})
        for interface_name, interface_stats in interfaces.items():
            if isinstance(interface_stats, dict):
                rx_packets = interface_stats.get("rx_packets", 0)
                tx_packets = interface_stats.get("tx_packets", 0)
                rx_bytes = interface_stats.get("rx_bytes", 0)
                tx_bytes = interface_stats.get("tx_bytes", 0)
                rx_errors = interface_stats.get("rx_errors", 0)
                tx_errors = interface_stats.get("tx_errors", 0)
                rx_drops = interface_stats.get("rx_drops", 0)
                tx_drops = interface_stats.get("tx_drops", 0)
                utilization = interface_stats.get("utilization_total", 0)
                error_rate = interface_stats.get("error_rate", 0)
                drop_rate = interface_stats.get("drop_rate", 0)
                
                # Calculate interface-specific metrics
                total_packets = rx_packets + tx_packets
                if total_packets > 0:
                    interface_error_rate = ((rx_errors + tx_errors) / total_packets) * 100
                    interface_drop_rate = ((rx_drops + tx_drops) / total_packets) * 100
                    
                    # Check for problematic interfaces
                    if interface_error_rate > 1.0:
                        issues.append({
                            "severity": SeverityLevel.HIGH.value,
                            "category": "network",
                            "description": f"High error rate on {interface_name}",
                            "impact": "Packet loss and performance degradation",
                            "evidence": f"Error rate {interface_error_rate:.2f}%"
                        })
                        recommendations.append(f"Investigate {interface_name} for physical issues")
                    
                    if interface_drop_rate > 1.0:
                        issues.append({
                            "severity": SeverityLevel.HIGH.value,
                            "category": "network",
                            "description": f"High drop rate on {interface_name}",
                            "impact": "Packet loss and performance degradation",
                            "evidence": f"Drop rate {interface_drop_rate:.2f}%"
                        })
                        recommendations.append(f"Check {interface_name} for congestion or buffer issues")
                    
                    if utilization > 80:
                        issues.append({
                            "severity": SeverityLevel.MEDIUM.value,
                            "category": "performance",
                            "description": f"High utilization on {interface_name}",
                            "impact": "Potential performance bottleneck",
                            "evidence": f"Utilization {utilization:.1f}%"
                        })
                        recommendations.append(f"Monitor {interface_name} for capacity planning")
        
        # Analyze physical layer
        physical_summary = physical_layer.get("summary", {})
        link_up = physical_summary.get("link_up", 0)
        link_down = physical_summary.get("link_down", 0)
        signal_detect_ok = physical_summary.get("signal_detect_ok", 0)
        signal_detect_nok = physical_summary.get("signal_detect_nok", 0)
        cdr_lock_ok = physical_summary.get("cdr_lock_ok", 0)
        cdr_lock_nok = physical_summary.get("cdr_lock_nok", 0)
        problematic_interfaces = physical_summary.get("problematic_interfaces", [])
        
        metrics.append(TechnicalMetric(
            name="Link Up Interfaces",
            value=link_up,
            unit="interfaces",
            analysis="Number of interfaces with physical link"
        ))
        
        metrics.append(TechnicalMetric(
            name="Link Down Interfaces",
            value=link_down,
            unit="interfaces",
            threshold=1,
            analysis="Number of interfaces without physical link"
        ))
        
        metrics.append(TechnicalMetric(
            name="Signal Detect OK",
            value=signal_detect_ok,
            unit="interfaces",
            analysis="Number of interfaces with signal detection"
        ))
        
        metrics.append(TechnicalMetric(
            name="Signal Detect NOK",
            value=signal_detect_nok,
            unit="interfaces",
            threshold=1,
            analysis="Number of interfaces without signal detection"
        ))
        
        metrics.append(TechnicalMetric(
            name="CDR Lock OK",
            value=cdr_lock_ok,
            unit="interfaces",
            analysis="Number of interfaces with CDR lock"
        ))
        
        metrics.append(TechnicalMetric(
            name="CDR Lock NOK",
            value=cdr_lock_nok,
            unit="interfaces",
            threshold=1,
            analysis="Number of interfaces without CDR lock"
        ))
        
        # Check for physical layer issues
        if link_down > 0:
            issues.append({
                "severity": SeverityLevel.HIGH.value,
                "category": "physical",
                "description": f"{link_down} interfaces without link",
                "impact": "Network connectivity issues",
                "evidence": f"Link down on {link_down} interfaces"
            })
            recommendations.append("Check physical connections and transceivers")
        
        if signal_detect_nok > 0:
            issues.append({
                "severity": SeverityLevel.HIGH.value,
                "category": "physical",
                "description": f"{signal_detect_nok} interfaces without signal detection",
                "impact": "Physical layer issues",
                "evidence": f"No signal on {signal_detect_nok} interfaces"
            })
            recommendations.append("Check transceiver modules and cables")
        
        if cdr_lock_nok > 0:
            issues.append({
                "severity": SeverityLevel.MEDIUM.value,
                "category": "physical",
                "description": f"{cdr_lock_nok} interfaces without CDR lock",
                "impact": "Clock recovery issues",
                "evidence": f"No CDR lock on {cdr_lock_nok} interfaces"
            })
            recommendations.append("Check clock synchronization and transceiver compatibility")
        
        # Analyze error counters
        error_summary = error_counters.get("summary", {})
        interfaces_with_errors = error_summary.get("interfaces_with_errors", 0)
        interfaces_with_drops = error_summary.get("interfaces_with_drops", 0)
        critical_error_interfaces = error_summary.get("critical_error_interfaces", [])
        
        metrics.append(TechnicalMetric(
            name="Interfaces with Errors",
            value=interfaces_with_errors,
            unit="interfaces",
            threshold=1,
            analysis="Number of interfaces experiencing errors"
        ))
        
        metrics.append(TechnicalMetric(
            name="Interfaces with Drops",
            value=interfaces_with_drops,
            unit="interfaces",
            threshold=1,
            analysis="Number of interfaces experiencing drops"
        ))
        
        # Generate recommendations
        if critical_error_interfaces:
            recommendations.append("Critical error interfaces require immediate attention")
        
        if high_utilization_interfaces:
            recommendations.append("Monitor high utilization interfaces for capacity planning")
        
        if error_prone_interfaces:
            recommendations.append("Investigate error-prone interfaces for physical issues")
        
        recommendations.append("Regular interface health monitoring")
        recommendations.append("Maintain interface documentation and labeling")
        
        return SystemComponent(
            name="Network Interfaces",
            type="network",
            status=self._calculate_component_status(issues),
            metrics=metrics,
            configuration=interface_counters,
            dependencies=["physical_layer", "transceivers"],
            issues=issues,
            recommendations=recommendations
        )
    
    def analyze_bgp_comprehensive(self, bgp_data: Dict[str, Any]) -> SystemComponent:
        """Comprehensive BGP analysis with expert-level detail"""
        
        metrics = []
        issues = []
        recommendations = []
        
        # Extract BGP information
        neighbor_status = bgp_data.get("neighbor_status", {})
        route_information = bgp_data.get("route_information", {})
        message_statistics = bgp_data.get("message_statistics", {})
        
        # Analyze BGP summary
        summary = neighbor_status.get("summary", {})
        total_neighbors = summary.get("total_neighbors", 0)
        established_neighbors = summary.get("established_neighbors", 0)
        active_neighbors = summary.get("active_neighbors", 0)
        idle_neighbors = summary.get("idle_neighbors", 0)
        total_routes_received = summary.get("total_routes_received", 0)
        total_routes_advertised = summary.get("total_routes_advertised", 0)
        total_messages_sent = summary.get("total_messages_sent", 0)
        total_messages_received = summary.get("total_messages_received", 0)
        problematic_neighbors = summary.get("problematic_neighbors", [])
        
        # Create BGP metrics
        metrics.append(TechnicalMetric(
            name="Total BGP Neighbors",
            value=total_neighbors,
            unit="neighbors",
            threshold=1,
            analysis="Total number of BGP neighbor relationships"
        ))
        
        metrics.append(TechnicalMetric(
            name="Established Neighbors",
            value=established_neighbors,
            unit="neighbors",
            threshold=1,
            status=self._classify_health_status((established_neighbors / max(1, total_neighbors)) * 100, 80, 50),
            analysis="Number of BGP neighbors in established state"
        ))
        
        metrics.append(TechnicalMetric(
            name="Active Neighbors",
            value=active_neighbors,
            unit="neighbors",
            threshold=0,
            analysis="Number of BGP neighbors in active state"
        ))
        
        metrics.append(TechnicalMetric(
            name="Idle Neighbors",
            value=idle_neighbors,
            unit="neighbors",
            threshold=0,
            analysis="Number of BGP neighbors in idle state"
        ))
        
        metrics.append(TechnicalMetric(
            name="Routes Received",
            value=total_routes_received,
            unit="routes",
            threshold=100,
            analysis="Total BGP routes received from neighbors"
        ))
        
        metrics.append(TechnicalMetric(
            name="Routes Advertised",
            value=total_routes_advertised,
            unit="routes",
            threshold=100,
            analysis="Total BGP routes advertised to neighbors"
        ))
        
        metrics.append(TechnicalMetric(
            name="Messages Sent",
            value=total_messages_sent,
            unit="messages",
            analysis="Total BGP messages sent to neighbors"
        ))
        
        metrics.append(TechnicalMetric(
            name="Messages Received",
            value=total_messages_received,
            unit="messages",
            analysis="Total BGP messages received from neighbors"
        ))
        
        # Analyze individual neighbors
        neighbors = neighbor_status.get("neighbors", {})
        for neighbor_ip, neighbor_data in neighbors.items():
            if isinstance(neighbor_data, dict):
                state = neighbor_data.get("state", "unknown")
                uptime = neighbor_data.get("uptime", "")
                prefixes_received = neighbor_data.get("prefixes_received", 0)
                prefixes_advertised = neighbor_data.get("prefixes_advertised", 0)
                messages_sent = neighbor_data.get("messages_sent", 0)
                messages_received = neighbor_data.get("messages_received", 0)
                health_score = neighbor_data.get("health_score", 100)
                
                # Check for neighbor issues
                if state.lower() != "established":
                    severity = SeverityLevel.HIGH.value if state.lower() == "idle" else SeverityLevel.MEDIUM.value
                    issues.append({
                        "severity": severity,
                        "category": "routing",
                        "description": f"BGP neighbor {neighbor_ip} not established",
                        "impact": "Routing table incomplete",
                        "evidence": f"Neighbor state: {state}"
                    })
                    recommendations.append(f"Investigate BGP neighbor {neighbor_ip}")
                
                if health_score < 70:
                    issues.append({
                        "severity": SeverityLevel.MEDIUM.value,
                        "category": "routing",
                        "description": f"BGP neighbor {neighbor_ip} health degraded",
                        "impact": "Potential routing instability",
                        "evidence": f"Health score: {health_score}"
                    })
                    recommendations.append(f"Monitor BGP neighbor {neighbor_ip}")
                
                if prefixes_received == 0 and state.lower() == "established":
                    issues.append({
                        "severity": SeverityLevel.MEDIUM.value,
                        "category": "routing",
                        "description": f"No routes received from {neighbor_ip}",
                        "impact": "Incomplete routing information",
                        "evidence": f"Routes received: {prefixes_received}"
                    })
                    recommendations.append(f"Check route advertisement from {neighbor_ip}")
        
        # Check for BGP session issues
        if established_neighbors == 0:
            issues.append({
                "severity": SeverityLevel.CRITICAL.value,
                "category": "routing",
                "description": "No BGP neighbors established",
                "impact": "Complete routing failure",
                "evidence": f"Established neighbors: {established_neighbors}"
            })
            recommendations.append("Investigate BGP configuration and connectivity")
        elif established_neighbors < total_neighbors:
            issues.append({
                "severity": SeverityLevel.HIGH.value,
                "category": "routing",
                "description": "Not all BGP neighbors established",
                "impact": "Partial routing table",
                "evidence": f"Established: {established_neighbors}/{total_neighbors}"
            })
            recommendations.append("Investigate non-established BGP neighbors")
        
        if active_neighbors > 0:
            issues.append({
                "severity": SeverityLevel.MEDIUM.value,
                "category": "routing",
                "description": f"{active_neighbors} BGP neighbors in active state",
                "impact": "BGP session negotiation issues",
                "evidence": f"Active neighbors: {active_neighbors}"
            })
            recommendations.append("Monitor active BGP neighbors")
        
        if idle_neighbors > 0:
            issues.append({
                "severity": SeverityLevel.MEDIUM.value,
                "category": "routing",
                "description": f"{idle_neighbors} BGP neighbors in idle state",
                "impact": "BGP connectivity issues",
                "evidence": f"Idle neighbors: {idle_neighbors}"
            })
            recommendations.append("Investigate idle BGP neighbors")
        
        # Generate BGP recommendations
        recommendations.append("Monitor BGP session stability")
        recommendations.append("Implement BGP route damping if needed")
        recommendations.append("Configure BGP graceful restart")
        recommendations.append("Regular BGP health monitoring")
        
        return SystemComponent(
            name="BGP Routing",
            type="network",
            status=self._calculate_component_status(issues),
            metrics=metrics,
            configuration=neighbor_status,
            dependencies=["interfaces", "ip_connectivity"],
            issues=issues,
            recommendations=recommendations
        )
    
    def analyze_arp_comprehensive(self, arp_data: Dict[str, Any]) -> SystemComponent:
        """Comprehensive ARP analysis with expert-level detail"""
        
        metrics = []
        issues = []
        recommendations = []
        
        # Extract ARP information
        arp_table = arp_data.get("arp_table", {})
        
        # Analyze ARP entries
        for table_name, table_data in arp_table.items():
            if isinstance(table_data, dict):
                entries = table_data.get("entries", [])
                summary = table_data.get("summary", {})
                
                total_entries = summary.get("total_entries", 0)
                unique_macs = summary.get("unique_macs", 0)
                unique_ips = summary.get("unique_ips", 0)
                interfaces = summary.get("interfaces", 0)
                incomplete_entries = summary.get("incomplete_entries", 0)
                permanent_entries = summary.get("permanent_entries", 0)
                dynamic_entries = summary.get("dynamic_entries", 0)
                mac_vendors = summary.get("mac_vendors", {})
                ip_ranges = summary.get("ip_ranges", {})
                
                # Create ARP metrics
                metrics.append(TechnicalMetric(
                    name=f"ARP Entries ({table_name})",
                    value=total_entries,
                    unit="entries",
                    analysis=f"Total ARP entries in {table_name}"
                ))
                
                metrics.append(TechnicalMetric(
                    name=f"Unique MACs ({table_name})",
                    value=unique_macs,
                    unit="addresses",
                    analysis=f"Unique MAC addresses in {table_name}"
                ))
                
                metrics.append(TechnicalMetric(
                    name=f"Unique IPs ({table_name})",
                    value=unique_ips,
                    unit="addresses",
                    analysis=f"Unique IP addresses in {table_name}"
                ))
                
                metrics.append(TechnicalMetric(
                    name=f"Interfaces ({table_name})",
                    value=interfaces,
                    unit="interfaces",
                    analysis=f"Interfaces with ARP entries in {table_name}"
                ))
                
                metrics.append(TechnicalMetric(
                    name=f"Incomplete Entries ({table_name})",
                    value=incomplete_entries,
                    unit="entries",
                    threshold=5,
                    analysis=f"Incomplete ARP entries in {table_name}"
                ))
                
                metrics.append(TechnicalMetric(
                    name=f"Permanent Entries ({table_name})",
                    value=permanent_entries,
                    unit="entries",
                    analysis=f"Permanent ARP entries in {table_name}"
                ))
                
                metrics.append(TechnicalMetric(
                    name=f"Dynamic Entries ({table_name})",
                    value=dynamic_entries,
                    unit="entries",
                    analysis=f"Dynamic ARP entries in {table_name}"
                ))
                
                # Analyze MAC vendors
                for vendor, count in mac_vendors.items():
                    metrics.append(TechnicalMetric(
                        name=f"MAC Vendor {vendor} ({table_name})",
                        value=count,
                        unit="devices",
                        analysis=f"{vendor} devices in {table_name}"
                    ))
                
                # Analyze IP ranges
                for ip_class, count in ip_ranges.items():
                    metrics.append(TechnicalMetric(
                        name=f"IP Class {ip_class} ({table_name})",
                        value=count,
                        unit="addresses",
                        analysis=f"{ip_class} addresses in {table_name}"
                    ))
                
                # Check for ARP issues
                if incomplete_entries > 5:
                    issues.append({
                        "severity": SeverityLevel.MEDIUM.value,
                        "category": "network",
                        "description": f"High number of incomplete ARP entries in {table_name}",
                        "impact": "Potential connectivity issues",
                        "evidence": f"Incomplete entries: {incomplete_entries}"
                    })
                    recommendations.append(f"Investigate incomplete ARP entries in {table_name}")
                
                if total_entries == 0:
                    issues.append({
                        "severity": SeverityLevel.INFO.value,
                        "category": "network",
                        "description": f"No ARP entries in {table_name}",
                        "impact": "No Layer 2 connectivity information",
                        "evidence": f"Total entries: {total_entries}"
                    })
                    recommendations.append(f"Check ARP table population in {table_name}")
        
        # Generate ARP recommendations
        recommendations.append("Monitor ARP table size and growth")
        recommendations.append("Implement ARP cache timeout optimization")
        recommendations.append("Regular ARP table validation")
        recommendations.append("Monitor for ARP spoofing attempts")
        
        return SystemComponent(
            name="ARP Table",
            type="network",
            status=self._calculate_component_status(issues),
            metrics=metrics,
            configuration=arp_table,
            dependencies=["interfaces", "ip_connectivity"],
            issues=issues,
            recommendations=recommendations
        )
    
    # Helper methods
    def _classify_health_status(self, value: float, warning_threshold: float, critical_threshold: float) -> HealthStatus:
        """Classify health status based on thresholds"""
        if value >= critical_threshold:
            return HealthStatus.CRITICAL
        elif value >= warning_threshold:
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY
    
    def _calculate_component_status(self, issues: List[Dict[str, Any]]) -> HealthStatus:
        """Calculate overall component status based on issues"""
        if not issues:
            return HealthStatus.HEALTHY
        
        critical_issues = [issue for issue in issues if issue.get("severity") == SeverityLevel.CRITICAL.value]
        high_issues = [issue for issue in issues if issue.get("severity") == SeverityLevel.HIGH.value]
        
        if critical_issues:
            return HealthStatus.CRITICAL
        elif high_issues:
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY
    
    def _create_interface_analysis_template(self) -> Dict[str, Any]:
        """Create interface analysis template"""
        return {
            "name": "Interface Analysis",
            "description": "Comprehensive network interface analysis",
            "metrics": [
                "packet_counts", "byte_counts", "error_rates", "drop_rates",
                "utilization", "physical_status", "queue_depths"
            ],
            "thresholds": {
                "error_rate_warning": 0.1,
                "error_rate_critical": 1.0,
                "drop_rate_warning": 0.1,
                "drop_rate_critical": 1.0,
                "utilization_warning": 70,
                "utilization_critical": 90
            }
        }
    
    def _create_bgp_analysis_template(self) -> Dict[str, Any]:
        """Create BGP analysis template"""
        return {
            "name": "BGP Analysis",
            "description": "Comprehensive BGP routing analysis",
            "metrics": [
                "neighbor_states", "route_counts", "message_statistics",
                "session_stability", "convergence_time"
            ],
            "thresholds": {
                "established_neighbors_warning": 80,
                "established_neighbors_critical": 50,
                "route_count_warning": 1000,
                "route_count_critical": 10000
            }
        }
    
    def _create_arp_analysis_template(self) -> Dict[str, Any]:
        """Create ARP analysis template"""
        return {
            "name": "ARP Analysis",
            "description": "Comprehensive ARP table analysis",
            "metrics": [
                "entry_counts", "mac_vendors", "ip_ranges", "incomplete_entries",
                "permanent_entries", "dynamic_entries"
            ],
            "thresholds": {
                "incomplete_entries_warning": 5,
                "incomplete_entries_critical": 20,
                "table_size_warning": 1000,
                "table_size_critical": 5000
            }
        }

# ============================================================================
# SERVICE ANALYSIS FRAMEWORK
# ============================================================================

class ServiceAnalysisFramework:
    """Comprehensive service analysis framework"""
    
    def __init__(self):
        self.container_analysis_template = self._create_container_analysis_template()
        self.process_analysis_template = self._create_process_analysis_template()
        self.dependency_analysis_template = self._create_dependency_analysis_template()
    
    def analyze_containers_comprehensive(self, container_data: Dict[str, Any]) -> SystemComponent:
        """Comprehensive container analysis with expert-level detail"""
        
        metrics = []
        issues = []
        recommendations = []
        
        # Extract container information
        containers = container_data.get("containers", {})
        summary = container_data.get("summary", {})
        
        # Analyze container summary
        total_containers = summary.get("total_containers", 0)
        running_containers = summary.get("running_containers", 0)
        stopped_containers = summary.get("stopped_containers", 0)
        healthy_containers = summary.get("healthy_containers", 0)
        unhealthy_containers = summary.get("unhealthy_containers", 0)
        total_memory_usage = summary.get("total_memory_usage", 0)
        total_cpu_usage = summary.get("total_cpu_usage", 0)
        container_types = summary.get("container_types", {})
        
        # Create container metrics
        metrics.append(TechnicalMetric(
            name="Total Containers",
            value=total_containers,
            unit="containers",
            threshold=1,
            analysis="Total number of containers"
        ))
        
        metrics.append(TechnicalMetric(
            name="Running Containers",
            value=running_containers,
            unit="containers",
            threshold=1,
            status=self._classify_health_status((running_containers / max(1, total_containers)) * 100, 80, 50),
            analysis="Number of running containers"
        ))
        
        metrics.append(TechnicalMetric(
            name="Stopped Containers",
            value=stopped_containers,
            unit="containers",
            threshold=0,
            analysis="Number of stopped containers"
        ))
        
        metrics.append(TechnicalMetric(
            name="Healthy Containers",
            value=healthy_containers,
            unit="containers",
            threshold=1,
            analysis="Number of healthy containers"
        ))
        
        metrics.append(TechnicalMetric(
            name="Unhealthy Containers",
            value=unhealthy_containers,
            unit="containers",
            threshold=0,
            analysis="Number of unhealthy containers"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total Memory Usage",
            value=total_memory_usage,
            unit="MB",
            threshold=4096,
            analysis="Total memory usage by all containers"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total CPU Usage",
            value=total_cpu_usage,
            unit="%",
            threshold=80,
            analysis="Total CPU usage by all containers"
        ))
        
        # Analyze container types
        for container_type, count in container_types.items():
            metrics.append(TechnicalMetric(
                name=f"Container Type {container_type}",
                value=count,
                unit="containers",
                analysis=f"Number of {container_type} containers"
            ))
        
        # Analyze individual containers
        for container_id, container_info in containers.items():
            if isinstance(container_info, dict):
                status = container_info.get("status", "unknown")
                health_status = container_info.get("health_status", "unknown")
                memory_usage = container_info.get("memory_usage", 0)
                cpu_usage = container_info.get("cpu_usage", 0)
                container_type = container_info.get("container_type", "unknown")
                
                # Check for container issues
                if health_status.lower() != "healthy":
                    severity = SeverityLevel.HIGH.value if "unhealthy" in health_status.lower() else SeverityLevel.MEDIUM.value
                    issues.append({
                        "severity": severity,
                        "category": "service",
                        "description": f"Container {container_id} unhealthy",
                        "impact": "Service degradation or failure",
                        "evidence": f"Health status: {health_status}"
                    })
                    recommendations.append(f"Investigate container {container_id}")
                
                if status.lower() != "up" and status.lower() != "running":
                    issues.append({
                        "severity": SeverityLevel.HIGH.value,
                        "category": "service",
                        "description": f"Container {container_id} not running",
                        "impact": "Service unavailable",
                        "evidence": f"Status: {status}"
                    })
                    recommendations.append(f"Restart container {container_id}")
                
                if memory_usage > 1024:  # More than 1GB
                    issues.append({
                        "severity": SeverityLevel.MEDIUM.value,
                        "category": "resource",
                        "description": f"High memory usage in {container_id}",
                        "impact": "Memory pressure on system",
                        "evidence": f"Memory usage: {memory_usage}MB"
                    })
                    recommendations.append(f"Monitor {container_id} memory usage")
                
                if cpu_usage > 80:
                    issues.append({
                        "severity": SeverityLevel.MEDIUM.value,
                        "category": "performance",
                        "description": f"High CPU usage in {container_id}",
                        "impact": "Performance degradation",
                        "evidence": f"CPU usage: {cpu_usage}%"
                    })
                    recommendations.append(f"Monitor {container_id} CPU usage")
        
        # Check for service issues
        if running_containers == 0:
            issues.append({
                "severity": SeverityLevel.CRITICAL.value,
                "category": "service",
                "description": "No containers running",
                "impact": "Complete service failure",
                "evidence": f"Running containers: {running_containers}"
            })
            recommendations.append("Investigate container runtime")
        elif running_containers < total_containers:
            issues.append({
                "severity": SeverityLevel.HIGH.value,
                "category": "service",
                "description": "Not all containers running",
                "impact": "Partial service availability",
                "evidence": f"Running: {running_containers}/{total_containers}"
            })
            recommendations.append("Investigate stopped containers")
        
        if unhealthy_containers > 0:
            issues.append({
                "severity": SeverityLevel.HIGH.value,
                "category": "service",
                "description": f"{unhealthy_containers} containers unhealthy",
                "impact": "Service degradation",
                "evidence": f"Unhealthy containers: {unhealthy_containers}"
            })
            recommendations.append("Investigate unhealthy containers")
        
        # Generate service recommendations
        recommendations.append("Monitor container health and resource usage")
        recommendations.append("Implement container restart policies")
        recommendations.append("Regular container image updates")
        recommendations.append("Container resource limit optimization")
        
        return SystemComponent(
            name="Container Services",
            type="service",
            status=self._calculate_component_status(issues),
            metrics=metrics,
            configuration=containers,
            dependencies=["docker_runtime", "system_resources"],
            issues=issues,
            recommendations=recommendations
        )
    
    def analyze_processes_comprehensive(self, process_data: Dict[str, Any]) -> SystemComponent:
        """Comprehensive process analysis with expert-level detail"""
        
        metrics = []
        issues = []
        recommendations = []
        
        # Extract process information
        processes = process_data.get("processes", {})
        summary = process_data.get("summary", {})
        
        # Analyze process summary
        total_processes = summary.get("total_processes", 0)
        running_processes = summary.get("running_processes", 0)
        sleeping_processes = summary.get("sleeping_processes", 0)
        zombie_processes = summary.get("zombie_processes", 0)
        total_memory_usage = summary.get("total_memory_usage", 0)
        total_cpu_usage = summary.get("total_cpu_usage", 0)
        
        # Create process metrics
        metrics.append(TechnicalMetric(
            name="Total Processes",
            value=total_processes,
            unit="processes",
            threshold=100,
            analysis="Total number of system processes"
        ))
        
        metrics.append(TechnicalMetric(
            name="Running Processes",
            value=running_processes,
            unit="processes",
            analysis="Number of running processes"
        ))
        
        metrics.append(TechnicalMetric(
            name="Sleeping Processes",
            value=sleeping_processes,
            unit="processes",
            analysis="Number of sleeping processes"
        ))
        
        metrics.append(TechnicalMetric(
            name="Zombie Processes",
            value=zombie_processes,
            unit="processes",
            threshold=5,
            analysis="Number of zombie processes"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total Process Memory",
            value=total_memory_usage,
            unit="MB",
            threshold=4096,
            analysis="Total memory usage by all processes"
        ))
        
        metrics.append(TechnicalMetric(
            name="Total Process CPU",
            value=total_cpu_usage,
            unit="%",
            threshold=80,
            analysis="Total CPU usage by all processes"
        ))
        
        # Check for process issues
        if zombie_processes > 5:
            issues.append({
                "severity": SeverityLevel.MEDIUM.value,
                "category": "system",
                "description": f"High number of zombie processes",
                "impact": "Process table pollution",
                "evidence": f"Zombie processes: {zombie_processes}"
            })
            recommendations.append("Investigate and clean up zombie processes")
        
        if total_processes > 500:
            issues.append({
                "severity": SeverityLevel.INFO.value,
                "category": "system",
                "description": f"High number of processes",
                "impact": "System resource usage",
                "evidence": f"Total processes: {total_processes}"
            })
            recommendations.append("Monitor process count and resource usage")
        
        # Generate process recommendations
        recommendations.append("Monitor process resource usage")
        recommendations.append("Implement process monitoring and alerting")
        recommendations.append("Regular process cleanup and optimization")
        
        return SystemComponent(
            name="System Processes",
            type="service",
            status=self._calculate_component_status(issues),
            metrics=metrics,
            configuration=processes,
            dependencies=["system_resources", "kernel"],
            issues=issues,
            recommendations=recommendations
        )
    
    def analyze_dependencies_comprehensive(self, dependency_data: Dict[str, Any]) -> SystemComponent:
        """Comprehensive dependency analysis with expert-level detail"""
        
        metrics = []
        issues = []
        recommendations = []
        
        # Extract dependency information
        dependencies = dependency_data.get("dependencies", {})
        startup_order = dependency_data.get("startup_order", {})
        service_graph = dependency_data.get("service_graph", {})
        
        # Analyze dependency graph
        total_dependencies = len(dependencies)
        metrics.append(TechnicalMetric(
            name="Total Dependencies",
            value=total_dependencies,
            unit="dependencies",
            analysis="Total number of service dependencies"
        ))
        
        # Analyze startup order
        startup_services = len(startup_order)
        metrics.append(TechnicalMetric(
            name="Startup Services",
            value=startup_services,
            unit="services",
            analysis="Number of services with startup order"
        ))
        
        # Generate dependency recommendations
        recommendations.append("Monitor service dependency health")
        recommendations.append("Implement service dependency monitoring")
        recommendations.append("Document service dependencies and startup order")
        
        return SystemComponent(
            name="Service Dependencies",
            type="service",
            status=self._calculate_component_status(issues),
            metrics=metrics,
            configuration=dependencies,
            dependencies=["container_runtime", "system_services"],
            issues=issues,
            recommendations=recommendations
        )
    
    # Helper methods
    def _classify_health_status(self, value: float, warning_threshold: float, critical_threshold: float) -> HealthStatus:
        """Classify health status based on thresholds"""
        if value >= critical_threshold:
            return HealthStatus.CRITICAL
        elif value >= warning_threshold:
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY
    
    def _calculate_component_status(self, issues: List[Dict[str, Any]]) -> HealthStatus:
        """Calculate overall component status based on issues"""
        if not issues:
            return HealthStatus.HEALTHY
        
        critical_issues = [issue for issue in issues if issue.get("severity") == SeverityLevel.CRITICAL.value]
        high_issues = [issue for issue in issues if issue.get("severity") == SeverityLevel.HIGH.value]
        
        if critical_issues:
            return HealthStatus.CRITICAL
        elif high_issues:
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY
    
    def _create_container_analysis_template(self) -> Dict[str, Any]:
        """Create container analysis template"""
        return {
            "name": "Container Analysis",
            "description": "Comprehensive container service analysis",
            "metrics": [
                "container_status", "resource_usage", "health_status",
                "restart_counts", "uptime", "image_analysis"
            ],
            "thresholds": {
                "memory_usage_warning": 1024,
                "memory_usage_critical": 2048,
                "cpu_usage_warning": 70,
                "cpu_usage_critical": 90,
                "restart_count_warning": 5,
                "restart_count_critical": 10
            }
        }
    
    def _create_process_analysis_template(self) -> Dict[str, Any]:
        """Create process analysis template"""
        return {
            "name": "Process Analysis",
            "description": "Comprehensive system process analysis",
            "metrics": [
                "process_counts", "resource_usage", "process_states",
                "parent_child_relationships", "zombie_processes"
            ],
            "thresholds": {
                "process_count_warning": 200,
                "process_count_critical": 500,
                "zombie_processes_warning": 5,
                "zombie_processes_critical": 20,
                "memory_usage_warning": 4096,
                "memory_usage_critical": 8192
            }
        }
    
    def _create_dependency_analysis_template(self) -> Dict[str, Any]:
        """Create dependency analysis template"""
        return {
            "name": "Dependency Analysis",
            "description": "Comprehensive service dependency analysis",
            "metrics": [
                "dependency_graph", "startup_order", "service_chains",
                "circular_dependencies", "failure_impact"
            ],
            "thresholds": {
                "dependency_depth_warning": 5,
                "dependency_depth_critical": 10,
                "startup_time_warning": 60,
                "startup_time_critical": 120
            }
        }

# ============================================================================
# MAIN COMPREHENSIVE ANALYSIS ENGINE
# ============================================================================

class ComprehensiveAnalysisEngine:
    """Main comprehensive analysis engine integrating all frameworks"""
    
    def __init__(self):
        self.hardware_framework = HardwareAnalysisFramework()
        self.network_framework = NetworkAnalysisFramework()
        self.service_framework = ServiceAnalysisFramework()
        self.analysis_depth = AnalysisDepth.EXPERT
        self.analysis_timestamp = datetime.now()
    
    def analyze_system_comprehensive(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive system analysis with expert-level detail"""
        
        print(f"[COMPREHENSIVE ANALYSIS] Starting expert-level system analysis")
        
        # Initialize analysis results
        analysis_results = {
            "analysis_metadata": {
                "timestamp": self.analysis_timestamp.isoformat(),
                "analysis_depth": self.analysis_depth.value,
                "technical_detail_level": "expert",
                "frameworks_used": ["hardware", "network", "service"],
                "analysis_duration": 0
            },
            "component_analysis": {},
            "system_health": {},
            "technical_findings": [],
            "recommendations": [],
            "executive_summary": {}
        }
        
        start_time = datetime.now()
        
        # Analyze hardware components
        hardware_data = extracted_data.get("hardware_data", {})
        analysis_results["component_analysis"]["cpu"] = asdict(self.hardware_framework.analyze_cpu_comprehensive(hardware_data.get("cpu_data", {})))
        analysis_results["component_analysis"]["memory"] = asdict(self.hardware_framework.analyze_memory_comprehensive(hardware_data.get("memory_data", {})))
        analysis_results["component_analysis"]["thermal"] = asdict(self.hardware_framework.analyze_temperature_comprehensive(hardware_data.get("temperature_data", {})))
        analysis_results["component_analysis"]["power"] = asdict(self.hardware_framework.analyze_power_comprehensive(hardware_data.get("power_data", {})))
        analysis_results["component_analysis"]["cooling"] = asdict(self.hardware_framework.analyze_cooling_comprehensive(hardware_data.get("cooling_data", {})))
        analysis_results["component_analysis"]["pci"] = asdict(self.hardware_framework.analyze_pci_comprehensive(hardware_data.get("pci_data", {})))
        
        # Analyze network components
        network_data = extracted_data.get("network_data", {})
        analysis_results["component_analysis"]["interfaces"] = asdict(self.network_framework.analyze_interfaces_comprehensive(network_data.get("interface_data", {})))
        analysis_results["component_analysis"]["bgp"] = asdict(self.network_framework.analyze_bgp_comprehensive(network_data.get("bgp_data", {})))
        analysis_results["component_analysis"]["arp"] = asdict(self.network_framework.analyze_arp_comprehensive(network_data.get("arp_data", {})))
        
        # Analyze service components
        service_data = extracted_data.get("service_data", {})
        analysis_results["component_analysis"]["containers"] = asdict(self.service_framework.analyze_containers_comprehensive(service_data.get("container_data", {})))
        analysis_results["component_analysis"]["processes"] = asdict(self.service_framework.analyze_processes_comprehensive(service_data.get("process_data", {})))
        analysis_results["component_analysis"]["dependencies"] = asdict(self.service_framework.analyze_dependencies_comprehensive(service_data.get("dependency_data", {})))
        
        # Calculate system health
        analysis_results["system_health"] = self._calculate_system_health(analysis_results["component_analysis"])
        
        # Generate technical findings
        analysis_results["technical_findings"] = self._generate_technical_findings(analysis_results["component_analysis"])
        
        # Generate recommendations
        analysis_results["recommendations"] = self._generate_system_recommendations(analysis_results["component_analysis"])
        
        # Generate executive summary
        analysis_results["executive_summary"] = self._generate_executive_summary(analysis_results)
        
        # Calculate analysis duration
        end_time = datetime.now()
        analysis_results["analysis_metadata"]["analysis_duration"] = (end_time - start_time).total_seconds()
        
        print(f"[COMPREHENSIVE ANALYSIS] Completed expert-level analysis in {analysis_results['analysis_metadata']['analysis_duration']:.2f} seconds")
        
        return analysis_results
    
    def _calculate_system_health(self, component_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall system health"""
        
        health_scores = []
        component_statuses = {}
        
        for component_name, component_data in component_analysis.items():
            if isinstance(component_data, dict):
                status = component_data.get("status", "unknown")
                component_statuses[component_name] = status
                
                # Convert status to numeric score
                if status == "healthy":
                    health_scores.append(100)
                elif status == "warning":
                    health_scores.append(70)
                elif status == "degraded":
                    health_scores.append(50)
                elif status == "critical":
                    health_scores.append(20)
                else:
                    health_scores.append(0)
        
        # Calculate overall health score
        if health_scores:
            overall_score = sum(health_scores) / len(health_scores)
        else:
            overall_score = 0
        
        # Determine overall status
        if overall_score >= 90:
            overall_status = "healthy"
        elif overall_score >= 70:
            overall_status = "warning"
        elif overall_score >= 50:
            overall_status = "degraded"
        else:
            overall_status = "critical"
        
        return {
            "overall_score": round(overall_score, 2),
            "overall_status": overall_status,
            "component_scores": dict(zip(component_statuses.keys(), health_scores)),
            "component_statuses": component_statuses,
            "health_summary": self._generate_health_summary(component_statuses)
        }
    
    def _generate_health_summary(self, component_statuses: Dict[str, str]) -> str:
        """Generate health summary"""
        
        healthy_count = sum(1 for status in component_statuses.values() if status == "healthy")
        warning_count = sum(1 for status in component_statuses.values() if status == "warning")
        degraded_count = sum(1 for status in component_statuses.values() if status == "degraded")
        critical_count = sum(1 for status in component_statuses.values() if status == "critical")
        
        total_components = len(component_statuses)
        
        if critical_count > 0:
            return f"System in CRITICAL state - {critical_count} critical components"
        elif degraded_count > 0:
            return f"System DEGRADED - {degraded_count} degraded components"
        elif warning_count > 0:
            return f"System WARNING - {warning_count} components with issues"
        else:
            return f"System HEALTHY - all {total_components} components operational"
    
    def _generate_technical_findings(self, component_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate technical findings from component analysis"""
        
        findings = []
        
        for component_name, component_data in component_analysis.items():
            if isinstance(component_data, dict):
                issues = component_data.get("issues", [])
                for issue in issues:
                    findings.append({
                        "component": component_name,
                        "severity": issue.get("severity", "unknown"),
                        "category": issue.get("category", "unknown"),
                        "description": issue.get("description", ""),
                        "impact": issue.get("impact", ""),
                        "evidence": issue.get("evidence", ""),
                        "timestamp": self.analysis_timestamp.isoformat()
                    })
        
        # Sort findings by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        findings.sort(key=lambda x: severity_order.get(x.get("severity", "low"), 5))
        
        return findings
    
    def _generate_system_recommendations(self, component_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate system-wide recommendations"""
        
        all_recommendations = []
        recommendation_counts = {}
        
        for component_name, component_data in component_analysis.items():
            if isinstance(component_data, dict):
                recommendations = component_data.get("recommendations", [])
                for recommendation in recommendations:
                    # Count recommendation frequency
                    recommendation_counts[recommendation] = recommendation_counts.get(recommendation, 0) + 1
                    
                    # Add component context
                    all_recommendations.append({
                        "component": component_name,
                        "recommendation": recommendation,
                        "priority": self._calculate_recommendation_priority(recommendation, component_data.get("status", "unknown")),
                        "category": "system_optimization",
                        "timestamp": self.analysis_timestamp.isoformat()
                    })
        
        # Sort by priority and frequency
        all_recommendations.sort(key=lambda x: (x.get("priority", 5), -recommendation_counts.get(x.get("recommendation", ""), 0)))
        
        # Remove duplicates and limit to top recommendations
        unique_recommendations = []
        seen_recommendations = set()
        
        for rec in all_recommendations:
            rec_text = rec.get("recommendation", "")
            if rec_text not in seen_recommendations:
                unique_recommendations.append(rec)
                seen_recommendations.add(rec_text)
        
        return unique_recommendations[:20]  # Top 20 recommendations
    
    def _calculate_recommendation_priority(self, recommendation: str, component_status: str) -> int:
        """Calculate recommendation priority"""
        
        # Critical status recommendations get higher priority
        if component_status == "critical":
            base_priority = 1
        elif component_status == "degraded":
            base_priority = 2
        elif component_status == "warning":
            base_priority = 3
        else:
            base_priority = 4
        
        # Adjust based on recommendation content
        recommendation_lower = recommendation.lower()
        if "critical" in recommendation_lower or "immediate" in recommendation_lower:
            return base_priority - 1
        elif "monitor" in recommendation_lower or "consider" in recommendation_lower:
            return base_priority + 1
        else:
            return base_priority
    
    def _generate_executive_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary"""
        
        system_health = analysis_results.get("system_health", {})
        technical_findings = analysis_results.get("technical_findings", [])
        recommendations = analysis_results.get("recommendations", [])
        component_analysis = analysis_results.get("component_analysis", {})
        
        # Count issues by severity
        critical_issues = [f for f in technical_findings if f.get("severity") == "critical"]
        high_issues = [f for f in technical_findings if f.get("severity") == "high"]
        medium_issues = [f for f in technical_findings if f.get("severity") == "medium"]
        
        # Count recommendations by priority
        urgent_recommendations = [r for r in recommendations if r.get("priority", 5) <= 2]
        
        # Generate key metrics
        key_metrics = {}
        for component_name, component_data in component_analysis.items():
            if isinstance(component_data, dict):
                metrics = component_data.get("metrics", [])
                for metric in metrics[:3]:  # Top 3 metrics per component
                    if isinstance(metric, dict):
                        metric_name = metric.get("name", "")
                        metric_value = metric.get("value", "")
                        metric_unit = metric.get("unit", "")
                        
                        if metric_name and metric_value is not None:
                            key_metrics[f"{component_name}_{metric_name}"] = f"{metric_value} {metric_unit}"
        
        return {
            "overall_health_score": system_health.get("overall_score", 0),
            "overall_status": system_health.get("overall_status", "unknown"),
            "critical_issues_count": len(critical_issues),
            "high_issues_count": len(high_issues),
            "medium_issues_count": len(medium_issues),
            "urgent_recommendations_count": len(urgent_recommendations),
            "total_components_analyzed": len(component_analysis),
            "key_metrics": key_metrics,
            "health_summary": system_health.get("health_summary", ""),
            "business_impact": self._assess_business_impact(system_health, technical_findings),
            "immediate_actions": urgent_recommendations[:5],
            "strategic_recommendations": recommendations[:10]
        }
    
    def _assess_business_impact(self, system_health: Dict[str, Any], technical_findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess business impact"""
        
        overall_score = system_health.get("overall_score", 0)
        critical_issues = [f for f in technical_findings if f.get("severity") == "critical"]
        
        if overall_score >= 90:
            impact_level = "low"
            impact_description = "System operating normally with minimal business impact"
        elif overall_score >= 70:
            impact_level = "medium"
            impact_description = "System experiencing some issues with moderate business impact"
        elif overall_score >= 50:
            impact_level = "high"
            impact_description = "System performance degraded with significant business impact"
        else:
            impact_level = "critical"
            impact_description = "System in critical state with severe business impact"
        
        # Adjust for critical issues
        if critical_issues:
            impact_level = "critical"
            impact_description += f" - {len(critical_issues)} critical issues require immediate attention"
        
        return {
            "impact_level": impact_level,
            "impact_description": impact_description,
            "risk_assessment": self._assess_risk_level(system_health, technical_findings),
            "operational_status": self._assess_operational_status(system_health)
        }
    
    def _assess_risk_level(self, system_health: Dict[str, Any], technical_findings: List[Dict[str, Any]]) -> str:
        """Assess risk level"""
        
        overall_score = system_health.get("overall_score", 0)
        critical_issues = len([f for f in technical_findings if f.get("severity") == "critical"])
        high_issues = len([f for f in technical_findings if f.get("severity") == "high"])
        
        if critical_issues > 0:
            return "critical"
        elif high_issues > 2 or overall_score < 50:
            return "high"
        elif high_issues > 0 or overall_score < 70:
            return "medium"
        else:
            return "low"
    
    def _assess_operational_status(self, system_health: Dict[str, Any]) -> str:
        """Assess operational status"""
        
        overall_status = system_health.get("overall_status", "unknown")
        
        if overall_status == "healthy":
            return "fully_operational"
        elif overall_status == "warning":
            return "operational_with_issues"
        elif overall_status == "degraded":
            return "limited_operation"
        else:
            return "non_operational"

# ============================================================================
# MAIN EXECUTION FOR TESTING
# ============================================================================

if __name__ == "__main__":
    # Test the comprehensive analysis engine
    engine = ComprehensiveAnalysisEngine()
    
    print("Comprehensive Analysis Framework initialized")
    print(f"Hardware framework: {len(engine.hardware_framework.cpu_analysis_template)} templates")
    print(f"Network framework: {len(engine.network_framework.interface_analysis_template)} templates")
    print(f"Service framework: {len(engine.service_framework.container_analysis_template)} templates")
    print(f"Analysis depth: {engine.analysis_depth.value}")
    print(f"Analysis timestamp: {engine.analysis_timestamp}")
    
    # Example usage (would need actual extracted_data)
    # results = engine.analyze_system_comprehensive(extracted_data)
    # print(json.dumps(results, indent=2, default=str))
    
    print("Comprehensive Analysis Framework ready for expert-level analysis")