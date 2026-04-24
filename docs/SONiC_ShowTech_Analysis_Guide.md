# SONiC ShowTech Analysis - Complete Guide to Invoking Knowledge and Skills

## Overview

This guide documents how to invoke the comprehensive SONiC Principal Intelligence Agent knowledge and skills for analyzing new showtech archives. The system provides enterprise-grade analysis capabilities powered by 284-archive multi-instance learning and advanced smart memory intelligence.

## Prerequisites

### Required Files
- **ShowTech Archive**: `.tar.gz` file containing SONiC showtech-support data
- **Skills Directory**: `C:\Users\SERIAL-REDACTED-SERIAL-REDACTED\SERIAL-REDACTED-SERIAL-REDACTED\Documents\AI\Devin\showtech_analyse\skills\`
- **Analysis Tools**: Python scripts in the skills directory

### Environment Setup
```bash
# Navigate to skills directory
cd "C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse\skills"

# Ensure Python 3.8+ is available
python --version

# Install required dependencies (if needed)
pip install httpx
```

## Quick Start - Basic Analysis

### Method 1: Direct Skill Invocation
```bash
# Navigate to skills directory
cd "C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse\skills"

# Invoke specific skill for memory analysis
python -c "
import sys
sys.path.append('.')
from sonic_memory_exhaustion_triage.SKILL import analyze_memory_exhaustion
result = analyze_memory_exhaustion('/path/to/showtech.tar.gz')
print(result)
"
```

### Method 2: Comprehensive Analysis Tool
```bash
# Use the comprehensive deep dive analyzer
python sonic_comprehensive_deep_dive_analyzer.py /path/to/showtech.tar.gz

# Or use the multi-instance analyzer
python sonic_multi_instance_analyzer.py /path/to/showtech.tar.gz
```

### Method 3: Complete Intelligence System
```bash
# Run the complete intelligence system
python sonic_principal_intelligence_complete.py /path/to/showtech.tar.gz
```

## Detailed Skill Invocation Methods

## 1. Memory Exhaustion Triage (Enhanced with Smart Memory Intelligence)

### When to Use
- High memory usage indicators (>80%)
- OOM killer events in logs
- Memory leak patterns suspected
- Container memory pressure
- System resource exhaustion

### Invocation Methods

#### Direct Skill Call
```python
from sonic_memory_exhaustion_triage.SKILL import analyze_memory_exhaustion

# Basic analysis
result = analyze_memory_exhaustion('/path/to/showtech.tar.gz')

# Enhanced analysis with smart memory intelligence
result = analyze_memory_exhaustion(
    showtech_path='/path/to/showtech.tar.gz',
    enable_smart_intelligence=True,
    known_issue_matching=True,
    cross_correlation_detection=True,
    memory_forecasting=True,
    system_advisories=True
)
```

#### Command Line
```bash
cd "C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse\skills"

python -c "
import sys
sys.path.append('.')
from sonic_memory_exhaustion_triage.SKILL import analyze_memory_exhaustion
result = analyze_memory_exhaustion('$SHOWTECH_FILE', enable_smart_intelligence=True)
print(result)
"
```

### Expected Output
```json
{
    "analysis_type": "memory_exhaustion_triage",
    "overall_health": "Moderate",
    "memory_analysis": {
        "system_memory": {
            "total_memory_mb": 8192,
            "available_memory_mb": 2048,
            "available_percentage": 25.0,
            "memory_pressure": "Moderate"
        },
        "containers": [
            {
                "name": "syncd",
                "memory_usage_mb": 1024,
                "memory_limit_mb": 2048,
                "usage_percentage": 50.0,
                "pattern_classification": "Gradual Linear",
                "daily_growth_mb": 0.15,
                "severity": "medium",
                "known_issue_match": {
                    "id": "KI-005",
                    "title": "syncd Memory Leak / OOM",
                    "match_strength": "strong",
                    "jira_ids": ["SNC-15432", "SNC-31967"],
                    "fixed_in": "4.3.0"
                }
            }
        ],
        "leak_determinations": [
            {
                "container": "syncd",
                "verdict": "Probable Memory Leak",
                "confidence": "High",
                "explanation": "Monotonic linear growth with no downward corrections over 8 data points"
            }
        ],
        "cross_correlations": [
            {
                "id": "CC-001",
                "title": "Interface Flap Storm - Multi-Container Memory Depletion",
                "matched_containers": ["syncd", "swss", "eventd"],
                "match_count": 3
            }
        ],
        "system_advisories": [
            {
                "id": "SA-003",
                "title": "System Available Memory Critically Low",
                "severity": "High",
                "recommendation": "Monitor memory usage and consider memory upgrade"
            }
        ],
        "memory_forecast": [
            {"timeframe": "Current", "available_mb": 2048, "risk_level": "Moderate"},
            {"timeframe": "+30 days", "available_mb": 1638, "risk_level": "Concerning"},
            {"timeframe": "+60 days", "available_mb": 1229, "risk_level": "High"}
        ]
    },
    "confidence_level": "HIGH-PROJECTED",
    "confidence_percentage": 95,
    "284_archive_knowledge_applied": true,
    "multi_instance_learning": true
}
```

## 2. Interface Connectivity Triage

### When to Use
- Interface flapping or link down events
- BGP/OSPF neighbor issues
- Physical layer problems
- Port configuration issues

### Invocation
```python
from sonic_interface_connectivity_triage.SKILL import analyze_interface_connectivity

