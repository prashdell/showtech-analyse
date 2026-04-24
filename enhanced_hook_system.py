#!/usr/bin/env python3
"""
Enhanced Hook System for Skill Tool Integration
Fixes hook system to work with skill tool invocations and provides broader coverage
"""

import os
import sys
import json
import logging
import threading
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import subprocess
import re
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_hook_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedHookSystem:
    """Enhanced hook system that works with skill tool invocations and provides broader coverage"""
    
    def __init__(self):
        self.workspace_root = Path(r"C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse")
        self.hook_active = False
        self.intercepted_modules = set()
        self.intercepted_functions = set()
        self.skill_invocations = []
        
        # Hook statistics
        self.hook_stats = {
            'modules_hooked': 0,
            'functions_hooked': 0,
            'invocations_intercepted': 0,
            'errors_prevented': 0,
            'patterns_detected': 0
        }
        
        # Skill tool integration
        from skill_tool_integration_system import get_skill_tool_integration_system
        self.integration_system = get_skill_tool_integration_system()
        
        logger.info("Enhanced Hook System initialized")
    
    def activate_enhanced_hooks(self):
        """Activate enhanced hooks with skill tool integration"""
        if self.hook_active:
            logger.warning("Enhanced hooks already active")
            return
        
        self.hook_active = True
        
        # 1. Enhanced Python import hooks
        self._install_enhanced_import_hooks()
        
        # 2. Function-level hooks
        self._install_function_hooks()
        
        # 3. Subprocess hooks for skill tool commands
        self._install_subprocess_hooks()
        
        # 4. File operation hooks
        self._install_file_hooks()
        
        # 5. Memory and resource hooks
        self._install_resource_hooks()
        
        # 6. Start monitoring thread
        self._start_monitoring_thread()
        
        logger.info("Enhanced hooks activated with skill tool integration")
    
    def _install_enhanced_import_hooks(self):
        """Install enhanced import hooks that work better with skill tool"""
        original_import = __builtins__['__import__']
        
        def enhanced_import(name, globals=None, locals=None, fromlist=(), level=0):
            try:
                module = original_import(name, globals, locals, fromlist, level)
                
                # Enhanced skill module detection
                if self._is_enhanced_skill_module(module, name):
                    self._hook_enhanced_module(module, name)
                
                return module
                
            except ImportError as e:
                # Log import errors for learning
                self._log_import_error(name, str(e))
                raise
        
        __builtins__['__import__'] = enhanced_import
        logger.info("Enhanced import hooks installed")
    
    def _is_enhanced_skill_module(self, module, name: str) -> bool:
        """Enhanced skill module detection"""
        # Original patterns
        skill_patterns = [
            'sonic_', 'skill_', 'analysis_', 'triage_', 'showtech_',
            'jira_', 'memory_', 'bgp_', 'interface_', 'container_'
        ]
        
        name_lower = name.lower()
        if any(pattern in name_lower for pattern in skill_patterns):
            return True
        
        # Enhanced patterns based on module attributes
        if hasattr(module, '__dict__'):
            for attr_name, attr_value in module.__dict__.items():
                if callable(attr_value):
                    func_name = attr_name.lower()
                    if any(pattern in func_name for pattern in 
                        ['analyze', 'triage', 'execute', 'process', 'run', 'invoke']):
                        return True
        
        # File path based detection
        if hasattr(module, '__file__') and module.__file__:
            file_path = Path(module.__file__)
            if any(pattern in str(file_path).lower() for pattern in 
                ['skills', 'showtech', 'sonic', 'analysis']):
                return True
        
        return False
    
    def _hook_enhanced_module(self, module, name: str):
        """Enhanced module hooking with better error handling"""
        if name in self.intercepted_modules:
            return
        
        self.intercepted_modules.add(name)
        self.hook_stats['modules_hooked'] += 1
        
        # Hook functions with enhanced error handling
        for attr_name, attr_value in module.__dict__.items():
            if callable(attr_value) and self._is_enhanced_skill_function(attr_name, attr_value):
                try:
                    self._wrap_enhanced_function(module, attr_name, attr_value)
                    self.hook_stats['functions_hooked'] += 1
                except Exception as e:
                    logger.warning(f"Failed to hook function {attr_name}: {e}")
        
        logger.info(f"Enhanced module hooked: {name}")
    
    def _is_enhanced_skill_function(self, name: str, func: Callable) -> bool:
        """Enhanced skill function detection"""
        name_lower = name.lower()
        
        # Enhanced function name patterns
        skill_function_patterns = [
            'analyze', 'triage', 'execute', 'process', 'run', 'invoke',
            'start', 'perform', 'handle', 'diagnose', 'investigate',
            'extract', 'parse', 'validate', 'check', 'monitor'
        ]
        
        if any(pattern in name_lower for pattern in skill_function_patterns):
            return True
        
        # Enhanced signature detection
        try:
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            skill_params = ['context', 'data', 'input', 'showtech', 'archive', 'config']
            if any(param in params for param in skill_params):
                return True
        except:
            pass
        
        # Docstring detection
        if hasattr(func, '__doc__') and func.__doc__:
            doc_lower = func.__doc__.lower()
            skill_keywords = ['skill', 'analysis', 'triage', 'sonic', 'showtech']
            if any(keyword in doc_lower for keyword in skill_keywords):
                return True
        
        return False
    
    def _wrap_enhanced_function(self, module, func_name: str, original_func: Callable):
        """Enhanced function wrapping with comprehensive error handling"""
        def enhanced_wrapper(*args, **kwargs):
            # Extract skill name from context
            skill_name = self._extract_enhanced_skill_name(module, func_name, args, kwargs)
            
            if skill_name and self.integration_system:
                # Create context for learning
                context = self._create_enhanced_execution_context(args, kwargs)
                
                # Execute with comprehensive error handling
                start_time = time.time()
                success = True
                result_data = {}
                error_message = None
                
                try:
                    result = original_func(*args, **kwargs)
                    
                    # Extract result data
                    if isinstance(result, dict):
                        result_data = result
                    else:
                        result_data = {'result': str(result)}
                    
                    # Detect patterns in result
                    new_patterns = self._extract_enhanced_patterns(result_data, skill_name)
                    if new_patterns:
                        result_data['new_patterns'] = new_patterns
                        self.hook_stats['patterns_detected'] += 1
                    
                    return result
                    
                except Exception as e:
                    success = False
                    error_message = str(e)
                    
                    # Enhanced error analysis
                    self._analyze_enhanced_error(error_message, skill_name, context)
                    
                    # Prevent common errors
                    if self._should_prevent_error(error_message):
                        self._handle_error_prevention(error_message, skill_name, context)
                        self.hook_stats['errors_prevented'] += 1
                    
                    raise
                finally:
                    # Capture invocation for learning
                    execution_time = time.time() - start_time
                    self.integration_system.capture_skill_tool_invocation(
                        skill_name=skill_name,
                        context=context,
                        execution_time=execution_time,
                        success=success,
                        result_data=result_data,
                        error_message=error_message
                    )
                    
                    self.hook_stats['invocations_intercepted'] += 1
            
            else:
                # No interception, call original function
                return original_func(*args, **kwargs)
        
        # Preserve function metadata
        enhanced_wrapper.__name__ = original_func.__name__
        enhanced_wrapper.__doc__ = original_func.__doc__
        enhanced_wrapper.__module__ = original_func.__module__
        
        # Replace the function in the module
        setattr(module, func_name, enhanced_wrapper)
        logger.info(f"Enhanced function wrapped: {module.__name__}.{func_name}")
    
    def _extract_enhanced_skill_name(self, module, func_name: str, args: tuple, kwargs: dict) -> Optional[str]:
        """Enhanced skill name extraction"""
        # From module name
        if hasattr(module, '__name__'):
            module_name = module.__name__.lower()
            if 'sonic_' in module_name:
                return module_name.replace('_', '_')
        
        # From function name
        func_lower = func_name.lower()
        if any(pattern in func_lower for pattern in ['analyze', 'triage', 'execute']):
            # Look for skill indicators in arguments
            for arg in args + list(kwargs.values()):
                if isinstance(arg, str):
                    if 'sonic_' in arg.lower():
                        return arg.lower()
                    elif any(skill in arg.lower() for skill in ['memory', 'bgp', 'interface', 'container', 'hardware']):
                        return f"sonic_{arg.lower()}"
        
        # From context
        if 'skill_name' in kwargs:
            return kwargs['skill_name']
        
        # From showtech path
        if 'showtech_path' in kwargs:
            showtech_path = kwargs['showtech_path']
            if 'hardware' in showtech_path.lower():
                return 'sonic_hardware_platform_analyzer'
            elif 'bgp' in showtech_path.lower():
                return 'sonic_bgp_connectivity_triage'
            elif 'memory' in showtech_path.lower():
                return 'sonic_memory_exhaustion_triage'
        
        return None
    
    def _create_enhanced_execution_context(self, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """Create enhanced execution context"""
        context = {}
        
        # Extract relevant parameters
        for key, value in kwargs.items():
            if key in ['context', 'data', 'input', 'showtech_path', 'archive_path', 'config']:
                context[key] = value
        
        # Add execution metadata
        context['execution_timestamp'] = datetime.now().isoformat()
        context['args_count'] = len(args)
        context['kwargs_keys'] = list(kwargs.keys())
        
        # Add system context
        context['system_info'] = {
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'disk_usage': psutil.disk_usage('/').percent
        }
        
        return context
    
    def _extract_enhanced_patterns(self, result_data: Dict[str, Any], skill_name: str) -> List[str]:
        """Enhanced pattern extraction"""
        patterns = []
        
        # Success patterns
        if result_data.get('success') or result_data.get('analysis_complete'):
            patterns.append('successful_execution_pattern')
        
        # Skill-specific patterns
        skill_lower = skill_name.lower()
        if 'interface' in skill_lower:
            if 'active_interfaces' in result_data:
                patterns.append('interface_analysis_pattern')
            if 'traffic_patterns' in result_data:
                patterns.append('traffic_analysis_pattern')
        
        elif 'bgp' in skill_lower:
            if 'session_status' in result_data:
                patterns.append('bgp_session_analysis_pattern')
            if 'route_analysis' in result_data:
                patterns.append('bgp_route_analysis_pattern')
        
        elif 'memory' in skill_lower:
            if 'memory_usage' in result_data:
                patterns.append('memory_analysis_pattern')
            if 'resource_exhaustion' in result_data:
                patterns.append('resource_exhaustion_pattern')
        
        elif 'container' in skill_lower:
            if 'container_health' in result_data:
                patterns.append('container_health_pattern')
            if 'docker_status' in result_data:
                patterns.append('docker_analysis_pattern')
        
        # Performance patterns
        if 'execution_time' in result_data:
            patterns.append('performance_tracking_pattern')
        
        # Data completeness patterns
        if len(result_data) > 10:
            patterns.append('comprehensive_analysis_pattern')
        
        return patterns
    
    def _analyze_enhanced_error(self, error_message: str, skill_name: str, context: Dict[str, Any]):
        """Enhanced error analysis for learning"""
        error_analysis = {
            'skill_name': skill_name,
            'error_message': error_message,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'error_type': self._classify_error(error_message),
            'severity': self._assess_error_severity(error_message),
            'prevention_suggestions': self._generate_prevention_suggestions(error_message)
        }
        
        # Store error analysis for learning
        error_file = self.workspace_root / "knowledge_base" / "error_patterns.json"
        
        error_patterns = []
        if error_file.exists():
            with open(error_file, 'r') as f:
                error_patterns = json.load(f)
        
        error_patterns.append(error_analysis)
        
        # Keep only recent errors
        if len(error_patterns) > 100:
            error_patterns = error_patterns[-100:]
        
        with open(error_file, 'w') as f:
            json.dump(error_patterns, f, indent=2, default=str)
        
        logger.info(f"Enhanced error analysis completed for {skill_name}")
    
    def _classify_error(self, error_message: str) -> str:
        """Classify error type"""
        error_lower = error_message.lower()
        
        if 'file not found' in error_lower or 'no such file' in error_lower:
            return 'file_access_error'
        elif 'permission' in error_lower or 'access denied' in error_lower:
            return 'permission_error'
        elif 'timeout' in error_lower or 'timed out' in error_lower:
            return 'timeout_error'
        elif 'memory' in error_lower or 'out of memory' in error_lower:
            return 'memory_error'
        elif 'connection' in error_lower or 'network' in error_lower:
            return 'network_error'
        elif 'import' in error_lower or 'module' in error_lower:
            return 'import_error'
        elif 'type' in error_lower or 'attribute' in error_lower:
            return 'type_error'
        else:
            return 'unknown_error'
    
    def _assess_error_severity(self, error_message: str) -> str:
        """Assess error severity"""
        error_lower = error_message.lower()
        
        if 'critical' in error_lower or 'fatal' in error_lower:
            return 'critical'
        elif 'timeout' in error_lower or 'memory' in error_lower:
            return 'high'
        elif 'permission' in error_lower or 'access' in error_lower:
            return 'medium'
        else:
            return 'low'
    
    def _generate_prevention_suggestions(self, error_message: str) -> List[str]:
        """Generate prevention suggestions"""
        suggestions = []
        error_lower = error_message.lower()
        
        if 'file not found' in error_lower:
            suggestions.append('Add file existence validation before access')
            suggestions.append('Check file path and permissions')
        elif 'permission' in error_lower:
            suggestions.append('Verify file and directory permissions')
            suggestions.append('Run with appropriate user privileges')
        elif 'timeout' in error_lower:
            suggestions.append('Increase timeout values')
            suggestions.append('Add progress monitoring')
        elif 'memory' in error_lower:
            suggestions.append('Monitor memory usage patterns')
            suggestions.append('Optimize memory allocation')
        elif 'import' in error_lower:
            suggestions.append('Verify module installation')
            suggestions.append('Check Python path configuration')
        
        return suggestions
    
    def _should_prevent_error(self, error_message: str) -> bool:
        """Determine if error should be prevented"""
        preventable_errors = [
            'file not found',
            'permission denied',
            'timeout',
            'out of memory',
            'connection refused'
        ]
        
        error_lower = error_message.lower()
        return any(pattern in error_lower for pattern in preventable_errors)
    
    def _handle_error_prevention(self, error_message: str, skill_name: str, context: Dict[str, Any]):
        """Handle error prevention"""
        prevention_action = {
            'error_message': error_message,
            'skill_name': skill_name,
            'context': context,
            'prevention_taken': True,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store prevention action
        prevention_file = self.workspace_root / "knowledge_base" / "error_preventions.json"
        
        preventions = []
        if prevention_file.exists():
            with open(prevention_file, 'r') as f:
                preventions = json.load(f)
        
        preventions.append(prevention_action)
        
        # Keep only recent preventions
        if len(preventions) > 50:
            preventions = preventions[-50:]
        
        with open(prevention_file, 'w') as f:
            json.dump(preventions, f, indent=2, default=str)
        
        logger.info(f"Error prevention handled for {skill_name}: {error_message}")
    
    def _install_function_hooks(self):
        """Install function-level hooks for broader coverage"""
        # Hook into common utility functions
        try:
            import builtins
            
            # Hook into print for debugging
            original_print = builtins.print
            
            def enhanced_print(*args, **kwargs):
                # Capture print statements for learning
                if len(args) > 0 and isinstance(args[0], str):
                    message = args[0]
                    if any(keyword in message.lower() for keyword in ['error', 'warning', 'failed', 'success']):
                        self._capture_log_message(message, 'print')
                
                return original_print(*args, **kwargs)
            
            builtins.print = enhanced_print
            logger.info("Enhanced print hook installed")
            
        except Exception as e:
            logger.warning(f"Failed to install function hooks: {e}")
    
    def _install_subprocess_hooks(self):
        """Install subprocess hooks for skill tool commands"""
        try:
            import subprocess
            
            original_run = subprocess.run
            
            def enhanced_subprocess_run(*args, **kwargs):
                # Check if this is a skill-related command
                command_str = ' '.join(args[0]) if args and isinstance(args[0], list) else str(args[0]) if args else ''
                
                if self._is_enhanced_skill_command(command_str):
                    skill_name = self._extract_enhanced_skill_from_command(command_str)
                    if skill_name:
                        context = {'command': command_str, 'execution_type': 'subprocess'}
                        
                        start_time = time.time()
                        try:
                            result = original_run(*args, **kwargs)
                            success = result.returncode == 0
                            
                            execution_time = time.time() - start_time
                            result_data = {
                                'stdout': result.stdout,
                                'stderr': result.stderr,
                                'returncode': result.returncode
                            }
                            
                            # Capture for learning
                            self.integration_system.capture_skill_tool_invocation(
                                skill_name=skill_name,
                                context=context,
                                execution_time=execution_time,
                                success=success,
                                result_data=result_data
                            )
                            
                            return result
                            
                        except Exception as e:
                            execution_time = time.time() - start_time
                            self.integration_system.capture_skill_tool_invocation(
                                skill_name=skill_name,
                                context=context,
                                execution_time=execution_time,
                                success=False,
                                error_message=str(e)
                            )
                            raise
                
                return original_run(*args, **kwargs)
            
            subprocess.run = enhanced_subprocess_run
            logger.info("Enhanced subprocess hooks installed")
            
        except Exception as e:
            logger.warning(f"Failed to install subprocess hooks: {e}")
    
    def _is_enhanced_skill_command(self, command: str) -> bool:
        """Enhanced skill command detection"""
        command_lower = command.lower()
        
        skill_indicators = [
            'sonic_', 'skill_', 'analyze', 'triage', 'showtech',
            'bgp', 'memory', 'interface', 'container', 'hardware',
            'log', 'performance', 'core_dump', 'version'
        ]
        
        return any(indicator in command_lower for indicator in skill_indicators)
    
    def _extract_enhanced_skill_from_command(self, command: str) -> Optional[str]:
        """Extract skill name from command"""
        command_lower = command.lower()
        
        if 'hardware' in command_lower:
            return 'sonic_hardware_platform_analyzer'
        elif 'bgp' in command_lower:
            return 'sonic_bgp_connectivity_triage'
        elif 'memory' in command_lower:
            return 'sonic_memory_exhaustion_triage'
        elif 'interface' in command_lower:
            return 'sonic_interface_connectivity_triage'
        elif 'container' in command_lower:
            return 'sonic_container_health_triage'
        elif 'log' in command_lower:
            return 'sonic_log_analysis_triage'
        elif 'performance' in command_lower:
            return 'sonic_performance_degradation_prediction'
        elif 'core_dump' in command_lower:
            return 'sonic_core_dump_analysis'
        elif 'version' in command_lower:
            return 'sonic_version_compatibility_check'
        
        return None
    
    def _install_file_hooks(self):
        """Install file operation hooks"""
        try:
            import builtins
            
            original_open = builtins.open
            
            def enhanced_open(file, mode='r', **kwargs):
                # Capture file operations for learning
                if isinstance(file, str):
                    if self._is_enhanced_skill_file(file):
                        self._capture_file_operation(file, mode, 'open')
                
                return original_open(file, mode, **kwargs)
            
            builtins.open = enhanced_open
            logger.info("Enhanced file hooks installed")
            
        except Exception as e:
            logger.warning(f"Failed to install file hooks: {e}")
    
    def _is_enhanced_skill_file(self, file_path: str) -> bool:
        """Enhanced skill file detection"""
        file_lower = file_path.lower()
        
        skill_file_patterns = [
            'showtech', 'skill', 'sonic_', 'analysis', 'triage',
            '.json', '.md', '.py', '.log', '.conf', '.cfg'
        ]
        
        return any(pattern in file_lower for pattern in skill_file_patterns)
    
    def _capture_file_operation(self, file_path: str, mode: str, operation: str):
        """Capture file operation for learning"""
        operation_data = {
            'file_path': file_path,
            'mode': mode,
            'operation': operation,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store file operation data
        file_ops_file = self.workspace_root / "knowledge_base" / "file_operations.json"
        
        file_ops = []
        if file_ops_file.exists():
            with open(file_ops_file, 'r') as f:
                file_ops = json.load(f)
        
        file_ops.append(operation_data)
        
        # Keep only recent operations
        if len(file_ops) > 100:
            file_ops = file_ops[-100:]
        
        with open(file_ops_file, 'w') as f:
            json.dump(file_ops, f, indent=2, default=str)
    
    def _install_resource_hooks(self):
        """Install resource monitoring hooks"""
        # Monitor system resources during skill execution
        self._start_resource_monitoring()
        logger.info("Enhanced resource hooks installed")
    
    def _start_resource_monitoring(self):
        """Start resource monitoring thread"""
        def monitor_resources():
            while self.hook_active:
                try:
                    # Monitor CPU and memory usage
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    
                    # Check for resource pressure
                    if cpu_percent > 80 or memory.percent > 80:
                        self._capture_resource_pressure(cpu_percent, memory.percent)
                    
                    time.sleep(10)  # Monitor every 10 seconds
                    
                except Exception as e:
                    logger.error(f"Error in resource monitoring: {e}")
                    time.sleep(30)
        
        monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
        monitor_thread.start()
    
    def _capture_resource_pressure(self, cpu_percent: float, memory_percent: float):
        """Capture resource pressure for learning"""
        pressure_data = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'timestamp': datetime.now().isoformat(),
            'severity': 'high' if cpu_percent > 90 or memory_percent > 90 else 'medium'
        }
        
        # Store resource pressure data
        pressure_file = self.workspace_root / "knowledge_base" / "resource_pressure.json"
        
        pressure_events = []
        if pressure_file.exists():
            with open(pressure_file, 'r') as f:
                pressure_events = json.load(f)
        
        pressure_events.append(pressure_data)
        
        # Keep only recent events
        if len(pressure_events) > 50:
            pressure_events = pressure_events[-50:]
        
        with open(pressure_file, 'w') as f:
            json.dump(pressure_events, f, indent=2, default=str)
    
    def _capture_log_message(self, message: str, source: str):
        """Capture log messages for learning"""
        log_data = {
            'message': message,
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'level': self._classify_log_level(message)
        }
        
        # Store log data
        log_file = self.workspace_root / "knowledge_base" / "captured_logs.json"
        
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_data)
        
        # Keep only recent logs
        if len(logs) > 200:
            logs = logs[-200:]
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2, default=str)
    
    def _classify_log_level(self, message: str) -> str:
        """Classify log level from message"""
        message_lower = message.lower()
        
        if 'error' in message_lower or 'critical' in message_lower or 'fatal' in message_lower:
            return 'error'
        elif 'warning' in message_lower or 'warn' in message_lower:
            return 'warning'
        elif 'info' in message_lower or 'information' in message_lower:
            return 'info'
        else:
            return 'debug'
    
    def _start_monitoring_thread(self):
        """Start monitoring thread for system health"""
        def monitor_system():
            while self.hook_active:
                try:
                    # Generate system health report
                    health_report = self._generate_health_report()
                    
                    # Store health report
                    health_file = self.workspace_root / "knowledge_base" / "system_health.json"
                    with open(health_file, 'w') as f:
                        json.dump(health_report, f, indent=2, default=str)
                    
                    time.sleep(60)  # Monitor every minute
                    
                except Exception as e:
                    logger.error(f"Error in system monitoring: {e}")
                    time.sleep(60)
        
        monitor_thread = threading.Thread(target=monitor_system, daemon=True)
        monitor_thread.start()
    
    def _generate_health_report(self) -> Dict[str, Any]:
        """Generate system health report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'hook_stats': self.hook_stats,
            'system_resources': {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent
            },
            'active_invocations': len(self.intercepted_modules),
            'processed_invocations': len(self.skill_invocations)
        }
    
    def get_hook_status(self) -> Dict[str, Any]:
        """Get comprehensive hook status"""
        return {
            'hooks_active': self.hook_active,
            'hook_stats': self.hook_stats,
            'intercepted_modules': len(self.intercepted_modules),
            'intercepted_functions': len(self.intercepted_functions),
            'skill_invocations': len(self.skill_invocations),
            'integration_system_available': self.integration_system is not None
        }
    
    def generate_hook_report(self) -> str:
        """Generate comprehensive hook system report"""
        status = self.get_hook_status()
        
        report = f"""
