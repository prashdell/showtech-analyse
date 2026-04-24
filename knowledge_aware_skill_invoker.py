#!/usr/bin/env python3
"""
Enhanced Skill Invoker with Automatic Knowledge Integration
Integrates the automatic knowledge capture system with the enhanced skill invoker
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import the automatic knowledge integrator
from automatic_knowledge_integrator import AutomaticKnowledgeIntegrator, get_global_integrator, auto_integrate

# Import the enhanced skill invoker
from enhanced_skill_invoker import EnhancedSkillInvoker

logger = logging.getLogger(__name__)

class KnowledgeAwareSkillInvoker:
    """Enhanced skill invoker with automatic knowledge integration"""
    
    def __init__(self):
        self.base_invoker = EnhancedSkillInvoker()
        self.knowledge_integrator = get_global_integrator()
        self.workspace_root = Path(r"C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse")
        
        logger.info("Knowledge-Aware Skill Invoker initialized")
    
    def invoke_skill_with_learning(self, skill_name: str, context: Dict[str, Any] = None, 
                                  showtech_path: str = None) -> Dict[str, Any]:
        """
        Invoke skill with automatic knowledge capture and learning
        """
        logger.info(f"Invoking skill with learning: {skill_name}")
        
        # Prepare context for knowledge capture
        learning_context = context or {}
        if showtech_path:
            learning_context['showtech_path'] = showtech_path
        
        # Use the knowledge integrator to intercept the invocation
        with self.knowledge_integrator.intercept_invocation(skill_name, learning_context) as ctx:
            try:
                # Execute the skill using the enhanced invoker
                result = self.base_invoker.invoke_skill(skill_name, context, showtech_path)
                
                # Extract learning data from result
                success = result.get('success', False)
                output_data = result.get('result', {})
                execution_time = result.get('execution_time', 0)
                error_message = result.get('error') if not success else None
                
                # Extract new patterns discovered
                new_patterns = self._extract_new_patterns(output_data, skill_name)
                
                # Record the result for learning
                ctx.record_result(success, output_data, error_message, new_patterns)
                
                # Add learning metadata to result
                result['learning_metadata'] = {
                    'lesson_captured': True,
                    'new_patterns': new_patterns,
                    'execution_time': execution_time,
                    'learning_timestamp': datetime.now().isoformat()
                }
                
                return result
                
            except Exception as e:
                # Record error for learning
                ctx.record_result(False, None, str(e))
                raise
    
    def _extract_new_patterns(self, output_data: Dict[str, Any], skill_name: str) -> List[str]:
        """Extract new patterns discovered during skill execution"""
        patterns = []
        
        # Analyze output data for new patterns
        if isinstance(output_data, dict):
            # Hardware-specific patterns
            if skill_name.lower().startswith('sonic_hardware'):
                if 'platform_id' in output_data:
                    patterns.append(f"platform_identification_{output_data['platform_id']}")
                if 'asic_type' in output_data:
                    patterns.append(f"asic_detection_{output_data['asic_type']}")
                if 'cpu_info' in output_data:
                    patterns.append("cpu_analysis_pattern")
            
            # BGP-specific patterns
            elif 'bgp' in skill_name.lower():
                if 'session_state' in output_data:
                    patterns.append("bgp_session_analysis")
                if 'neighbor_count' in output_data:
                    patterns.append("bgp_neighbor_counting")
                if 'route_analysis' in output_data:
                    patterns.append("bgp_route_analysis")
            
            # Memory-specific patterns
            elif 'memory' in skill_name.lower():
                if 'memory_usage' in output_data:
                    patterns.append("memory_usage_analysis")
                if 'process_memory' in output_data:
                    patterns.append("process_memory_tracking")
                if 'optimization_suggestions' in output_data:
                    patterns.append("memory_optimization_pattern")
            
            # Interface-specific patterns
            elif 'interface' in skill_name.lower():
                if 'port_status' in output_data:
                    patterns.append("interface_status_analysis")
                if 'error_counters' in output_data:
                    patterns.append("interface_error_tracking")
                if 'link_flapping' in output_data:
                    patterns.append("link_flap_detection")
            
            # Container-specific patterns
            elif 'container' in skill_name.lower():
                if 'container_health' in output_data:
                    patterns.append("container_health_monitoring")
                if 'resource_usage' in output_data:
                    patterns.append("container_resource_tracking")
                if 'restart_patterns' in output_data:
                    patterns.append("container_restart_analysis")
            
            # Generic success patterns
            if output_data.get('success') or output_data.get('analysis_complete'):
                patterns.append("successful_execution_pattern")
            
            # Performance patterns
            if 'execution_time' in output_data:
                patterns.append("performance_tracking_pattern")
            
            # Data completeness patterns
            if len(output_data) > 10:  # Rich output
                patterns.append("comprehensive_analysis_pattern")
        
        return patterns
    
    def batch_invoke_with_learning(self, skill_requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Batch invoke multiple skills with learning for each
        """
        results = []
        
        for request in skill_requests:
            skill_name = request.get('skill_name')
            context = request.get('context', {})
            showtech_path = request.get('showtech_path')
            
            result = self.invoke_skill_with_learning(skill_name, context, showtech_path)
            results.append(result)
        
        return results
    
    def get_learning_insights(self, skill_name: str = None) -> Dict[str, Any]:
        """Get learning insights for specific skill or all skills"""
        if skill_name:
            return self._get_skill_learning_insights(skill_name)
        else:
            return self._get_all_learning_insights()
    
    def _get_skill_learning_insights(self, skill_name: str) -> Dict[str, Any]:
        """Get learning insights for specific skill"""
        knowledge_base = self.knowledge_integrator.knowledge_base_dir
        
        # Load pattern data
        patterns_file = knowledge_base / "patterns" / f"{skill_name}_patterns.json"
        patterns = {}
        if patterns_file.exists():
            with open(patterns_file, 'r') as f:
                patterns = json.load(f)
        
        # Load performance data
        perf_file = knowledge_base / "performance" / f"{skill_name}_performance.json"
        performance = {}
        if perf_file.exists():
            with open(perf_file, 'r') as f:
                performance = json.load(f)
        
        # Load recent lessons
        lessons_dir = knowledge_base / "lessons_learned"
        recent_lessons = []
        for lesson_file in lessons_dir.glob(f"*{skill_name}*.json"):
            with open(lesson_file, 'r') as f:
                lesson = json.load(f)
                recent_lessons.append(lesson)
        
        # Sort by timestamp and get recent ones
        recent_lessons.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        recent_lessons = recent_lessons[:5]  # Last 5 lessons
        
        return {
            'skill_name': skill_name,
            'total_patterns': len(patterns),
            'patterns': patterns,
            'performance_stats': performance.get('stats', {}),
            'recent_lessons': recent_lessons,
            'last_updated': datetime.now().isoformat()
        }
    
    def _get_all_learning_insights(self) -> Dict[str, Any]:
        """Get learning insights for all skills"""
        knowledge_base = self.knowledge_integrator.knowledge_base_dir
        
        # Count all patterns
        patterns_dir = knowledge_base / "patterns"
        total_patterns = len(list(patterns_dir.glob('*.json')))
        
        # Count all performance records
        perf_dir = knowledge_base / "performance"
        total_perf_records = len(list(perf_dir.glob('*.json')))
        
        # Count all lessons
        lessons_dir = knowledge_base / "lessons_learned"
        total_lessons = len(list(lessons_dir.glob('*.json')))
        
        # Get skill summary
        skills_summary = {}
        for pattern_file in patterns_dir.glob('*.json'):
            skill_name = pattern_file.stem.replace('_patterns', '')
            skills_summary[skill_name] = self._get_skill_learning_insights(skill_name)
        
        return {
            'total_skills_with_learning': len(skills_summary),
            'total_patterns': total_patterns,
            'total_performance_records': total_perf_records,
            'total_lessons': total_lessons,
            'skills_summary': skills_summary,
            'knowledge_base_status': self.knowledge_integrator.get_knowledge_summary(),
            'last_updated': datetime.now().isoformat()
        }
    
    def generate_learning_report(self) -> str:
        """Generate comprehensive learning report"""
        insights = self.get_learning_insights()
        
        report = f"""
# Skill Learning & Knowledge Integration Report
Generated: {datetime.now().isoformat()}

## Knowledge Base Overview
- Total Skills with Learning: {insights['total_skills_with_learning']}
- Total Patterns Discovered: {insights['total_patterns']}
- Total Performance Records: {insights['total_performance_records']}
- Total Lessons Captured: {insights['total_lessons']}

## Knowledge Base Status
{json.dumps(insights['knowledge_base_status'], indent=2)}

## Skills with Learning Data
"""
        
        for skill_name, skill_insights in insights['skills_summary'].items():
            report += f"""
### {skill_name}
- Patterns: {skill_insights['total_patterns']}
- Recent Lessons: {len(skill_insights['recent_lessons'])}
- Performance Data: {'Available' if skill_insights['performance_stats'] else 'Not Available'}
"""
        
        return report
    
    def apply_learned_optimizations(self, skill_name: str) -> Dict[str, Any]:
        """Apply learned optimizations to skill execution"""
        insights = self._get_skill_learning_insights(skill_name)
        
        optimizations = {
            'applied_optimizations': [],
            'performance_improvements': {},
            'error_prevention': [],
            'pattern_utilization': []
        }
        
        # Apply performance optimizations
        perf_stats = insights.get('performance_stats', {})
        if perf_stats.get('avg_time', 0) > 30:  # Slow execution
            optimizations['performance_improvements']['caching'] = 'Enable result caching'
            optimizations['performance_improvements']['parallel_processing'] = 'Consider parallel execution'
        
        # Apply error prevention
        for lesson in insights.get('recent_lessons', []):
            if lesson.get('lesson_type') == 'error':
                error_pattern = lesson.get('lesson_content', {}).get('error_pattern', '')
                solution = lesson.get('lesson_content', {}).get('solution', '')
                if error_pattern and solution:
                    optimizations['error_prevention'].append({
                        'pattern': error_pattern,
                        'solution': solution
                    })
        
        # Apply pattern utilization
        patterns = insights.get('patterns', {})
        for pattern_name, pattern_data in patterns.items():
            if pattern_data.get('frequency', 0) > 5:  # Frequent pattern
                optimizations['pattern_utilization'].append({
                    'pattern': pattern_name,
                    'confidence': pattern_data.get('confidence', 0),
                    'usage': 'Incorporate into primary analysis path'
                })
        
        return optimizations

