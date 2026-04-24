---
name: sonic_knowledge_integrator
description: Advanced skill for integrating SONiC knowledge base with configuration, CLI, and compatibility matrix analysis
---

# SONiC Knowledge Integrator

## Overview

This skill provides **advanced knowledge integration capabilities** for SONiC systems by combining:
- Configuration database schema analysis
- CLI command reference and syntax validation
- Version compatibility matrix management
- Release notes and documentation integration
- Platform-specific knowledge synthesis

## When to Invoke

Invoke this skill when analyzing:
- Version upgrade compatibility and planning
- Configuration validation across SONiC versions
- CLI command syntax and behavior analysis
- Platform-specific configuration requirements
- Release-specific feature changes and deprecations
- Known issue correlation and pattern recognition

## Core Integration Capabilities

### 1. Knowledge Base Integration
- **Documentation Ingestion**: Process SONiC hardware and guides documentation
- **Schema Evolution Tracking**: Monitor CONFIG_DB changes across versions
- **CLI Reference Management**: Maintain version-specific CLI command references
- **Compatibility Matrix Updates**: Track platform and version compatibility

### 2. Version-Specific Analysis
- **Upgrade Path Validation**: Analyze upgrade compatibility and risks
- **Configuration Migration**: Identify required configuration changes
- **Feature Support Tracking**: Monitor feature availability across versions
- **Known Issue Correlation**: Map issues to version/platform patterns

### 3. Platform Knowledge Synthesis
- **Hardware-Specific Knowledge**: Platform configuration requirements
- **CLI Variation Analysis**: Platform-specific CLI differences
- **Performance Characteristics**: Platform-specific performance data
- **Limitation Identification**: Platform-specific constraints and issues

## Knowledge Base Sources

### 📚 Documentation Sources
```
C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\SONiC\
├── Hardware\                    # Platform specifications and compatibility
├── Guides\                     # User guides, installation guides, release notes
│   ├── AI SONiC Guides\       # AI fabrics and enterprise SONiC guides
│   ├── Vortex IRC4\           # Enterprise SONiC documentation
│   └── Release Notes\         # Version-specific release documentation
└── Configuration\             # Configuration templates and examples
```

### 🎯 Key Documents for Analysis

#### Release Notes & Matrix Documents
- `dell-enterprise-sonic-matrix-4-5-1.pdf` - Compatibility matrix
- `dell-ai-sonic-matrix-4.5.1.pdf` - AI SONiC matrix
- `dell-enterprise-sonic-rn-451.pdf` - Release notes
- `ai-sonic-451_rn.pdf` - AI SONiC release notes

#### Configuration & CLI Documentation
- `dell-enterprise-sonic-ug-4-5-1.pdf` - User guide
- `dell-enterprise-sonic-mgmt-frame-cli-4-5-1.pdf` - CLI reference
- `ent-sonic-ug-sn-460-first.pdf` - Enterprise SONiC user guide

#### Platform-Specific Documentation
- Hardware compatibility matrices
- Platform configuration guides
- Installation and upgrade procedures

## Enhanced Analysis Capabilities

### Version Compatibility Analysis
```python
def analyze_upgrade_compatibility(from_version, to_version, platform):
    """Comprehensive upgrade compatibility analysis"""
    
    compatibility_data = {
        'upgrade_path': f"{from_version} -> {to_version}",
        'platform': platform,
        'compatibility_score': calculate_compatibility_score(from_version, to_version, platform),
        'known_issues': get_version_specific_issues(from_version, to_version, platform),
        'required_actions': get_upgrade_requirements(from_version, to_version, platform),
        'configuration_changes': get_config_changes(from_version, to_version),
        'cli_impact': analyze_cli_changes(from_version, to_version),
        'feature_changes': get_feature_changes(from_version, to_version)
    }
    
    return compatibility_data

def get_version_specific_issues(from_version, to_version, platform):
    """Get known issues for specific version upgrade"""
    
    issues = []
    
    # Check BGP docker issues (NEE-13470 pattern)
    if from_version in ['4.2.0', '4.4.1'] and to_version == '4.5.0':
        if platform in ['S5248F', 'S5232F']:
            issues.append({
                'issue': 'BGP docker startup failure',
                'pattern': 'Process zebra exited unexpectedly',
                'severity': 'High',
                'workaround': 'Manual BGP docker restart',
                'status': 'Known issue in 4.5.0'
            })
    
    # Check route-map issues
    if to_version == '4.5.0':
        issues.append({
            'issue': 'Route-map static protocol deprecation',
            'pattern': 'match source-protocol static stopped working',
            'severity': 'High',
            'workaround': 'Remove static protocol match',
            'status': 'MUST_FIX in 4.5.0'
        })
    
    return issues
```

