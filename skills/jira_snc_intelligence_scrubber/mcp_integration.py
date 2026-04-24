#!/usr/bin/env python3
"""
SNC JIRA Intelligence Scrubber - MCP Integration Wrapper
Direct MCP integration for real SNC and NEE data fetching
"""

import json
import sys
from pathlib import Path

def fetch_snc_data():
    """Fetch real SNC and NEE data using MCP tools"""
    
    print("="*80)
    print("SNC JIRA Intelligence Scrubber - Real MCP Integration")
    print("="*80)
    
    # Import MCP tools - these are available in the interactive context
    try:
        from tool_calls import mcp_call_tool
        print("MCP tools loaded successfully")
    except ImportError:
        print("MCP tools not available - using sample data")
        return create_sample_data()
    
    # Fetch SNC issues
    print("\n" + "="*60)
    print("Fetching SNC Project Issues")
    print("="*60)
    
    try:
        snc_result = mcp_call_tool(
            server_name="jira-cec",
            tool_name="jira_search",
            arguments={
                "jql": "project = SNC ORDER BY updated DESC",
                "limit": 10,
                "fields": "summary,status,priority,labels,components,description,assignee,reporter,created,updated,resolved,issuetype"
            }
        )
        
        if snc_result and len(snc_result) > 0:
            snc_data = json.loads(snc_result[0]["text"])
            snc_issues = snc_data.get("issues", [])
            print(f"Successfully fetched {len(snc_issues)} SNC issues")
            
            # Get detailed information for each SNC issue
            detailed_snc_issues = []
            for issue in snc_issues[:5]:  # Limit to 5 for demo
                try:
                    issue_details = mcp_call_tool(
                        server_name="jira-cec",
                        tool_name="jira_get_issue",
                        arguments={
                            "issue_key": issue["key"],
                            "fields": "*all",
                            "comment_limit": 20,
                            "expand": "renderedFields,changelog"
                        }
                    )
                    
                    if issue_details and len(issue_details) > 0:
                        detailed_issue = json.loads(issue_details[0]["text"])
                        detailed_snc_issues.append(detailed_issue)
                        print(f"  Retrieved details for {issue['key']}: {issue['summary']}")
                    
                except Exception as e:
                    print(f"  Error fetching details for {issue['key']}: {e}")
                    detailed_snc_issues.append(issue)
        else:
            print("No SNC issues found")
            snc_issues = []
            detailed_snc_issues = []
            
    except Exception as e:
        print(f"Error fetching SNC issues: {e}")
        snc_issues = []
        detailed_snc_issues = []
    
    # Fetch NEE issues
    print("\n" + "="*60)
    print("Fetching NEE Project Issues")
    print("="*60)
    
    try:
        nee_result = mcp_call_tool(
            server_name="jira-cec",
            tool_name="jira_search",
            arguments={
                "jql": "project = NEE ORDER BY updated DESC",
                "limit": 10,
                "fields": "summary,status,priority,labels,components,description,assignee,reporter,created,updated,resolved,issuetype"
            }
        )
        
        if nee_result and len(nee_result) > 0:
            nee_data = json.loads(nee_result[0]["text"])
            nee_issues = nee_data.get("issues", [])
            print(f"Successfully fetched {len(nee_issues)} NEE issues")
            
            # Get detailed information for each NEE issue
            detailed_nee_issues = []
            for issue in nee_issues[:5]:  # Limit to 5 for demo
                try:
                    issue_details = mcp_call_tool(
                        server_name="jira-cec",
                        tool_name="jira_get_issue",
                        arguments={
                            "issue_key": issue["key"],
                            "fields": "*all",
                            "comment_limit": 20,
                            "expand": "renderedFields,changelog"
                        }
                    )
                    
                    if issue_details and len(issue_details) > 0:
                        detailed_issue = json.loads(issue_details[0]["text"])
                        detailed_nee_issues.append(detailed_issue)
                        print(f"  Retrieved details for {issue['key']}: {issue['summary']}")
                    
                except Exception as e:
                    print(f"  Error fetching details for {issue['key']}: {e}")
                    detailed_nee_issues.append(issue)
        else:
            print("No NEE issues found")
            nee_issues = []
            detailed_nee_issues = []
            
    except Exception as e:
        print(f"Error fetching NEE issues: {e}")
        nee_issues = []
        detailed_nee_issues = []
    
    # Combine all issues
    all_issues = detailed_snc_issues + detailed_nee_issues
    
    print(f"\n" + "="*60)
    print("Data Fetching Summary")
    print("="*60)
    print(f"Total SNC Issues: {len(detailed_snc_issues)}")
    print(f"Total NEE Issues: {len(detailed_nee_issues)}")
    print(f"Total Issues: {len(all_issues)}")
    
    # Save the real data
    output_file = Path("C:/Users/Prasanth_Sasidharan/OneDrive - Dell Technologies/Documents/AI/Devin/showtech_analyse/knowledge/real_snc_nee_data.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump({
            "metadata": {
                "source": "JIRA MCP Integration",
                "timestamp": "2026-04-22",
                "snc_count": len(detailed_snc_issues),
                "nee_count": len(detailed_nee_issues),
                "total_count": len(all_issues)
            },
            "snc_issues": detailed_snc_issues,
            "nee_issues": detailed_nee_issues,
            "all_issues": all_issues
        }, f, indent=2)
    
    print(f"Real data saved to: {output_file}")
    return all_issues