# Global knowledge-aware invoker
_global_knowledge_aware_invoker = None

def get_knowledge_aware_invoker() -> KnowledgeAwareSkillInvoker:
    """Get or create global knowledge-aware invoker"""
    global _global_knowledge_aware_invoker
    if _global_knowledge_aware_invoker is None:
        _global_knowledge_aware_invoker = KnowledgeAwareSkillInvoker()
    return _global_knowledge_aware_invoker

# Enhanced decorator for automatic learning
def auto_learn_skill(skill_name: str, context: Dict[str, Any] = None):
    """Enhanced decorator for automatic skill learning"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            invoker = get_knowledge_aware_invoker()
            
            # Extract context from function arguments
            func_context = context or {}
            if 'showtech_path' in kwargs:
                func_context['showtech_path'] = kwargs['showtech_path']
            
            return invoker.invoke_skill_with_learning(skill_name, func_context)
        
        return wrapper
    return decorator

# Example usage
if __name__ == "__main__":
    invoker = get_knowledge_aware_invoker()
    
    # Example invocation with learning
    result = invoker.invoke_skill_with_learning(
        'sonic_hardware_platform_analyzer',
        context={'test_mode': True},
        showtech_path='/path/to/showtech.tar.gz'
    )
    
    print("Learning Result:", result)
    
    # Generate learning report
    print(invoker.generate_learning_report())