### Configuration Knowledge Integration
```python
def get_configuration_guidance(version, feature, platform):
    """Get comprehensive configuration guidance"""
    
    guidance = {
        'version': version,
        'feature': feature,
        'platform': platform,
        'cli_syntax': get_cli_syntax(version, feature, platform),
        'config_schema': get_config_schema(version, feature),
        'validation_rules': get_validation_rules(version, feature),
        'best_practices': get_best_practices(version, feature, platform),
        'known_limitations': get_limitations(version, feature, platform),
        'migration_notes': get_migration_notes(version, feature)
    }
    
    return guidance

def get_cli_syntax(version, feature, platform):
    """Get CLI syntax with version and platform variations"""
    
    syntax_variations = {}
    
    # BGP configuration syntax
    if feature == 'BGP':
        if version.startswith('4.5'):
            syntax_variations['basic'] = """
router bgp <asn>
 bgp log neighbor changes
 bgp bestpath med missing-as-worst
 neighbor <ip> remote-as <asn>
  description <description>
  timers <connect> <holdtime>
  address-family ipv4 unicast
   route-reflector-client
  soft-reconfiguration inbound
  route-map <name> in
  route-map <name> out
  exit-address-family
 exit-address-family
exit-address-family
"""
        else:
            syntax_variations['basic'] = """
router bgp <asn>
 neighbor <ip> remote-as <asn>
  timers <connect> <holdtime>
 exit-address-family
"""
    
    return syntax_variations
```

### Release Notes Integration
```python
def analyze_release_changes(release_version):
    """Analyze changes in specific release"""
    
    release_analysis = {
        'version': release_version,
        'release_date': get_release_date(release_version),
        'new_features': get_new_features(release_version),
        'deprecated_features': get_deprecated_features(release_version),
        'bug_fixes': get_bug_fixes(release_version),
        'known_issues': get_release_known_issues(release_version),
        'security_updates': get_security_updates(release_version),
        'platform_support': get_platform_support(release_version),
        'configuration_changes': get_config_schema_changes(release_version)
    }
    
    return release_analysis

def get_new_features(release_version):
    """Get new features for specific release"""
    
    if release_version == '4.5.1':
        return [
            {
                'feature': 'Enhanced BGP stability',
                'description': 'Improved BGP docker stability and error handling',
                'impact': 'High',
                'platforms': ['S5248F', 'S5232F', 'S5448F']
            },
            {
                'feature': 'CLI rendering improvements',
                'description': 'Better CLI output formatting for automation',
                'impact': 'Medium',
                'platforms': 'All Dell platforms'
            }
        ]
    
    return []
```

## Platform-Specific Knowledge

