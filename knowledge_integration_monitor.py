#!/usr/bin/env python3
"""
Knowledge Integration Monitoring and Validation System
Monitors the health of the automatic knowledge integration system and validates updates
"""

import os
import json
import logging
import time
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import psutil
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('knowledge_integration_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class SystemHealthMetrics:
    """Health metrics for the knowledge integration system"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_threads: int
    knowledge_base_size: int
    lesson_queue_size: int
    update_queue_size: int
    error_count: int
    success_rate: float

@dataclass
class ValidationResult:
    """Result of validation check"""
    validation_type: str
    status: str  # 'pass', 'warning', 'fail'
    message: str
    details: Dict[str, Any]
    timestamp: datetime

class KnowledgeIntegrationMonitor:
    """Monitors and validates the automatic knowledge integration system"""
    
    def __init__(self):
        self.workspace_root = Path(r"C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse")
        self.knowledge_base_dir = self.workspace_root / "knowledge_base"
        self.monitoring_active = False
        self.monitoring_thread = None
        self.validation_thread = None
        
        # Metrics tracking
        self.health_metrics = []
        self.validation_results = []
        self.error_log = []
        
        # Thresholds
        self.thresholds = {
            'cpu_usage_warning': 70.0,
            'cpu_usage_critical': 90.0,
            'memory_usage_warning': 70.0,
            'memory_usage_critical': 85.0,
            'disk_usage_warning': 80.0,
            'disk_usage_critical': 90.0,
            'queue_size_warning': 100,
            'queue_size_critical': 500,
            'success_rate_warning': 80.0,
            'success_rate_critical': 60.0
        }
        
        logger.info("Knowledge Integration Monitor initialized")
    
    def start_monitoring(self, interval_seconds: int = 60):
        """Start continuous monitoring"""
        if self.monitoring_active:
            logger.warning("Monitoring already active")
            return
        
        self.monitoring_active = True
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval_seconds,),
            daemon=True,
            name="KnowledgeMonitor"
        )
        self.monitoring_thread.start()
        
        # Start validation thread
        self.validation_thread = threading.Thread(
            target=self._validation_loop,
            args=(300,),  # Validate every 5 minutes
            daemon=True,
            name="KnowledgeValidator"
        )
        self.validation_thread.start()
        
        logger.info(f"Monitoring started with {interval_seconds}s interval")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring_active = False
        logger.info("Monitoring stopped")
    
    def _monitoring_loop(self, interval_seconds: int):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect health metrics
                metrics = self._collect_health_metrics()
                self.health_metrics.append(metrics)
                
                # Check for alerts
                alerts = self._check_alerts(metrics)
                if alerts:
                    for alert in alerts:
                        self._handle_alert(alert)
                
                # Keep only recent metrics (last 24 hours)
                cutoff_time = datetime.now() - timedelta(hours=24)
                self.health_metrics = [m for m in self.health_metrics if m.timestamp > cutoff_time]
                
                time.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                self.error_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'error': str(e),
                    'context': 'monitoring_loop'
                })
                time.sleep(interval_seconds)
    
    def _validation_loop(self, interval_seconds: int):
        """Validation loop"""
        while self.monitoring_active:
            try:
                # Run validations
                validations = self._run_validations()
                self.validation_results.extend(validations)
                
                # Keep only recent validations (last 24 hours)
                cutoff_time = datetime.now() - timedelta(hours=24)
                self.validation_results = [v for v in self.validation_results if v.timestamp > cutoff_time]
                
                time.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"Error in validation loop: {e}")
                self.error_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'error': str(e),
                    'context': 'validation_loop'
                })
                time.sleep(interval_seconds)
    
    def _collect_health_metrics(self) -> SystemHealthMetrics:
        """Collect system health metrics"""
        # System metrics
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(str(self.workspace_root))
        
        # Knowledge base metrics
        knowledge_base_size = self._get_directory_size(self.knowledge_base_dir)
        
        # Queue metrics (would need to access the actual integrator)
        lesson_queue_size = self._estimate_queue_size('lessons')
        update_queue_size = self._estimate_queue_size('updates')
        
        # Thread metrics
        active_threads = threading.active_count()
        
        # Success rate (from recent validations)
        success_rate = self._calculate_success_rate()
        
        # Error count (recent errors)
        error_count = self._get_recent_error_count()
        
        return SystemHealthMetrics(
            timestamp=datetime.now(),
            cpu_usage=cpu_usage,
            memory_usage=memory.percent,
            disk_usage=disk.percent,
            active_threads=active_threads,
            knowledge_base_size=knowledge_base_size,
            lesson_queue_size=lesson_queue_size,
            update_queue_size=update_queue_size,
            error_count=error_count,
            success_rate=success_rate
        )
    
    def _get_directory_size(self, directory: Path) -> int:
        """Get total size of directory in bytes"""
        total_size = 0
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception as e:
            logger.warning(f"Error calculating directory size: {e}")
        
        return total_size
    
    def _estimate_queue_size(self, queue_type: str) -> int:
        """Estimate queue size (simplified implementation)"""
        # In real implementation, this would access actual queue objects
        if queue_type == 'lessons':
            lessons_dir = self.knowledge_base_dir / "lessons_learned"
            return len(list(lessons_dir.glob('*.json')))
        elif queue_type == 'updates':
            updates_dir = self.knowledge_base_dir / "skill_updates"
            return len(list(updates_dir.glob('*.json')))
        
        return 0
    
    def _calculate_success_rate(self) -> float:
        """Calculate success rate from recent validations"""
        if not self.validation_results:
            return 100.0  # Assume 100% if no data
        
        recent_results = [v for v in self.validation_results 
                         if v.timestamp > datetime.now() - timedelta(hours=1)]
        
        if not recent_results:
            return 100.0
        
        pass_count = sum(1 for v in recent_results if v.status == 'pass')
        return (pass_count / len(recent_results)) * 100.0
    
    def _get_recent_error_count(self) -> int:
        """Get count of recent errors"""
        cutoff_time = datetime.now() - timedelta(hours=1)
        return len([e for e in self.error_log if datetime.fromisoformat(e['timestamp']) > cutoff_time])
    
    def _check_alerts(self, metrics: SystemHealthMetrics) -> List[Dict[str, Any]]:
        """Check for alert conditions"""
        alerts = []
        
        # CPU usage alerts
        if metrics.cpu_usage > self.thresholds['cpu_usage_critical']:
            alerts.append({
                'type': 'critical',
                'metric': 'cpu_usage',
                'value': metrics.cpu_usage,
                'threshold': self.thresholds['cpu_usage_critical'],
                'message': f'Critical CPU usage: {metrics.cpu_usage:.1f}%'
            })
        elif metrics.cpu_usage > self.thresholds['cpu_usage_warning']:
            alerts.append({
                'type': 'warning',
                'metric': 'cpu_usage',
                'value': metrics.cpu_usage,
                'threshold': self.thresholds['cpu_usage_warning'],
                'message': f'High CPU usage: {metrics.cpu_usage:.1f}%'
            })
        
        # Memory usage alerts
        if metrics.memory_usage > self.thresholds['memory_usage_critical']:
            alerts.append({
                'type': 'critical',
                'metric': 'memory_usage',
                'value': metrics.memory_usage,
                'threshold': self.thresholds['memory_usage_critical'],
                'message': f'Critical memory usage: {metrics.memory_usage:.1f}%'
            })
        elif metrics.memory_usage > self.thresholds['memory_usage_warning']:
            alerts.append({
                'type': 'warning',
                'metric': 'memory_usage',
                'value': metrics.memory_usage,
                'threshold': self.thresholds['memory_usage_warning'],
                'message': f'High memory usage: {metrics.memory_usage:.1f}%'
            })
        
        # Disk usage alerts
        if metrics.disk_usage > self.thresholds['disk_usage_critical']:
            alerts.append({
                'type': 'critical',
                'metric': 'disk_usage',
                'value': metrics.disk_usage,
                'threshold': self.thresholds['disk_usage_critical'],
                'message': f'Critical disk usage: {metrics.disk_usage:.1f}%'
            })
        elif metrics.disk_usage > self.thresholds['disk_usage_warning']:
            alerts.append({
                'type': 'warning',
                'metric': 'disk_usage',
                'value': metrics.disk_usage,
                'threshold': self.thresholds['disk_usage_warning'],
                'message': f'High disk usage: {metrics.disk_usage:.1f}%'
            })
        
        # Queue size alerts
        if metrics.lesson_queue_size > self.thresholds['queue_size_critical']:
            alerts.append({
                'type': 'critical',
                'metric': 'lesson_queue_size',
                'value': metrics.lesson_queue_size,
                'threshold': self.thresholds['queue_size_critical'],
                'message': f'Critical lesson queue size: {metrics.lesson_queue_size}'
            })
        elif metrics.lesson_queue_size > self.thresholds['queue_size_warning']:
            alerts.append({
                'type': 'warning',
                'metric': 'lesson_queue_size',
                'value': metrics.lesson_queue_size,
                'threshold': self.thresholds['queue_size_warning'],
                'message': f'Large lesson queue: {metrics.lesson_queue_size}'
            })
        
        # Success rate alerts
        if metrics.success_rate < self.thresholds['success_rate_critical']:
            alerts.append({
                'type': 'critical',
                'metric': 'success_rate',
                'value': metrics.success_rate,
                'threshold': self.thresholds['success_rate_critical'],
                'message': f'Critical success rate: {metrics.success_rate:.1f}%'
            })
        elif metrics.success_rate < self.thresholds['success_rate_warning']:
            alerts.append({
                'type': 'warning',
                'metric': 'success_rate',
                'value': metrics.success_rate,
                'threshold': self.thresholds['success_rate_warning'],
                'message': f'Low success rate: {metrics.success_rate:.1f}%'
            })
        
        return alerts
    
    def _handle_alert(self, alert: Dict[str, Any]):
        """Handle alert (log, notify, etc.)"""
        alert_level = alert['type'].upper()
        message = alert['message']
        
        if alert['type'] == 'critical':
            logger.error(f"CRITICAL ALERT: {message}")
        else:
            logger.warning(f"WARNING: {message}")
        
        # Could add additional notification methods here (email, Slack, etc.)
    
    def _run_validations(self) -> List[ValidationResult]:
        """Run all validation checks"""
        validations = []
        
        # Knowledge base integrity validation
        validations.append(self._validate_knowledge_base_integrity())
        
        # Skill file validation
        validations.append(self._validate_skill_files())
        
        # Update consistency validation
        validations.append(self._validate_update_consistency())
        
        # Performance validation
        validations.append(self._validate_performance())
        
        # Data quality validation
        validations.append(self._validate_data_quality())
        
        return validations
    
    def _validate_knowledge_base_integrity(self) -> ValidationResult:
        """Validate knowledge base integrity"""
        issues = []
        
        # Check knowledge base directory exists
        if not self.knowledge_base_dir.exists():
            issues.append("Knowledge base directory does not exist")
        
        # Check required subdirectories
        required_dirs = ["lessons_learned", "patterns", "performance", "skill_updates"]
        for dir_name in required_dirs:
            dir_path = self.knowledge_base_dir / dir_name
            if not dir_path.exists():
                issues.append(f"Missing subdirectory: {dir_name}")
        
        # Check for corrupted JSON files
        for json_file in self.knowledge_base_dir.rglob('*.json'):
            try:
                with open(json_file, 'r') as f:
                    json.load(f)
            except json.JSONDecodeError:
                issues.append(f"Corrupted JSON file: {json_file}")
        
        status = 'fail' if issues else 'pass'
        if issues and len(issues) < 3:
            status = 'warning'
        
        return ValidationResult(
            validation_type='knowledge_base_integrity',
            status=status,
            message=f"Knowledge base integrity: {len(issues)} issues found",
            details={'issues': issues, 'total_files': len(list(self.knowledge_base_dir.rglob('*.json')))},
            timestamp=datetime.now()
        )
    
    def _validate_skill_files(self) -> ValidationResult:
        """Validate skill files"""
        skills_dir = self.workspace_root / "skills"
        issues = []
        valid_skills = 0
        
        if not skills_dir.exists():
            return ValidationResult(
                validation_type='skill_files',
                status='fail',
                message="Skills directory does not exist",
                details={'issues': ['Skills directory missing']},
                timestamp=datetime.now()
            )
        
        # Check each skill directory
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    # Validate skill file format
                    try:
                        with open(skill_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Check for required sections
                        required_sections = ["## Overview", "## Trigger Condition", "## Source Files"]
                        missing_sections = [section for section in required_sections if section not in content]
                        
                        if missing_sections:
                            issues.append(f"Skill {skill_dir.name} missing sections: {missing_sections}")
                        else:
                            valid_skills += 1
                            
                    except Exception as e:
                        issues.append(f"Error reading skill {skill_dir.name}: {e}")
                else:
                    issues.append(f"Skill {skill_dir.name} missing SKILL.md file")
        
        status = 'fail' if valid_skills == 0 else 'warning' if issues else 'pass'
        
        return ValidationResult(
            validation_type='skill_files',
            status=status,
            message=f"Skill files: {valid_skills} valid, {len(issues)} issues",
            details={'valid_skills': valid_skills, 'issues': issues},
            timestamp=datetime.now()
        )
    
    def _validate_update_consistency(self) -> ValidationResult:
        """Validate update consistency"""
        updates_dir = self.knowledge_base_dir / "skill_updates"
        issues = []
        consistent_updates = 0
        
        if not updates_dir.exists():
            return ValidationResult(
                validation_type='update_consistency',
                status='warning',
                message="Updates directory does not exist",
                details={'issues': ['Updates directory missing']},
                timestamp=datetime.now()
            )
        
        # Check each update record
        for update_file in updates_dir.glob('*.json'):
            try:
                with open(update_file, 'r') as f:
                    update = json.load(f)
                
                # Validate required fields
                required_fields = ['skill_name', 'update_type', 'timestamp', 'source_lesson_id']
                missing_fields = [field for field in required_fields if field not in update]
                
                if missing_fields:
                    issues.append(f"Update {update_file.name} missing fields: {missing_fields}")
                else:
                    # Check timestamp format
                    try:
                        datetime.fromisoformat(update['timestamp'].replace('Z', '+00:00'))
                        consistent_updates += 1
                    except ValueError:
                        issues.append(f"Update {update_file.name} has invalid timestamp")
                        
            except Exception as e:
                issues.append(f"Error reading update {update_file.name}: {e}")
        
        status = 'fail' if consistent_updates == 0 else 'warning' if issues else 'pass'
        
        return ValidationResult(
            validation_type='update_consistency',
            status=status,
            message=f"Update consistency: {consistent_updates} valid, {len(issues)} issues",
            details={'consistent_updates': consistent_updates, 'issues': issues},
            timestamp=datetime.now()
        )
    
    def _validate_performance(self) -> ValidationResult:
        """Validate system performance"""
        issues = []
        
        # Get recent metrics
        recent_metrics = [m for m in self.health_metrics 
                         if m.timestamp > datetime.now() - timedelta(minutes=10)]
        
        if not recent_metrics:
            return ValidationResult(
                validation_type='performance',
                status='warning',
                message="No recent performance metrics available",
                details={'issues': ['No metrics data']},
                timestamp=datetime.now()
            )
        
        # Check performance trends
        avg_cpu = sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
        
        if avg_cpu > 80:
            issues.append(f"High average CPU usage: {avg_cpu:.1f}%")
        
        if avg_memory > 80:
            issues.append(f"High average memory usage: {avg_memory:.1f}%")
        
        status = 'fail' if len(issues) > 2 else 'warning' if issues else 'pass'
        
        return ValidationResult(
            validation_type='performance',
            status=status,
            message=f"Performance: {len(issues)} issues",
            details={
                'avg_cpu': avg_cpu,
                'avg_memory': avg_memory,
                'issues': issues,
                'metrics_count': len(recent_metrics)
            },
            timestamp=datetime.now()
        )
    
    def _validate_data_quality(self) -> ValidationResult:
        """Validate data quality in knowledge base"""
        issues = []
        
        # Check for duplicate lessons
        lessons_dir = self.knowledge_base_dir / "lessons_learned"
        lesson_ids = set()
        duplicate_count = 0
        
        for lesson_file in lessons_dir.glob('*.json'):
            try:
                with open(lesson_file, 'r') as f:
                    lesson = json.load(f)
                
                lesson_id = lesson.get('lesson_id', '')
                if lesson_id:
                    if lesson_id in lesson_ids:
                        duplicate_count += 1
                    else:
                        lesson_ids.add(lesson_id)
                        
            except Exception:
                issues.append(f"Invalid lesson file: {lesson_file}")
        
        if duplicate_count > 0:
            issues.append(f"Found {duplicate_count} duplicate lesson IDs")
        
        # Check for empty or incomplete lessons
        incomplete_lessons = 0
        for lesson_file in lessons_dir.glob('*.json'):
            try:
                with open(lesson_file, 'r') as f:
                    lesson = json.load(f)
                
                # Check for required fields
                if not all(key in lesson for key in ['lesson_id', 'skill_name', 'lesson_type']):
                    incomplete_lessons += 1
                    
            except Exception:
                continue
        
        if incomplete_lessons > 0:
            issues.append(f"Found {incomplete_lessons} incomplete lessons")
        
        status = 'fail' if len(issues) > 5 else 'warning' if issues else 'pass'
        
        return ValidationResult(
            validation_type='data_quality',
            status=status,
            message=f"Data quality: {len(issues)} issues",
            details={
                'issues': issues,
                'total_lessons': len(list(lessons_dir.glob('*.json'))),
                'unique_lesson_ids': len(lesson_ids)
            },
            timestamp=datetime.now()
        )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        if not self.health_metrics:
            return {'status': 'no_data', 'message': 'No metrics available'}
        
        latest_metrics = self.health_metrics[-1]
        
        # Get latest validation results
        recent_validations = [v for v in self.validation_results 
                             if v.timestamp > datetime.now() - timedelta(minutes=30)]
        
        # Calculate overall health score
        health_score = self._calculate_health_score(latest_metrics, recent_validations)
        
        return {
            'status': 'healthy' if health_score > 80 else 'warning' if health_score > 60 else 'critical',
            'health_score': health_score,
            'latest_metrics': {
                'cpu_usage': latest_metrics.cpu_usage,
                'memory_usage': latest_metrics.memory_usage,
                'disk_usage': latest_metrics.disk_usage,
                'lesson_queue_size': latest_metrics.lesson_queue_size,
                'update_queue_size': latest_metrics.update_queue_size,
                'success_rate': latest_metrics.success_rate
            },
            'validation_summary': {
                'total_validations': len(recent_validations),
                'pass_count': sum(1 for v in recent_validations if v.status == 'pass'),
                'warning_count': sum(1 for v in recent_validations if v.status == 'warning'),
                'fail_count': sum(1 for v in recent_validations if v.status == 'fail')
            },
            'monitoring_active': self.monitoring_active,
            'last_updated': latest_metrics.timestamp.isoformat()
        }
    
    def _calculate_health_score(self, metrics: SystemHealthMetrics, validations: List[ValidationResult]) -> float:
        """Calculate overall health score (0-100)"""
        score = 100.0
        
        # System resource penalties
        if metrics.cpu_usage > 90:
            score -= 20
        elif metrics.cpu_usage > 70:
            score -= 10
        
        if metrics.memory_usage > 85:
            score -= 20
        elif metrics.memory_usage > 70:
            score -= 10
        
        if metrics.disk_usage > 90:
            score -= 15
        elif metrics.disk_usage > 80:
            score -= 5
        
        # Queue size penalties
        if metrics.lesson_queue_size > 500:
            score -= 15
        elif metrics.lesson_queue_size > 100:
            score -= 5
        
        # Success rate penalty
        if metrics.success_rate < 60:
            score -= 25
        elif metrics.success_rate < 80:
            score -= 10
        
        # Validation penalties
        if validations:
            fail_count = sum(1 for v in validations if v.status == 'fail')
            warning_count = sum(1 for v in validations if v.status == 'warning')
            
            score -= (fail_count * 10) + (warning_count * 3)
        
        return max(0, min(100, score))
    
    def generate_monitoring_report(self) -> str:
        """Generate comprehensive monitoring report"""
        status = self.get_system_status()
        
        report = f"""
# Knowledge Integration Monitoring Report
Generated: {datetime.now().isoformat()}

## System Status
- Overall Status: {status['status'].upper()}
- Health Score: {status['health_score']:.1f}/100
- Monitoring Active: {status['monitoring_active']}

## Latest Metrics
- CPU Usage: {status['latest_metrics']['cpu_usage']:.1f}%
- Memory Usage: {status['latest_metrics']['memory_usage']:.1f}%
- Disk Usage: {status['latest_metrics']['disk_usage']:.1f}%
- Lesson Queue Size: {status['latest_metrics']['lesson_queue_size']}
- Update Queue Size: {status['latest_metrics']['update_queue_size']}
- Success Rate: {status['latest_metrics']['success_rate']:.1f}%

## Recent Validations
- Total Validations: {status['validation_summary']['total_validations']}
- Pass: {status['validation_summary']['pass_count']}
- Warnings: {status['validation_summary']['warning_count']}
- Failures: {status['validation_summary']['fail_count']}

## Recent Validation Details
"""
        
        recent_validations = [v for v in self.validation_results 
                             if v.timestamp > datetime.now() - timedelta(hours=1)]
        
        for validation in recent_validations[-10:]:  # Last 10 validations
            report += f"""
### {validation.validation_type.replace('_', ' ').title()}
- Status: {validation.status.upper()}
- Message: {validation.message}
- Time: {validation.timestamp.strftime('%H:%M:%S')}
"""
        
        report += f"""
## System Configuration
- Workspace Root: {self.workspace_root}
- Knowledge Base: {self.knowledge_base_dir}
- Monitoring Interval: 60 seconds
- Validation Interval: 300 seconds

## Alert Thresholds
- CPU Warning: {self.thresholds['cpu_usage_warning']}%, Critical: {self.thresholds['cpu_usage_critical']}%
- Memory Warning: {self.thresholds['memory_usage_warning']}%, Critical: {self.thresholds['memory_usage_critical']}%
- Disk Warning: {self.thresholds['disk_usage_warning']}%, Critical: {self.thresholds['disk_usage_critical']}%
- Queue Warning: {self.thresholds['queue_size_warning']}, Critical: {self.thresholds['queue_size_critical']}
- Success Rate Warning: {self.thresholds['success_rate_warning']}%, Critical: {self.thresholds['success_rate_critical']}%
"""
        
        return report

# Global monitor instance
_global_monitor = None

def get_knowledge_monitor() -> KnowledgeIntegrationMonitor:
    """Get or create global knowledge monitor"""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = KnowledgeIntegrationMonitor()
    return _global_monitor

# Auto-start monitoring when imported
if __name__ != "__main__":
    try:
        monitor = get_knowledge_monitor()
        monitor.start_monitoring()
        logger.info("Knowledge monitoring auto-started")
    except Exception as e:
        logger.error(f"Failed to auto-start monitoring: {e}")

# Example usage
if __name__ == "__main__":
    monitor = get_knowledge_monitor()
    
    # Start monitoring
    monitor.start_monitoring(interval_seconds=30)
    
    # Wait for some data
    time.sleep(60)
    
    # Get status
    status = monitor.get_system_status()
    print("System Status:", json.dumps(status, indent=2, default=str))
    
    # Generate report
    print(monitor.generate_monitoring_report())
    
    # Stop monitoring
    monitor.stop_monitoring()