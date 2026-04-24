# Skill Invocation Best Practices and Guidelines

## Overview
This document provides comprehensive guidelines for skill invocation, error handling, and fallback mechanisms to ensure reliable and user-friendly skill execution.

## Skill Invocation Issues and Solutions

### Problem: Skill File Exists But Not Recognized
**Issue**: `sonic_hardware_platform_analyzer` file exists but skill system returns "skill not found"

**Root Cause**: Skill discovery mechanism limited to specific directories, not scanning subdirectories

**Solution**: Implement comprehensive skill discovery system with fallback mechanisms

### Problem: Poor Error Messages
**Issue**: Users receive generic "skill not found" errors without guidance

**Solution**: Provide actionable error messages with alternative methods

## Enhanced Skill Invocation Pattern

### Universal Skill Invoker
```python
class UniversalSkillInvoker:
    def __init__(self):
        self.skill_paths = [
            "C:\\Users\\Prasanth_Sasidharan\\.codeium\\windsurf\\skills\\",
            "C:\\Users\\Prasanth_Sasidharan\\OneDrive - Dell Technologies\\Documents\\AI\\Devin\\showtech_analyse\\skills\\",
            "C:\\Users\\Prasanth_Sasidharan\\OneDrive - Dell Technologies\\Documents\\AI\\Devin\\show_tech_extractor_docs\\"
        ]
        self.fallback_methods = ['direct', 'manual', 'template', 'import']
    
    def invoke_skill(self, skill_name, context=None, method='auto'):
        """Universal skill invocation with comprehensive fallback"""
        
    def discover_skill(self, skill_name):
        """Discover skill across all possible locations"""
        
    def execute_with_fallback(self, skill_name, skill_path, context):
        """Execute skill with multiple fallback options"""
```

### Fallback Execution Methods

#### Method 1: Direct Skill Invocation
```python
def direct_skill_invoke(skill_name, skill_path):
    """Try direct skill system invocation"""
    try:
        return skill.invoke(skill_name, skill_path)
    except Exception as e:
        log_error(f"Direct invocation failed: {e}")
        return None
```

#### Method 2: Manual Skill Execution
```python
def manual_skill_execution(skill_name, skill_path, context):
    """Execute skill manually using file content"""
    try:
        # Read skill file
        with open(skill_path, 'r') as f:
            skill_content = f.read()
        
        # Parse and execute skill logic
        return execute_skill_logic(skill_content, context)
    except Exception as e:
        log_error(f"Manual execution failed: {e}")
        return None
```

#### Method 3: Template-Based Execution
```python
def template_based_execution(skill_name, skill_path, context):
    """Execute using predefined skill templates"""
    try:
        template = get_skill_template(skill_name)
        return execute_template(template, context, skill_path)
    except Exception as e:
        log_error(f"Template execution failed: {e}")
        return None
```

#### Method 4: Python Import Execution
```python
def python_import_execution(skill_name, skill_path, context):
    """Execute skill by importing as Python module"""
    try:
        # Import skill as module
        spec = importlib.util.spec_from_file_location(skill_name, skill_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Execute skill
        return module.execute(context)
    except Exception as e:
        log_error(f"Python import execution failed: {e}")
        return None
```

## Enhanced Error Handling

### User-Friendly Error Messages
```python
class SkillErrorHandler:
    def handle_skill_not_found(self, skill_name):
        """Handle skill not found with actionable guidance"""
        
    def handle_invocation_failure(self, skill_name, error):
        """Handle invocation failure with alternatives"""
        
    def provide_fallback_options(self, skill_name):
        """Provide user with alternative options"""
```