result = analyze_interface_connectivity(
    showtech_path='/path/to/showtech.tar.gz',
    enable_284_archive_intelligence=True,
    cross_customer_analysis=True
)
```

## 3. Log Analysis Triage

### When to Use
- System error analysis
- Service failure investigation
- Performance degradation
- Error pattern recognition

### Invocation
```python
from sonic_log_analysis_triage.SKILL import analyze_logs

result = analyze_logs(
    showtech_path='/path/to/showtech.tar.gz',
    temporal_pattern_analysis=True,
    284_archive_benchmark=True
)
```

## 4. Container Health Triage

### When to Use
- Container restart issues
- Service availability problems
- Container resource constraints
- Docker daemon issues

### Invocation
```python
from sonic_container_health_triage.SKILL import analyze_container_health

result = analyze_container_health(
    showtech_path='/path/to/showtech.tar.gz',
    multi_instance_learning=True
)
```

## 5. BGP Connectivity Triage

### When to Use
- BGP session flapping
- Route convergence issues
- Neighbor establishment problems
- Routing protocol errors

### Invocation
```python
from sonic_bgp_connectivity_triage.SKILL import analyze_bgp_connectivity

result = analyze_bgp_connectivity(
    showtech_path='/path/to/showtech.tar.gz',
    cross_customer_patterns=True
)
```

## Comprehensive Analysis Tools

## 1. SONiC Comprehensive Deep Dive Analyzer

### Usage
```bash
cd "C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse\skills"

python sonic_comprehensive_deep_dive_analyzer.py /path/to/showtech.tar.gz
```

### Features
- All 15 skills invoked automatically
- 284-archive knowledge integration
- Cross-correlation analysis
- Comprehensive reporting
- Performance benchmarking

### Output
- `comprehensive_analysis_report.json`
- `executive_summary.md`
- `detailed_findings.json`

## 2. Multi-Instance Analyzer

### Usage
```bash
python sonic_multi_instance_analyzer.py /path/to/showtech.tar.gz
```

### Features
- Progressive enhancement
- Instance comparison
- Pattern learning
- Confidence scoring

## 3. Complete Intelligence System

### Usage
```bash
python sonic_principal_intelligence_complete.py /path/to/showtech.tar.gz
```

### Features
- Full intelligence integration
- Smart memory analysis
- Customer-specific patterns
- Temporal analysis

## Advanced Configuration

## Environment Variables
```bash
# Set analysis depth
export SONIC_ANALYSIS_DEPTH=comprehensive

# Enable 284-archive learning
export SONIC_MULTI_INSTANCE_LEARNING=true

# Set confidence threshold
export SONIC_CONFIDENCE_THRESHOLD=90

# Enable debug mode
export SONIC_DEBUG=true
```

## Configuration Files

### analysis_config.json
```json
{
    "analysis_settings": {
        "enable_284_archive_intelligence": true,
        "enable_multi_instance_learning": true,
        "enable_cross_customer_analysis": true,
        "enable_temporal_patterns": true,
        "confidence_threshold": 90,
        "analysis_depth": "comprehensive"
    },
    "memory_analysis": {
        "enable_smart_intelligence": true,
        "known_issue_matching": true,
        "cross_correlation_detection": true,
        "memory_forecasting": true,
        "system_advisories": true
    },
    "output_settings": {
        "format": "json",
        "include_executive_summary": true,
        "include_detailed_findings": true,
        "include_recommendations": true
    }
}
```

## Batch Analysis

## Multiple ShowTech Files
```bash
# Create batch analysis script
python sonic_batch_analyzer.py \
    --input_dir /path/to/showtech_archives \
    --output_dir /path/to/results \
    --config analysis_config.json \
    --parallel 4