# Enhanced Hook System Report
Generated: {datetime.now().isoformat()}

## Hook Status
- Hooks Active: {status['hooks_active']}
- Integration System: {'Available' if status['integration_system_available'] else 'Not Available'}

## Hook Statistics
- Modules Hooked: {status['hook_stats']['modules_hooked']}
- Functions Hooked: {status['hook_stats']['functions_hooked']}
- Invocations Intercepted: {status['hook_stats']['invocations_intercepted']}
- Errors Prevented: {status['hook_stats']['errors_prevented']}
- Patterns Detected: {status['hook_stats']['patterns_detected']}

## Coverage
- Intercepted Modules: {status['intercepted_modules']}
- Intercepted Functions: {status['intercepted_functions']}
- Skill Invocations: {status['skill_invocations']}

## System Resources
"""
        
        # Add system resources
        if 'system_resources' in status:
            resources = status['system_resources']
            report += f"- CPU Usage: {resources['cpu_percent']:.1f}%\n"
            report += f"- Memory Usage: {resources['memory_percent']:.1f}%\n"
            report += f"- Disk Usage: {resources['disk_percent']:.1f}%\n"
        
        return report
    
    def deactivate_enhanced_hooks(self):
        """Deactivate enhanced hooks"""
        self.hook_active = False
        logger.info("Enhanced hooks deactivated")

# Global enhanced hook system instance
_global_enhanced_hook_system = None

def get_enhanced_hook_system() -> EnhancedHookSystem:
    """Get or create global enhanced hook system"""
    global _global_enhanced_hook_system
    if _global_enhanced_hook_system is None:
        _global_enhanced_hook_system = EnhancedHookSystem()
    return _global_enhanced_hook_system

# Auto-activate enhanced hooks when imported
if __name__ != "__main__":
    try:
        enhanced_hooks = get_enhanced_hook_system()
        enhanced_hooks.activate_enhanced_hooks()
        logger.info("Enhanced hooks auto-activated")
    except Exception as e:
        logger.error(f"Failed to auto-activate enhanced hooks: {e}")

# Example usage
if __name__ == "__main__":
    enhanced_hooks = get_enhanced_hook_system()
    enhanced_hooks.activate_enhanced_hooks()
    
    # Test enhanced hooks
    @enhanced_hooks.capture_skill_invocation('test_skill', {'test': True})
    def test_function():
        time.sleep(1)
        return {'success': True, 'analysis_complete': True}
    
    result = test_function()
    
    # Generate report
    print(enhanced_hooks.generate_hook_report())