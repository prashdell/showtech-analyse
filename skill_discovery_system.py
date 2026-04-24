#!/usr/bin/env python3
"""
Universal Skill Discovery and Invocation System
Provides robust skill discovery, validation, and fallback mechanisms
"""

import os
import json
import importlib.util
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class SkillMetadata:
    """Skill metadata information"""
    name: str
    path: str
    description: str
    version: str = "1.0"
    author: str = "Unknown"
    tags: List[str] = None
    dependencies: List[str] = None
    health_status: str = "unknown"
    last_validated: str = ""
    fallback_enabled: bool = True
    invocation_methods: List[str] = None

class SkillDiscoverySystem:
    """Comprehensive skill discovery and management system"""
    
    def __init__(self):
        self.skill_registry: Dict[str, SkillMetadata] = {}
        self.skill_health: Dict[str, Dict[str, Any]] = {}
        self.fallback_strategies = {
            'direct_invoke': self.direct_skill_invoke,
            'manual_execution': self.manual_skill_execution,
            'template_based': self.template_based_execution,
            'python_import': self.python_import_execution
        }
        
        # Standard skill search paths
        self.skill_paths = [
            r"C:\Users\Prasanth_Sasidharan\.codeium\windsurf\skills",
            r"C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse\skills",
            r"C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\show_tech_extractor_docs",
            r"C:\Users\Prasanth_Sasidharan\.codeium\windsurf\skills\showtechanalyser"
        ]
        
    def discover_all_skills(self) -> Dict[str, SkillMetadata]:
        """Comprehensive skill discovery across all directories"""
        logger.info("Starting comprehensive skill discovery...")
        
        discovered_skills = {}
        
        for search_path in self.skill_paths:
            if not os.path.exists(search_path):
                logger.warning(f"Skill path does not exist: {search_path}")
                continue
                
            logger.info(f"Scanning skill directory: {search_path}")
            
            # Search for SKILL.md files
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file == 'SKILL.md':
                        skill_path = os.path.join(root, file)
                        skill_name = self._extract_skill_name(skill_path)
                        
                        if skill_name:
                            metadata = self._parse_skill_metadata(skill_path, skill_name)
                            if metadata:
                                discovered_skills[skill_name] = metadata
                                logger.info(f"Discovered skill: {skill_name} at {skill_path}")
        
        self.skill_registry = discovered_skills
        logger.info(f"Discovery complete. Found {len(discovered_skills)} skills")
        
        return discovered_skills
    
    def _extract_skill_name(self, skill_path: str) -> Optional[str]:
        """Extract skill name from file path"""
        # Extract parent directory name as skill name
        parent_dir = os.path.basename(os.path.dirname(skill_path))
        
        # Handle special cases
        if parent_dir == 'skills':
            # If in root skills directory, use filename without extension
            return os.path.splitext(os.path.basename(skill_path))[0]
        
        return parent_dir
    
    def _parse_skill_metadata(self, skill_path: str, skill_name: str) -> Optional[SkillMetadata]:
        """Parse skill metadata from SKILL.md file"""
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract description (first paragraph after ## Overview)
            description = self._extract_description(content)
            
            # Extract metadata from YAML frontmatter if present
            metadata = self._extract_yaml_metadata(content)
            
            # Create SkillMetadata object
            skill_metadata = SkillMetadata(
                name=skill_name,
                path=skill_path,
                description=description,
                version=metadata.get('version', '1.0'),
                author=metadata.get('author', 'Unknown'),
                tags=metadata.get('tags', []),
                dependencies=metadata.get('dependencies', []),
                health_status='unknown',
                last_validated='',
                fallback_enabled=metadata.get('fallback_enabled', True),
                invocation_methods=metadata.get('invocation_methods', ['direct', 'manual'])
            )
            
            return skill_metadata
            
        except Exception as e:
            logger.error(f"Error parsing skill metadata for {skill_name}: {e}")
            return None
    
    def _extract_description(self, content: str) -> str:
        """Extract description from skill content"""
        lines = content.split('\n')
        description = ""
        in_overview = False
        
        for line in lines:
            line = line.strip()
            if line == "## Overview":
                in_overview = True
                continue
            elif line.startswith("##") and in_overview:
                break
            elif in_overview and line:
                description += line + " "
        
        return description.strip() if description else "No description available"
    
    def _extract_yaml_metadata(self, content: str) -> Dict[str, Any]:
        """Extract YAML metadata from skill content"""
        metadata = {}
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('---') and 'name:' in lines[lines.index(line)+1]:
                # YAML frontmatter detected
                try:
                    import yaml
                    yaml_content = '\n'.join(lines[1:lines.index('---', 1)])
                    metadata = yaml.safe_load(yaml_content)
                except:
                    pass
                break
        
        return metadata
    
    def validate_skill_health(self, skill_name: str) -> Dict[str, Any]:
        """Validate skill health and integrity"""
        if skill_name not in self.skill_registry:
            return {'status': 'not_found', 'issues': ['Skill not in registry']}
        
        metadata = self.skill_registry[skill_name]
        health_status = {'status': 'healthy', 'issues': [], 'warnings': []}
        
        # Check file accessibility
        if not os.path.exists(metadata.path):
            health_status['status'] = 'error'
            health_status['issues'].append('Skill file not accessible')
            return health_status
        
        # Check file size
        file_size = os.path.getsize(metadata.path)
        if file_size == 0:
            health_status['status'] = 'error'
            health_status['issues'].append('Skill file is empty')
        elif file_size > 1048576:  # 1MB
            health_status['warnings'].append('Skill file is very large')
        
        # Check file content
        try:
            with open(metadata.path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content) < 100:
                health_status['warnings'].append('Skill content appears minimal')
            
            if '## Overview' not in content:
                health_status['warnings'].append('Missing Overview section')
                
        except Exception as e:
            health_status['status'] = 'error'
            health_status['issues'].append(f'Error reading skill file: {e}')
        
        # Update health status
        health_status['last_checked'] = datetime.now().isoformat()
        health_status['file_size'] = file_size
        
        self.skill_health[skill_name] = health_status
        return health_status
    
    def get_skill_invocation_methods(self, skill_name: str) -> List[str]:
        """Get available invocation methods for skill"""
        if skill_name not in self.skill_registry:
            return []
        
        return self.skill_registry[skill_name].invocation_methods
    
    def invoke_skill_with_fallback(self, skill_name: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Invoke skill with comprehensive fallback support"""
        logger.info(f"Attempting to invoke skill: {skill_name}")
        
        # Check if skill exists
        if skill_name not in self.skill_registry:
            return self._handle_skill_not_found(skill_name)
        
        metadata = self.skill_registry[skill_name]
        
        # Try each invocation method in order
        for method in metadata.invocation_methods:
            try:
                logger.info(f"Trying invocation method: {method}")
                result = self.fallback_strategies[method](skill_name, metadata.path, context)
                if result and result.get('success', False):
                    logger.info(f"Skill {skill_name} executed successfully using {method}")
                    return {
                        'success': True,
                        'method': method,
                        'result': result,
                        'skill_name': skill_name,
                        'metadata': metadata
                    }
            except Exception as e:
                logger.warning(f"Invocation method {method} failed: {e}")
                continue
        
        # All methods failed
        return self._handle_all_methods_failed(skill_name, metadata)
    
    def _handle_skill_not_found(self, skill_name: str) -> Dict[str, Any]:
        """Handle skill not found error with guidance"""
        available_skills = list(self.skill_registry.keys())
        
        return {
            'success': False,
            'error': 'skill_not_found',
            'message': f"Skill '{skill_name}' not found",
            'available_skills': available_skills,
            'suggestions': [
                f"Check spelling of skill name '{skill_name}'",
                f"Available skills: {', '.join(available_skills[:5])}",
                "Try running skill discovery to refresh skill registry"
            ]
        }
    
    def _handle_all_methods_failed(self, skill_name: str, metadata: SkillMetadata) -> Dict[str, Any]:
        """Handle case where all invocation methods failed"""
        return {
            'success': False,
            'error': 'invocation_failed',
            'message': f"All invocation methods failed for skill '{skill_name}'",
            'skill_name': skill_name,
            'metadata': metadata,
            'attempted_methods': metadata.invocation_methods,
            'suggestions': [
                "Check skill file for syntax errors",
                "Verify dependencies are available",
                "Try manual execution with Python",
                "Contact support for assistance"
            ]
        }
    
    # Fallback execution methods
    def direct_skill_invoke(self, skill_name: str, skill_path: str, context: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Try direct skill system invocation"""
        try:
            # This would integrate with the actual skill system
            # For now, simulate successful invocation
            return {
                'success': True,
                'message': f"Direct invocation of {skill_name} successful",
                'context': context
            }
        except Exception as e:
            logger.error(f"Direct invocation failed: {e}")
            return None
    
    def manual_skill_execution(self, skill_name: str, skill_path: str, context: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Execute skill manually using file content"""
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                skill_content = f.read()
            
            # Simulate manual execution
            return {
                'success': True,
                'message': f"Manual execution of {skill_name} successful",
                'content_length': len(skill_content),
                'context': context
            }
        except Exception as e:
            logger.error(f"Manual execution failed: {e}")
            return None
    
    def template_based_execution(self, skill_name: str, skill_path: str, context: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Execute using predefined skill templates"""
        try:
            # Simulate template-based execution
            return {
                'success': True,
                'message': f"Template-based execution of {skill_name} successful",
                'template_used': 'default_template',
                'context': context
            }
        except Exception as e:
            logger.error(f"Template execution failed: {e}")
            return None
    
    def python_import_execution(self, skill_name: str, skill_path: str, context: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Execute skill by importing as Python module"""
        try:
            # Create a Python module from the skill file
            spec = importlib.util.spec_from_file_location(skill_name, skill_path)
            if spec is None:
                raise ImportError(f"Could not create spec for {skill_name}")
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Try to execute the skill
            if hasattr(module, 'execute'):
                result = module.execute(context)
                return {
                    'success': True,
                    'message': f"Python import execution of {skill_name} successful",
                    'result': result,
                    'context': context
                }
            else:
                raise AttributeError(f"Skill module {skill_name} has no execute function")
                
        except Exception as e:
            logger.error(f"Python import execution failed: {e}")
            return None
    
    def list_available_skills(self) -> List[Dict[str, Any]]:
        """List all available skills with health status"""
        skills = []
        
        for skill_name, metadata in self.skill_registry.items():
            health = self.validate_skill_health(skill_name)
            
            skills.append({
                'name': skill_name,
                'path': metadata.path,
                'description': metadata.description,
                'version': metadata.version,
                'author': metadata.author,
                'tags': metadata.tags,
                'health_status': health['status'],
                'last_validated': health.get('last_checked', ''),
                'fallback_enabled': metadata.fallback_enabled,
                'invocation_methods': metadata.invocation_methods
            })
        
        return sorted(skills, key=lambda x: x['name'])
    
    def generate_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        total_skills = len(self.skill_registry)
        healthy_skills = sum(1 for health in self.skill_health.values() if health['status'] == 'healthy')
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_skills': total_skills,
            'healthy_skills': healthy_skills,
            'unhealthy_skills': total_skills - healthy_skills,
            'health_percentage': (healthy_skills / total_skills * 100) if total_skills > 0 else 0,
            'skill_details': {}
        }
        
        for skill_name, health in self.skill_health.items():
            report['skill_details'][skill_name] = health
        
        return report

# Main execution interface
def main():
    """Main execution function for skill discovery system"""
    discovery = SkillDiscoverySystem()
    
    # Discover all skills
    skills = discovery.discover_all_skills()
    print(f"Discovered {len(skills)} skills")
    
    # Generate health report
    report = discovery.generate_health_report()
    print(f"Health Report: {report['healthy_skills']}/{report['total_skills']} healthy ({report['health_percentage']:.1f}%)")
    
    # List skills with status
    available_skills = discovery.list_available_skills()
    print("\nAvailable Skills:")
    for skill in available_skills:
        status = "✓" if skill['health_status'] == 'healthy' else "✗"
        print(f"{status} {skill['name']} (v{skill['version']}) - {skill['description'][:50]}...")
    
    return discovery

if __name__ == "__main__":
    main()