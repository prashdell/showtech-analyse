#!/usr/bin/env python3
"""
Automatic Skill File Update System
Automatically updates skill files based on lessons learned and knowledge base insights
"""

import os
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import difflib
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('skill_file_updater.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class SkillUpdate:
    """Represents a skill file update"""
    skill_name: str
    update_type: str  # 'pattern', 'performance', 'error_handling', 'new_insight'
    update_content: str
    confidence_score: float
    impact_level: str  # 'low', 'medium', 'high', 'critical'
    timestamp: datetime
    source_lesson_id: str
    backup_file: str

class AutomaticSkillFileUpdater:
    """System for automatically updating skill files based on learned lessons"""
    
    def __init__(self):
        self.workspace_root = Path(r"C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse")
        self.knowledge_base_dir = self.workspace_root / "knowledge_base"
        self.skill_updates_dir = self.knowledge_base_dir / "skill_updates"
        self.backup_dir = self.workspace_root / "skill_backups"
        
        # Create directories
        for directory in [self.knowledge_base_dir, self.skill_updates_dir, self.backup_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Update tracking
        self.update_history = []
        self.pending_updates = []
        self.update_rules = self._load_update_rules()
        
        logger.info("Automatic Skill File Updater initialized")
    
    def _load_update_rules(self) -> Dict[str, Any]:
        """Load update rules and templates"""
        return {
            'pattern_updates': {
                'add_to_known_patterns': r"## Known Patterns\n",
                'add_to_success_patterns': r"### Success Patterns\n",
                'pattern_template': "- **{pattern}**: {description} (Confidence: {confidence:.1f}, Added: {date})\n"
            },
            'performance_updates': {
                'add_to_performance_section': r"## Performance Insights\n",
                'add_to_execution_time': r"### Execution Time Analysis\n",
                'performance_template': "- **{metric}**: {value} (Recorded: {date})\n"
            },
            'error_updates': {
                'add_to_error_handling': r"## Error Handling\n",
                'add_to_known_issues': r"### Known Issues and Solutions\n",
                'error_template': "- **{error_pattern}**: {solution} (Added: {date}, Confidence: {confidence:.1f})\n"
            },
            'insight_updates': {
                'add_to_recent_insights': r"## Recent Insights\n",
                'add_to_discoveries': r"### Newly Discovered Patterns\n",
                'insight_template': "- **{insight}**: {description} (Discovered: {date}, Impact: {impact})\n"
            }
        }
    
    def process_pending_updates(self) -> List[SkillUpdate]:
        """Process all pending skill file updates"""
        processed_updates = []
        
        # Load pending updates from knowledge base
        pending_lessons = self._load_pending_lessons()
        
        for lesson in pending_lessons:
            updates = self._create_updates_from_lesson(lesson)
            for update in updates:
                if self._validate_update(update):
                    applied_update = self._apply_skill_update(update)
                    if applied_update:
                        processed_updates.append(applied_update)
                        self._record_update(applied_update)
        
        logger.info(f"Processed {len(processed_updates)} skill updates")
        return processed_updates
    
    def _load_pending_lessons(self) -> List[Dict[str, Any]]:
        """Load lessons that haven't been applied to skill files yet"""
        lessons_dir = self.knowledge_base_dir / "lessons_learned"
        pending_lessons = []
        
        # Get applied lesson IDs
        applied_lesson_ids = self._get_applied_lesson_ids()
        
        for lesson_file in lessons_dir.glob('*.json'):
            try:
                with open(lesson_file, 'r') as f:
                    lesson = json.load(f)
                
                lesson_id = lesson.get('lesson_id', '')
                if lesson_id and lesson_id not in applied_lesson_ids:
                    pending_lessons.append(lesson)
                    
            except Exception as e:
                logger.error(f"Error loading lesson {lesson_file}: {e}")
        
        return pending_lessons
    
    def _get_applied_lesson_ids(self) -> set:
        """Get set of lesson IDs that have already been applied"""
        applied_ids = set()
        
        for update_file in self.skill_updates_dir.glob('*.json'):
            try:
                with open(update_file, 'r') as f:
                    update = json.load(f)
                applied_ids.add(update.get('source_lesson_id', ''))
            except:
                continue
        
        return applied_ids
    
    def _create_updates_from_lesson(self, lesson: Dict[str, Any]) -> List[SkillUpdate]:
        """Create skill updates from a lesson"""
        updates = []
        skill_name = lesson.get('skill_name', '')
        lesson_type = lesson.get('lesson_type', '')
        lesson_content = lesson.get('lesson_content', {})
        confidence = lesson.get('confidence_score', 0.0)
        timestamp = lesson.get('timestamp', datetime.now().isoformat())
        lesson_id = lesson.get('lesson_id', '')
        
        if not skill_name or not lesson_id:
            return updates
        
        # Create updates based on lesson type
        if lesson_type == 'pattern':
            updates.extend(self._create_pattern_updates(skill_name, lesson_content, confidence, timestamp, lesson_id))
        elif lesson_type == 'performance':
            updates.extend(self._create_performance_updates(skill_name, lesson_content, confidence, timestamp, lesson_id))
        elif lesson_type == 'error':
            updates.extend(self._create_error_updates(skill_name, lesson_content, confidence, timestamp, lesson_id))
        elif lesson_type == 'new_insight':
            updates.extend(self._create_insight_updates(skill_name, lesson_content, confidence, timestamp, lesson_id))
        
        return updates
    
    def _create_pattern_updates(self, skill_name: str, content: Dict[str, Any], 
                              confidence: float, timestamp: str, lesson_id: str) -> List[SkillUpdate]:
        """Create pattern-related updates"""
        updates = []
        
        success_patterns = content.get('success_patterns', [])
        if not success_patterns:
            return updates
        
        # Create update content
        update_content = "### Success Patterns Identified\n\n"
        for pattern in success_patterns:
            pattern_desc = self._get_pattern_description(pattern)
            update_content += f"- **{pattern}**: {pattern_desc} (Confidence: {confidence:.1f}, Identified: {timestamp[:10]})\n"
        
        update = SkillUpdate(
            skill_name=skill_name,
            update_type='pattern',
            update_content=update_content,
            confidence_score=confidence,
            impact_level='high' if confidence > 0.8 else 'medium',
            timestamp=datetime.fromisoformat(timestamp.replace('Z', '+00:00')),
            source_lesson_id=lesson_id,
            backup_file=""
        )
        
        updates.append(update)
        return updates
    
    def _create_performance_updates(self, skill_name: str, content: Dict[str, Any], 
                                  confidence: float, timestamp: str, lesson_id: str) -> List[SkillUpdate]:
        """Create performance-related updates"""
        updates = []
        
        execution_time = content.get('execution_time', 0)
        if execution_time <= 0:
            return updates
        
        # Create performance insights
        update_content = "### Performance Analysis\n\n"
        update_content += f"- **Average Execution Time**: {execution_time:.2f}s (Measured: {timestamp[:10]})\n"
        
        if execution_time > 30:
            update_content += f"- **Performance Note**: Consider optimization for long-running executions\n"
        
        if execution_time < 5:
            update_content += f"- **Performance Note**: Good execution time performance\n"
        
        update = SkillUpdate(
            skill_name=skill_name,
            update_type='performance',
            update_content=update_content,
            confidence_score=confidence,
            impact_level='medium',
            timestamp=datetime.fromisoformat(timestamp.replace('Z', '+00:00')),
            source_lesson_id=lesson_id,
            backup_file=""
        )
        
        updates.append(update)
        return updates
    
    def _create_error_updates(self, skill_name: str, content: Dict[str, Any], 
                            confidence: float, timestamp: str, lesson_id: str) -> List[SkillUpdate]:
        """Create error-handling updates"""
        updates = []
        
        error_pattern = content.get('error_pattern', '')
        solution = content.get('solution', '')
        prevention = content.get('prevention', '')
        
        if not error_pattern or not solution:
            return updates
        
        # Create error handling content
        update_content = "### Error Prevention\n\n"
        update_content += f"- **{error_pattern}**: {solution} (Added: {timestamp[:10]}, Confidence: {confidence:.1f})\n"
        
        if prevention:
            update_content += f"- **Prevention**: {prevention}\n"
        
        update = SkillUpdate(
            skill_name=skill_name,
            update_type='error_handling',
            update_content=update_content,
            confidence_score=confidence,
            impact_level='high' if confidence > 0.8 else 'medium',
            timestamp=datetime.fromisoformat(timestamp.replace('Z', '+00:00')),
            source_lesson_id=lesson_id,
            backup_file=""
        )
        
        updates.append(update)
        return updates
    
    def _create_insight_updates(self, skill_name: str, content: Dict[str, Any], 
                              confidence: float, timestamp: str, lesson_id: str) -> List[SkillUpdate]:
        """Create insight-related updates"""
        updates = []
        
        new_patterns = content.get('new_patterns', [])
        if not new_patterns:
            return updates
        
        # Create insights content
        update_content = "### New Discoveries\n\n"
        for pattern in new_patterns:
            pattern_desc = self._get_pattern_description(pattern)
            update_content += f"- **{pattern}**: {pattern_desc} (Discovered: {timestamp[:10]}, Confidence: {confidence:.1f})\n"
        
        update = SkillUpdate(
            skill_name=skill_name,
            update_type='new_insight',
            update_content=update_content,
            confidence_score=confidence,
            impact_level='high',
            timestamp=datetime.fromisoformat(timestamp.replace('Z', '+00:00')),
            source_lesson_id=lesson_id,
            backup_file=""
        )
        
        updates.append(update)
        return updates
    
    def _get_pattern_description(self, pattern: str) -> str:
        """Get human-readable description for pattern"""
        pattern_descriptions = {
            'successful_execution_pattern': 'Successfully completed analysis',
            'hardware_platform_identified': 'Hardware platform correctly identified',
            'asic_type_detected': 'ASIC type successfully detected',
            'cpu_analysis_pattern': 'CPU information analyzed',
            'bgp_session_analyzed': 'BGP session state analyzed',
            'bgp_neighbors_counted': 'BGP neighbor relationships counted',
            'memory_usage_analyzed': 'Memory usage patterns analyzed',
            'memory_optimization_suggested': 'Memory optimization recommendations provided',
            'interface_status_analysis': 'Interface operational status analyzed',
            'interface_error_tracking': 'Interface error counters tracked',
            'link_flap_detection': 'Link flapping patterns detected',
            'container_health_monitoring': 'Container health status monitored',
            'container_resource_tracking': 'Container resource usage tracked',
            'container_restart_analysis': 'Container restart patterns analyzed',
            'performance_tracking_pattern': 'Performance metrics tracked',
            'comprehensive_analysis_pattern': 'Comprehensive analysis performed'
        }
        
        return pattern_descriptions.get(pattern, f'Pattern: {pattern}')
    
    def _validate_update(self, update: SkillUpdate) -> bool:
        """Validate if update should be applied"""
        # Check confidence threshold
        if update.confidence_score < 0.6:
            logger.info(f"Skipping low-confidence update for {update.skill_name}: {update.confidence_score}")
            return False
        
        # Check if skill file exists
        skill_file = self._find_skill_file(update.skill_name)
        if not skill_file or not skill_file.exists():
            logger.warning(f"Skill file not found for {update.skill_name}")
            return False
        
        # Check if similar update already applied recently
        if self._is_duplicate_update(update):
            logger.info(f"Skipping duplicate update for {update.skill_name}")
            return False
        
        return True
    
    def _find_skill_file(self, skill_name: str) -> Optional[Path]:
        """Find skill file for given skill name"""
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
    
    def _is_duplicate_update(self, update: SkillUpdate) -> bool:
        """Check if similar update was already applied recently"""
        cutoff_date = datetime.now() - timedelta(days=7)
        
        for existing_update in self.update_history:
            if (existing_update.skill_name == update.skill_name and 
                existing_update.update_type == update.update_type and
                existing_update.timestamp > cutoff_date):
                
                # Check content similarity
                similarity = difflib.SequenceMatcher(None, 
                                                  existing_update.update_content, 
                                                  update.update_content).ratio()
                
                if similarity > 0.8:  # 80% similarity threshold
                    return True
        
        return False
    
    def _apply_skill_update(self, update: SkillUpdate) -> Optional[SkillUpdate]:
        """Apply update to skill file"""
        try:
            skill_file = self._find_skill_file(update.skill_name)
            if not skill_file:
                logger.error(f"Skill file not found: {update.skill_name}")
                return None
            
            # Create backup
            backup_file = self._create_backup(skill_file)
            update.backup_file = str(backup_file)
            
            # Read current content
            with open(skill_file, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            # Apply update based on type
            updated_content = self._apply_update_to_content(current_content, update)
            
            if updated_content != current_content:
                # Write updated content
                with open(skill_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                logger.info(f"Applied update to {skill_file}")
                return update
            else:
                logger.info(f"No changes needed for {skill_file}")
                return None
                
        except Exception as e:
            logger.error(f"Error applying update to {update.skill_name}: {e}")
            return None
    
    def _create_backup(self, skill_file: Path) -> Path:
        """Create backup of skill file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{skill_file.stem}_backup_{timestamp}{skill_file.suffix}"
        backup_file = self.backup_dir / backup_name
        
        shutil.copy2(skill_file, backup_file)
        logger.info(f"Created backup: {backup_file}")
        
        return backup_file
    
    def _apply_update_to_content(self, content: str, update: SkillUpdate) -> str:
        """Apply update to skill file content"""
        updated_content = content
        
        if update.update_type == 'pattern':
            updated_content = self._add_pattern_section(updated_content, update.update_content)
        elif update.update_type == 'performance':
            updated_content = self._add_performance_section(updated_content, update.update_content)
        elif update.update_type == 'error_handling':
            updated_content = self._add_error_section(updated_content, update.update_content)
        elif update.update_type == 'new_insight':
            updated_content = self._add_insight_section(updated_content, update.update_content)
        
        return updated_content
    
    def _add_pattern_section(self, content: str, update_content: str) -> str:
        """Add pattern section to content"""
        # Look for existing patterns section
        if "## Known Patterns" in content:
            # Add to existing section
            section_end = content.find("##", content.find("## Known Patterns") + 1)
            if section_end == -1:
                section_end = len(content)
            
            before_section = content[:section_end]
            after_section = content[section_end:]
            
            # Find the right place to insert
            if "### Success Patterns" in before_section:
                insert_pos = before_section.find("### Success Patterns")
                insert_pos = before_section.find("\n", insert_pos) + 1
                updated = before_section[:insert_pos] + "\n" + update_content + before_section[insert_pos:] + after_section
            else:
                updated = before_section + "\n" + update_content + after_section
        else:
            # Add new section at the end
            updated = content + f"\n\n## Known Patterns\n{update_content}"
        
        return updated
    
    def _add_performance_section(self, content: str, update_content: str) -> str:
        """Add performance section to content"""
        if "## Performance Insights" in content:
            # Add to existing section
            section_end = content.find("##", content.find("## Performance Insights") + 1)
            if section_end == -1:
                section_end = len(content)
            
            before_section = content[:section_end]
            after_section = content[section_end:]
            updated = before_section + "\n" + update_content + after_section
        else:
            # Add new section before the end
            if "## Source Files" in content:
                insert_pos = content.find("## Source Files")
                updated = content[:insert_pos] + f"\n## Performance Insights\n{update_content}\n\n" + content[insert_pos:]
            else:
                updated = content + f"\n\n## Performance Insights\n{update_content}"
        
        return updated
    
    def _add_error_section(self, content: str, update_content: str) -> str:
        """Add error handling section to content"""
        if "## Error Handling" in content:
            # Add to existing section
            section_end = content.find("##", content.find("## Error Handling") + 1)
            if section_end == -1:
                section_end = len(content)
            
            before_section = content[:section_end]
            after_section = content[section_end:]
            updated = before_section + "\n" + update_content + after_section
        else:
            # Add new section
            if "## Source Files" in content:
                insert_pos = content.find("## Source Files")
                updated = content[:insert_pos] + f"\n## Error Handling\n{update_content}\n\n" + content[insert_pos:]
            else:
                updated = content + f"\n\n## Error Handling\n{update_content}"
        
        return updated
    
    def _add_insight_section(self, content: str, update_content: str) -> str:
        """Add insights section to content"""
        if "## Recent Insights" in content:
            # Add to existing section
            section_end = content.find("##", content.find("## Recent Insights") + 1)
            if section_end == -1:
                section_end = len(content)
            
            before_section = content[:section_end]
            after_section = content[section_end:]
            updated = before_section + "\n" + update_content + after_section
        else:
            # Add new section
            updated = content + f"\n\n## Recent Insights\n{update_content}"
        
        return updated
    
    def _record_update(self, update: SkillUpdate):
        """Record update in history"""
        self.update_history.append(update)
        
        # Save update record
        update_record = {
            'skill_name': update.skill_name,
            'update_type': update.update_type,
            'confidence_score': update.confidence_score,
            'impact_level': update.impact_level,
            'timestamp': update.timestamp.isoformat(),
            'source_lesson_id': update.source_lesson_id,
            'backup_file': update.backup_file,
            'update_content_length': len(update.update_content)
        }
        
        update_file = self.skill_updates_dir / f"{update.source_lesson_id}_update.json"
        with open(update_file, 'w') as f:
            json.dump(update_record, f, indent=2)
    
    def get_update_statistics(self) -> Dict[str, Any]:
        """Get statistics about skill updates"""
        stats = {
            'total_updates': len(self.update_history),
            'updates_by_type': {},
            'updates_by_skill': {},
            'average_confidence': 0.0,
            'high_impact_updates': 0,
            'recent_updates': 0
        }
        
        if not self.update_history:
            return stats
        
        # Calculate statistics
        total_confidence = 0
        one_week_ago = datetime.now() - timedelta(days=7)
        
        for update in self.update_history:
            # By type
            update_type = update.update_type
            stats['updates_by_type'][update_type] = stats['updates_by_type'].get(update_type, 0) + 1
            
            # By skill
            skill_name = update.skill_name
            stats['updates_by_skill'][skill_name] = stats['updates_by_skill'].get(skill_name, 0) + 1
            
            # Confidence
            total_confidence += update.confidence_score
            
            # Impact
            if update.impact_level == 'high' or update.impact_level == 'critical':
                stats['high_impact_updates'] += 1
            
            # Recent updates
            if update.timestamp > one_week_ago:
                stats['recent_updates'] += 1
        
        stats['average_confidence'] = total_confidence / len(self.update_history)
        
        return stats
    
    def generate_update_report(self) -> str:
        """Generate comprehensive update report"""
        stats = self.get_update_statistics()
        
        report = f"""
# Skill File Auto-Update Report
Generated: {datetime.now().isoformat()}

## Update Statistics
- Total Updates Applied: {stats['total_updates']}
- High Impact Updates: {stats['high_impact_updates']}
- Recent Updates (7 days): {stats['recent_updates']}
- Average Confidence: {stats['average_confidence']:.2f}

## Updates by Type
"""
        
        for update_type, count in stats['updates_by_type'].items():
            report += f"- {update_type}: {count}\n"
        
        report += "\n## Updates by Skill\n"
        
        for skill_name, count in sorted(stats['updates_by_skill'].items()):
            report += f"- {skill_name}: {count}\n"
        
        report += f"\n## System Status\n"
        report += f"- Knowledge Base Directory: {self.knowledge_base_dir}\n"
        report += f"- Backup Directory: {self.backup_dir}\n"
        report += f"- Skill Updates Directory: {self.skill_updates_dir}\n"
        
        return report

# Global updater instance
_global_updater = None

def get_skill_file_updater() -> AutomaticSkillFileUpdater:
    """Get or create global skill file updater"""
    global _global_updater
    if _global_updater is None:
        _global_updater = AutomaticSkillFileUpdater()
    return _global_updater

# Example usage
if __name__ == "__main__":
    updater = get_skill_file_updater()
    
    # Process pending updates
    updates = updater.process_pending_updates()
    
    print(f"Processed {len(updates)} updates")
    
    # Generate report
    print(updater.generate_update_report())