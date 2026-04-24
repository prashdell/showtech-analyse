#!/usr/bin/env python3
"""
SNC JIRA Intelligence Processing System
Processes extracted JIRA intelligence and updates knowledge bases
"""

import json
import re
import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict, Counter
from pathlib import Path

@dataclass
class IssueIntelligence:
    """Structure for extracted issue intelligence"""
    issue_key: str
    summary: str
    description: str
    comments: List[Dict]
    root_cause: str
    rca: str
    commands_used: List[str]
    solutions: List[str]
    customer_info: Dict
    platform_info: Dict
    timestamp: str
    status: str
    priority: str
    labels: List[str]

class SNCIntelligenceProcessor:
    """Main processor for SNC JIRA intelligence"""
    
    def __init__(self):
        # Updated paths for correct directory structure
        self.base_dir = Path("C:/Users/Prasanth_Sasidharan/OneDrive - Dell Technologies/Documents/AI/Devin/showtech_analyse")
        self.knowledge_dir = self.base_dir / "knowledge"
        self.knowledge_base_path = self.knowledge_dir / "snc_intelligence_base.json"
        
        # Ensure directories exist
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        self.knowledge_base = self.load_knowledge_base()
        self.pattern_matchers = self.initialize_pattern_matchers()
    
    def load_knowledge_base(self) -> Dict:
        """Load existing knowledge base"""
        try:
            with open(self.knowledge_base_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.create_empty_knowledge_base()
    
    def create_empty_knowledge_base(self) -> Dict:
        """Create empty knowledge base structure"""
        return {
            "metadata": {
                "version": "1.0",
                "created": datetime.datetime.now().isoformat(),
                "source": "SNC JIRA Project",
                "total_issues_processed": 0,
                "last_updated": datetime.datetime.now().isoformat()
            },
            "root_cause_patterns": {},
            "command_patterns": {},
            "solution_patterns": {},
            "customer_patterns": {},
            "platform_patterns": {},
            "temporal_patterns": {},
            "correlation_patterns": {}
        }
    
    def initialize_pattern_matchers(self) -> Dict:
        """Initialize pattern matching dictionaries"""
        return {
            "memory_patterns": [
                "memory leak", "out of memory", "memory exhaustion", "oom",
                "memory usage", "memory allocation", "memory fragmentation",
                "high memory", "memory pressure", "memory threshold"
            ],
            "interface_patterns": [
                "link flap", "interface down", "port flapping", "connectivity loss",
                "interface error", "port down", "link failure", "interface reset",
                "temperature", "thermal", "overheating", "port temperature"
            ],
            "routing_patterns": [
                "bgp down", "routing loop", "route missing", "neighbor down",
                "routing table", "bgp neighbor", "ospf", "route convergence",
                "routing protocol", "neighbor adjacency", "route flap"
            ],
            "service_patterns": [
                "service crash", "container restart", "process killed", "service failure",
                "service down", "container crash", "process restart", "daemon failure",
                "service restart", "systemd", "docker", "container failure"
            ],
            "hardware_patterns": [
                "hardware failure", "asic error", "port failure", "power issue",
                "hardware fault", "asic reset", "port error", "power supply",
                "fan failure", "temperature sensor", "hardware malfunction"
            ]
        }
    
    def process_issue_intelligence(self, issue_data: Dict) -> IssueIntelligence:
        """Process single issue intelligence"""
        
        # Extract text intelligence
        description_intel = self.extract_text_intelligence(issue_data.get('description', ''))
        comments_intel = [self.extract_text_intelligence(comment.get('body', '')) 
                         for comment in issue_data.get('comments', [])]
        
        # Extract commands
        all_text = issue_data.get('description', '') + ' ' + \
                 ' '.join([comment.get('body', '') for comment in issue_data.get('comments', [])])
        commands = self.extract_commands_from_text(all_text)
        
        # Extract solutions
        solutions = self.extract_solutions_from_text(all_text)
        
        # Extract customer info
        customer_info = self.extract_customer_intelligence(all_text)
        
        # Extract platform info
        platform_info = self.extract_platform_intelligence(all_text)
        
        return IssueIntelligence(
            issue_key=issue_data.get('key', ''),
            summary=issue_data.get('summary', ''),
            description=issue_data.get('description', ''),
            comments=issue_data.get('comments', []),
            root_cause=self.identify_root_cause(all_text),
            rca=self.extract_rca_analysis(issue_data.get('comments', [])),
            commands_used=commands,
            solutions=solutions,
            customer_info=customer_info,
            platform_info=platform_info,
            timestamp=issue_data.get('created', ''),
            status=issue_data.get('status', ''),
            priority=issue_data.get('priority', ''),
            labels=issue_data.get('labels', [])
        )
    
    def extract_text_intelligence(self, text: str) -> Dict:
        """Extract structured intelligence from text"""
        
        intelligence = {
            "root_cause_indicators": self.extract_root_cause_indicators(text),
            "commands_mentioned": self.extract_commands_from_text(text),
            "symptoms_described": self.extract_symptoms(text),
            "solutions_attempted": self.extract_solutions_from_text(text),
            "customer_context": self.extract_customer_context(text),
            "platform_information": self.extract_platform_info(text),
            "environment_details": self.extract_environment_info(text),
            "error_messages": self.extract_error_messages(text),
            "performance_indicators": self.extract_performance_indicators(text)
        }
        
        return intelligence
    
    def extract_root_cause_indicators(self, text: str) -> Dict:
        """Extract root cause indicators from text"""
        
        found_patterns = {}
        
        for category, patterns in self.pattern_matchers.items():
            found_patterns[category] = []
            for pattern in patterns:
                if pattern.lower() in text.lower():
                    # Extract context around the pattern
                    context = self.extract_pattern_context(text, pattern)
                    found_patterns[category].append({
                        "pattern": pattern,
                        "context": context,
                        "frequency": text.lower().count(pattern.lower())
                    })
        
        return found_patterns
    
    def extract_pattern_context(self, text: str, pattern: str, context_size: int = 100) -> str:
        """Extract context around a pattern"""
        
        pattern_lower = pattern.lower()
        text_lower = text.lower()
        
        index = text_lower.find(pattern_lower)
        if index == -1:
            return ""
        
        start = max(0, index - context_size)
        end = min(len(text), index + len(pattern) + context_size)
        
        return text[start:end].strip()
    
    def extract_commands_from_text(self, text: str) -> List[str]:
        """Extract CLI commands from text"""
        
        command_patterns = [
            r"show tech-support",
            r"show memory",
            r"show interface",
            r"show process",
            r"show log",
            r"show version",
            r"show running-config",
            r"show startup-config",
            r"show vlan",
            r"show bgp",
            r"show ospf",
            r"show ip route",
            r"show system",
            r"show environment",
            r"show temperature",
            r"show clock",
            r"show users",
            r"restart service",
            r"clear counters",
            r"clear interface",
            r"configure terminal",
            r"set interface",
            r"add vlan",
            r"delete vlan",
            r"reload",
            r"shutdown",
            r"no shutdown",
            r"reset port",
            r"clear bgp",
            r"clear ospf"
        ]
        
        extracted_commands = []
        for pattern in command_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            extracted_commands.extend(matches)
        
        return list(set(extracted_commands))  # Remove duplicates
    
    def extract_symptoms(self, text: str) -> List[str]:
        """Extract symptoms from text"""
        
        symptom_patterns = [
            "slow response", "high cpu", "memory usage", "packet loss",
            "connection timeout", "interface down", "link flap", "error message",
            "crash", "restart", "hang", "freeze", "unresponsive", "degraded performance"
        ]
        
        found_symptoms = []
        for symptom in symptom_patterns:
            if symptom.lower() in text.lower():
                found_symptoms.append(symptom)
        
        return found_symptoms
    
    def extract_solutions_from_text(self, text: str) -> List[str]:
        """Extract solutions from text"""
        
        solution_patterns = [
            "restart the service", "reboot the device", "upgrade firmware",
            "apply patch", "clear configuration", "reset to defaults",
            "replace hardware", "update configuration", "disable feature",
            "enable feature", "modify setting", "increase memory",
            "add monitoring", "implement workaround", "apply fix"
        ]
        
        found_solutions = []
        for solution in solution_patterns:
            if solution.lower() in text.lower():
                found_solutions.append(solution)
        
        return found_solutions
    
    def extract_customer_context(self, text: str) -> Dict:
        """Extract customer context from text"""
        
        context = {
            "customer_type": "",
            "deployment_size": "",
            "industry": "",
            "geographic_location": "",
            "performance_requirements": "",
            "compliance_needs": ""
        }
        
        # Customer type indicators
        if any(word in text.lower() for word in ["data center", "datacenter", "cloud"]):
            context["customer_type"] = "data_center"
        elif any(word in text.lower() for word in ["enterprise", "corporate", "business"]):
            context["customer_type"] = "enterprise"
        elif any(word in text.lower() for word in ["service provider", "isp", "telecom"]):
            context["customer_type"] = "service_provider"
        
        # Industry indicators
        if any(word in text.lower() for word in ["healthcare", "medical", "hospital"]):
            context["industry"] = "healthcare"
        elif any(word in text.lower() for word in ["finance", "banking", "financial"]):
            context["industry"] = "finance"
        elif any(word in text.lower() for word in ["government", "federal", "public sector"]):
            context["industry"] = "government"
        
        return context
    
    def extract_platform_intelligence(self, text: str) -> Dict:
        """Extract platform intelligence from text"""
        
        platform_info = {
            "vendor": "",
            "model": "",
            "os_version": "",
            "firmware_version": "",
            "hardware_specs": {}
        }
        
        # Vendor detection
        if any(word in text.lower() for word in ["dell", "force10", "powerconnect"]):
            platform_info["vendor"] = "dell"
        elif any(word in text.lower() for word in ["mellanox", "nvidia", "spectrum"]):
            platform_info["vendor"] = "mellanox"
        elif any(word in text.lower() for word in ["arista", "eos"]):
            platform_info["vendor"] = "arista"
        
        return platform_info
    
    def extract_environment_info(self, text: str) -> Dict:
        """Extract environment information from text"""
        
        env_info = {
            "temperature": "",
            "humidity": "",
            "power_status": "",
            "cooling_status": "",
            "rack_location": ""
        }
        
        # Temperature extraction
        temp_patterns = [
            r"(\d+)\s*°C",
            r"(\d+)\s*celsius",
            r"temperature\s*[:=]\s*(\d+)",
            r"temp\s*[:=]\s*(\d+)"
        ]
        
        for pattern in temp_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                env_info["temperature"] = matches[0] + "°C"
                break
        
        return env_info
    
    def extract_error_messages(self, text: str) -> List[str]:
        """Extract error messages from text"""
        
        error_patterns = [
            r"error[:\s]+(.+)",
            r"failed[:\s]+(.+)",
            r"exception[:\s]+(.+)",
            r"critical[:\s]+(.+)",
            r"fatal[:\s]+(.+)",
            r"panic[:\s]+(.+)"
        ]
        
        errors = []
        for pattern in error_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            errors.extend(matches)
        
        return errors
    
    def extract_performance_indicators(self, text: str) -> Dict:
        """Extract performance indicators from text"""
        
        indicators = {
            "cpu_usage": "",
            "memory_usage": "",
            "packet_loss": "",
            "latency": "",
            "throughput": ""
        }
        
        # CPU usage extraction
        cpu_patterns = [
            r"cpu[:\s]*(\d+)%",
            r"processor[:\s]*(\d+)%"
        ]
        
        for pattern in cpu_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                indicators["cpu_usage"] = matches[0] + "%"
                break
        
        # Memory usage extraction
        mem_patterns = [
            r"memory[:\s]*(\d+)%",
            r"ram[:\s]*(\d+)%"
        ]
        
        for pattern in mem_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                indicators["memory_usage"] = matches[0] + "%"
                break
        
        return indicators
    
    def identify_root_cause(self, text: str) -> str:
        """Identify primary root cause from text"""
        
        category_scores = {}
        
        for category, patterns in self.pattern_matchers.items():
            score = 0
            for pattern in patterns:
                score += text.lower().count(pattern.lower())
            category_scores[category] = score
        
        if not category_scores or max(category_scores.values()) == 0:
            return "unknown"
        
        return max(category_scores, key=category_scores.get)
    
    def extract_rca_analysis(self, comments: List[Dict]) -> str:
        """Extract RCA analysis from comments"""
        
        rca_comments = []
        
        for comment in comments:
            comment_text = comment.get('body', '')
            if self.is_rca_comment(comment_text):
                rca_comments.append(comment_text)
        
        if rca_comments:
            return " | ".join(rca_comments)
        
        return ""
    
    def is_rca_comment(self, comment_text: str) -> bool:
        """Identify if comment contains root cause analysis"""
        
        rca_indicators = [
            "root cause", "rca", "investigation", "analysis", "findings",
            "conclusion", "diagnosis", "troubleshooting", "determination"
        ]
        
        for indicator in rca_indicators:
            if indicator.lower() in comment_text.lower():
                return True
        
        return False
    
    def update_knowledge_base(self, intelligence: IssueIntelligence) -> None:
        """Update knowledge base with new intelligence"""
        
        # Update root cause patterns
        self.update_root_cause_patterns(intelligence)
        
        # Update command patterns
        self.update_command_patterns(intelligence)
        
        # Update solution patterns
        self.update_solution_patterns(intelligence)
        
        # Update customer patterns
        self.update_customer_patterns(intelligence)
        
        # Update platform patterns
        self.update_platform_patterns(intelligence)
        
        # Update metadata
        self.update_metadata()
    
    def update_root_cause_patterns(self, intelligence: IssueIntelligence) -> None:
        """Update root cause patterns"""
        
        root_cause = self.identify_root_cause(intelligence.description + " " + 
                                             " ".join([c.get('body', '') for c in intelligence.comments]))
        
        if root_cause != "unknown":
            if root_cause not in self.knowledge_base["root_cause_patterns"]:
                self.knowledge_base["root_cause_patterns"][root_cause] = {
                    "patterns": [],
                    "frequency": {},
                    "platform_correlations": {},
                    "solutions": {},
                    "customer_impact": {},
                    "detection_methods": {},
                    "prevention_strategies": {}
                }
            
            # Add pattern
            pattern_entry = {
                "issue_key": intelligence.issue_key,
                "summary": intelligence.summary,
                "timestamp": intelligence.timestamp,
                "platform": intelligence.platform_info.get("vendor", "unknown"),
                "customer_type": intelligence.customer_info.get("customer_type", "unknown"),
                "solutions": intelligence.solutions,
                "commands_used": intelligence.commands_used
            }
            
            self.knowledge_base["root_cause_patterns"][root_cause]["patterns"].append(pattern_entry)
    
    def update_command_patterns(self, intelligence: IssueIntelligence) -> None:
        """Update command patterns"""
        
        for command in intelligence.commands_used:
            command_category = self.categorize_command(command)
            
            if command_category not in self.knowledge_base["command_patterns"]:
                self.knowledge_base["command_patterns"][command_category] = {}
            
            if command not in self.knowledge_base["command_patterns"][command_category]:
                self.knowledge_base["command_patterns"][command_category][command] = {
                    "usage_frequency": 0,
                    "success_rate": 0,
                    "context": [],
                    "effectiveness_by_issue_type": {},
                    "common_combinations": []
                }
            
            # Update usage frequency
            self.knowledge_base["command_patterns"][command_category][command]["usage_frequency"] += 1
    
    def categorize_command(self, command: str) -> str:
        """Categorize command by type"""
        
        diagnostic_commands = ["show", "display", "list", "get"]
        troubleshooting_commands = ["restart", "clear", "reset", "reload"]
        configuration_commands = ["configure", "set", "add", "delete", "modify"]
        monitoring_commands = ["monitor", "watch", "track", "log"]
        
        command_lower = command.lower()
        
        if any(cmd in command_lower for cmd in diagnostic_commands):
            return "diagnostic_commands"
        elif any(cmd in command_lower for cmd in troubleshooting_commands):
            return "troubleshooting_commands"
        elif any(cmd in command_lower for cmd in configuration_commands):
            return "configuration_commands"
        elif any(cmd in command_lower for cmd in monitoring_commands):
            return "monitoring_commands"
        else:
            return "other_commands"
    
    def update_solution_patterns(self, intelligence: IssueIntelligence) -> None:
        """Update solution patterns"""
        
        for solution in intelligence.solutions:
            solution_category = self.categorize_solution(solution)
            
            if solution_category not in self.knowledge_base["solution_patterns"]:
                self.knowledge_base["solution_patterns"][solution_category] = {}
            
            if solution not in self.knowledge_base["solution_patterns"][solution_category]:
                self.knowledge_base["solution_patterns"][solution_category][solution] = {
                    "effectiveness": 0,
                    "usage_frequency": 0,
                    "applicable_issues": [],
                    "success_by_platform": {},
                    "side_effects": []
                }
            
            # Update usage frequency
            self.knowledge_base["solution_patterns"][solution_category][solution]["usage_frequency"] += 1
    
    def categorize_solution(self, solution: str) -> str:
        """Categorize solution by type"""
        
        immediate_fixes = ["restart", "reload", "clear", "reset"]
        configuration_changes = ["configure", "set", "modify", "update"]
        hardware_actions = ["replace", "rma", "hardware", "physical"]
        software_updates = ["upgrade", "patch", "install", "update"]
        
        solution_lower = solution.lower()
        
        if any(fix in solution_lower for fix in immediate_fixes):
            return "immediate_fixes"
        elif any(config in solution_lower for config in configuration_changes):
            return "configuration_changes"
        elif any(hw in solution_lower for hw in hardware_actions):
            return "hardware_actions"
        elif any(sw in solution_lower for sw in software_updates):
            return "software_updates"
        else:
            return "other_solutions"
    
    def update_customer_patterns(self, intelligence: IssueIntelligence) -> None:
        """Update customer patterns"""
        
        customer_type = intelligence.customer_info.get("customer_type", "unknown")
        
        if customer_type != "unknown":
            if customer_type not in self.knowledge_base["customer_patterns"]["customer_types"]:
                self.knowledge_base["customer_patterns"]["customer_types"][customer_type] = {
                    "common_issues": [],
                    "platform_preference": [],
                    "scale_characteristics": "",
                    "tolerance_level": "",
                    "issue_count": 0
                }
            
            # Update issue count
            self.knowledge_base["customer_patterns"]["customer_types"][customer_type]["issue_count"] += 1
            
            # Add common issues
            root_cause = self.identify_root_cause(intelligence.description + " " + 
                                                 " ".join([c.get('body', '') for c in intelligence.comments]))
            if root_cause != "unknown":
                if root_cause not in self.knowledge_base["customer_patterns"]["customer_types"][customer_type]["common_issues"]:
                    self.knowledge_base["customer_patterns"]["customer_types"][customer_type]["common_issues"].append(root_cause)
    
    def update_platform_patterns(self, intelligence: IssueIntelligence) -> None:
        """Update platform patterns"""
        
        platform = intelligence.platform_info.get("vendor", "unknown")
        
        if platform != "unknown":
            if platform not in self.knowledge_base["platform_patterns"]:
                self.knowledge_base["platform_patterns"][platform] = {
                    "common_issues": [],
                    "strengths": [],
                    "weaknesses": [],
                    "issue_count": 0
                }
            
            # Update issue count
            self.knowledge_base["platform_patterns"][platform]["issue_count"] += 1
            
            # Add common issues
            root_cause = self.identify_root_cause(intelligence.description + " " + 
                                                 " ".join([c.get('body', '') for c in intelligence.comments]))
            if root_cause != "unknown":
                if root_cause not in self.knowledge_base["platform_patterns"][platform]["common_issues"]:
                    self.knowledge_base["platform_patterns"][platform]["common_issues"].append(root_cause)
    
    def update_metadata(self) -> None:
        """Update knowledge base metadata"""
        
        self.knowledge_base["metadata"]["total_issues_processed"] += 1
        self.knowledge_base["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
    
    def save_knowledge_base(self) -> None:
        """Save knowledge base to file"""
        
        with open(self.knowledge_base_path, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
    
    def process_batch_intelligence(self, issues_data: List[Dict]) -> None:
        """Process batch of issue intelligence"""
        
        for issue_data in issues_data:
            intelligence = self.process_issue_intelligence(issue_data)
            self.update_knowledge_base(intelligence)
        
        self.save_knowledge_base()

if __name__ == "__main__":
    # Example usage
    processor = SNCIntelligenceProcessor()
    
    # Process sample issue
    sample_issue = {
        "key": "SNC-12345",
        "summary": "Memory leak in syncd process",
        "description": "System experiencing memory leak in syncd process after 7 days of uptime",
        "comments": [
            {"body": "Root cause appears to be memory allocation issue in syncd"},
            {"body": "Restart service resolved the issue temporarily"}
        ],
        "created": "2026-04-14T10:00:00Z",
        "status": "Resolved",
        "priority": "High",
        "labels": ["memory", "bug"]
    }
    
    intelligence = processor.process_issue_intelligence(sample_issue)
    processor.update_knowledge_base(intelligence)
    processor.save_knowledge_base()
    
    print("Intelligence processed and knowledge base updated")