#!/usr/bin/env python3
"""
SNC Issue Inventory and Tracking System
Comprehensive tracking of all SNC issues with detailed audit trails and update timelines
"""

import json
import datetime
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict

@dataclass
class SNCIssueRecord:
    """Complete record for a single SNC issue"""
    issue_key: str
    summary: str
    status: str
    priority: str
    assignee: str
    reporter: str
    created: str
    updated: str
    resolved: Optional[str]
    labels: List[str]
    components: List[str]
    issue_type: str
    description: str
    comments_count: int
    attachments_count: int
    
    # Tracking fields
    first_discovered: str
    last_processed: str
    processing_count: int
    total_updates: int
    update_history: List[Dict]
    
    # Intelligence extraction
    intelligence_extracted: bool
    root_cause_identified: bool
    commands_extracted: List[str]
    solutions_identified: List[str]
    customer_patterns: List[str]
    platform_patterns: List[str]

@dataclass
class SNCUpdateRecord:
    """Record of each update to an SNC issue"""
    issue_key: str
    update_timestamp: str
    update_type: str  # "created", "updated", "comment_added", "status_changed", "resolved"
    previous_values: Dict
    new_values: Dict
    processing_timestamp: str
    intelligence_extracted: bool
    changes_detected: List[str]

class SNCInventoryManager:
    """Manages complete inventory of SNC issues with detailed tracking"""
    
    def __init__(self, knowledge_dir: Path):
        self.knowledge_dir = knowledge_dir
        self.inventory_path = knowledge_dir / "snc_inventory.json"
        self.snc_master_list_path = knowledge_dir / "snc_master_list.json"
        self.update_timeline_path = knowledge_dir / "snc_update_timeline.json"
        self.snc_audit_log_path = knowledge_dir / "snc_audit_log.json"
        
        # Ensure directory exists
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        self.inventory = self.load_inventory()
        self.master_list = self.load_master_list()
        self.update_timeline = self.load_update_timeline()
        self.audit_log = self.load_audit_log()
    
    def load_inventory(self) -> Dict:
        """Load SNC inventory from file"""
        try:
            with open(self.inventory_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "metadata": {
                    "created": datetime.datetime.now().isoformat(),
                    "last_updated": datetime.datetime.now().isoformat(),
                    "total_snc_issues": 0,
                    "first_pull_completed": False,
                    "last_pull_timestamp": None
                },
                "snc_issues": {},
                "processing_statistics": {
                    "total_processing_runs": 0,
                    "successful_extractions": 0,
                    "failed_extractions": 0,
                    "average_processing_time": 0
                }
            }
    
    def load_master_list(self) -> Dict:
        """Load SNC master list from file"""
        try:
            with open(self.snc_master_list_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "metadata": {
                    "created": datetime.datetime.now().isoformat(),
                    "last_updated": datetime.datetime.now().isoformat()
                },
                "snc_issues_by_key": {},
                "snc_issues_by_date": {},
                "snc_issues_by_status": {},
                "snc_issues_by_priority": {},
                "snc_issues_by_assignee": {},
                "snc_issues_by_customer": {}
            }
    
    def load_update_timeline(self) -> Dict:
        """Load update timeline from file"""
        try:
            with open(self.update_timeline_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "metadata": {
                    "created": datetime.datetime.now().isoformat(),
                    "last_updated": datetime.datetime.now().isoformat()
                },
                "daily_updates": {},
                "weekly_updates": {},
                "monthly_updates": {},
                "issue_update_history": {}
            }
    
    def load_audit_log(self) -> List[Dict]:
        """Load audit log from file"""
        try:
            with open(self.snc_audit_log_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_inventory(self) -> None:
        """Save inventory to file"""
        self.inventory["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
        with open(self.inventory_path, 'w') as f:
            json.dump(self.inventory, f, indent=2)
    
    def save_master_list(self) -> None:
        """Save master list to file"""
        self.master_list["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
        with open(self.snc_master_list_path, 'w') as f:
            json.dump(self.master_list, f, indent=2)
    
    def save_update_timeline(self) -> None:
        """Save update timeline to file"""
        self.update_timeline["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
        with open(self.update_timeline_path, 'w') as f:
            json.dump(self.update_timeline, f, indent=2)
    
    def save_audit_log(self) -> None:
        """Save audit log to file"""
        with open(self.snc_audit_log_path, 'w') as f:
            json.dump(self.audit_log, f, indent=2)
    
    def is_first_pull(self) -> bool:
        """Check if this is the first pull"""
        return not self.inventory["metadata"]["first_pull_completed"]
    
    def get_all_snc_issues_count(self) -> int:
        """Get total count of all SNC issues"""
        return len(self.master_list["snc_issues_by_key"])
    
    def get_snc_issues_list(self) -> List[str]:
        """Get list of all SNC issue keys"""
        return list(self.master_list["snc_issues_by_key"].keys())
    
    def add_snc_issue_to_inventory(self, issue_data: Dict) -> None:
        """Add new SNC issue to inventory"""
        
        issue_key = issue_data.get("key", "")
        
        # Create issue record
        issue_record = SNCIssueRecord(
            issue_key=issue_key,
            summary=issue_data.get("summary", ""),
            status=issue_data.get("status", ""),
            priority=issue_data.get("priority", ""),
            assignee=issue_data.get("assignee", ""),
            reporter=issue_data.get("reporter", ""),
            created=issue_data.get("created", ""),
            updated=issue_data.get("updated", ""),
            resolved=issue_data.get("resolved", None),
            labels=issue_data.get("labels", []),
            components=issue_data.get("components", []),
            issue_type=issue_data.get("issuetype", ""),
            description=issue_data.get("description", ""),
            comments_count=len(issue_data.get("comments", [])),
            attachments_count=0,  # Would be extracted from attachments
            first_discovered=datetime.datetime.now().isoformat(),
            last_processed=datetime.datetime.now().isoformat(),
            processing_count=1,
            total_updates=0,
            update_history=[],
            intelligence_extracted=False,
            root_cause_identified=False,
            commands_extracted=[],
            solutions_identified=[],
            customer_patterns=[],
            platform_patterns=[]
        )
        
        # Add to inventory
        self.inventory["snc_issues"][issue_key] = asdict(issue_record)
        
        # Add to master list with various indexes
        self.add_to_master_list(issue_data, issue_record)
        
        # Add to update timeline
        self.add_to_update_timeline(issue_key, "created", issue_data)
        
        # Add to audit log
        self.add_to_audit_log("issue_discovered", issue_key, {
            "summary": issue_data.get("summary", ""),
            "status": issue_data.get("status", ""),
            "priority": issue_data.get("priority", ""),
            "created": issue_data.get("created", "")
        })
        
        # Update metadata
        self.inventory["metadata"]["total_snc_issues"] = len(self.inventory["snc_issues"])
        
    def add_to_master_list(self, issue_data: Dict, issue_record: SNCIssueRecord) -> None:
        """Add issue to master list with various indexes"""
        
        issue_key = issue_data.get("key", "")
        created_date = issue_data.get("created", "")[:10]  # YYYY-MM-DD format
        status = issue_data.get("status", "")
        priority = issue_data.get("priority", "")
        assignee = issue_data.get("assignee", "")
        
        # By key
        self.master_list["snc_issues_by_key"][issue_key] = {
            "summary": issue_data.get("summary", ""),
            "status": status,
            "priority": priority,
            "created": created_date,
            "updated": issue_data.get("updated", ""),
            "last_processed": issue_record.last_processed
        }
        
        # By date
        if created_date not in self.master_list["snc_issues_by_date"]:
            self.master_list["snc_issues_by_date"][created_date] = []
        self.master_list["snc_issues_by_date"][created_date].append(issue_key)
        
        # By status
        if status not in self.master_list["snc_issues_by_status"]:
            self.master_list["snc_issues_by_status"][status] = []
        self.master_list["snc_issues_by_status"][status].append(issue_key)
        
        # By priority
        if priority not in self.master_list["snc_issues_by_priority"]:
            self.master_list["snc_issues_by_priority"][priority] = []
        self.master_list["snc_issues_by_priority"][priority].append(issue_key)
        
        # By assignee
        if assignee not in self.master_list["snc_issues_by_assignee"]:
            self.master_list["snc_issues_by_assignee"][assignee] = []
        self.master_list["snc_issues_by_assignee"][assignee].append(issue_key)
        
        # By customer (extract from labels/description)
        customer = self.extract_customer_type(issue_data)
        if customer not in self.master_list["snc_issues_by_customer"]:
            self.master_list["snc_issues_by_customer"][customer] = []
        self.master_list["snc_issues_by_customer"][customer].append(issue_key)
    
    def extract_customer_type(self, issue_data: Dict) -> str:
        """Extract customer type from issue data"""
        
        labels = issue_data.get("labels", [])
        description = issue_data.get("description", "").lower()
        summary = issue_data.get("summary", "").lower()
        
        # Check labels first
        if "nee-series" in labels or "nee" in labels:
            return "NEE-series"
        elif "athena-health" in labels or "athena" in labels:
            return "Athena-Health"
        
        # Check text content
        if "nee" in description or "nee" in summary:
            return "NEE-series"
        elif "athena" in description or "healthcare" in description:
            return "Athena-Health"
        elif "data center" in description or "datacenter" in description:
            return "Data Center"
        elif "enterprise" in description or "corporate" in description:
            return "Enterprise"
        elif "service provider" in description or "isp" in description:
            return "Service Provider"
        
        return "Unknown"
    
    def add_to_update_timeline(self, issue_key: str, update_type: str, issue_data: Dict) -> None:
        """Add update to timeline"""
        
        timestamp = datetime.datetime.now().isoformat()
        date_key = timestamp[:10]  # YYYY-MM-DD
        week_key = self.get_week_key(timestamp)
        month_key = timestamp[:7]  # YYYY-MM
        
        # Create update record
        update_record = {
            "issue_key": issue_key,
            "update_type": update_type,
            "timestamp": timestamp,
            "issue_data": {
                "status": issue_data.get("status", ""),
                "priority": issue_data.get("priority", ""),
                "updated": issue_data.get("updated", ""),
                "comments_count": len(issue_data.get("comments", []))
            }
        }
        
        # Add to daily updates
        if date_key not in self.update_timeline["daily_updates"]:
            self.update_timeline["daily_updates"][date_key] = []
        self.update_timeline["daily_updates"][date_key].append(update_record)
        
        # Add to weekly updates
        if week_key not in self.update_timeline["weekly_updates"]:
            self.update_timeline["weekly_updates"][week_key] = []
        self.update_timeline["weekly_updates"][week_key].append(update_record)
        
        # Add to monthly updates
        if month_key not in self.update_timeline["monthly_updates"]:
            self.update_timeline["monthly_updates"][month_key] = []
        self.update_timeline["monthly_updates"][month_key].append(update_record)
        
        # Add to issue-specific history
        if issue_key not in self.update_timeline["issue_update_history"]:
            self.update_timeline["issue_update_history"][issue_key] = []
        self.update_timeline["issue_update_history"][issue_key].append(update_record)
    
    def get_week_key(self, timestamp: str) -> str:
        """Get week key from timestamp"""
        dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        # Get ISO week number
        week_number = dt.isocalendar()[1]
        return f"{dt.year}-W{week_number:02d}"
    
    def add_to_audit_log(self, action: str, issue_key: str, details: Dict) -> None:
        """Add entry to audit log"""
        
        audit_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action,
            "issue_key": issue_key,
            "details": details,
            "processing_run_id": self.inventory["processing_statistics"]["total_processing_runs"] + 1
        }
        
        self.audit_log.append(audit_entry)
    
    def mark_first_pull_completed(self, total_issues: int) -> None:
        """Mark first pull as completed"""
        
        self.inventory["metadata"]["first_pull_completed"] = True
        self.inventory["metadata"]["last_pull_timestamp"] = datetime.datetime.now().isoformat()
        self.inventory["metadata"]["total_snc_issues"] = total_issues
        
        # Add to audit log
        self.add_to_audit_log("first_pull_completed", "SYSTEM", {
            "total_issues": total_issues,
            "completion_timestamp": datetime.datetime.now().isoformat()
        })
        
        self.save_inventory()
        self.save_audit_log()
    
    def update_snc_issue(self, issue_key: str, issue_data: Dict, intelligence_data: Dict) -> None:
        """Update existing SNC issue with new data"""
        
        if issue_key not in self.inventory["snc_issues"]:
            # Issue not found, add as new
            self.add_snc_issue_to_inventory(issue_data)
            return
        
        # Get existing record
        existing_record = self.inventory["snc_issues"][issue_key]
        
        # Detect changes
        changes = self.detect_issue_changes(existing_record, issue_data)
        
        if changes:
            # Update record
            existing_record["updated"] = issue_data.get("updated", existing_record["updated"])
            existing_record["status"] = issue_data.get("status", existing_record["status"])
            existing_record["priority"] = issue_data.get("priority", existing_record["priority"])
            existing_record["comments_count"] = len(issue_data.get("comments", []))
            existing_record["last_processed"] = datetime.datetime.now().isoformat()
            existing_record["processing_count"] += 1
            existing_record["total_updates"] += 1
            
            # Add to update history
            existing_record["update_history"].append({
                "timestamp": datetime.datetime.now().isoformat(),
                "changes": changes,
                "intelligence_extracted": bool(intelligence_data)
            })
            
            # Update intelligence if provided
            if intelligence_data:
                existing_record["intelligence_extracted"] = True
                existing_record["commands_extracted"] = intelligence_data.get("commands_used", [])
                existing_record["solutions_identified"] = intelligence_data.get("solutions", [])
                existing_record["customer_patterns"] = intelligence_data.get("customer_patterns", [])
                existing_record["platform_patterns"] = intelligence_data.get("platform_patterns", [])
            
            # Add to update timeline
            self.add_to_update_timeline(issue_key, "updated", issue_data)
            
            # Add to audit log
            self.add_to_audit_log("issue_updated", issue_key, {
                "changes": changes,
                "new_status": issue_data.get("status", ""),
                "new_priority": issue_data.get("priority", ""),
                "intelligence_extracted": bool(intelligence_data)
            })
            
            # Update master list
            self.update_master_list_entry(issue_key, issue_data)
    
    def detect_issue_changes(self, existing_record: Dict, new_data: Dict) -> List[str]:
        """Detect changes between existing record and new data"""
        
        changes = []
        
        if existing_record["status"] != new_data.get("status", ""):
            changes.append(f"status: {existing_record['status']} -> {new_data.get('status', '')}")
        
        if existing_record["priority"] != new_data.get("priority", ""):
            changes.append(f"priority: {existing_record['priority']} -> {new_data.get('priority', '')}")
        
        if existing_record["comments_count"] != len(new_data.get("comments", [])):
            changes.append(f"comments: {existing_record['comments_count']} -> {len(new_data.get('comments', []))}")
        
        if existing_record["updated"] != new_data.get("updated", ""):
            changes.append(f"updated: {existing_record['updated']} -> {new_data.get('updated', '')}")
        
        return changes
    
    def update_master_list_entry(self, issue_key: str, issue_data: Dict) -> None:
        """Update master list entry for issue"""
        
        if issue_key in self.master_list["snc_issues_by_key"]:
            entry = self.master_list["snc_issues_by_key"][issue_key]
            entry["status"] = issue_data.get("status", entry["status"])
            entry["priority"] = issue_data.get("priority", entry["priority"])
            entry["updated"] = issue_data.get("updated", entry["updated"])
            entry["last_processed"] = datetime.datetime.now().isoformat()
    
    def get_snc_issues_by_date_range(self, start_date: str, end_date: str) -> List[str]:
        """Get SNC issues created within date range"""
        
        issues_in_range = []
        
        for date_key in self.master_list["snc_issues_by_date"]:
            if start_date <= date_key <= end_date:
                issues_in_range.extend(self.master_list["snc_issues_by_date"][date_key])
        
        return issues_in_range
    
    def get_snc_issues_updated_since(self, timestamp: str) -> List[str]:
        """Get SNC issues updated since timestamp"""
        
        updated_issues = []
        
        for issue_key, issue_data in self.master_list["snc_issues_by_key"].items():
            if issue_data.get("updated", "") >= timestamp:
                updated_issues.append(issue_key)
        
        return updated_issues
    
    def get_snc_issue_details(self, issue_key: str) -> Optional[Dict]:
        """Get detailed information about a specific SNC issue"""
        
        if issue_key in self.inventory["snc_issues"]:
            return self.inventory["snc_issues"][issue_key]
        
        return None
    
    def get_snc_statistics(self) -> Dict:
        """Get comprehensive SNC statistics"""
        
        stats = {
            "total_issues": len(self.master_list["snc_issues_by_key"]),
            "issues_by_status": {
                status: len(issues) for status, issues in self.master_list["snc_issues_by_status"].items()
            },
            "issues_by_priority": {
                priority: len(issues) for priority, issues in self.master_list["snc_issues_by_priority"].items()
            },
            "issues_by_customer": {
                customer: len(issues) for customer, issues in self.master_list["snc_issues_by_customer"].items()
            },
            "processing_statistics": self.inventory["processing_statistics"],
            "first_pull_completed": self.inventory["metadata"]["first_pull_completed"],
            "last_pull_timestamp": self.inventory["metadata"]["last_pull_timestamp"],
            "total_processing_runs": self.inventory["processing_statistics"]["total_processing_runs"]
        }
        
        return stats
    
    def generate_snc_inventory_report(self) -> Dict:
        """Generate comprehensive SNC inventory report"""
        
        report = {
            "report_metadata": {
                "generated_at": datetime.datetime.now().isoformat(),
                "total_snc_issues": len(self.master_list["snc_issues_by_key"]),
                "first_pull_completed": self.inventory["metadata"]["first_pull_completed"],
                "last_pull_timestamp": self.inventory["metadata"]["last_pull_timestamp"]
            },
            "snc_summary": {
                "total_issues": len(self.master_list["snc_issues_by_key"]),
                "issues_by_status": self.master_list["snc_issues_by_status"],
                "issues_by_priority": self.master_list["snc_issues_by_priority"],
                "issues_by_customer": self.master_list["snc_issues_by_customer"]
            },
            "processing_timeline": {
                "daily_updates": len(self.update_timeline["daily_updates"]),
                "weekly_updates": len(self.update_timeline["weekly_updates"]),
                "monthly_updates": len(self.update_timeline["monthly_updates"])
            },
            "recent_activity": {
                "last_24_hours": self.get_recent_activity_count(1),
                "last_7_days": self.get_recent_activity_count(7),
                "last_30_days": self.get_recent_activity_count(30)
            },
            "audit_summary": {
                "total_audit_entries": len(self.audit_log),
                "recent_actions": self.audit_log[-10:] if len(self.audit_log) > 10 else self.audit_log
            }
        }
        
        return report
    
    def get_recent_activity_count(self, days: int) -> int:
        """Get count of recent activity"""
        
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()
        count = 0
        
        for date_key in self.update_timeline["daily_updates"]:
            if date_key >= cutoff_date[:10]:
                count += len(self.update_timeline["daily_updates"][date_key])
        
        return count
    
    def export_snc_master_list(self) -> Dict:
        """Export complete SNC master list"""
        
        export_data = {
            "export_metadata": {
                "exported_at": datetime.datetime.now().isoformat(),
                "total_issues": len(self.master_list["snc_issues_by_key"]),
                "export_type": "complete_master_list"
            },
            "snc_issues": self.master_list["snc_issues_by_key"],
            "indexes": {
                "by_date": self.master_list["snc_issues_by_date"],
                "by_status": self.master_list["snc_issues_by_status"],
                "by_priority": self.master_list["snc_issues_by_priority"],
                "by_customer": self.master_list["snc_issues_by_customer"]
            }
        }
        
        return export_data

if __name__ == "__main__":
    # Example usage
    knowledge_dir = Path("C:/Users/Prasanth_Sasidharan/OneDrive - Dell Technologies/Documents/AI/Devin/showtech_analyse/knowledge")
    
    inventory_manager = SNCInventoryManager(knowledge_dir)
    
    # Check if first pull
    if inventory_manager.is_first_pull():
        print("First pull detected - will process all SNC issues")
    else:
        print(f"Incremental update - {inventory_manager.get_all_snc_issues_count()} SNC issues in inventory")
    
    # Get statistics
    stats = inventory_manager.get_snc_statistics()
    print(f"SNC Statistics: {stats}")
    
    # Generate report
    report = inventory_manager.generate_snc_inventory_report()
    print(f"Inventory Report: {report}")