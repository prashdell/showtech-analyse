#!/usr/bin/env python3
"""
Optimized Background Processing System
Fixes background processing issues and provides efficient knowledge capture and skill updates
"""

import os
import sys
import json
import logging
import threading
import time
import queue
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('optimized_background_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ProcessingTask:
    """Represents a background processing task"""
    task_id: str
    task_type: str  # 'lesson_processing', 'skill_update', 'pattern_analysis', 'performance_tracking'
    priority: int  # 1=high, 2=medium, 3=low
    data: Dict[str, Any]
    created_at: datetime
    retry_count: int = 0
    max_retries: int = 3

class OptimizedBackgroundProcessor:
    """Optimized background processing system with efficient task management"""
    
    def __init__(self):
        self.workspace_root = Path(r"C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse")
        self.knowledge_base_dir = self.workspace_root / "knowledge_base"
        
        # Ensure knowledge base directories exist
        for subdir in ['lessons_learned', 'patterns', 'performance', 'skill_updates', 'processing_stats']:
            (self.knowledge_base_dir / subdir).mkdir(parents=True, exist_ok=True)
        
        # Task queues with priority
        self.task_queues = {
            'high': queue.PriorityQueue(),
            'medium': queue.PriorityQueue(),
            'low': queue.PriorityQueue()
        }
        
        # Thread pool for parallel processing
        self.executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="BackgroundProcessor")
        
        # Processing statistics
        self.processing_stats = {
            'tasks_processed': 0,
            'tasks_failed': 0,
            'tasks_retried': 0,
            'avg_processing_time': 0.0,
            'last_processed': None,
            'processing_rates': {
                'lessons_per_hour': 0,
                'updates_per_hour': 0,
                'patterns_per_hour': 0
            }
        }
        
        # Performance tracking
        self.performance_metrics = {
            'lesson_processing_times': [],
            'skill_update_times': [],
            'pattern_analysis_times': []
        }
        
        # Background workers
        self.workers = []
        self.monitor_thread = None
        self.stats_thread = None
        
        # System status
        self.system_active = True
        self.last_health_check = datetime.now()
        
        logger.info("Optimized Background Processor initialized")
    
    def start_processing(self):
        """Start the optimized background processing system"""
        if self.system_active:
            logger.warning("Background processor already active")
            return
        
        self.system_active = True
        
        # Start worker threads
        self._start_worker_threads()
        
        # Start monitoring thread
        self._start_monitoring_thread()
        
        # Start statistics thread
        self._start_statistics_thread()
        
        logger.info("Optimized background processing started")
    
    def _start_worker_threads(self):
        """Start worker threads for parallel processing"""
        for i in range(3):  # 3 worker threads
            worker = threading.Thread(
                target=self._worker_loop,
                args=(f"Worker-{i+1}",),
                daemon=True,
                name=f"BackgroundWorker-{i+1}"
            )
            worker.start()
            self.workers.append(worker)
        
        logger.info(f"Started {len(self.workers)} worker threads")
    
    def _worker_loop(self, worker_name: str):
        """Main worker loop for processing tasks"""
        logger.info(f"{worker_name} started")
        
        while self.system_active:
            try:
                # Get next task (high priority first)
                task = self._get_next_task()
                
                if task is None:
                    time.sleep(1)  # No tasks, wait
                    continue
                
                # Process task
                start_time = time.time()
                success = self._process_task(task)
                processing_time = time.time() - start_time
                
                # Update statistics
                self._update_processing_stats(task, success, processing_time)
                
                if success:
                    logger.info(f"{worker_name} processed {task.task_type} task {task.task_id}")
                else:
                    logger.warning(f"{worker_name} failed to process {task.task_type} task {task.task_id}")
                
            except Exception as e:
                logger.error(f"Error in {worker_name}: {e}")
                time.sleep(5)  # Wait before retrying
        
        logger.info(f"{worker_name} stopped")
    
    def _get_next_task(self) -> Optional[ProcessingTask]:
        """Get next task based on priority"""
        # Check queues in priority order
        for priority_name in ['high', 'medium', 'low']:
            queue = self.task_queues[priority_name]
            if not queue.empty():
                return queue.get()
        
        return None
    
    def _process_task(self, task: ProcessingTask) -> bool:
        """Process individual task"""
        try:
            if task.task_type == 'lesson_processing':
                return self._process_lesson_task(task)
            elif task.task_type == 'skill_update':
                return self._process_skill_update_task(task)
            elif task.task_type == 'pattern_analysis':
                return self._process_pattern_analysis_task(task)
            elif task.task_type == 'performance_tracking':
                return self._process_performance_tracking_task(task)
            else:
                logger.warning(f"Unknown task type: {task.task_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error processing task {task.task_id}: {e}")
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                self._queue_task(task)  # Re-queue for retry
                self.processing_stats['tasks_retried'] += 1
                logger.info(f"Retrying task {task.task_id} (attempt {task.retry_count})")
                return False
            else:
                logger.error(f"Task {task.task_id} failed after {task.max_retries} retries")
                self.processing_stats['tasks_failed'] += 1
                return False
    
    def _process_lesson_task(self, task: ProcessingTask) -> bool:
        """Process lesson capture task"""
        start_time = time.time()
        
        lesson_data = task.data
        
        # Generate lesson ID
        lesson_id = f"lesson_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(str(lesson_data).encode()).hexdigest()[:8]}"
        
        # Store lesson in knowledge base
        lesson_file = self.knowledge_base_dir / "lessons_learned" / f"{lesson_id}.json"
        
        lesson_with_metadata = {
            'lesson_id': lesson_id,
            'task_id': task.task_id,
            'timestamp': datetime.now().isoformat(),
            'processing_time': time.time() - start_time,
            'processed_by': 'optimized_background_processor',
            **lesson_data
        }
        
        with open(lesson_file, 'w') as f:
            json.dump(lesson_with_metadata, f, indent=2, default=str)
        
        # Update pattern database if needed
        if lesson_data.get('lesson_type') == 'pattern':
            self._update_pattern_database_optimized(lesson_data)
        
        # Update performance database if needed
        if lesson_data.get('lesson_type') == 'performance':
            self._update_performance_database_optimized(lesson_data)
        
        # Track processing time
        self.performance_metrics['lesson_processing_times'].append(time.time() - start_time)
        
        return True
    
    def _process_skill_update_task(self, task: ProcessingTask) -> bool:
        """Process skill update task"""
        start_time = time.time()
        
        update_data = task.data
        skill_name = update_data.get('skill_name')
        pattern = update_data.get('pattern')
        
        if not skill_name or not pattern:
            logger.warning(f"Invalid skill update task: missing skill_name or pattern")
            return False
        
        # Find skill file
        skill_file = self._find_skill_file_optimized(skill_name)
        if not skill_file:
            logger.warning(f"Skill file not found for {skill_name}")
            return False
        
        # Read current content
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add pattern to skill content
        updated_content = self._add_pattern_to_skill_content_optimized(content, pattern, update_data)
        
        if updated_content != content:
            # Create backup
            backup_file = skill_file.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Write updated content
            with open(skill_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            # Record update
            update_record = {
                'task_id': task.task_id,
                'skill_name': skill_name,
                'pattern': pattern,
                'timestamp': datetime.now().isoformat(),
                'backup_file': str(backup_file),
                'processing_time': time.time() - start_time,
                'processed_by': 'optimized_background_processor'
            }
            
            update_file = self.knowledge_base_dir / "skill_updates" / f"pattern_update_{pattern}_{task.task_id}.json"
            with open(update_file, 'w') as f:
                json.dump(update_record, f, indent=2, default=str)
            
            logger.info(f"Updated skill file {skill_name} with pattern {pattern}")
        
        # Track processing time
        self.performance_metrics['skill_update_times'].append(time.time() - start_time)
        
        return True
    
    def _process_pattern_analysis_task(self, task: ProcessingTask) -> bool:
        """Process pattern analysis task"""
        start_time = time.time()
        
        analysis_data = task.data
        
        # Load existing patterns
        pattern_file = self.knowledge_base_dir / "patterns" / "skill_patterns.json"
        patterns_db = {}
        
        if pattern_file.exists():
            with open(pattern_file, 'r') as f:
                patterns_db = json.load(f)
        
        # Analyze patterns
        analysis_result = self._analyze_patterns_optimized(patterns_db, analysis_data)
        
        # Store analysis result
        analysis_file = self.knowledge_base_dir / "patterns" / f"pattern_analysis_{task.task_id}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis_result, f, indent=2, default=str)
        
        # Track processing time
        self.performance_metrics['pattern_analysis_times'].append(time.time() - start_time)
        
        return True
    
    def _process_performance_tracking_task(self, task: ProcessingTask) -> bool:
        """Process performance tracking task"""
        start_time = time.time()
        
        tracking_data = task.data
        
        # Generate performance report
        performance_report = self._generate_performance_report_optimized(tracking_data)
        
        # Store performance report
        report_file = self.knowledge_base_dir / "performance" / f"performance_report_{task.task_id}.json"
        with open(report_file, 'w') as f:
            json.dump(performance_report, f, indent=2, default=str)
        
        # Track processing time
        self.performance_metrics['performance_tracking_times'].append(time.time() - start_time)
        
        return True
    
    def _update_pattern_database_optimized(self, lesson_data: Dict[str, Any]):
        """Optimized pattern database update"""
        patterns = lesson_data.get('content', {}).get('success_patterns', [])
        if not patterns:
            return
        
        pattern_file = self.knowledge_base_dir / "patterns" / "skill_patterns.json"
        
        # Load existing patterns with file locking
        patterns_db = {}
        if pattern_file.exists():
            with open(pattern_file, 'r') as f:
                patterns_db = json.load(f)
        
        # Update patterns efficiently
        current_time = datetime.now().isoformat()
        for pattern in patterns:
            if pattern not in patterns_db:
                patterns_db[pattern] = {
                    'first_seen': current_time,
                    'frequency': 1,
                    'confidence': lesson_data.get('confidence', 0.8),
                    'skill_types': [lesson_data.get('lesson_type', 'unknown')],
                    'last_updated': current_time
                }
            else:
                patterns_db[pattern]['frequency'] += 1
                patterns_db[pattern]['last_updated'] = current_time
                if lesson_data.get('lesson_type') not in patterns_db[pattern]['skill_types']:
                    patterns_db[pattern]['skill_types'].append(lesson_data.get('lesson_type', 'unknown'))
        
        # Save updated patterns
        with open(pattern_file, 'w') as f:
            json.dump(patterns_db, f, indent=2, default=str)
    
    def _update_performance_database_optimized(self, lesson_data: Dict[str, Any]):
        """Optimized performance database update"""
        execution_time = lesson_data.get('content', {}).get('execution_time', 0)
        if execution_time <= 0:
            return
        
        perf_file = self.knowledge_base_dir / "performance" / "skill_performance.json"
        
        # Load existing performance data
        perf_db = {}
        if perf_file.exists():
            with open(perf_file, 'r') as f:
                perf_db = json.load(f)
        
        # Determine skill name
        skill_name = lesson_data.get('skill_name', 'unknown_skill')
        
        # Update performance data
        if skill_name not in perf_db:
            perf_db[skill_name] = {
                'execution_times': [],
                'total_executions': 0,
                'avg_time': 0,
                'max_time': 0,
                'min_time': float('inf'),
                'last_updated': datetime.now().isoformat()
            }
        
        perf_db[skill_name]['execution_times'].append({
            'timestamp': datetime.now().isoformat(),
            'execution_time': execution_time,
            'lesson_id': lesson_data.get('lesson_id', 'unknown')
        })
        perf_db[skill_name]['total_executions'] += 1
        perf_db[skill_name]['last_updated'] = datetime.now().isoformat()
        
        # Update statistics
        times = [entry['execution_time'] for entry in perf_db[skill_name]['execution_times']]
        perf_db[skill_name]['avg_time'] = sum(times) / len(times)
        perf_db[skill_name]['max_time'] = max(times)
        perf_db[skill_name]['min_time'] = min(times)
        
        # Save updated performance data
        with open(perf_file, 'w') as f:
            json.dump(perf_db, f, indent=2, default=str)
    
    def _analyze_patterns_optimized(self, patterns_db: Dict[str, Any], analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimized pattern analysis"""
        analysis_result = {
            'analysis_id': analysis_data.get('task_id', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'total_patterns': len(patterns_db),
            'high_frequency_patterns': [],
            'high_confidence_patterns': [],
            'pattern_correlations': {},
            'recommendations': []
        }
        
        # Analyze patterns
        for pattern, data in patterns_db.items():
            if data['frequency'] >= 5:
                analysis_result['high_frequency_patterns'].append({
                    'pattern': pattern,
                    'frequency': data['frequency'],
                    'confidence': data['confidence']
                })
            
            if data['confidence'] >= 0.9:
                analysis_result['high_confidence_patterns'].append({
                    'pattern': pattern,
                    'confidence': data['confidence'],
                    'frequency': data['frequency']
                })
        
        # Generate recommendations
        if len(analysis_result['high_frequency_patterns']) > 10:
            analysis_result['recommendations'].append("Consider creating specialized skills for high-frequency patterns")
        
        if len(analysis_result['high_confidence_patterns']) > 5:
            analysis_result['recommendations'].append("High-confidence patterns should be prioritized for skill updates")
        
        return analysis_result
    
    def _generate_performance_report_optimized(self, tracking_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimized performance report"""
        report = {
            'report_id': tracking_data.get('task_id', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'system_performance': self._get_system_performance_metrics(),
            'processing_performance': self._get_processing_performance_metrics(),
            'recommendations': []
        }
        
        # Generate recommendations
        if report['processing_performance']['avg_processing_time'] > 5.0:
            report['recommendations'].append("Consider optimizing processing algorithms for better performance")
        
        if report['system_performance']['memory_usage'] > 80:
            report['recommendations'].append("High memory usage detected - consider memory optimization")
        
        return report
    
    def _get_system_performance_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        import psutil
        
        return {
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'active_threads': threading.active_count(),
            'task_queue_sizes': {
                'high': self.task_queues['high'].qsize(),
                'medium': self.task_queues['medium'].qsize(),
                'low': self.task_queues['low'].qsize()
            }
        }
    
    def _get_processing_performance_metrics(self) -> Dict[str, Any]:
        """Get processing performance metrics"""
        all_times = (
            self.performance_metrics['lesson_processing_times'] +
            self.performance_metrics['skill_update_times'] +
            self.performance_metrics['pattern_analysis_times'] +
            self.performance_metrics['performance_tracking_times']
        )
        
        if all_times:
            return {
                'avg_processing_time': sum(all_times) / len(all_times),
                'min_processing_time': min(all_times),
                'max_processing_time': max(all_times),
                'total_processed': len(all_times)
            }
        else:
            return {
                'avg_processing_time': 0.0,
                'min_processing_time': 0.0,
                'max_processing_time': 0.0,
                'total_processed': 0
            }
    
    def _find_skill_file_optimized(self, skill_name: str) -> Optional[Path]:
        """Optimized skill file finding"""
        search_paths = [
            self.workspace_root / "skills",
            self.workspace_root / "skills" / "showtechanalyser",
            self.workspace_root / "skills" / "jira_snc_intelligence_scrubber"
        ]
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
            
            # Direct skill directory search
            skill_dir = search_path / skill_name
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                return skill_file
            
            # Subdirectory search
            for item in search_path.iterdir():
                if item.is_dir() and item.name == skill_name:
                    skill_file = item / "SKILL.md"
                    if skill_file.exists():
                        return skill_file
        
        return None
    
    def _add_pattern_to_skill_content_optimized(self, content: str, pattern: str, pattern_data: Dict[str, Any]) -> str:
        """Optimized pattern addition to skill content"""
        # Look for existing patterns section
        if "## Known Patterns" in content:
            # Add to existing section
            section_end = content.find("##", content.find("## Known Patterns") + 1)
            if section_end == -1:
                section_end = len(content)
            
            before_section = content[:section_end]
            after_section = content[section_end:]
            
            # Add new pattern
            pattern_text = f"- **{pattern}**: Frequency: {pattern_data.get('frequency', 1)}, Confidence: {pattern_data.get('confidence', 0.8):.1f} (Added: {datetime.now().strftime('%Y-%m-%d')})\n"
            
            updated = before_section + "\n" + pattern_text + after_section
        else:
            # Add new section before Source Files
            if "## Source Files" in content:
                insert_pos = content.find("## Source Files")
                updated = content[:insert_pos] + f"\n## Known Patterns\n\n### Success Patterns Identified\n- **{pattern}**: Frequency: {pattern_data.get('frequency', 1)}, Confidence: {pattern_data.get('confidence', 0.8):.1f} (Added: {datetime.now().strftime('%Y-%m-%d')})\n\n" + content[insert_pos:]
            else:
                updated = content + f"\n\n## Known Patterns\n\n### Success Patterns Identified\n- **{pattern}**: Frequency: {pattern_data.get('frequency', 1)}, Confidence: {pattern_data.get('confidence', 0.8):.1f} (Added: {datetime.now().strftime('%Y-%m-%d')})\n"
        
        return updated
    
    def _update_processing_stats(self, task: ProcessingTask, success: bool, processing_time: float):
        """Update processing statistics"""
        self.processing_stats['tasks_processed'] += 1
        self.processing_stats['last_processed'] = datetime.now().isoformat()
        
        if not success:
            self.processing_stats['tasks_failed'] += 1
        
        # Update average processing time
        if self.processing_stats['tasks_processed'] > 0:
            # Simple moving average
            current_avg = self.processing_stats['avg_processing_time']
            new_avg = ((current_avg * (self.processing_stats['tasks_processed'] - 1)) + processing_time) / self.processing_stats['tasks_processed']
            self.processing_stats['avg_processing_time'] = new_avg
    
    def _start_monitoring_thread(self):
        """Start monitoring thread"""
        def monitor_system():
            while self.system_active:
                try:
                    # Health check
                    self._perform_health_check()
                    
                    # Task queue monitoring
                    self._monitor_task_queues()
                    
                    # Performance monitoring
                    self._monitor_performance()
                    
                    time.sleep(30)  # Monitor every 30 seconds
                    
                except Exception as e:
                    logger.error(f"Error in monitoring thread: {e}")
                    time.sleep(60)
        
        monitor_thread = threading.Thread(target=monitor_system, daemon=True, name="SystemMonitor")
        monitor_thread.start()
    
    def _start_statistics_thread(self):
        """Start statistics thread"""
        def update_statistics():
            while self.system_active:
                try:
                    # Update processing rates
                    self._update_processing_rates()
                    
                    # Generate statistics report
                    self._generate_statistics_report()
                    
                    time.sleep(300)  # Update every 5 minutes
                    
                except Exception as e:
                    logger.error(f"Error in statistics thread: {e}")
                    time.sleep(300)
        
        stats_thread = threading.Thread(target=update_statistics, daemon=True, name="StatisticsUpdater")
        stats_thread.start()
    
    def _perform_health_check(self):
        """Perform system health check"""
        self.last_health_check = datetime.now()
        
        # Check thread health
        active_workers = sum(1 for worker in self.workers if worker.is_alive())
        if active_workers < len(self.workers):
            logger.warning(f"Only {active_workers}/{len(self.workers)} workers active")
        
        # Check queue sizes
        total_queued = sum(queue.qsize() for queue in self.task_queues.values())
        if total_queued > 100:
            logger.warning(f"High queue size: {total_queued} tasks queued")
        
        # Check system resources
        import psutil
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        
        if cpu_percent > 90:
            logger.warning(f"High CPU usage: {cpu_percent}%")
        
        if memory_percent > 90:
            logger.warning(f"High memory usage: {memory_percent}%")
    
    def _monitor_task_queues(self):
        """Monitor task queue sizes"""
        queue_sizes = {
            'high': self.task_queues['high'].qsize(),
            'medium': self.task_queues['medium'].qsize(),
            'low': self.task_queues['low'].qsize()
        }
        
        # Store queue statistics
        queue_stats_file = self.knowledge_base_dir / "processing_stats" / "queue_sizes.json"
        with open(queue_stats_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'queue_sizes': queue_sizes,
                'total_queued': sum(queue_sizes.values())
            }, f, indent=2, default=str)
    
    def _monitor_performance(self):
        """Monitor system performance"""
        performance_data = {
            'timestamp': datetime.now().isoformat(),
            'processing_stats': self.processing_stats,
            'performance_metrics': self._get_processing_performance_metrics(),
            'system_metrics': self._get_system_performance_metrics()
        }
        
        # Store performance data
        perf_file = self.knowledge_base_dir / "processing_stats" / "performance_monitoring.json"
        with open(perf_file, 'w') as f:
            json.dump(performance_data, f, indent=2, default=str)
    
    def _update_processing_rates(self):
        """Update processing rates"""
        # Calculate rates per hour
        current_time = datetime.now()
        
        # Get recent tasks (last hour)
        recent_tasks = []
        for subdir in ['lessons_learned', 'skill_updates', 'patterns', 'performance']:
            subdir_path = self.knowledge_base_dir / subdir
            if subdir_path.exists():
                for file in subdir_path.glob('*.json'):
                    file_time = datetime.fromtimestamp(file.stat().st_mtime)
                    if current_time - file_time < timedelta(hours=1):
                        recent_tasks.append(file.name)
        
        # Update rates
        self.processing_stats['processing_rates'] = {
            'lessons_per_hour': len([f for f in recent_tasks if 'lesson' in f]),
            'updates_per_hour': len([f for f in recent_tasks if 'update' in f]),
            'patterns_per_hour': len([f for f in recent_tasks if 'pattern' in f])
        }
    
    def _generate_statistics_report(self):
        """Generate comprehensive statistics report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'processing_stats': self.processing_stats,
            'performance_metrics': self._get_processing_performance_metrics(),
            'system_metrics': self._get_system_performance_metrics(),
            'worker_status': {
                'total_workers': len(self.workers),
                'active_workers': sum(1 for worker in self.workers if worker.is_alive())
            }
        }
        
        # Store statistics report
        stats_file = self.knowledge_base_dir / "processing_stats" / "statistics_report.json"
        with open(stats_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
    
    def queue_task(self, task: ProcessingTask):
        """Queue task with priority handling"""
        priority_map = {
            1: 'high',
            2: 'medium',
            3: 'low'
        }
        
        queue_name = priority_map.get(task.priority, 'medium')
        queue = self.task_queues[queue_name]
        
        # Add priority to queue item
        queue.put((task.priority, task))
    
    def queue_lesson_processing(self, lesson_data: Dict[str, Any], priority: int = 2):
        """Queue lesson processing task"""
        task = ProcessingTask(
            task_id=f"lesson_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(str(lesson_data).encode()).hexdigest()[:8]}",
            task_type='lesson_processing',
            priority=priority,
            data=lesson_data,
            created_at=datetime.now()
        )
        
        self.queue_task(task)
        logger.info(f"Queued lesson processing task: {task.task_id}")
    
    def queue_skill_update(self, skill_name: str, pattern: str, pattern_data: Dict[str, Any], priority: int = 2):
        """Queue skill update task"""
        task = ProcessingTask(
            task_id=f"update_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(f'{skill_name}_{pattern}'.encode()).hexdigest()[:8]}",
            task_type='skill_update',
            priority=priority,
            data={
                'skill_name': skill_name,
                'pattern': pattern,
                **pattern_data
            },
            created_at=datetime.now()
        )
        
        self.queue_task(task)
        logger.info(f"Queued skill update task: {task.task_id}")
    
    def queue_pattern_analysis(self, analysis_data: Dict[str, Any], priority: int = 3):
        """Queue pattern analysis task"""
        task = ProcessingTask(
            task_id=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(str(analysis_data).encode()).hexdigest()[:8]}",
            task_type='pattern_analysis',
            priority=priority,
            data=analysis_data,
            created_at=datetime.now()
        )
        
        self.queue_task(task)
        logger.info(f"Queued pattern analysis task: {task.task_id}")
    
    def queue_performance_tracking(self, tracking_data: Dict[str, Any], priority: int = 3):
        """Queue performance tracking task"""
        task = ProcessingTask(
            task_id=f"perf_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(str(tracking_data).encode()).hexdigest()[:8]}",
            task_type='performance_tracking',
            priority=priority,
            data=tracking_data,
            created_at=datetime.now()
        )
        
        self.queue_task(task)
        logger.info(f"Queued performance tracking task: {task.task_id}")
    
    def get_processing_status(self) -> Dict[str, Any]:
        """Get comprehensive processing status"""
        return {
            'system_active': self.system_active,
            'processing_stats': self.processing_stats,
            'queue_sizes': {
                'high': self.task_queues['high'].qsize(),
                'medium': self.task_queues['medium'].qsize(),
                'low': self.task_queues['low'].qsize(),
                'total': sum(queue.qsize() for queue in self.task_queues.values())
            },
            'worker_status': {
                'total_workers': len(self.workers),
                'active_workers': sum(1 for worker in self.workers if worker.is_alive())
            },
            'performance_metrics': self._get_processing_performance_metrics(),
            'last_health_check': self.last_health_check.isoformat()
        }
    
    def generate_processing_report(self) -> str:
        """Generate comprehensive processing report"""
        status = self.get_processing_status()
        
        report = f"""
# Optimized Background Processing Report
Generated: {datetime.now().isoformat()}

## System Status
- System Active: {status['system_active']}
- Last Health Check: {status['last_health_check']}

## Processing Statistics
- Tasks Processed: {status['processing_stats']['tasks_processed']}
- Tasks Failed: {status['processing_stats']['tasks_failed']}
- Tasks Retried: {status['processing_stats']['tasks_retried']}
- Avg Processing Time: {status['processing_stats']['avg_processing_time']:.3f}s

## Queue Status
- High Priority: {status['queue_sizes']['high']} tasks
- Medium Priority: {status['queue_sizes']['medium']} tasks
- Low Priority: {status['queue_sizes']['low']} tasks
- Total Queued: {status['queue_sizes']['total']} tasks

## Worker Status
- Total Workers: {status['worker_status']['total_workers']}
- Active Workers: {status['worker_status']['active_workers']}

## Performance Metrics
"""
        
        # Add performance metrics
        perf_metrics = status['performance_metrics']
        if perf_metrics['total_processed'] > 0:
            report += f"- Avg Processing Time: {perf_metrics['avg_processing_time']:.3f}s\n"
            report += f"- Min Processing Time: {perf_metrics['min_processing_time']:.3f}s\n"
            report += f"- Max Processing Time: {perf_metrics['max_processing_time']:.3f}s\n"
            report += f"- Total Processed: {perf_metrics['total_processed']}\n"
        
        # Add processing rates
        rates = status['processing_stats'].get('processing_rates', {})
        report += f"\n## Processing Rates (Last Hour)\n"
        report += f"- Lessons Per Hour: {rates.get('lessons_per_hour', 0)}\n"
        report += f"- Updates Per Hour: {rates.get('updates_per_hour', 0)}\n"
        report += f"- Patterns Per Hour: {rates.get('patterns_per_hour', 0)}\n"
        
        return report
    
    def stop_processing(self):
        """Stop the optimized background processing system"""
        self.system_active = False
        
        # Wait for workers to finish
        for worker in self.workers:
            if worker.is_alive():
                worker.join(timeout=5)
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        logger.info("Optimized background processing stopped")

# Global optimized processor instance
_global_processor = None

def get_optimized_background_processor() -> OptimizedBackgroundProcessor:
    """Get or create global optimized background processor"""
    global _global_processor
    if _global_processor is None:
        _global_processor = OptimizedBackgroundProcessor()
    return _global_processor

# Auto-start processor when imported
if __name__ != "__main__":
    try:
        processor = get_optimized_background_processor()
        processor.start_processing()
        logger.info("Optimized background processor auto-started")
    except Exception as e:
        logger.error(f"Failed to auto-start optimized processor: {e}")

# Example usage
if __name__ == "__main__":
    processor = get_optimized_background_processor()
    processor.start_processing()
    
    # Example task queuing
    processor.queue_lesson_processing({
        'lesson_type': 'pattern',
        'content': {'success_patterns': ['test_pattern']},
        'confidence': 0.9
    })
    
    # Generate report
    print(processor.generate_processing_report())
    
    # Stop processing
    processor.stop_processing()