### Error Message Templates
```python
ERROR_MESSAGES = {
    'skill_not_found': """
Skill '{skill_name}' not found in standard locations.

Available options:
1. Check skill name spelling
2. Verify skill file exists at: {skill_path}
3. Try manual execution with: python -c "execute_skill('{skill_name}')"
4. Contact support if issue persists

Available skills: {available_skills}
""",
    
    'invocation_failed': """
Skill '{skill_name}' found but invocation failed.

Error: {error}

Fallback options:
1. Manual execution available
2. Template-based execution available  
3. Python import execution available
4. Alternative skills: {alternative_skills}

Try: python -c "fallback_execute('{skill_name}')"
"""
}
```

## Skill Health Monitoring

### Health Check System
```python
class SkillHealthMonitor:
    def __init__(self):
        self.health_status = {}
        self.last_check = {}
        
    def check_skill_health(self, skill_name, skill_path):
        """Comprehensive skill health check"""
        
    def validate_skill_structure(self, skill_path):
        """Validate skill file structure"""
        
    def test_skill_execution(self, skill_name, skill_path):
        """Test skill execution with sample data"""
        
    def generate_health_report(self):
        """Generate comprehensive health report"""
```

### Health Metrics
- File existence and accessibility
- File structure validation
- Execution capability testing
- Dependency availability
- Performance benchmarks
- Error rate tracking

## Implementation Guidelines

### For Skill Developers
1. **Standardized Skill Structure**: Follow consistent file naming and structure
2. **Metadata Inclusion**: Include comprehensive metadata in skill files
3. **Error Handling**: Implement robust error handling in skill logic
4. **Testing**: Provide test cases and sample data
5. **Documentation**: Include clear usage examples and troubleshooting

### For System Administrators
1. **Skill Registry Maintenance**: Keep skill registry up to date
2. **Health Monitoring**: Regular skill health checks
3. **Performance Monitoring**: Track skill execution performance
4. **User Support**: Provide user support and training
5. **Continuous Improvement**: Regular system updates and improvements

## User Experience Improvements

### Skill Discovery Interface
```python
def list_available_skills():
    """List all available skills with health status"""
    skills = []
    for skill_path in scan_skill_directories():
        skill_name = extract_skill_name(skill_path)
        health = check_skill_health(skill_name, skill_path)
        skills.append({
            'name': skill_name,
            'path': skill_path,
            'health': health,
            'description': get_skill_description(skill_path)
        })
    return skills
```

### Interactive Skill Selection
```python
def interactive_skill_selection():
    """Interactive skill selection with guidance"""
    skills = list_available_skills()
    
    print("Available Skills:")
    for i, skill in enumerate(skills, 1):
        status = "✓" if skill['health']['status'] == 'healthy' else "✗"
        print(f"{i}. {skill['name']} {status}")
        print(f"   {skill['description']}")
        print(f"   Health: {skill['health']['status']}")
    
    choice = input("Select skill number: ")
    return execute_selected_skill(skills[int(choice)-1])
```

## Success Metrics

### Reliability Metrics
- Skill discovery success rate: > 99%
- Fallback activation success rate: > 95%
- User error resolution time: < 30 seconds
- System uptime: > 99.9%

### User Experience Metrics
- User satisfaction score: > 4.5/5
- Self-service resolution rate: > 90%
- Support ticket reduction: > 50%
- Learning curve improvement: > 40%

## Implementation Checklist

### Phase 1: Core System
- [ ] Implement comprehensive skill discovery
- [ ] Create fallback execution methods
- [ ] Add error handling and logging
- [ ] Build user-friendly error messages

### Phase 2: Health Monitoring
- [ ] Implement skill health checks
- [ ] Create performance monitoring
- [ ] Add health reporting
- [ ] Set up alerting system

### Phase 3: User Interface
- [ ] Create skill discovery interface
- [ ] Implement interactive selection
- [ ] Add skill management tools
- [ ] Provide comprehensive documentation

### Phase 4: Integration & Testing
- [ ] Integrate with existing systems
- [ ] Comprehensive testing
- [ ] User training materials
- [ ] Performance optimization

This comprehensive approach ensures that users never face skill invocation issues and always have reliable access to all available skills.