### Dell PowerSwitch Platforms
```python
def get_platform_knowledge(platform):
    """Get platform-specific knowledge and requirements"""
    
    platform_data = {
        'S5248F': {
            'sonic_versions': ['4.2.0', '4.4.1', '4.5.0', '4.5.1'],
            'known_issues': [
                'BGP docker startup failures in 4.5.0',
                'QoS mapping upgrade requirements',
                'CLI rendering inconsistencies'
            ],
            'configuration_requirements': {
                'bgp': 'Enhanced validation required for 4.5.0+',
                'qos': 'RoCE disable/enable cycle after upgrade',
                'vlans': 'Reserved VLAN awareness needed'
            },
            'upgrade_recommendations': {
                '4.2.0 -> 4.5.1': 'Use with caution (BGP issues)',
                '4.4.1 -> 4.5.1': 'Recommended path',
                '4.5.0a -> 4.5.1': 'Recommended for bug fixes'
            }
        },
        'S5232F': {
            'sonic_versions': ['4.2.0', '4.4.1', '4.5.0', '4.5.1'],
            'known_issues': [
                'BGP docker stability issues',
                'Telemetry connection failures in some scenarios'
            ],
            'configuration_requirements': {
                'bgp': 'Stability improvements in 4.5.1',
                'telemetry': 'Schema validation fixes'
            },
            'upgrade_recommendations': {
                '4.2.0 -> 4.5.1': 'Stable with caveats',
                '4.4.1 -> 4.5.1': 'Recommended'
            }
        }
    }
    
    return platform_data.get(platform, {})
```

## Issue Correlation and Pattern Recognition

### Pattern Recognition Framework
```python
def correlate_issue_pattern(issue_data):
    """Correlate issue with known patterns"""
    
    patterns = []
    
    # Extract key information
    summary = issue_data.get('summary', '')
    description = issue_data.get('description', '')
    platform = extract_platform_from_issue(issue_data)
    version = extract_version_from_issue(issue_data)
    
    # BGP-related patterns
    if 'BGP' in summary or 'bgp' in description.lower():
        bgp_patterns = analyze_bgp_patterns(summary, description, platform, version)
        patterns.extend(bgp_patterns)
    
    # Upgrade-related patterns
    if 'upgrade' in summary.lower() or 'upgrade' in description.lower():
        upgrade_patterns = analyze_upgrade_patterns(summary, description, platform, version)
        patterns.extend(upgrade_patterns)
    
    # Configuration-related patterns
    if 'config' in summary.lower() or 'configuration' in description.lower():
        config_patterns = analyze_config_patterns(summary, description, platform, version)
        patterns.extend(config_patterns)
    
    return patterns

def analyze_bgp_patterns(summary, description, platform, version):
    """Analyze BGP-related issue patterns"""
    
    patterns = []
    
    # BGP docker failure pattern (NEE-13470)
    if 'docker' in summary.lower() and 'bgp' in summary.lower():
        if version in ['4.5.0', '4.5.0a']:
            patterns.append({
                'pattern': 'BGP_DOCKER_FAILURE',
                'description': 'BGP docker fails to start after upgrade',
                'known_causes': ['Zebra process exit', 'Supervisor termination'],
                'platforms_affected': ['S5248F', 'S5232F'],
                'versions_affected': ['4.5.0', '4.5.0a'],
                'resolution': 'Upgrade to 4.5.1 or manual intervention'
            })
    
    return patterns
```

## Automated Knowledge Updates

### Knowledge Base Maintenance
```python
def update_knowledge_with_new_release(release_info):
    """Update knowledge base with new release information"""
    
    # Process release notes
    release_notes = extract_release_notes(release_info['documentation_path'])
    
    # Update compatibility matrix
    compatibility_updates = process_compatibility_changes(release_notes)
    
    # Update CLI reference
    cli_updates = process_cli_changes(release_notes)
    
    # Update known issues
    issue_updates = process_known_issues(release_notes)
    
    # Update skills with new knowledge
    skill_updates = update_skills_with_release_knowledge(release_info)
    
    return {
        'compatibility_updates': compatibility_updates,
        'cli_updates': cli_updates,
        'issue_updates': issue_updates,
        'skill_updates': skill_updates
    }
```

### Skill Enhancement Process
```python
def enhance_skills_with_knowledge():
    """Enhance skills with integrated knowledge base"""
    
    skill_enhancements = {}
    
    # Update showtech expert with version-specific knowledge
    showtech_enhancements = {
        'version_patterns': get_version_issue_patterns(),
        'platform_knowledge': get_platform_specific_knowledge(),
        'configuration_schemas': get_config_schema_knowledge()
    }
    
    # Update JIRA access with compatibility knowledge
    jira_enhancements = {
        'upgrade_patterns': get_upgrade_issue_patterns(),
        'known_issue_correlation': get_issue_correlation_patterns(),
        'version_specific_guidance': get_version_guidance()
    }
    
    return {
        'sonic_showtech_expert': showtech_enhancements,
        'jira_snc_nee_access': jira_enhancements
    }
```

