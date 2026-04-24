# SONiC ShowTech Auto-Analysis - Complete Automatic Skill Invocation Guide

## Overview

This guide provides the simplest way to analyze new showtech archives automatically against all appropriate skills. The system automatically detects relevant issues and invokes the right skills without manual intervention.

## Quick Start - One Command Analysis

### Method 1: Complete Auto-Analysis (Recommended)
```bash
cd "C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse\skills"

# Feed your showtech and get automatic analysis
python sonic_principal_intelligence_complete.py "C:\path\to\your\showtech.tar.gz"
```

### Method 2: Deep Dive Auto-Analysis
```bash
cd "C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse\skills"

# Comprehensive analysis with all skills
python sonic_comprehensive_deep_dive_analyzer.py "C:\path\to\your\showtech.tar.gz"
```

### Method 3: Multi-Instance Auto-Analysis
```bash
cd "C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse\skills"

# Analysis with 284-archive intelligence
python sonic_multi_instance_analyzer.py "C:\path\to\your\showtech.tar.gz"
```

## What Happens Automatically

### Automatic Skill Detection
The system automatically:
- **Analyzes showtech content** to identify relevant issues
- **Invokes appropriate skills** based on detected patterns
- **Applies 284-archive intelligence** for enhanced accuracy
- **Correlates findings** across multiple skills
- **Provides comprehensive results** with confidence scores

### Skills Auto-Invoked Based on Content
```
Memory Issues Detected:
- sonic_memory_exhaustion_triage (Enhanced with Smart Memory Intelligence)
- sonic_container_health_triage
- sonic_resource_exhaustion_triage

Interface/Connectivity Issues:
- sonic_interface_connectivity_triage
- sonic_bgp_connectivity_triage
- sonic_multi_switch_correlation

Log/System Issues:
- sonic_log_analysis_triage
- sonic_log_analysis
- sonic_kernel_stability_triage
- sonic_core_dump_analysis

Performance Issues:
- sonic_performance_degradation_prediction
- sonic_temporal_pattern_analysis

Customer-Specific Analysis:
- sonic_customer_specific_triage
- sonic_service_dependency_mapping

Compatibility/Version Issues:
- sonic_version_compatibility_check
```

## Usage Examples

### Example 1: Memory Issues ShowTech
```bash
# Feed showtech with memory problems
python sonic_principal_intelligence_complete.py "memory_issues_showtech.tar.gz"

# Automatic Results:
# - Memory exhaustion triage invoked
# - Smart memory intelligence applied
# - Known issue matching (KI-001 through KI-012)
# - Cross-correlation detection
# - Memory forecasting provided
# - Container health analysis included
```

### Example 2: Interface Connectivity Issues
```bash
# Feed showtech with link flapping
python sonic_comprehensive_deep_dive_analyzer.py "interface_flap_showtech.tar.gz"

# Automatic Results:
# - Interface connectivity triage invoked
# - BGP connectivity analysis included
# - Multi-switch correlation analysis
# - Customer-specific pattern matching
# - Performance degradation assessment
```

### Example 3: General System Issues
```bash
# Feed any showtech for comprehensive analysis
python sonic_multi_instance_analyzer.py "general_showtech.tar.gz"

# Automatic Results:
# - All relevant skills invoked based on content
# - 284-archive intelligence applied
# - Cross-customer pattern analysis
# - Temporal pattern recognition
# - Comprehensive health assessment
```

## Output Files Generated

### Automatic Analysis Results
```
showtech_analysis_results/
|-- comprehensive_report.json          # All findings from all skills
|-- executive_summary.md               # High-level summary
|-- memory_analysis.json               # Detailed memory findings
|-- connectivity_analysis.json         # Interface/BGP findings
|-- log_analysis.json                  # System log findings
|-- performance_analysis.json          # Performance metrics
|-- recommendations.md                 # Actionable recommendations
|-- confidence_scores.json             # Confidence levels
|-- 284_archive_correlation.json       # Multi-instance learning results
```

### Sample Executive Summary
```markdown
# SONiC ShowTech Analysis - Executive Summary

## Overall Health: MODERATE
## Confidence: 93% (HIGH-PROJECTED)

### Critical Findings:
1. **Memory Exhaustion Detected** - syncd container showing memory leak (KI-005)
2. **Interface Flapping** - Ethernet24 link instability detected
3. **BGP Session Instability** - 2 BGP neighbors flapping

### Recommendations:
1. **Upgrade SONiC** to version 4.3.0+ to resolve syncd memory leak
2. **Check Physical Layer** for Ethernet24 connectivity issues
3. **Monitor BGP Timers** and neighbor stability

### Skills Invoked:
- Memory Exhaustion Triage (Smart Memory Intelligence)
- Interface Connectivity Triage
- BGP Connectivity Triage
- Container Health Triage
- Performance Degradation Prediction
```

## Advanced Automatic Options

### Environment Setup (Optional)
```bash
# Set environment variables for enhanced analysis
export SONIC_AUTO_ANALYSIS=true
export SONIC_284_ARCHIVE_INTELLIGENCE=true
export SONIC_CONFIDENCE_THRESHOLD=90
export SONIC_OUTPUT_FORMAT=json
```

