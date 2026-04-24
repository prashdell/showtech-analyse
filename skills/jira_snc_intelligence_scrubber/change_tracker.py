#!/usr/bin/env python3
"""
SNC JIRA Change Tracking System
Tracks changes and enables incremental updates for SNC intelligence
"""

import json
import datetime
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class IssueChange:
    """Represents a change to an issue"""
    issue_key: str
    change_type: str  # "new", "updated", "comment_added", "status_changed"
    timestamp: str
    details: Dict
    processed: bool = False

class SNChangeTracker:
    """Tracks changes to SNC issues for incremental processing"""
    
    def __init__(self, knowledge_dir: Path):
        self.knowledge_dir = knowledge_dir
        self.change_log_path = knowledge_dir / "snc_change_log.json"
        self.last_sync_path = knowledge_dir / "last_sync_timestamp.json"
        self.processed_issues_path = knowledge_dir / "processed_issues.json"
        
        # Ensure directory exists
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        self.change_log = self.load_change_log()
        self.last_sync = self.load_last_sync()
        self.processed_issues = self.load_processed_issues()
    
    def load_change_log(self) -> List[Dict]:
        """Load change log from file"""
        try:
            with open(self.change_log_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_change_log(self) -> None:
        """Save change log to file"""
        with open(self.change_log_path, 'w') as f:
            json.dump(self.change_log, f, indent=2)
    
    def load_last_sync(self) -> Dict:
        """Load last sync timestamp"""
        try:
            with open(self.last_sync_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "timestamp": "1970-01-01T00:00:00Z",
                "full_pull_completed": False,
                "total_issues_processed": 0
            }
    
    def save_last_sync(self) -> None:
        """Save last sync timestamp"""
        with open(self.last_sync_path, 'w') as f:
            json.dump(self.last_sync, f, indent=2)
    
    def load_processed_issues(self) -> Dict:
        """Load processed issues tracking"""
        try:
            with open(self.processed_issues_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "processed_issues": {},
                "issue_versions": {},
                "last_processed": {}
            }
    
    def save_processed_issues(self) -> None:
        """Save processed issues tracking"""
        with open(self.processed_issues_path, 'w') as f:
            json.dump(self.processed_issues, f, indent=2)
    
    def is_first_run(self) -> bool:
        """Check if this is the first run"""
        return not self.last_sync.get("full_pull_completed", False)
    
    def mark_full_pull_completed(self, total_issues: int) -> None:
        """Mark full pull as completed"""
        self.last_sync.update({
            "timestamp": datetime.datetime.now().isoformat(),
            "full_pull_completed": True,
            "total_issues_processed": total_issues
        })
        self.save_last_sync()
    
    def get_incremental_filter(self) -> str:
        """Generate JQL filter for incremental updates"""
        if self.is_first_run():
            # First run - get all issues
            return "project = SNC"
        else:
            # Incremental run - get only updated issues
            last_sync_time = self.last_sync.get("timestamp", "1970-01-01T00:00:00Z")
            return f"project = SNC AND updated >= '{last_sync_time}'"
    
    def track_issue_change(self, issue_key: str, change_type: str, details: Dict) -> None:
        """Track a change to an issue"""
        change = {
            "issue_key": issue_key,
            "change_type": change_type,
            "timestamp": datetime.datetime.now().isoformat(),
            "details": details,
            "processed": False
        }
        
        self.change_log.append(change)
        self.save_change_log()
    
    def is_issue_processed(self, issue_key: str, issue_version: str) -> bool:
        """Check if issue has been processed with this version"""
        return (issue_key in self.processed_issues["processed_issues"] and 
                self.processed_issues["issue_versions"].get(issue_key, "") == issue_version)
    
    def mark_issue_processed(self, issue_key: str, issue_version: str, processing_data: Dict) -> None:
        """Mark issue as processed"""
        self.processed_issues["processed_issues"][issue_key] = True
        self.processed_issues["issue_versions"][issue_key] = issue_version
        self.processed_issues["last_processed"][issue_key] = {
            "timestamp": datetime.datetime.now().isoformat(),
            "processing_data": processing_data
        }
        self.save_processed_issues()
    
    def get_unprocessed_changes(self) -> List[Dict]:
        """Get list of unprocessed changes"""
        return [change for change in self.change_log if not change.get("processed", False)]
    
    def mark_changes_processed(self, change_keys: List[str]) -> None:
        """Mark changes as processed"""
        for change in self.change_log:
            if change.get("issue_key") in change_keys:
                change["processed"] = True
        self.save_change_log()
    
    def get_processing_statistics(self) -> Dict:
        """Get processing statistics"""
        total_changes = len(self.change_log)
        processed_changes = len([c for c in self.change_log if c.get("processed", False)])
        unprocessed_changes = total_changes - processed_changes
        
        return {
            "total_changes": total_changes,
            "processed_changes": processed_changes,
            "unprocessed_changes": unprocessed_changes,
            "first_run": self.is_first_run(),
            "last_sync": self.last_sync.get("timestamp"),
            "total_issues_processed": len(self.processed_issues["processed_issues"]),
            "full_pull_completed": self.last_sync.get("full_pull_completed", False)
        }

class SNCIncrementalProcessor:
    """Processes SNC issues with incremental updates"""
    
    def __init__(self, knowledge_dir: Path):
        self.change_tracker = SNChangeTracker(knowledge_dir)
        self.knowledge_dir = knowledge_dir
    
    def determine_processing_strategy(self) -> Dict:
        """Determine whether to do full pull or incremental update"""
        
        if self.change_tracker.is_first_run():
            return {
                "strategy": "full_pull",
                "reason": "First run - no previous data",
                "jql_filter": "project = SNC",
                "expected_issues": "All SNC issues"
            }
        else:
            last_sync = self.change_tracker.last_sync.get("timestamp", "")
            days_since_sync = self.calculate_days_since(last_sync)
            
            if days_since_sync > 30:
                return {
                    "strategy": "full_pull",
                    "reason": f"Too long since last sync ({days_since_sync} days)",
                    "jql_filter": "project = SNC",
                    "expected_issues": "All SNC issues"
                }
            else:
                jql_filter = self.change_tracker.get_incremental_filter()
                return {
                    "strategy": "incremental",
                    "reason": f"Recent sync ({days_since_sync} days ago)",
                    "jql_filter": jql_filter,
                    "expected_issues": "Issues updated since last sync"
                }
    
    def calculate_days_since(self, timestamp: str) -> int:
        """Calculate days since timestamp"""
        try:
            last_sync = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            now = datetime.datetime.now(datetime.timezone.utc)
            delta = now - last_sync
            return delta.days
        except:
            return 999  # Large number to force full pull
    
    def process_issues_with_strategy(self, issues: List[Dict]) -> Dict:
        """Process issues using the determined strategy"""
        
        strategy = self.determine_processing_strategy()
        processing_results = {
            "strategy": strategy["strategy"],
            "issues_found": len(issues),
            "issues_processed": 0,
            "issues_skipped": 0,
            "new_intelligence": {},
            "processing_details": []
        }
        
        print(f"Processing strategy: {strategy['strategy']}")
        print(f"Reason: {strategy['reason']}")
        print(f"Issues found: {len(issues)}")
        
        for issue in issues:
            issue_key = issue.get("key", "")
            issue_version = self.generate_issue_version(issue)
            
            # Check if issue needs processing
            if strategy["strategy"] == "incremental":
                if self.change_tracker.is_issue_processed(issue_key, issue_version):
                    processing_results["issues_skipped"] += 1
                    processing_results["processing_details"].append({
                        "issue_key": issue_key,
                        "action": "skipped",
                        "reason": "Already processed with current version"
                    })
                    continue
            
            # Process the issue
            try:
                intelligence = self.extract_issue_intelligence(issue)
                self.update_knowledge_base(intelligence)
                
                # Track the change
                change_type = "new" if strategy["strategy"] == "full_pull" else "updated"
                self.change_tracker.track_issue_change(issue_key, change_type, {
                    "summary": issue.get("summary", ""),
                    "status": issue.get("status", ""),
                    "priority": issue.get("priority", "")
                })
                
                # Mark as processed
                self.change_tracker.mark_issue_processed(issue_key, issue_version, {
                    "strategy": strategy["strategy"],
                    "processed_at": datetime.datetime.now().isoformat()
                })
                
                processing_results["issues_processed"] += 1
                processing_results["processing_details"].append({
                    "issue_key": issue_key,
                    "action": "processed",
                    "strategy": strategy["strategy"]
                })
                
            except Exception as e:
                processing_results["processing_details"].append({
                    "issue_key": issue_key,
                    "action": "error",
                    "error": str(e)
                })
        
        # Update sync timestamp
        if strategy["strategy"] == "full_pull":
            self.change_tracker.mark_full_pull_completed(len(issues))
        else:
            self.change_tracker.last_sync["timestamp"] = datetime.datetime.now().isoformat()
            self.change_tracker.save_last_sync()
        
        return processing_results
    
    def generate_issue_version(self, issue: Dict) -> str:
        """Generate version hash for issue"""
        import hashlib
        
        # Create version based on key fields that indicate change
        version_fields = [
            issue.get("summary", ""),
            issue.get("description", ""),
            issue.get("status", ""),
            issue.get("priority", ""),
            str(len(issue.get("comments", []))),  # Comment count
            issue.get("updated", "")  # Last updated timestamp
        ]
        
        version_string = "|".join(version_fields)
        return hashlib.md5(version_string.encode()).hexdigest()[:16]
    
    def extract_issue_intelligence(self, issue: Dict) -> Dict:
        """Extract intelligence from issue (simplified version)"""
        # This would use the full intelligence processor
        # For now, return basic extraction
        return {
            "issue_key": issue.get("key", ""),
            "summary": issue.get("summary", ""),
            "description": issue.get("description", ""),
            "status": issue.get("status", ""),
            "priority": issue.get("priority", ""),
            "comments": issue.get("comments", []),
            "labels": issue.get("labels", []),
            "extracted_at": datetime.datetime.now().isoformat()
        }
    
    def update_knowledge_base(self, intelligence: Dict) -> None:
        """Update knowledge base with new intelligence"""
        # This would integrate with the main knowledge base
        # For now, just track the update
        pass
    
    def generate_processing_report(self) -> Dict:
        """Generate comprehensive processing report"""
        
        stats = self.change_tracker.get_processing_statistics()
        strategy = self.determine_processing_strategy()
        
        report = {
            "processing_summary": {
                "strategy": strategy["strategy"],
                "reason": strategy["reason"],
                "statistics": stats,
                "generated_at": datetime.datetime.now().isoformat()
            },
            "change_analysis": {
                "total_changes": stats["total_changes"],
                "processed_changes": stats["processed_changes"],
                "unprocessed_changes": stats["unprocessed_changes"],
                "change_types": self.analyze_change_types()
            },
            "recommendations": self.generate_recommendations(stats)
        }
        
        return report
    
    def analyze_change_types(self) -> Dict:
        """Analyze types of changes"""
        change_types = {}
        
        for change in self.change_tracker.change_log:
            change_type = change.get("change_type", "unknown")
            change_types[change_type] = change_types.get(change_type, 0) + 1
        
        return change_types
    
    def generate_recommendations(self, stats: Dict) -> List[str]:
        """Generate processing recommendations"""
        recommendations = []
        
        if stats["first_run"]:
            recommendations.append("Complete full pull to establish baseline intelligence")
        elif stats["unprocessed_changes"] > 100:
            recommendations.append("Consider running incremental processing to clear backlog")
        elif stats["total_issues_processed"] < 1000:
            recommendations.append("Continue monitoring to build comprehensive intelligence")
        
        return recommendations

if __name__ == "__main__":
    # Example usage
    knowledge_dir = Path("C:/Users/Prasanth_Sasidharan/OneDrive - Dell Technologies/Documents/AI/Devin/showtech_analyse/knowledge")
    
    processor = SNCIncrementalProcessor(knowledge_dir)
    
    # Determine processing strategy
    strategy = processor.determine_processing_strategy()
    print(f"Processing strategy: {strategy}")
    
    # Generate processing report
    report = processor.generate_processing_report()
    print(f"Processing report: {report}")