## Usage Examples

### Upgrade Planning Analysis
```python
# Analyze upgrade path
upgrade_analysis = analyze_upgrade_compatibility('4.2.0', '4.5.1', 'S5248F')

print("=== Upgrade Compatibility Analysis ===")
print(f"Compatibility Score: {upgrade_analysis['compatibility_score']}")
print(f"Known Issues: {len(upgrade_analysis['known_issues'])}")
print(f"Required Actions: {len(upgrade_analysis['required_actions'])}")

for issue in upgrade_analysis['known_issues']:
    print(f"Issue: {issue['issue']} (Severity: {issue['severity']})")
    print(f"  Workaround: {issue['workaround']}")
```

### Configuration Guidance
```python
# Get configuration guidance
guidance = get_configuration_guidance('4.5.1', 'BGP', 'S5248F')

print("=== Configuration Guidance ===")
print(f"Version: {guidance['version']}")
print(f"Feature: {guidance['feature']}")
print(f"Platform: {guidance['platform']}")

if 'cli_syntax' in guidance:
    print("CLI Syntax:")
    print(guidance['cli_syntax']['basic'])

if 'known_limitations' in guidance:
    print("Known Limitations:")
    for limitation in guidance['known_limitations']:
        print(f"  - {limitation}")
```

### Issue Pattern Correlation
```python
# Correlate JIRA issue
issue_data = {
    'summary': 'BGP docker failed to start after upgrade to 4.5.0a',
    'description': 'Process zebra exited unexpectedly',
    'platform': 'S5248F',
    'version': '4.5.0a'
}

patterns = correlate_issue_pattern(issue_data)

print("=== Issue Pattern Correlation ===")
for pattern in patterns:
    print(f"Pattern: {pattern['pattern']}")
    print(f"Description: {pattern['description']}")
    print(f"Resolution: {pattern['resolution']}")
```

## Integration with Existing Skills

### Enhanced Skill Capabilities
The knowledge integrator enhances existing skills by providing:

1. **Version-Specific Context**: Historical knowledge of version changes
2. **Platform Awareness**: Platform-specific requirements and limitations
3. **Pattern Recognition**: Known issue patterns and resolutions
4. **Configuration Guidance**: Best practices and validation rules
5. **Upgrade Intelligence**: Compatibility analysis and risk assessment

### Knowledge Sharing Framework
```python
def share_knowledge_with_skills():
    """Share knowledge base information with all skills"""
    
    knowledge_sharing = {
        'version_knowledge': get_version_knowledge(),
        'platform_knowledge': get_platform_knowledge(),
        'feature_knowledge': get_feature_knowledge(),
        'issue_patterns': get_issue_patterns(),
        'best_practices': get_best_practices()
    }
    
    return knowledge_sharing
```

## Future Enhancements

### Planned Capabilities
1. **Real-time Knowledge Updates**: Automatic ingestion of new documentation
2. **Predictive Analysis**: AI-powered issue prediction and prevention
3. **Interactive Guidance**: Context-aware configuration assistance
4. **Cross-Version Migration**: Automated configuration migration tools

### Knowledge Quality Assurance
```python
def validate_knowledge_quality():
    """Validate knowledge base quality and completeness"""
    
    quality_metrics = {
        'documentation_coverage': measure_documentation_coverage(),
        'knowledge_accuracy': validate_knowledge_accuracy(),
        'pattern_recognition_accuracy': validate_pattern_accuracy(),
        'upgrade_prediction_accuracy': validate_upgrade_predictions()
    }
    
    return quality_metrics
```

---

*Skill Version: 1.0*  
*Created: April 24, 2026*  
*Integration: SONiC Knowledge Base, Configuration Analysis, CLI Reference*  
*Scope: Knowledge Integration, Version Compatibility, Pattern Recognition*