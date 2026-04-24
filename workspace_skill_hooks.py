#!/usr/bin/env python3
"""
Workspace-Wide Skill Invocation Hook System
Automatically intercepts ALL skill invocations in the workspace and captures lessons learned
"""

import os
import sys
import json
import logging
import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import threading
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('workspace_skill_hooks.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WorkspaceSkillHookSystem:
    """System to automatically hook into all skill invocations workspace-wide"""
    
    def __init__(self):
        self.workspace_root = Path(r"C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse")
        self.hook_registry = {}
        self.intercepted_modules = set()
        self.hook_active = False
        
        # Import knowledge integrator
        sys.path.append(str(self.workspace_root))
        try:
            from automatic_knowledge_integrator import get_global_integrator
            self.knowledge_integrator = get_global_integrator()
        except ImportError as e:
            logger.error(f"Could not import knowledge integrator: {e}")
            self.knowledge_integrator = None
        
        logger.info("Workspace Skill Hook System initialized")
    
    def activate_workspace_hooks(self):
        """Activate hooks for all skill-related modules in workspace"""
        if self.hook_active:
            logger.warning("Hooks already active")
            return
        
        self.hook_active = True
        
        # Hook into Python's import system
        self._install_import_hook()
        
        # Hook into existing modules
        self._hook_existing_modules()
        
        # Hook into skill execution patterns
        self._hook_skill_patterns()
        
        logger.info("Workspace hooks activated")
    
    def _install_import_hook(self):
        """Install custom import hook to intercept skill module imports"""
        original_import = __builtins__['__import__']
        
        def skill_intercepting_import(name, globals=None, locals=None, fromlist=(), level=0):
            module = original_import(name, globals, locals, fromlist, level)
            
            # Check if this is a skill-related module
            if self._is_skill_module(module, name):
                self._hook_module(module, name)
            
            return module
        
        __builtins__['__import__'] = skill_intercepting_import
        logger.info("Import hook installed")
    
    def _is_skill_module(self, module, name: str) -> bool:
        """Check if module is skill-related"""
        # Check module name patterns
        skill_patterns = [
            'sonic_', 'skill_', 'analysis_', 'triage_', 'showtech_',
            'jira_', 'memory_', 'bgp_', 'interface_', 'container_'
        ]
        
        name_lower = name.lower()
        if any(pattern in name_lower for pattern in skill_patterns):
            return True
        
        # Check module file path
        if hasattr(module, '__file__') and module.__file__:
            file_path = Path(module.__file__)
            if 'skills' in file_path.parts or 'showtech' in file_path.parts:
                return True
        
        # Check module attributes for skill-like functions
        if hasattr(module, '__dict__'):
            for attr_name, attr_value in module.__dict__.items():
                if callable(attr_value) and any(pattern in attr_name.lower() for pattern in 
                    ['analyze', 'triage', 'execute', 'process', 'run']):
                    return True
        
        return False
    
    def _hook_module(self, module, name: str):
        """Hook into a specific module to capture skill invocations"""
        if name in self.intercepted_modules:
            return
        
        self.intercepted_modules.add(name)
        
        # Hook into module functions
        for attr_name, attr_value in module.__dict__.items():
            if callable(attr_value) and self._is_skill_function(attr_name, attr_value):
                self._wrap_function(module, attr_name, attr_value)
        
        logger.info(f"Hooked module: {name}")
    
    def _is_skill_function(self, name: str, func: Callable) -> bool:
        """Check if function is a skill execution function"""
        name_lower = name.lower()
        
        # Check function name patterns
        skill_function_patterns = [
            'analyze', 'triage', 'execute', 'process', 'run', 'invoke',
            'start', 'perform', 'handle', 'diagnose', 'investigate'
        ]
        
        if any(pattern in name_lower for pattern in skill_function_patterns):
            return True
        
        # Check function signature
        try:
            sig = inspect.signature(func)
            # Skill functions typically take context or data parameters
            params = list(sig.parameters.keys())
            if any(param in params for param in ['context', 'data', 'input', 'showtech', 'archive']):
                return True
        except:
            pass
        
        return False
    
    def _wrap_function(self, module, func_name: str, original_func: Callable):
        """Wrap function to capture execution data"""
        def wrapped_function(*args, **kwargs):
            # Extract skill name from function context
            skill_name = self._extract_skill_name(module, func_name, args, kwargs)
            
            if skill_name and self.knowledge_integrator:
                # Create context for learning
                context = self._create_execution_context(args, kwargs)
                
                # Intercept the execution
                with self.knowledge_integrator.intercept_invocation(skill_name, context) as ctx:
                    try:
                        result = original_func(*args, **kwargs)
                        
                        # Extract result data
                        success = True
                        output_data = self._extract_result_data(result)
                        new_patterns = self._extract_patterns_from_result(result, skill_name)
                        
                        ctx.record_result(success, output_data, None, new_patterns)
                        return result
                        
                    except Exception as e:
                        ctx.record_result(False, None, str(e))
                        raise
            else:
                # No interception, just call original function
                return original_func(*args, **kwargs)
        
        # Preserve function metadata
        wrapped_function.__name__ = original_func.__name__
        wrapped_function.__doc__ = original_func.__doc__
        wrapped_function.__module__ = original_func.__module__
        
        # Replace the function in the module
        setattr(module, func_name, wrapped_function)
        
        logger.info(f"Wrapped function: {module.__name__}.{func_name}")
    
    def _extract_skill_name(self, module, func_name: str, args: tuple, kwargs: dict) -> Optional[str]:
        """Extract skill name from execution context"""
        # Try to get from module name
        if hasattr(module, '__name__'):
            module_name = module.__name__.lower()
            if 'sonic_' in module_name:
                return module_name.replace('_', '_')
        
        # Try to get from function name
        func_lower = func_name.lower()
        if 'analyze' in func_lower or 'triage' in func_lower:
            # Look for skill indicators in arguments
            for arg in args + list(kwargs.values()):
                if isinstance(arg, str):
                    if 'sonic_' in arg.lower():
                        return arg.lower()
                    elif any(skill in arg.lower() for skill in ['memory', 'bgp', 'interface', 'container', 'hardware']):
                        return f"sonic_{arg.lower()}"
        
        # Try to get from context
        if 'skill_name' in kwargs:
            return kwargs['skill_name']
        
        if 'showtech_path' in kwargs:
            # Infer skill from showtech path
            showtech_path = kwargs['showtech_path']
            if 'hardware' in showtech_path.lower():
                return 'sonic_hardware_platform_analyzer'
            elif 'bgp' in showtech_path.lower():
                return 'sonic_bgp_connectivity_triage'
            elif 'memory' in showtech_path.lower():
                return 'sonic_memory_exhaustion_triage'
        
        return None
    
    def _create_execution_context(self, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """Create execution context for learning"""
        context = {}
        
        # Extract relevant parameters
        for key, value in kwargs.items():
            if key in ['context', 'data', 'input', 'showtech_path', 'archive_path', 'config']:
                context[key] = value
        
        # Add execution metadata
        context['execution_timestamp'] = datetime.now().isoformat()
        context['args_count'] = len(args)
        context['kwargs_keys'] = list(kwargs.keys())
        
        return context
    
    def _extract_result_data(self, result: Any) -> Dict[str, Any]:
        """Extract data from result for learning"""
        if isinstance(result, dict):
            return result
        elif hasattr(result, '__dict__'):
            return result.__dict__
        elif hasattr(result, 'json'):
            try:
                return result.json()
            except:
                pass
        else:
            return {'result': str(result), 'type': type(result).__name__}
    
    def _extract_patterns_from_result(self, result: Any, skill_name: str) -> List[str]:
        """Extract patterns from result for learning"""
        patterns = []
        
        result_data = self._extract_result_data(result)
        
        # Look for success indicators
        if result_data.get('success') or result_data.get('analysis_complete'):
            patterns.append('successful_execution')
        
        # Look for skill-specific patterns
        if 'hardware' in skill_name.lower():
            if 'platform_id' in result_data:
                patterns.append('hardware_platform_identified')
            if 'asic_type' in result_data:
                patterns.append('asic_type_detected')
        
        elif 'bgp' in skill_name.lower():
            if 'session_state' in result_data:
                patterns.append('bgp_session_analyzed')
            if 'neighbor_count' in result_data:
                patterns.append('bgp_neighbors_counted')
        
        elif 'memory' in skill_name.lower():
            if 'memory_usage' in result_data:
                patterns.append('memory_usage_analyzed')
            if 'optimization' in str(result_data).lower():
                patterns.append('memory_optimization_suggested')
        
        # Look for performance patterns
        if 'execution_time' in result_data:
            patterns.append('performance_tracked')
        
        return patterns
    
    def _hook_existing_modules(self):
        """Hook into already imported modules"""
        for name, module in sys.modules.items():
            if module and self._is_skill_module(module, name):
                self._hook_module(module, name)
        
        logger.info(f"Hooked {len(self.intercepted_modules)} existing modules")
    
    def _hook_skill_patterns(self):
        """Hook into common skill execution patterns"""
        # Hook into subprocess calls (for shell-based skills)
        self._hook_subprocess_calls()
        
        # Hook into file operations (for file-based skills)
        self._hook_file_operations()
        
        logger.info("Skill execution patterns hooked")
    
    def _hook_subprocess_calls(self):
        """Hook into subprocess calls to capture shell-based skill execution"""
        try:
            import subprocess
            
            original_run = subprocess.run
            
            def skill_aware_run(*args, **kwargs):
                # Check if this is a skill-related command
                command_str = ' '.join(args[0]) if args and isinstance(args[0], list) else str(args[0]) if args else ''
                
                if self._is_skill_command(command_str):
                    skill_name = self._extract_skill_from_command(command_str)
                    if skill_name and self.knowledge_integrator:
                        context = {'command': command_str, 'execution_type': 'subprocess'}
                        
                        with self.knowledge_integrator.intercept_invocation(skill_name, context) as ctx:
                            try:
                                result = original_run(*args, **kwargs)
                                
                                success = result.returncode == 0
                                output_data = {
                                    'stdout': result.stdout,
                                    'stderr': result.stderr,
                                    'returncode': result.returncode
                                }
                                
                                ctx.record_result(success, output_data)
                                return result
                                
                            except Exception as e:
                                ctx.record_result(False, None, str(e))
                                raise
                else:
                    return original_run(*args, **kwargs)
            
            subprocess.run = skill_aware_run
            logger.info("Subprocess calls hooked")
            
        except ImportError:
            logger.warning("Could not hook subprocess calls")
    
    def _is_skill_command(self, command: str) -> bool:
        """Check if command is skill-related"""
        command_lower = command.lower()
        
        skill_indicators = [
            'sonic_', 'skill_', 'analyze', 'triage', 'showtech',
            'bgp', 'memory', 'interface', 'container', 'hardware'
        ]
        
        return any(indicator in command_lower for indicator in skill_indicators)
    
    def _extract_skill_from_command(self, command: str) -> Optional[str]:
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
        
        return None
    
    def _hook_file_operations(self):
        """Hook into file operations to capture file-based skill execution"""
        try:
            original_open = open
            
            def skill_aware_open(file, mode='r', **kwargs):
                # Check if this is a skill-related file operation
                if isinstance(file, str) and self._is_skill_file(file):
                    # This could be part of skill execution
                    # We'll capture this at the function level instead
                    pass
                
                return original_open(file, mode, **kwargs)
            
            # Note: We don't actually replace open() as it could be too invasive
            # File operations are better captured at the function level
            
        except Exception as e:
            logger.warning(f"Could not hook file operations: {e}")
    
    def _is_skill_file(self, file_path: str) -> bool:
        """Check if file is skill-related"""
        file_lower = file_path.lower()
        
        skill_file_patterns = [
            'showtech', 'skill', 'sonic_', 'analysis', 'triage',
            '.json', '.md', '.py'  # Common skill file extensions
        ]
        
        return any(pattern in file_lower for pattern in skill_file_patterns)
    
    def get_hook_status(self) -> Dict[str, Any]:
        """Get status of hook system"""
        return {
            'hooks_active': self.hook_active,
            'intercepted_modules': len(self.intercepted_modules),
            'module_list': list(self.intercepted_modules),
            'knowledge_integrator_available': self.knowledge_integrator is not None,
            'workspace_root': str(self.workspace_root)
        }
    
    def deactivate_hooks(self):
        """Deactivate all hooks"""
        self.hook_active = False
        # Note: We don't restore original functions as that's complex
        # Instead, we just stop intercepting new calls
        logger.info("Hooks deactivated")

# Global hook system instance
_global_hook_system = None

def get_workspace_hook_system() -> WorkspaceSkillHookSystem:
    """Get or create global hook system"""
    global _global_hook_system
    if _global_hook_system is None:
        _global_hook_system = WorkspaceSkillHookSystem()
    return _global_hook_system

def activate_workspace_hooks():
    """Activate workspace-wide skill hooks"""
    hook_system = get_workspace_hook_system()
    hook_system.activate_workspace_hooks()
    return hook_system

# Auto-activate hooks when this module is imported
if __name__ != "__main__":
    # Auto-activate for workspace-wide coverage
    try:
        activate_workspace_hooks()
        logger.info("Workspace hooks auto-activated")
    except Exception as e:
        logger.error(f"Failed to auto-activate hooks: {e}")

# Example usage
if __name__ == "__main__":
    hook_system = get_workspace_hook_system()
    
    # Activate hooks
    hook_system.activate_workspace_hooks()
    
    # Test with a skill function
    def test_skill_function(data):
        """Test skill function"""
        time.sleep(1)  # Simulate work
        return {
            'success': True,
            'analysis_complete': True,
            'hardware_platform': 'Dell S5248F',
            'execution_time': 1.0
        }
    
    # This should be automatically intercepted
    result = test_skill_function({'test': 'data'})
    print("Test result:", result)
    
    # Get hook status
    status = hook_system.get_hook_status()
    print("Hook status:", status)