```

## Scheduled Analysis
```bash
# Set up automated analysis
python sonic_scheduled_analyzer.py \
    --monitor_dir /path/to/incoming_showtechs \
    --output_dir /path/to/analysis_results \
    --schedule hourly
```

## Output Interpretation

## Confidence Levels
- **SERIAL-REDACTED-SERIAL-REDACTED**: 92-98% confidence (284-archive validated)
- **HIGH**: 85-92% confidence (production validated)
- **SERIAL-REDACTED-SERIAL-REDACTED**: 70-85% confidence (limited data)
- **LOW**: <70% confidence (insufficient data)

## Risk Classifications
- **Critical**: Immediate action required
- **High**: Action required within 24 hours
- **Moderate**: Action required within 72 hours
- **Low**: Monitor and plan

## Known Issue Status
- **Resolved**: Fixed in current version
- **Upgrade Recommended**: Upgrade available
- **Pending Fix**: Fix in development
- **Unknown**: Status unclear

## Troubleshooting

## Common Issues

### 1. Skill Import Error
```bash
# Ensure skills directory is in Python path
export PYTHONPATH="$PYTHONPATH:/path/to/skills"
```

### 2. Memory Analysis Timeout
```bash
# Increase timeout for large archives
export SONIC_ANALYSIS_TIMEOUT=300
```

### 3. 284-Archive Knowledge Not Loading
```bash
# Verify knowledge files exist
ls -la /path/to/skills/*_knowledge.json

# Rebuild knowledge base
python rebuild_284_archive_knowledge.py
```

## Performance Optimization

## Memory Usage
- Use incremental analysis for large archives
- Enable memory-efficient mode
- Clear cache between analyses

## Processing Speed
- Use parallel processing for batch analysis
- Enable SSD caching
- Optimize analysis depth

## Integration with Other Systems

## API Integration
```python
import requests

# Submit showtech for analysis
response = requests.post(
    'http://localhost:8080/api/analyze',
    files={'showtech': open('/path/to/showtech.tar.gz', 'rb')},
    data={'analysis_type': 'comprehensive'}
)

result = response.json()
```

## SIEM Integration
```python
# Forward findings to SIEM
import json
from datetime import datetime

findings = analyze_memory_exhaustion(showtech_path)

siem_event = {
    'timestamp': datetime.now().isoformat(),
    'source': 'sonic_intelligence',
    'severity': findings['overall_health'],
    'findings': findings['memory_analysis']
}

# Send to SIEM
send_to_siem(siem_event)
```

## Best Practices

## 1. Preparation
- Validate showtech archive integrity
- Check file permissions
- Ensure sufficient disk space

## 2. Analysis
- Start with comprehensive analysis
- Review confidence levels
- Validate findings against known issues

## 3. Follow-up
- Implement recommendations
- Monitor system after changes
- Document results and outcomes

## 4. Continuous Improvement
- Feed results back into knowledge base
- Update known issue database
- Refine analysis parameters

## Support and Maintenance

## Knowledge Base Updates
```bash
# Update 284-archive knowledge
python update_284_archive_knowledge.py

# Update known issue database
python update_known_issues.py

# Validate knowledge integrity
python validate_knowledge_base.py
```

## Performance Monitoring
```bash
# Monitor analysis performance
python monitor_analysis_performance.py

# Check knowledge base health
python check_knowledge_health.py
```

## Conclusion

The SONiC Principal Intelligence Agent provides comprehensive analysis capabilities for showtech archives. By following this guide, you can effectively invoke the knowledge and skills to identify issues, predict problems, and optimize SONiC network performance.

The system combines:
- **284-archive multi-instance learning** for pattern recognition
- **Advanced smart memory intelligence** for sophisticated analysis
- **Cross-customer correlation** for enterprise insights
- **Temporal pattern analysis** for predictive capabilities
- **Production-validated accuracy** for reliable results

For additional support or questions, refer to the individual skill documentation or contact the SONiC intelligence team.