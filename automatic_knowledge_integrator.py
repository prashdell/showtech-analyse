#!/usr/bin/env python3
"""
Automatic Knowledge Base Integration System
Captures lessons learned from every skill invocation and automatically updates knowledge base and skill files
"""

import os
import sys
import json
import time
import logging
import hashlib
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from contextlib import contextmanager
import importlib.util
import inspect

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('knowledge_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class InvocationContext:
    """Context information for skill invocation"""
    skill_name: str
    invocation_id: str
    timestamp: datetime
    user_context: Dict[str, Any]
    input_parameters: Dict[str, Any]
    execution_method: str
    caller_info: Dict[str, Any]

@dataclass
class ExecutionResult:
    """Result of skill execution"""
    success: bool
    output_data: Dict[str, Any]
    execution_time: float
    error_message: Optional[str] = None
    performance_metrics: Dict[str, Any] = None
    new_patterns_discovered: List[str] = None

@dataclass
class LessonLearned:
    """Structured lesson learned from invocation"""
    lesson_id: str
    skill_name: str
    invocation_context: InvocationContext
    lesson_type: str  # 'pattern', 'performance', 'error', 'optimization', 'new_insight'
    lesson_content: Dict[str, Any]
    confidence_score: float
    impact_assessment: str  # 'low', 'medium', 'high', 'critical'
    applicable_contexts: List[str]
    timestamp: datetime

class AutomaticKnowledgeIntegrator:
    """Main system for automatic knowledge base integration"""
    
    def __init__(self):
        self.workspace_root = Path(r"C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse")
        self.knowledge_base_dir = self.workspace_root / "knowledge_base"
        self.lessons_dir = self.knowledge_base_dir / "lessons_learned"
        self.patterns_dir = self.knowledge_base_dir / "patterns"
        self.performance_dir = self.knowledge_base_dir / "performance"
        self.skill_updates_dir = self.knowledge_base_dir / "skill_updates"
        
        # Create directories
        for directory in [self.knowledge_base_dir, self.lessons_dir, self.patterns_dir, 
                         self.performance_dir, self.skill_updates_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize tracking systems
        self.invocation_tracker = {}
        self.lesson_queue = []
        self.update_queue = []
        
        # Background processors
        self.lesson_processor = None
        self.skill_updater = None
        
        # Start background processing
        self._start_background_processors()
        
        logger.info("Automatic Knowledge Integrator initialized")
    
    def _start_background_processors(self):
        """Start background threads for lesson processing and skill updates"""
        # Lesson processor thread
        self.lesson_processor = threading.Thread(
            target=self._process_lessons_background,
            daemon=True,
            name="LessonProcessor"
        )
        self.lesson_processor.start()
        
        # Skill updater thread
        self.skill_updater = threading.Thread(
            target=self._update_skills_background,
            daemon=True,
            name="SkillUpdater"
        )
        self.skill_updater.start()
        
        logger.info("Background processors started")
    
    @contextmanager
    def intercept_invocation(self, skill_name: str, context: Dict[str, Any] = None):
        """
        Context manager to intercept skill invocations and capture lessons
        
        Usage:
        with integrator.intercept_invocation('skill_name', context) as ctx:
            result = execute_skill(skill_name, context)
            ctx.record_result(result)
        """
        invocation_id = self._generate_invocation_id(skill_name)
        invocation_context = InvocationContext(
            skill_name=skill_name,
            invocation_id=invocation_id,
            timestamp=datetime.now(),
            user_context=context or {},
            input_parameters=self._extract_input_parameters(),
            execution_method=self._detect_execution_method(),
            caller_info=self._get_caller_info()
        )
        
        # Track invocation
        self.invocation_tracker[invocation_id] = {
            'context': invocation_context,
            'start_time': time.time(),
            'status': 'running'
        }
        
        logger.info(f"Intercepting invocation: {skill_name} (ID: {invocation_id})")
        
        try:
            yield InvocationInterceptor(invocation_context, self)
        except Exception as e:
            # Record error lesson
            self._capture_error_lesson(invocation_context, str(e))
            raise
        finally:
            # Update invocation status
            if invocation_id in self.invocation_tracker:
                self.invocation_tracker[invocation_id]['status'] = 'completed'
    
    def _generate_invocation_id(self, skill_name: str) -> str:
        """Generate unique invocation ID"""
        timestamp = datetime.now().isoformat()
        hash_input = f"{skill_name}_{timestamp}_{os.getpid()}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]
    
    def _extract_input_parameters(self) -> Dict[str, Any]:
        """Extract input parameters from current context"""
        # Try to extract from various sources
        params = {}
        
        # Check for command line arguments
        if len(sys.argv) > 1:
            params['cli_args'] = sys.argv[1:]
        
        # Check environment variables
        skill_env_vars = {k: v for k, v in os.environ.items() 
                         if k.startswith(('SKILL_', 'ANALYSIS_', 'SHOWTECH_'))}
        if skill_env_vars:
            params['env_vars'] = skill_env_vars
        
        return params
    
    def _detect_execution_method(self) -> str:
        """Detect how the skill is being executed"""
        stack = inspect.stack()
        
        # Check execution context
        for frame in stack:
            if 'skill' in frame.filename.lower():
                return 'skill_direct'
            elif 'enhanced_skill_invoker' in frame.filename:
                return 'enhanced_invoker'
            elif 'python' in frame.filename.lower():
                return 'python_import'
            elif 'shell' in frame.filename.lower() or 'terminal' in frame.filename.lower():
                return 'shell_command'
        
        return 'unknown'
    
    def _get_caller_info(self) -> Dict[str, Any]:
        """Get information about the caller"""
        stack = inspect.stack()
        caller_frame = stack[2] if len(stack) > 2 else stack[1]
        
        return {
            'file': caller_frame.filename,
            'line': caller_frame.lineno,
            'function': caller_frame.function,
            'module': inspect.getmodule(caller_frame.frame).__name__ if inspect.getmodule(caller_frame.frame) else 'unknown'
        }
    
    def capture_lesson(self, invocation_context: InvocationContext, result: ExecutionResult):
        """Capture lesson learned from invocation"""
        lesson_id = self._generate_lesson_id(invocation_context)
        
        # Analyze result for lessons
        lessons = self._analyze_execution_for_lessons(invocation_context, result)
        
        for lesson_data in lessons:
            lesson = LessonLearned(
                lesson_id=lesson_id,
                skill_name=invocation_context.skill_name,
                invocation_context=invocation_context,
                lesson_type=lesson_data['type'],
                lesson_content=lesson_data['content'],
                confidence_score=lesson_data['confidence'],
                impact_assessment=lesson_data['impact'],
                applicable_contexts=lesson_data['contexts'],
                timestamp=datetime.now()
            )
            
            # Queue for processing
            self.lesson_queue.append(lesson)
            
            logger.info(f"Captured lesson: {lesson.lesson_type} for {invocation_context.skill_name}")
    
    def _analyze_execution_for_lessons(self, context: InvocationContext, result: ExecutionResult) -> List[Dict[str, Any]]:
        """Analyze execution result to extract lessons"""
        lessons = []
        
        # Performance lessons
        if result.execution_time > 30:  # Slow execution
            lessons.append({
                'type': 'performance',
                'content': {
                    'issue': 'slow_execution',
                    'execution_time': result.execution_time,
                    'suggested_optimization': 'Consider caching or parallel processing'
                },
                'confidence': 0.8,
                'impact': 'medium',
                'contexts': ['large_datasets', 'complex_analysis']
            })
        
        # Success pattern lessons
        if result.success and result.output_data:
            patterns = self._extract_success_patterns(result.output_data)
            if patterns:
                lessons.append({
                    'type': 'pattern',
                    'content': {
                        'success_patterns': patterns,
                        'context_factors': context.user_context
                    },
                    'confidence': 0.9,
                    'impact': 'high',
                    'contexts': ['successful_execution']
                })
        
        # Error lessons
        if not result.success and result.error_message:
            error_lessons = self._analyze_error_for_lessons(result.error_message, context)
            lessons.extend(error_lessons)
        
        # New insight lessons
        if result.new_patterns_discovered:
            lessons.append({
                'type': 'new_insight',
                'content': {
                    'new_patterns': result.new_patterns_discovered,
                    'discovery_context': context.user_context
                },
                'confidence': 0.7,
                'impact': 'high',
                'contexts': ['pattern_discovery']
            })
        
        return lessons
    
    def _extract_success_patterns(self, output_data: Dict[str, Any]) -> List[str]:
        """Extract success patterns from output data"""
        patterns = []
        
        # Look for common success indicators
        if 'analysis_complete' in str(output_data):
            patterns.append('analysis_completion_pattern')
        
        if 'hardware_platform' in str(output_data).lower():
            patterns.append('hardware_identification_pattern')
        
        if 'bgp_session' in str(output_data).lower():
            patterns.append('bgp_analysis_pattern')
        
        # Look for performance patterns
        if 'execution_time' in output_data:
            patterns.append('performance_tracking_pattern')
        
        return patterns
    
    def _analyze_error_for_lessons(self, error_message: str, context: InvocationContext) -> List[Dict[str, Any]]:
        """Analyze errors to extract learning opportunities"""
        lessons = []
        
        # Common error patterns
        if 'file not found' in error_message.lower():
            lessons.append({
                'type': 'error',
                'content': {
                    'error_pattern': 'file_not_found',
                    'solution': 'Add file existence validation',
                    'prevention': 'Pre-check file availability'
                },
                'confidence': 0.9,
                'impact': 'medium',
                'contexts': ['file_operations']
            })
        
        elif 'permission' in error_message.lower():
            lessons.append({
                'type': 'error',
                'content': {
                    'error_pattern': 'permission_denied',
                    'solution': 'Add permission checks',
                    'prevention': 'Validate access rights'
                },
                'confidence': 0.8,
                'impact': 'medium',
                'contexts': ['file_operations', 'system_access']
            })
        
        elif 'timeout' in error_message.lower():
            lessons.append({
                'type': 'performance',
                'content': {
                    'error_pattern': 'execution_timeout',
                    'solution': 'Increase timeout or optimize performance',
                    'prevention': 'Add progress monitoring'
                },
                'confidence': 0.8,
                'impact': 'high',
                'contexts': ['long_running_operations']
            })
        
        return lessons
    
    def _capture_error_lesson(self, context: InvocationContext, error_message: str):
        """Capture lesson from unhandled exception"""
        lesson_id = self._generate_lesson_id(context)
        
        lesson = LessonLearned(
            lesson_id=lesson_id,
            skill_name=context.skill_name,
            invocation_context=context,
            lesson_type='error',
            lesson_content={
                'unhandled_exception': error_message,
                'stack_trace': traceback.format_exc(),
                'recovery_suggestion': 'Add exception handling'
            },
            confidence_score=0.9,
            impact_assessment='high',
            applicable_contexts=['exception_handling'],
            timestamp=datetime.now()
        )
        
        self.lesson_queue.append(lesson)
        logger.error(f"Captured error lesson for {context.skill_name}: {error_message}")
    
    def _generate_lesson_id(self, context: InvocationContext) -> str:
        """Generate unique lesson ID"""
        timestamp = datetime.now().isoformat()
        hash_input = f"{context.skill_name}_{context.invocation_id}_{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:16]
    
    def _process_lessons_background(self):
        """Background thread to process lessons and update knowledge base"""
        while True:
            try:
                if self.lesson_queue:
                    lesson = self.lesson_queue.pop(0)
                    self._process_lesson(lesson)
                else:
                    time.sleep(1)  # Wait for new lessons
            except Exception as e:
                logger.error(f"Error in lesson processor: {e}")
                time.sleep(5)
    
    def _process_lesson(self, lesson: LessonLearned):
        """Process individual lesson and update knowledge base"""
        try:
            # Store lesson in knowledge base
            lesson_file = self.lessons_dir / f"{lesson.lesson_id}.json"
            with open(lesson_file, 'w') as f:
                json.dump(asdict(lesson), f, indent=2, default=str)
            
            # Update pattern database
            if lesson.lesson_type == 'pattern':
                self._update_pattern_database(lesson)
            
            # Update performance database
            if lesson.lesson_type == 'performance':
                self._update_performance_database(lesson)
            
            # Queue skill update
            self.update_queue.append({
                'lesson': lesson,
                'timestamp': datetime.now()
            })
            
            logger.info(f"Processed lesson: {lesson.lesson_type} for {lesson.skill_name}")
            
        except Exception as e:
            logger.error(f"Error processing lesson {lesson.lesson_id}: {e}")
    
    def _update_pattern_database(self, lesson: LessonLearned):
        """Update pattern database with new patterns"""
        pattern_file = self.patterns_dir / f"{lesson.skill_name}_patterns.json"
        
        # Load existing patterns
        patterns = {}
        if pattern_file.exists():
            with open(pattern_file, 'r') as f:
                patterns = json.load(f)
        
        # Add new patterns
        new_patterns = lesson.lesson_content.get('success_patterns', [])
        for pattern in new_patterns:
            if pattern not in patterns:
                patterns[pattern] = {
                    'first_seen': lesson.timestamp.isoformat(),
                    'frequency': 1,
                    'confidence': lesson.confidence_score,
                    'contexts': lesson.applicable_contexts
                }
            else:
                patterns[pattern]['frequency'] += 1
                patterns[pattern]['last_seen'] = lesson.timestamp.isoformat()
        
        # Save updated patterns
        with open(pattern_file, 'w') as f:
            json.dump(patterns, f, indent=2, default=str)
    
    def _update_performance_database(self, lesson: LessonLearned):
        """Update performance database with performance insights"""
        perf_file = self.performance_dir / f"{lesson.skill_name}_performance.json"
        
        # Load existing performance data
        perf_data = {}
        if perf_file.exists():
            with open(perf_file, 'r') as f:
                perf_data = json.load(f)
        
        # Add performance data
        execution_time = lesson.lesson_content.get('execution_time', 0)
        if execution_time > 0:
            if 'execution_times' not in perf_data:
                perf_data['execution_times'] = []
            
            perf_data['execution_times'].append({
                'timestamp': lesson.timestamp.isoformat(),
                'execution_time': execution_time,
                'context': lesson.applicable_contexts
            })
            
            # Calculate statistics
            times = [entry['execution_time'] for entry in perf_data['execution_times']]
            perf_data['stats'] = {
                'avg_time': sum(times) / len(times),
                'min_time': min(times),
                'max_time': max(times),
                'total_executions': len(times)
            }
        
        # Save updated performance data
        with open(perf_file, 'w') as f:
            json.dump(perf_data, f, indent=2, default=str)
    
    def _update_skills_background(self):
        """Background thread to update skill files based on lessons"""
        while True:
            try:
                if self.update_queue:
                    update_request = self.update_queue.pop(0)
                    self._update_skill_file(update_request['lesson'])
                else:
                    time.sleep(2)  # Wait for new updates
            except Exception as e:
                logger.error(f"Error in skill updater: {e}")
                time.sleep(5)
    
    def _update_skill_file(self, lesson: LessonLearned):
        """Update skill file based on lesson learned"""
        try:
            skill_file = self._find_skill_file(lesson.skill_name)
            if not skill_file:
                logger.warning(f"Skill file not found for {lesson.skill_name}")
                return
            
            # Read current skill content
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply updates based on lesson type
            updated_content = self._apply_lesson_to_skill(content, lesson)
            
            if updated_content != content:
                # Create backup
                backup_file = skill_file.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Write updated content
                with open(skill_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                logger.info(f"Updated skill file: {skill_file}")
            
            # Record update
            update_record = {
                'lesson_id': lesson.lesson_id,
                'skill_name': lesson.skill_name,
                'update_type': lesson.lesson_type,
                'timestamp': datetime.now().isoformat(),
                'backup_file': str(backup_file)
            }
            
            update_file = self.skill_updates_dir / f"{lesson.lesson_id}_update.json"
            with open(update_file, 'w') as f:
                json.dump(update_record, f, indent=2, default=str)
            
        except Exception as e:
            logger.error(f"Error updating skill file for {lesson.skill_name}: {e}")
    
    def _find_skill_file(self, skill_name: str) -> Optional[Path]:
        """Find skill file in the workspace"""
        search_paths = [
            self.workspace_root / "skills",
            self.workspace_root / "skills" / "showtechanalyser",
            self.workspace_root / "skills" / "jira_snc_intelligence_scrubber"
        ]
        
        for search_path in search_paths:
            skill_dir = search_path / skill_name
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                return skill_file
        
        return None
    
    def _apply_lesson_to_skill(self, content: str, lesson: LessonLearned) -> str:
        """Apply lesson learned to skill content"""
        updated_content = content
        
        if lesson.lesson_type == 'pattern':
            updated_content = self._add_pattern_insights(updated_content, lesson)
        elif lesson.lesson_type == 'performance':
            updated_content = self._add_performance_insights(updated_content, lesson)
        elif lesson.lesson_type == 'error':
            updated_content = self._add_error_handling(updated_content, lesson)
        elif lesson.lesson_type == 'new_insight':
            updated_content = self._add_new_insights(updated_content, lesson)
        
        return updated_content
    
    def _add_pattern_insights(self, content: str, lesson: LessonLearned) -> str:
        """Add pattern insights to skill content"""
        patterns = lesson.lesson_content.get('success_patterns', [])
        
        # Add to "Known Patterns" section or create new one
        if "## Known Patterns" not in content:
            content += "\n\n## Known Patterns\n"
            content += "### Success Patterns Identified\n"
        
        for pattern in patterns:
            pattern_text = f"- **{pattern}**: Discovered in {lesson.timestamp.strftime('%Y-%m-%d')} with {lesson.confidence_score:.1f} confidence\n"
            if pattern_text not in content:
                content += pattern_text
        
        return content
    
    def _add_performance_insights(self, content: str, lesson: LessonLearned) -> str:
        """Add performance insights to skill content"""
        execution_time = lesson.lesson_content.get('execution_time', 0)
        if execution_time > 0:
            # Add performance insights
            if "## Performance Insights" not in content:
                content += "\n\n## Performance Insights\n"
                content += "### Execution Time Analysis\n"
            
            perf_text = f"- **Average Execution Time**: {execution_time:.2f}s (Recorded: {lesson.timestamp.strftime('%Y-%m-%d')})\n"
            if perf_text not in content:
                content += perf_text
        
        return content
    
    def _add_error_handling(self, content: str, lesson: LessonLearned) -> str:
        """Add error handling insights to skill content"""
        error_pattern = lesson.lesson_content.get('error_pattern', '')
        solution = lesson.lesson_content.get('solution', '')
        
        if error_pattern and solution:
            # Add error handling section
            if "## Error Handling" not in content:
                content += "\n\n## Error Handling\n"
                content += "### Known Issues and Solutions\n"
            
            error_text = f"- **{error_pattern}**: {solution} (Added: {lesson.timestamp.strftime('%Y-%m-%d')})\n"
            if error_text not in content:
                content += error_text
        
        return content
    
    def _add_new_insights(self, content: str, lesson: LessonLearned) -> str:
        """Add new insights to skill content"""
        new_patterns = lesson.lesson_content.get('new_patterns', [])
        
        if new_patterns:
            # Add new insights section
            if "## Recent Insights" not in content:
                content += "\n\n## Recent Insights\n"
                content += "### Newly Discovered Patterns\n"
            
            for pattern in new_patterns:
                insight_text = f"- **{pattern}**: Discovered {lesson.timestamp.strftime('%Y-%m-%d')} (Confidence: {lesson.confidence_score:.1f})\n"
                if insight_text not in content:
                    content += insight_text
        
        return content
    
    def get_knowledge_summary(self) -> Dict[str, Any]:
        """Get summary of knowledge base status"""
        summary = {
            'total_lessons': len(list(self.lessons_dir.glob('*.json'))),
            'skills_with_patterns': len(list(self.patterns_dir.glob('*.json'))),
            'skills_with_performance_data': len(list(self.performance_dir.glob('*.json'))),
            'total_skill_updates': len(list(self.skill_updates_dir.glob('*.json'))),
            'pending_lessons': len(self.lesson_queue),
            'pending_updates': len(self.update_queue),
            'active_invocations': len([i for i in self.invocation_tracker.values() if i['status'] == 'running'])
        }
        
        return summary
    
    def generate_integration_report(self) -> str:
        """Generate comprehensive integration report"""
        summary = self.get_knowledge_summary()
        
        report = f"""
# Automatic Knowledge Integration Report
Generated: {datetime.now().isoformat()}

## Knowledge Base Status
- Total Lessons Captured: {summary['total_lessons']}
- Skills with Pattern Data: {summary['skills_with_patterns']}
- Skills with Performance Data: {summary['skills_with_performance_data']}
- Total Skill Updates Applied: {summary['total_skill_updates']}

## Queue Status
- Pending Lessons: {summary['pending_lessons']}
- Pending Skill Updates: {summary['pending_updates']}
- Active Invocations: {summary['active_invocations']}

## System Health
- Background Processors: {'Running' if self.lesson_processor.is_alive() else 'Stopped'}
- Skill Updater: {'Running' if self.skill_updater.is_alive() else 'Stopped'}
- Knowledge Base Directory: {self.knowledge_base_dir}
"""
        
        return report

class InvocationInterceptor:
    """Helper class for intercepting invocations"""
    
    def __init__(self, context: InvocationContext, integrator: AutomaticKnowledgeIntegrator):
        self.context = context
        self.integrator = integrator
        self.start_time = time.time()
    
    def record_result(self, success: bool, output_data: Dict[str, Any] = None, 
                     error_message: str = None, new_patterns: List[str] = None):
        """Record execution result for lesson capture"""
        execution_time = time.time() - self.start_time
        
        result = ExecutionResult(
            success=success,
            output_data=output_data or {},
            execution_time=execution_time,
            error_message=error_message,
            new_patterns_discovered=new_patterns or []
        )
        
        # Capture lesson
        self.integrator.capture_lesson(self.context, result)

# Global integrator instance
_global_integrator = None

def get_global_integrator() -> AutomaticKnowledgeIntegrator:
    """Get or create global integrator instance"""
    global _global_integrator
    if _global_integrator is None:
        _global_integrator = AutomaticKnowledgeIntegrator()
    return _global_integrator

def auto_integrate(skill_name: str, context: Dict[str, Any] = None):
    """Decorator for automatic integration"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            integrator = get_global_integrator()
            
            with integrator.intercept_invocation(skill_name, context) as ctx:
                try:
                    result = func(*args, **kwargs)
                    
                    # Extract result data
                    success = True
                    output_data = result if isinstance(result, dict) else {'result': result}
                    new_patterns = output_data.get('new_patterns', [])
                    
                    ctx.record_result(success, output_data, None, new_patterns)
                    return result
                    
                except Exception as e:
                    ctx.record_result(False, None, str(e))
                    raise
        
        return wrapper
    return decorator

# Example usage
if __name__ == "__main__":
    integrator = get_global_integrator()
    
    # Example skill execution with automatic integration
    @auto_integrate("example_skill", {"test": True})
    def example_skill_execution():
        time.sleep(2)  # Simulate work
        return {
            "analysis_complete": True,
            "hardware_platform": "Dell S5248F",
            "execution_time": 2.0
        }
    
    # Execute skill
    result = example_skill_execution()
    
    # Generate report
    print(integrator.generate_integration_report())