def create_sample_data():
    """Create sample data when MCP is not available"""
    print("Using sample data - MCP not available")
    return []

def analyze_intelligence(issues):
    """Analyze the fetched issues for intelligence patterns"""
    
    print("\n" + "="*60)
    print("Intelligence Analysis")
    print("="*60)
    
    intelligence_summary = {
        "total_issues": len(issues),
        "root_cause_patterns": {},
        "command_effectiveness": {},
        "platform_intelligence": {},
        "customer_intelligence": {},
        "priority_distribution": {},
        "status_distribution": {}
    }
    
    if not issues:
        print("No issues to analyze")
        return intelligence_summary
    
    # Analyze patterns
    for issue in issues:
        # Extract priority
        priority = issue.get("fields", {}).get("priority", {}).get("name", "Unknown")
        intelligence_summary["priority_distribution"][priority] = intelligence_summary["priority_distribution"].get(priority, 0) + 1
        
        # Extract status
        status = issue.get("fields", {}).get("status", {}).get("name", "Unknown")
        intelligence_summary["status_distribution"][status] = intelligence_summary["status_distribution"].get(status, 0) + 1
        
        # Extract labels for patterns
        labels = issue.get("fields", {}).get("labels", [])
        for label in labels:
            if "memory" in label.lower():
                intelligence_summary["root_cause_patterns"]["memory_issues"] = intelligence_summary["root_cause_patterns"].get("memory_issues", 0) + 1
            elif "interface" in label.lower():
                intelligence_summary["root_cause_patterns"]["interface_issues"] = intelligence_summary["root_cause_patterns"].get("interface_issues", 0) + 1
            elif "bgp" in label.lower():
                intelligence_summary["root_cause_patterns"]["bgp_issues"] = intelligence_summary["root_cause_patterns"].get("bgp_issues", 0) + 1
    
    # Print analysis results
    print(f"Total Issues Analyzed: {intelligence_summary['total_issues']}")
    print(f"Priority Distribution: {intelligence_summary['priority_distribution']}")
    print(f"Status Distribution: {intelligence_summary['status_distribution']}")
    print(f"Root Cause Patterns: {intelligence_summary['root_cause_patterns']}")
    
    return intelligence_summary

if __name__ == "__main__":
    # Fetch real SNC and NEE data
    issues = fetch_snc_data()
    
    # Analyze intelligence
    intelligence = analyze_intelligence(issues)
    
    # Save intelligence analysis
    intelligence_file = Path("C:/Users/Prasanth_Sasidharan/OneDrive - Dell Technologies/Documents/AI/Devin/showtech_analyse/knowledge/intelligence_analysis.json")
    with open(intelligence_file, 'w') as f:
        json.dump(intelligence, f, indent=2)
    
    print(f"\nIntelligence analysis saved to: {intelligence_file}")
    print("\n" + "="*80)
    print("SNC JIRA Intelligence Scrubber - COMPLETED")
    print("="*80)