---
name: sonic_vlan_configuration_analyzer
description: Specialized skill for analyzing SONiC VLAN configuration issues, reserved VLAN conflicts, and trunk port configuration problems
---

# SONiC VLAN Configuration Analyzer

## Overview

This skill specializes in **analyzing SONiC VLAN configuration issues** with focus on:
- Reserved VLAN conflicts and validation
- Trunk port allowed VLAN configuration
- VLAN manager and interface configuration interactions
- CLI command processing and validation logic

## When to Invoke

Invoke this skill when analyzing:

- VLAN configuration errors and validation failures
- "One or more given vlans is a reserved vlan" errors
- Trunk port configuration issues
- Reserved VLAN modification impacts
- VLAN manager and interface configuration conflicts
- CLI command validation problems

## Core Analysis Capabilities

### 1. VLAN Configuration Analysis
- **Reserved VLAN Validation**: Analyze reserved VLAN settings and conflicts
- **Trunk Port Configuration**: Examine switchport trunk allowed VLAN logic
- **VLAN Range Processing**: Validate VLAN range expansion and validation
- **Interface State Analysis**: Check interface configuration consistency

### 2. Configuration Database Analysis
- **CONFIG_DB VLAN Table**: Analyze VLAN configuration and reservations
- **INTERFACE Table**: Examine interface VLAN membership and settings
- **VLAN_MEMBER Table**: Validate VLAN-to-interface associations
- **VLAN_SUB_INTERFACE**: Check sub-interface VLAN configurations

### 3. CLI Command Processing
- **Command Validation Logic**: Analyze CLI parser and validation routines
- **Error Message Generation**: Trace error sources and conditions
- **Command Expansion**: Examine how "all" keyword gets expanded to VLAN ranges
- **Reserved VLAN Checking**: Validate reserved VLAN exclusion logic

## Key Files for Analysis

### Showtech Bundle Priority Files
```
High Priority:
- dump/CONFIG_DB.json - Current VLAN and interface configuration
- dump/VLAN_TABLE.json - VLAN table configuration
- dump/INTERFACE_TABLE.json - Interface configuration
- log/syslog* - System logs with VLAN configuration errors
- dump/bash_history.admin - Command execution history

Medium Priority:
- dump/VLAN_MEMBER_TABLE.json - VLAN membership details
- log/vlanmgrd.log - VLAN manager daemon logs
- log/swss.rec - Switch state service recording
- log/sonic.cfg - SONiC configuration files
- dump/redis-cli-VLAN_DB.txt - VLAN database contents

Analysis Focus:
- Reserved VLAN configuration and validation
- Trunk port allowed VLAN processing
- CLI command expansion and validation
- Error message generation and tracing
```

### VLAN Configuration Analysis
```
Key Configuration Areas:
- Reserved VLAN settings in CONFIG_DB
- Interface trunk port configurations
- VLAN_MEMBER table associations
- CLI command processing logs

Critical Files:
- CONFIG_DB|VLAN_TABLE - VLAN definitions and reservations
- CONFIG_DB|INTERFACE_TABLE - Interface configurations
- CONFIG_DB|VLAN_MEMBER_TABLE - VLAN-to-interface mappings
- vlanmgrd logs - VLAN manager operations
- CLI history - Command execution patterns
```

## Problem Analysis Framework

### NEE-13385 Specific Analysis

**Issue Classification**: VLAN Configuration Validation Error  
**Root Cause**: Reserved VLAN validation logic in trunk port configuration  
**Impact**: Cannot use "switchport trunk allowed vlan all" after reserved VLAN change  

**Technical Investigation**:
1. **Command**: `switchport trunk allowed vlan all`
2. **Error**: "%Error: One or more given vlans is a reserved vlan"
3. **Condition**: Occurs after reserved VLAN modification
4. **Expected Behavior**: Should exclude reserved VLANs automatically

### VLAN Configuration Deep Dive

**Reserved VLAN Logic**:
```bash
# Current problematic behavior
switchport trunk allowed vlan all
# Expands to: 1-4094 (including reserved VLAN)
# Error: One or more given vlans is a reserved vlan

# Expected behavior
switchport trunk allowed vlan all
# Should expand to: 1-4094 excluding reserved VLANs
# Should work without error
```

**Configuration Analysis**:
```json
// CONFIG_DB|VLAN_TABLE
{
    "VLAN_TABLE": {
        "Vlan1": {
            "vlanid": "1",
            "name": "default",
            "admin_status": "up"
        },
        "Vlan4094": {
            "vlanid": "4094", 
            "name": "reserved",
            "admin_status": "up"
        }
    }
}

// CONFIG_DB|INTERFACE_TABLE
{
    "INTERFACE_TABLE": {
        "Ethernet1": {
            "vlan": "1"
        },
        "PortChannel1": {
            "vlan": "1"
        }
    }
}
```

## Solution Development

### Immediate Workarounds

**Alternative Commands**:
```bash
# Use explicit VLAN range excluding reserved
switchport trunk allowed vlan 1-4093
# Works if reserved VLAN is 4094

# Check current reserved VLAN
show vlan brief
# Identify reserved VLAN and exclude manually

# Use specific VLAN list
switchport trunk allowed vlan 1,10,20,30
# Explicit configuration avoids validation issues
```

