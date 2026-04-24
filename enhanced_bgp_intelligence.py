#!/usr/bin/env python3
"""
Enhanced BGP Intelligence Module with SONiC Wiki Knowledge Base Integration
Incorporates comprehensive SONiC showtech analysis knowledge from Dell Enterprise wiki
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# ============================================================================
# SONiC WIKI KNOWLEDGE BASE INTEGRATION
# ============================================================================

class BGPAnalysisDepth(Enum):
    """BGP analysis depth levels based on SONiC wiki knowledge"""
    BASIC = "basic"           # Peer status, prefix counts
    STANDARD = "standard"     # Neighbor details, update groups
    COMPREHENSIVE = "comprehensive"  # EVPN, VNI, route analysis
    EXPERT = "expert"        # Forensic-level with correlations

class BGPIssueSeverity(Enum):
    """BGP issue severity classification"""
    CRITICAL = "critical"     # Session down, route withdrawal
    HIGH = "high"           # Flapping, high error rates
    MEDIUM = "medium"        # Convergence delays, warning states
    LOW = "low"             # Configuration inconsistencies
    INFO = "info"            # Operational observations

@dataclass
class BGPKnowledgePattern:
    """SONiC wiki-derived BGP knowledge pattern"""
    pattern_name: str
    file_pattern: str
    regex_pattern: str
    severity: BGPIssueSeverity
    description: str
    remediation: str
    confidence: float
    wiki_reference: str

@dataclass
class BGPForensicFinding:
    """Detailed BGP forensic finding with wiki context"""
    finding_type: str
    severity: BGPIssueSeverity
    evidence: List[str]
    files_involved: List[str]
    wiki_context: str
    remediation_steps: List[str]
    correlation_factors: List[str]
    confidence_score: float

class SONiCBGPKnowledgeBase:
    """Comprehensive SONiC BGP knowledge base from wiki intelligence"""
    
    def __init__(self):
        self.knowledge_patterns = self._initialize_wiki_patterns()
        self.file_priorities = self._initialize_file_priorities()
        self.correlation_rules = self._initialize_correlation_rules()
        self.triage_checklist = self._initialize_triage_checklist()
        
    def _initialize_wiki_patterns(self) -> Dict[str, List[BGPKnowledgePattern]]:
        """Initialize BGP patterns from SONiC wiki knowledge base"""
        
        patterns = {
            "bgp_session_issues": [
                BGPKnowledgePattern(
                    pattern_name="bgp_session_down",
                    file_pattern="bgp.summary",
                    regex_pattern=r"BGP neighbor is ([\d\.]+), remote AS (\d+),\s+state\s+(\w+)",
                    severity=BGPIssueSeverity.CRITICAL,
                    description="BGP session not in Established state",
                    remediation="Check physical connectivity, peer configuration, and firewall rules",
                    confidence=0.95,
                    wiki_reference="directory_encyclopedia.md#1.4-bgp-routing"
                ),
                BGPKnowledgePattern(
                    pattern_name="bgp_prefix_withdrawal",
                    file_pattern="bgp.summary",
                    regex_pattern=r"(\d+)\s+(?:withdrawn|withdraw)",
                    severity=BGPIssueSeverity.HIGH,
                    description="BGP prefix withdrawals detected",
                    remediation="Investigate route instability or network changes",
                    confidence=0.85,
                    wiki_reference="troubleshooting_guide.md#bgp-triage"
                )
            ],
            "evpn_vxlan_issues": [
                BGPKnowledgePattern(
                    pattern_name="evpn_vni_mismatch",
                    file_pattern="bgp.evpn.vni",
                    regex_pattern=r"VNI:\s+(\d+).*Type:\s+(\w+).*Tenant VRF:\s+(\w+)",
                    severity=BGPIssueSeverity.MEDIUM,
                    description="EVPN VNI configuration inconsistency",
                    remediation="Verify VNI-to-VRF mapping across all VTEPs",
                    confidence=0.90,
                    wiki_reference="directory_encyclopedia.md#1.4-evpn-files"
                ),
                BGPKnowledgePattern(
                    pattern_name="vxlan_tunnel_down",
                    file_pattern="bgp.evpn.vni",
                    regex_pattern=r"Client State:\s+(Down|Idle)",
                    severity=BGPIssueSeverity.HIGH,
                    description="VXLAN tunnel client not operational",
                    remediation="Check underlay connectivity and VTEP configuration",
                    confidence=0.88,
                    wiki_reference="triage_and_automation.md#evpn-checks"
                )
            ],
            "memory_resource_issues": [
                BGPKnowledgePattern(
                    pattern_name="bgp_memory_exhaustion",
                    file_pattern="frr.memory",
                    regex_pattern=r"(\d+)\s+ordinary blocks.*fragmentation",
                    severity=BGPIssueSeverity.CRITICAL,
                    description="FRR memory fragmentation affecting BGP",
                    remediation="Restart BGP process and monitor memory trends",
                    confidence=0.92,
                    wiki_reference="triage_and_automation.md#memory-health"
                )
            ],
            "configuration_issues": [
                BGPKnowledgePattern(
                    pattern_name="config_db_appl_db_mismatch",
                    file_pattern=["CONFIG_DB.json", "APPL_DB.json"],
                    regex_pattern=r"BGP_NEIGHBOR.*Ethernet\d+",
                    severity=BGPIssueSeverity.MEDIUM,
                    description="BGP configuration inconsistency between CONFIG_DB and APPL_DB",
                    remediation="Verify configuration persistence and daemon synchronization",
                    confidence=0.87,
                    wiki_reference="triage_and_automation.md#top-10-files"
                )
            ]
        }
        
        return patterns
    
    def _initialize_file_priorities(self) -> Dict[str, int]:
        """Initialize file priorities based on SONiC wiki triage guide"""
        return {
            "dump/bgp.summary": 1,                    # Top priority for BGP health
            "dump/bgp.neighbors": 2,                  # Detailed neighbor info
            "dump/bgp.evpn.summary": 3,               # EVPN overview
            "dump/bgp.evpn.vni": 4,                   # VNI state
            "dump/CONFIG_DB.json": 5,                 # Configuration reference
            "dump/APPL_DB.json": 6,                   # Application state
            "dump/frr.memory": 7,                    # Memory analysis
            "dump/frr.running_config": 8,            # FRR configuration
            "dump/bgp.evpn.routes": 9,               # Detailed routes
            "log/sairedis.rec": 10,                  # ASIC programming log
            "debugsh/orchagent/vxlanorchagent_dump.log": 11,  # VXLAN details
        }
    
    def _initialize_correlation_rules(self) -> Dict[str, List[str]]:
        """Initialize correlation rules from wiki knowledge"""
        return {
            "bgp_session_down": [
                "dump/interface.status.txt",           # Physical interface status
                "log/syslog",                         # System logs for errors
                "dump/dmesg",                         # Kernel messages
                "debugsh/orchagent/orchagent_dump.log"  # Orchagent errors
            ],
            "evpn_route_missing": [
                "dump/bgp.evpn.import_rt",            # Route target configuration
                "dump/bgp.evpn.es_detail",            # Ethernet segment details
                "debugsh/orchagent/vxlanorchagent_dump.log"  # VXLAN programming
            ],
            "memory_fragmentation": [
                "proc/meminfo",                       # System memory state
                "dump/histogram.mem.system",          # Memory trends
                "log/syslog",                         # OOM events
                "core/"                              # Core dumps
            ]
        }
    
    def _initialize_triage_checklist(self) -> List[Dict[str, Any]]:
        """Initialize BGP-specific triage checklist from wiki"""
        return [
            {
                "check_name": "bgp_peer_status",
                "description": "Check all BGP peer states",
                "command": "cat dump/bgp.summary | grep -E 'BGP neighbor|state'",
                "expected_result": "All peers in Established state",
                "priority": 1,
                "wiki_reference": "triage_and_automation.md#check-4-bgp-health"
            },
            {
                "check_name": "evpn_vni_state",
                "description": "Verify EVPN VNI operational state",
                "command": "cat dump/bgp.evpn.vni | grep -E 'VNI:|Client State:'",
                "expected_result": "All VNIs in UP state",
                "priority": 2,
                "wiki_reference": "triage_and_automation.md#evpn-checks"
            },
            {
                "check_name": "bgp_prefix_counts",
                "description": "Check BGP prefix distribution",
                "command": "cat dump/bgp.summary | grep -E 'received|advertised'",
                "expected_result": "Expected prefix counts present",
                "priority": 3,
                "wiki_reference": "troubleshooting_guide.md#bgp-analysis"
            },
            {
                "check_name": "frr_memory_health",
                "description": "Check FRR memory fragmentation",
                "command": "cat dump/frr.memory | grep 'ordinary blocks'",
                "expected_result": "< 40000 ordinary blocks",
                "priority": 4,
                "wiki_reference": "triage_and_automation.md#memory-health"
            }
        ]

class EnhancedBGPAnalyzer:
    """Enhanced BGP analyzer with SONiC wiki intelligence integration"""
    
    def __init__(self):
        self.knowledge_base = SONiCBGPKnowledgeBase()
        self.analysis_depth = BGPAnalysisDepth.COMPREHENSIVE
        self.findings: List[BGPForensicFinding] = []
        
    def analyze_bgp_with_wiki_intelligence(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform BGP analysis enhanced with SONiC wiki knowledge"""
        
        print("[BGP ANALYSIS] Starting wiki-enhanced BGP analysis...")
        
        analysis_result = {
            "analysis_metadata": {
                "timestamp": datetime.now().isoformat(),
                "analysis_depth": self.analysis_depth.value,
                "wiki_intelligence_applied": True,
                "knowledge_patterns_used": 0
            },
            "bgp_health_assessment": self._assess_bgp_health_wiki_guided(extracted_data),
            "evpn_vxlan_analysis": self._analyze_evpn_vxlan_wiki_guided(extracted_data),
            "memory_resource_analysis": self._analyze_memory_resources_wiki_guided(extracted_data),
            "configuration_consistency": self._analyze_configuration_consistency_wiki_guided(extracted_data),
            "triage_recommendations": self._generate_wiki_based_triage_recommendations(extracted_data),
            "forensic_findings": self._generate_forensic_findings_wiki_enhanced(extracted_data),
            "wiki_correlations": self._perform_wiki_based_correlations(extracted_data)
        }
        
        return analysis_result
    
    def _assess_bgp_health_wiki_guided(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess BGP health using wiki-derived patterns"""
        
        health_assessment = {
            "overall_health": "unknown",
            "peer_status": {},
            "session_analysis": {},
            "prefix_analysis": {},
            "wiki_findings": []
        }
        
        # Analyze BGP summary using wiki patterns
        bgp_summary = self._extract_file_content(extracted_data, "bgp.summary")
        if bgp_summary:
            peer_analysis = self._analyze_bgp_peers_wiki_pattern(bgp_summary)
            health_assessment["peer_status"] = peer_analysis
            
            # Determine overall health
            established_peers = sum(1 for peer in peer_analysis.values() if peer.get("state") == "Established")
            total_peers = len(peer_analysis)
            
            if total_peers == 0:
                health_assessment["overall_health"] = "no_bgp_configured"
            elif established_peers == total_peers:
                health_assessment["overall_health"] = "healthy"
            elif established_peers > total_peers * 0.5:
                health_assessment["overall_health"] = "degraded"
            else:
                health_assessment["overall_health"] = "critical"
        
        return health_assessment
    
    def _analyze_evpn_vxlan_wiki_guided(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze EVPN/VXLAN using wiki knowledge"""
        
        evpn_analysis = {
            "vni_status": {},
            "route_targets": {},
            "tunnel_health": {},
            "wiki_findings": []
        }
        
        # Analyze EVPN VNI information
        evpn_vni = self._extract_file_content(extracted_data, "bgp.evpn.vni")
        if evpn_vni:
            vni_analysis = self._analyze_evpn_vni_wiki_pattern(evpn_vni)
            evpn_analysis["vni_status"] = vni_analysis
        
        # Analyze route targets
        import_rt = self._extract_file_content(extracted_data, "bgp.evpn.import_rt")
        if import_rt:
            rt_analysis = self._analyze_route_targets_wiki_pattern(import_rt)
            evpn_analysis["route_targets"] = rt_analysis
        
        return evpn_analysis
    
    def _analyze_memory_resources_wiki_guided(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze memory resources using wiki guidance"""
        
        memory_analysis = {
            "frr_memory": {},
            "system_memory": {},
            "fragmentation_risk": "low",
            "wiki_findings": []
        }
        
        # Analyze FRR memory
        frr_memory = self._extract_file_content(extracted_data, "frr.memory")
        if frr_memory:
            memory_assessment = self._analyze_frr_memory_wiki_pattern(frr_memory)
            memory_analysis["frr_memory"] = memory_assessment
        
        # Analyze system memory
        meminfo = self._extract_file_content(extracted_data, "meminfo")
        if meminfo:
            system_memory = self._analyze_system_memory_wiki_pattern(meminfo)
            memory_analysis["system_memory"] = system_memory
        
        return memory_analysis
    
    def _analyze_configuration_consistency_wiki_guided(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze configuration consistency using wiki patterns"""
        
        config_analysis = {
            "config_db_vs_appl_db": {},
            "bgp_neighbor_consistency": {},
            "persistent_config_check": {},
            "wiki_findings": []
        }
        
        # Compare CONFIG_DB and APPL_DB
        config_db = self._extract_json_content(extracted_data, "CONFIG_DB.json")
        appl_db = self._extract_json_content(extracted_data, "APPL_DB.json")
        
        if config_db and appl_db:
            consistency_check = self._compare_config_appl_db_wiki_pattern(config_db, appl_db)
            config_analysis["config_db_vs_appl_db"] = consistency_check
        
        return config_analysis
    
    def _generate_wiki_based_triage_recommendations(self, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate triage recommendations using wiki checklist"""
        
        recommendations = []
        
        for checklist_item in self.knowledge_base.triage_checklist:
            recommendation = {
                "check_name": checklist_item["check_name"],
                "description": checklist_item["description"],
                "priority": checklist_item["priority"],
                "wiki_reference": checklist_item["wiki_reference"],
                "status": "pending",
                "automated_result": None
            }
            
            # Execute automated check if possible
            try:
                result = self._execute_triage_check(checklist_item, extracted_data)
                recommendation["automated_result"] = result
                recommendation["status"] = "completed" if result else "failed"
            except Exception as e:
                recommendation["status"] = "error"
                recommendation["error"] = str(e)
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_forensic_findings_wiki_enhanced(self, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate forensic findings enhanced with wiki intelligence"""
        
        forensic_findings = []
        
        # Apply wiki patterns to extract findings
        for category, patterns in self.knowledge_base.knowledge_patterns.items():
            for pattern in patterns:
                findings = self._apply_wiki_pattern(pattern, extracted_data)
                forensic_findings.extend(findings)
        
        # Sort findings by severity and confidence
        forensic_findings.sort(key=lambda x: (
            self._severity_priority(x["severity"]),
            -x["confidence_score"]
        ), reverse=True)
        
        return forensic_findings
    
    def _perform_wiki_based_correlations(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform correlations using wiki-derived rules"""
        
        correlations = {
            "cross_file_correlations": {},
            "temporal_correlations": {},
            "causal_relationships": {}
        }
        
        # Apply correlation rules
        for issue_type, related_files in self.knowledge_base.correlation_rules.items():
            correlation_result = self._correlate_files_for_issue(issue_type, related_files, extracted_data)
            correlations["cross_file_correlations"][issue_type] = correlation_result
        
        return correlations
    
    # Helper methods for wiki pattern analysis
    def _analyze_bgp_peers_wiki_pattern(self, bgp_summary: str) -> Dict[str, Any]:
        """Analyze BGP peers using wiki-derived patterns"""
        
        peers = {}
        
        # Extract neighbor information using wiki pattern
        neighbor_pattern = r"BGP neighbor is ([\d\.]+),\s+remote AS (\d+),\s+state\s+(\w+)"
        matches = re.findall(neighbor_pattern, bgp_summary)
        
        for neighbor_ip, remote_as, state in matches:
            peers[neighbor_ip] = {
                "remote_as": remote_as,
                "state": state,
                "health": "healthy" if state == "Established" else "unhealthy",
                "wiki_context": "BGP session state analysis per SONiC wiki"
            }
        
        return peers
    
    def _analyze_evpn_vni_wiki_pattern(self, evpn_vni: str) -> Dict[str, Any]:
        """Analyze EVPN VNI using wiki patterns"""
        
        vni_status = {}
        
        # Extract VNI information
        vni_pattern = r"VNI:\s+(\d+).*Type:\s+(\w+).*Tenant VRF:\s+(\w+).*Client State:\s+(\w+)"
        matches = re.findall(vni_pattern, evpn_vni, re.DOTALL)
        
        for vni_id, vni_type, tenant_vrf, client_state in matches:
            vni_status[vni_id] = {
                "type": vni_type,
                "tenant_vrf": tenant_vrf,
                "client_state": client_state,
                "health": "healthy" if client_state == "Up" else "unhealthy",
                "wiki_context": "EVPN VNI state analysis per SONiC wiki"
            }
        
        return vni_status
    
    def _analyze_frr_memory_wiki_pattern(self, frr_memory: str) -> Dict[str, Any]:
        """Analyze FRR memory using wiki guidance"""
        
        memory_assessment = {
            "fragmentation_risk": "low",
            "ordinary_blocks": 0,
            "wiki_guidance": "FRR memory analysis per SONiC triage guide"
        }
        
        # Extract ordinary blocks count
        blocks_pattern = r"(\d+)\s+ordinary blocks"
        match = re.search(blocks_pattern, frr_memory)
        
        if match:
            ordinary_blocks = int(match.group(1))
            memory_assessment["ordinary_blocks"] = ordinary_blocks
            
            # Apply wiki threshold
            if ordinary_blocks > 40000:
                memory_assessment["fragmentation_risk"] = "high"
            elif ordinary_blocks > 20000:
                memory_assessment["fragmentation_risk"] = "medium"
        
        return memory_assessment
    
    def _extract_file_content(self, extracted_data: Dict[str, Any], filename: str) -> Optional[str]:
        """Extract file content from extracted data"""
        # This would be implemented based on the data structure
        # For now, return None as placeholder
        return None
    
    def _extract_json_content(self, extracted_data: Dict[str, Any], filename: str) -> Optional[Dict[str, Any]]:
        """Extract JSON content from extracted data"""
        # This would be implemented based on the data structure
        # For now, return None as placeholder
        return None
    
    def _apply_wiki_pattern(self, pattern: BGPKnowledgePattern, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply wiki pattern to extract findings"""
        # This would implement pattern matching logic
        # For now, return empty list as placeholder
        return []
    
    def _execute_triage_check(self, checklist_item: Dict[str, Any], extracted_data: Dict[str, Any]) -> bool:
        """Execute automated triage check"""
        # This would implement automated check logic
        # For now, return True as placeholder
        return True
    
    def _correlate_files_for_issue(self, issue_type: str, related_files: List[str], extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Correlate files for specific issue type"""
        # This would implement correlation logic
        # For now, return empty dict as placeholder
        return {}
    
    def _compare_config_appl_db_wiki_pattern(self, config_db: Dict[str, Any], appl_db: Dict[str, Any]) -> Dict[str, Any]:
        """Compare CONFIG_DB and APPL_DB using wiki patterns"""
        # This would implement comparison logic
        # For now, return empty dict as placeholder
        return {}
    
    def _analyze_route_targets_wiki_pattern(self, import_rt: str) -> Dict[str, Any]:
        """Analyze route targets using wiki patterns"""
        # This would implement RT analysis logic
        # For now, return empty dict as placeholder
        return {}
    
    def _analyze_system_memory_wiki_pattern(self, meminfo: str) -> Dict[str, Any]:
        """Analyze system memory using wiki patterns"""
        # This would implement system memory analysis
        # For now, return empty dict as placeholder
        return {}
    
    def _severity_priority(self, severity: str) -> int:
        """Get numeric priority for severity"""
        severity_map = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1,
            "info": 0
        }
        return severity_map.get(severity, 0)

# ============================================================================
# ENHANCED BGP SKILL INTEGRATION
# ============================================================================

class EnhancedBGPSkill:
    """Enhanced BGP analysis skill with wiki intelligence integration"""
    
    def __init__(self):
        self.analyzer = EnhancedBGPAnalyzer()
        self.skill_name = "enhanced_bgp_analysis_with_wiki_intelligence"
        self.skill_version = "2.0"
        self.wiki_knowledge_base = "SONiC_PowerSwitch_KnowledgeBase"
        
    def analyze_bgp_comprehensive(self, archive_path: str, analysis_depth: str = "comprehensive") -> Dict[str, Any]:
        """Perform comprehensive BGP analysis with wiki intelligence"""
        
        print(f"[ENHANCED BGP SKILL] Starting comprehensive analysis with wiki intelligence")
        print(f"[ARCHIVE] {archive_path}")
        print(f"[DEPTH] {analysis_depth}")
        print(f"[WIKI KB] {self.wiki_knowledge_base}")
        
        # Set analysis depth
        self.analyzer.analysis_depth = BGPAnalysisDepth(analysis_depth)
        
        # Extract archive (placeholder - would implement actual extraction)
        extracted_data = self._extract_archive_data(archive_path)
        
        # Perform wiki-enhanced analysis
        analysis_result = self.analyzer.analyze_bgp_with_wiki_intelligence(extracted_data)
        
        # Add skill metadata
        analysis_result["skill_metadata"] = {
            "skill_name": self.skill_name,
            "skill_version": self.skill_version,
            "wiki_knowledge_base": self.wiki_knowledge_base,
            "analysis_timestamp": datetime.now().isoformat(),
            "wiki_patterns_applied": len(self.analyzer.knowledge_base.knowledge_patterns),
            "triage_checks_executed": len(self.analyzer.knowledge_base.triage_checklist)
        }
        
        return analysis_result
    
    def _extract_archive_data(self, archive_path: str) -> Dict[str, Any]:
        """Extract data from archive (placeholder implementation)"""
        # This would implement actual archive extraction
        # For now, return empty dict as placeholder
        return {}

# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Example usage of enhanced BGP skill
    skill = EnhancedBGPSkill()
    
    # Perform analysis
    result = skill.analyze_bgp_comprehensive(
        archive_path="sonic_dump_example.tar.gz",
        analysis_depth="comprehensive"
    )
    
    print("Enhanced BGP Analysis with Wiki Intelligence:")
    print(json.dumps(result, indent=2, default=str))