### Configuration File (Optional)
Create `auto_analysis_config.json`:
```json
{
    "auto_detection": {
        "enable_all_skills": true,
        "confidence_threshold": 90,
        "284_archive_intelligence": true,
        "cross_customer_analysis": true
    },
    "output_settings": {
        "generate_executive_summary": true,
        "include_recommendations": true,
        "create_detailed_reports": true,
        "export_format": ["json", "md"]
    }
}
```

### Batch Auto-Analysis
```bash
# Analyze multiple showtech files automatically
python sonic_batch_auto_analyzer.py \
    --input_dir "C:\path\to\showtechs" \
    --output_dir "C:\path\to\results" \
    --auto_detect_skills
```

## Troubleshooting

### Common Issues and Solutions

#### 1. "No skills invoked" Error
```bash
# Solution: Use comprehensive analyzer for full detection
python sonic_comprehensive_deep_dive_analyzer.py "showtech.tar.gz"
```

#### 2. "Memory analysis timeout" 
```bash
# Solution: Increase timeout for large archives
set SONIC_ANALYSIS_TIMEOUT=300
python sonic_principal_intelligence_complete.py "showtech.tar.gz"
```

#### 3. "Permission denied" error
```bash
# Solution: Run as administrator or check file permissions
# Right-click -> Run as administrator
# Or: copy showtech to accessible location
```

#### 4. "Python not found" error
```bash
# Solution: Ensure Python 3.8+ is installed and in PATH
python --version
# If not found, install Python or use full path
C:\Python39\python.exe sonic_principal_intelligence_complete.py "showtech.tar.gz"
```

## Performance Tips

### For Large ShowTech Archives
```bash
# Use memory-efficient mode
set SONIC_MEMORY_EFFICIENT=true
python sonic_multi_instance_analyzer.py "large_showtech.tar.gz"
```

### For Fast Analysis
```bash
# Use quick analysis mode
set SONIC_QUICK_ANALYSIS=true
python sonic_principal_intelligence_complete.py "showtech.tar.gz"
```

### For Maximum Accuracy
```bash
# Use comprehensive mode (default)
python sonic_comprehensive_deep_dive_analyzer.py "showtech.tar.gz"
```

## Integration Examples

### Windows PowerShell Script
```powershell
# Auto-analysis script for Windows
$ShowTechPath = "C:\Data\showtech.tar.gz"
$SkillsPath = "C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse\skills"

cd $SkillsPath
python sonic_principal_intelligence_complete.py $ShowTechPath

# Display results
Get-Content "comprehensive_report.json" | ConvertFrom-Json | Format-Table
```

### Linux Bash Script
```bash
#!/bin/bash
# Auto-analysis script for Linux

SHOWTECH_FILE="$1"
SKILLS_DIR="/path/to/showtech_analyse/skills"

if [ -z "$SHOWTECH_FILE" ]; then
    echo "Usage: $0 <showtech_file.tar.gz>"
    exit 1
fi

cd "$SKILLS_DIR"
python sonic_principal_intelligence_complete.py "$SHOWTECH_FILE"

echo "Analysis complete. Results in comprehensive_report.json"
```

### Python Integration
```python
import subprocess
import json
import os

def analyze_showtech_auto(showtech_path):
    """Analyze showtech automatically with all skills"""
    
    skills_dir = r"C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse\skills"
    
    # Run automatic analysis
    result = subprocess.run([
        "python", "sonic_principal_intelligence_complete.py", 
        showtech_path
    ], cwd=skills_dir, capture_output=True, text=True)
    
    if result.returncode == 0:
        # Load results
        with open("comprehensive_report.json", "r") as f:
            analysis_results = json.load(f)
        
        return analysis_results
    else:
        raise Exception(f"Analysis failed: {result.stderr}")

# Usage
results = analyze_showtech_auto("path/to/showtech.tar.gz")
print(f"Overall Health: {results['overall_health']}")
print(f"Confidence: {results['confidence_percentage']}%")
```

## Best Practices

### 1. File Preparation
- Ensure showtech is in `.tar.gz` format
- Verify file integrity (not corrupted)
- Use accessible file path

### 2. Analysis Workflow
- Start with `sonic_principal_intelligence_complete.py` for best results
- Review executive summary first
- Check confidence levels
- Follow recommendations in order

### 3. Result Interpretation
- **SERIAL-REDACTED-SERIAL-REDACTED confidence** (92-98%) = Most reliable
- **Critical findings** = Immediate action required
- **Known issue matches** = Specific fixes available
- **Cross-customer patterns** = Enterprise-wide insights

### 4. Follow-up Actions
- Implement high-priority recommendations
- Monitor system after changes
- Document results for future reference

## Support

### Quick Help Commands
```bash
# Get help for any analyzer
python sonic_principal_intelligence_complete.py --help

# Check system status
python sonic_system_check.py

# Validate knowledge base
python validate_knowledge_base.py
```

### Contact Information
For additional support or questions:
- Check individual skill documentation in skills directory
- Review comprehensive_analysis_log.txt for detailed analysis steps
- Contact SONiC intelligence team for advanced issues

---

## Summary

**The simplest way to analyze any showtech:**

```bash
cd "C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\showtech_analyse\skills"
python sonic_principal_intelligence_complete.py "your_showtech.tar.gz"
```

**This single command will:**
- Automatically detect all relevant issues
- Invoke appropriate skills based on content
- Apply 284-archive intelligence for accuracy
- Provide comprehensive results with recommendations
- Generate executive summary and detailed reports

No manual skill selection required - the system handles everything automatically!