**Configuration Workarounds**:
```python
# Python script to generate allowed VLAN list
def generate_trunk_allowed_vlans(reserved_vlan):
    """Generate VLAN list excluding reserved VLAN"""
    all_vlans = range(1, 4095)
    allowed_vlans = [str(v) for v in all_vlans if v != reserved_vlan]
    return ','.join(allowed_vlans)

# Usage
reserved_vlan = get_reserved_vlan()
allowed_vlans = generate_trunk_allowed_vlans(reserved_vlan)
print(f"switchport trunk allowed vlan {allowed_vlans}")
```

### Long-term Solutions

**Option 1: CLI Validation Enhancement**
- Modify VLAN validation logic to exclude reserved VLANs from "all" expansion
- Update CLI parser to handle "all" keyword with reserved VLAN awareness
- Implement smart VLAN range expansion

**Option 2: VLAN Manager Update**
- Enhance VLAN manager to handle reserved VLAN exclusion automatically
- Update VLAN_MEMBER table validation logic
- Implement configuration validation with reserved VLAN awareness

**Option 3: Configuration Database Enhancement**
- Add reserved VLAN metadata to CONFIG_DB
- Implement automatic exclusion in interface configuration
- Add validation at database level

## Implementation Strategy

### Phase 1: Investigation
- Extract and analyze showtech bundle
- Review VLAN manager source code
- Identify validation logic in CLI processing
- Document current vs expected behavior

### Phase 2: Development
- Modify VLAN validation functions
- Implement smart VLAN range expansion
- Update CLI command processing
- Test with various reserved VLAN configurations

### Phase 3: Testing
- Unit testing for VLAN validation
- Integration testing with interface configuration
- Regression testing for existing VLAN functionality
- Customer validation in lab environment

### Phase 4: Deployment
- Code review and merge
- Release in SONiC 4.6.0 (as planned)
- Customer communication
- Documentation updates

## Testing Framework

### VLAN Configuration Test Cases
```python
def test_vlan_all_with_reserved_vlan():
    """Test 'switchport trunk allowed vlan all' with reserved VLAN"""
    
    # Test case 1: Default reserved VLAN (4094)
    reserved_vlan = 4094
    result = expand_vlan_all(reserved_vlan)
    expected = "1-4093"
    assert result == expected
    
    # Test case 2: Custom reserved VLAN (100)
    reserved_vlan = 100
    result = expand_vlan_all(reserved_vlan)
    expected = "1-99,101-4094"
    assert result == expected
    
    # Test case 3: Reserved VLAN 1
    reserved_vlan = 1
    result = expand_vlan_all(reserved_vlan)
    expected = "2-4094"
    assert result == expected

def test_vlan_validation_logic():
    """Test VLAN validation with reserved VLANs"""
    
    # Test validation passes for non-reserved VLANs
    assert validate_vlan_range("1-4093", reserved_vlan=4094) == True
    
    # Test validation fails for reserved VLAN inclusion
    assert validate_vlan_range("1-4094", reserved_vlan=4094) == False
    
    # Test validation passes with smart exclusion
    assert validate_vlan_all_smart(reserved_vlan=4094) == True
```

## Error Analysis and Debugging

### Error Message Tracing
```python
def trace_vlan_validation_error(command, reserved_vlan):
    """Trace VLAN validation error sources"""
    
    error_sources = {
        'cli_parser': check_cli_parser_validation(command),
        'vlan_manager': check_vlan_manager_validation(command),
        'config_db': check_config_db_validation(command),
        'interface_mgr': check_interface_manager_validation(command)
    }
    
    return {
        'command': command,
        'reserved_vlan': reserved_vlan,
        'validation_results': error_sources,
        'error_source': identify_error_source(error_sources)
    }
```

### Configuration Validation
```bash
# Debug VLAN configuration
show vlan brief
show running-config interface Ethernet1
show running-config interface PortChannel1

# Check reserved VLAN
redis-cli -n 4 HGETALL "VLAN_TABLE|Vlan4094"
redis-cli -n 4 HGETALL "RESERVED_VLAN_TABLE"

# Test command expansion
debug cli expand "switchport trunk allowed vlan all"
debug vlan validation "switchport trunk allowed vlan all"
```

## Customer Impact Assessment

### Current Impact
- **Configuration Limitation**: Cannot use "all" keyword with custom reserved VLANs
- **Manual Workaround**: Requires explicit VLAN range specification
- **Operational Overhead**: Additional configuration complexity

### Expected Resolution
- **Automation Support**: "all" keyword works with any reserved VLAN configuration
- **Configuration Simplicity**: No need for manual VLAN exclusion
- **Consistent Behavior**: Predictable "all" expansion regardless of reserved VLAN

## Success Criteria

### Functional Requirements
- [ ] "switchport trunk allowed vlan all" works with any reserved VLAN
- [ ] Automatic exclusion of reserved VLANs from "all" expansion
- [ ] Consistent behavior across different reserved VLAN configurations
- [ ] Backward compatibility maintained for existing configurations

### Technical Requirements
- [ ] CLI validation logic updated with reserved VLAN awareness
- [ ] VLAN manager enhanced for automatic exclusion
- [ ] Configuration database validation improved
- [ ] Error messages updated for clarity

---

*Skill Version: 1.0*  
*Created: April 24, 2026*  
*Focus: VLAN Configuration Issues - NEE-13385 Analysis*  
*Integration: SONiC Showtech Expert, VLAN Manager Analysis*