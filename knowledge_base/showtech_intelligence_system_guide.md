# Showtech Intelligence System: Tool Issue Capture & Documentation Updates

## 🎯 **Executive Overview**

This is the intelligence system that captures tool issues during showtech ingestion and automatically triggers documentation updates when skills are invoked. It's a **comprehensive learning system** that continuously improves from every skill execution and includes **tool execution troubleshooting insights** for seamless operation.

## 🏗️ **System Architecture**

### **Core Components**
```yaml
1. Automatic Knowledge Integrator (AKI)
   - Captures lessons from every skill invocation
   - Updates skill files automatically
   - Maintains pattern databases
   - Tracks performance metrics

2. Enhanced Skill Invoker (ESI)
   - Universal skill execution with fallbacks
   - Context capture for learning
   - Error handling and recovery
   - Integration with knowledge system

3. Tool Execution Monitor (TEM)
   - Captures tool-related hiccups during execution
   - Documents Unicode encoding issues
   - Tracks archive format compatibility
   - Records system requirement insights

4. Knowledge Base Structure
   - lessons_learned/ - Individual lesson JSON files
   - patterns/ - Skill-specific pattern databases
   - performance/ - Performance tracking data
   - skill_updates/ - Update history and records
   - tool_troubleshooting/ - Tool execution insights
```

## 🔍 **Tool Issue Capture During Showtech Ingestion**

### **1. Invocation Interception**
```python
# From automatic_knowledge_integrator.py (lines 117-156)
@contextmanager
def intercept_invocation(self, skill_name: str, context: Dict[str, Any] = None):
    """
    Context manager to intercept skill invocations and capture lessons
    """
    invocation_id = self._generate_invocation_id(skill_name)
    invocation_context = InvocationContext(
        skill_name=skill_name,
        invocation_id=invocation_id,
        timestamp=datetime.now(),
        user_context=context or {},
        input_parameters=self._extract_input_parameters(),
        execution_method=self._detect_execution_method(),
        caller_info=self._get_caller_info()
    )
    
    # Track invocation
    self.invocation_tracker[invocation_id] = {
        'context': invocation_context,
        'start_time': time.time(),
        'status': 'running'
    }
```

### **2. Real-Time Issue Detection**
```python
# From automatic_knowledge_integrator.py (lines 308-349)
def _analyze_error_for_lessons(self, error_message: str, context: InvocationContext):
    """Analyze errors to extract learning opportunities"""
    lessons = []
    
    # Common error patterns automatically detected
    if 'file not found' in error_message.lower():
        lessons.append({
            'type': 'error',
            'content': {
                'error_pattern': 'file_not_found',
                'solution': 'Add file existence validation',
                'prevention': 'Pre-check file availability'
            },
            'confidence': 0.9,
            'impact': 'medium',
            'contexts': ['file_operations']
        })
    
    elif 'permission' in error_message.lower():
        lessons.append({
            'type': 'error',
            'content': {
                'error_pattern': 'permission_denied',
                'solution': 'Add permission checks',
                'prevention': 'Validate access rights'
            },
            'confidence': 0.8,
            'impact': 'medium',
            'contexts': ['file_operations', 'system_access']
        })
```

### **3. Performance Issue Capture**
```python
# From automatic_knowledge_integrator.py (lines 240-251)
# Performance lessons
if result.execution_time > 30:  # Slow execution
    lessons.append({
        'type': 'performance',
        'content': {
            'issue': 'slow_execution',
            'execution_time': result.execution_time,
            'suggested_optimization': 'Consider caching or parallel processing'
        },
        'confidence': 0.8,
        'impact': 'medium',
        'contexts': ['large_datasets', 'complex_analysis']
    })
```

## 🔄 **Documentation Update Triggers**

### **1. Skill Invocation Triggers Updates**
```python
# From automatic_knowledge_integrator.py (lines 210-233)
def capture_lesson(self, invocation_context: InvocationContext, result: ExecutionResult):
    """Capture lesson learned from invocation"""
    lesson_id = self._generate_lesson_id(invocation_context)
    
    # Analyze result for lessons
    lessons = self._analyze_execution_for_lessons(invocation_context, result)
    
    for lesson_data in lessons:
        lesson = LessonLearned(
            lesson_id=lesson_id,
            skill_name=invocation_context.skill_name,
            invocation_context=invocation_context,
            lesson_type=lesson_data['type'],
            lesson_content=lesson_data['content'],
            confidence_score=lesson_data['confidence'],
            impact_assessment=lesson_data['impact'],
            applicable_contexts=lesson_data['contexts'],
            timestamp=datetime.now()
        )
        
        # Queue for processing
        self.lesson_queue.append(lesson)
```

### **2. Background Processing System**
```python
# From automatic_knowledge_integrator.py (lines 390-421)
def _process_lessons_background(self):
    """Background thread to process lessons and update knowledge base"""
    while True:
        try:
            if self.lesson_queue:
                lesson = self.lesson_queue.pop(0)
                
                # Save lesson to knowledge base
                lesson_file = self.lessons_dir / f"{lesson.lesson_id}.json"
                with open(lesson_file, 'w') as f:
                    json.dump(asdict(lesson), f, indent=2, default=str)
                
                # Update pattern database
                if lesson.lesson_type == 'pattern':
                    self._update_pattern_database(lesson)
                
                # Update performance database
                if lesson.lesson_type == 'performance':
                    self._update_performance_database(lesson)
                
                # Queue skill update
                self.update_queue.append({
                    'lesson': lesson,
                    'timestamp': datetime.now()
                })
```

### **3. Automatic Skill File Updates**
```python
# From automatic_knowledge_integrator.py (lines 499-540)
def _update_skill_file(self, lesson: LessonLearned):
    """Update skill file based on lesson learned"""
    try:
        skill_file = self._find_skill_file(lesson.skill_name)
        if not skill_file:
            logger.warning(f"Skill file not found for {lesson.skill_name}")
            return
        
        # Read current skill content
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply updates based on lesson type
        updated_content = self._apply_lesson_to_skill(content, lesson)
        
        if updated_content != content:
            # Create backup
            backup_file = skill_file.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Write updated content
            with open(skill_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            logger.info(f"Updated skill file: {skill_file}")
```

## 📝 **Documentation Update Types**

### **1. Pattern Insights (SKILL.md)**
```python
# From automatic_knowledge_integrator.py (lines 573-587)
def _add_pattern_insights(self, content: str, lesson: LessonLearned) -> str:
    """Add pattern insights to skill content"""
    patterns = lesson.lesson_content.get('success_patterns', [])
    
    # Add to "Known Patterns" section or create new one
    if "## Known Patterns" not in content:
        content += "\n\n## Known Patterns\n"
        content += "### Success Patterns Identified\n"
    
    for pattern in patterns:
        pattern_text = f"- **{pattern}**: Discovered in {lesson.timestamp.strftime('%Y-%m-%d')} with {lesson.confidence_score:.1f} confidence\n"
        if pattern_text not in content:
            content += pattern_text
    
    return content
```

### **2. Performance Insights (SKILL.md)**
```python
# From automatic_knowledge_integrator.py (lines 589-602)
def _add_performance_insights(self, content: str, lesson: LessonLearned) -> str:
    """Add performance insights to skill content"""
    execution_time = lesson.lesson_content.get('execution_time', 0)
    if execution_time > 0:
        # Add performance insights
        if "## Performance Insights" not in content:
            content += "\n\n## Performance Insights\n"
            content += "### Execution Time Analysis\n"
        
        perf_text = f"- **Average Execution Time**: {execution_time:.2f}s (Recorded: {lesson.timestamp.strftime('%Y-%m-%d')})\n"
        if perf_text not in content:
            content += perf_text
    
    return content
```

### **3. Error Handling (SKILL.md)**
```python
# From automatic_knowledge_integrator.py (lines 604-619)
def _add_error_handling(self, content: str, lesson: LessonLearned) -> str:
    """Add error handling insights to skill content"""
    error_pattern = lesson.lesson_content.get('error_pattern', '')
    solution = lesson.lesson_content.get('solution', '')
    
    if error_pattern and solution:
        # Add error handling section
        if "## Error Handling" not in content:
            content += "\n\n## Error Handling\n"
            content += "### Known Issues and Solutions\n"
        
        error_text = f"- **{error_pattern}**: {solution} (Added: {lesson.timestamp.strftime('%Y-%m-%d')})\n"
        if error_text not in content:
            content += error_text
    
    return content
```

## 📊 **Knowledge Base Structure**

### **1. Lessons Learned (JSON)**
```json
// knowledge_base/lessons_learned/lesson_20260424_143022.json
{
  "lesson_id": "lesson_20260424_143022",
  "skill_name": "sonic_memory_exhaustion_triage",
  "invocation_context": {
    "skill_name": "sonic_memory_exhaustion_triage",
    "invocation_id": "abc123def456",
    "timestamp": "2026-04-24T14:30:22",
    "user_context": {"showtech_path": "/path/to/archive.tar.gz"},
    "input_parameters": {"cli_args": ["--verbose"]},
    "execution_method": "enhanced_invoker"
  },
  "lesson_type": "pattern",
  "lesson_content": {
    "success_patterns": ["memory_growth_pattern", "container_restart_pattern"],
    "confidence": 0.9
  },
  "confidence_score": 0.9,
  "impact_assessment": "high",
  "applicable_contexts": ["memory_analysis", "container_health"],
  "timestamp": "2026-04-24T14:30:22"
}
```

### **2. Pattern Database (JSON)**
```json
// knowledge_base/patterns/sonic_memory_exhaustion_triage_patterns.json
{
  "memory_growth_pattern": {
    "first_seen": "2026-04-24T14:30:22",
    "frequency": 5,
    "confidence": 0.9,
    "contexts": ["memory_analysis", "container_health"],
    "last_seen": "2026-04-24T16:45:10"
  },
  "container_restart_pattern": {
    "first_seen": "2026-04-24T14:30:22",
    "frequency": 3,
    "confidence": 0.8,
    "contexts": ["container_health", "service_disruption"]
  }
}
```

### **3. Performance Database (JSON)**
```json
// knowledge_base/performance/sonic_memory_exhaustion_triage_performance.json
{
  "execution_times": [
    {
      "timestamp": "2026-04-24T14:30:22",
      "execution_time": 45.2,
      "context": ["memory_analysis", "large_dataset"]
    },
    {
      "timestamp": "2026-04-24T16:45:10",
      "execution_time": 38.7,
      "context": ["memory_analysis", "medium_dataset"]
    }
  ],
  "stats": {
    "avg_time": 41.95,
    "min_time": 38.7,
    "max_time": 45.2,
    "total_executions": 2
  }
}
```

## 🚀 **Skill Invocation Flow**

### **1. Universal Skill Invocation**
```python
# From enhanced_skill_invoker.py (lines 51-94)
def invoke_skill(self, skill_name: str, context: Optional[Dict[str, Any]] = None, 
                showtech_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Universal skill invocation with comprehensive fallback support
    """
    logger.info(f"Invoking skill: {skill_name}")
    
    # Add showtech path to context if provided
    if showtech_path:
        if context is None:
            context = {}
        context['showtech_path'] = showtech_path
    
    # Try each fallback method in order
    for method_name, method_func in self.fallback_methods.items():
        try:
            logger.info(f"Trying fallback method: {method_name}")
            result = method_func(skill_name, context)
            
            if result and result.get('success', False):
                logger.info(f"Skill {skill_name} executed successfully using {method_name}")
                return {
                    'success': True,
                    'method': method_name,
                    'result': result,
                    'skill_name': skill_name,
                    'context': context,
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            logger.warning(f"Fallback method {method_name} failed: {e}")
            continue
```

### **2. Fallback Methods**
```python
# From enhanced_skill_invoker.py (lines 24-30)
self.fallback_methods = {
    'skill_discovery': self._invoke_via_discovery,
    'direct_file_execution': self._execute_skill_file,
    'template_execution': self._execute_with_template,
    'python_import': self._execute_as_module,
    'manual_analysis': self._manual_analysis_execution
}
```

## 🎯 **Real-World Example: Memory Analysis Skill**

### **Before Invocation**
```markdown
# sonic_memory_exhaustion_triage/SKILL.md

## Overview
This skill analyzes memory usage patterns in SONiC showtech archives.

## Files Analyzed
- `/proc/meminfo`
- `docker/containers/*/status`
- `show memory`
```

### **After Multiple Invocations with Learning**
```markdown
# sonic_memory_exhaustion_triage/SKILL.md

## Overview
This skill analyzes memory usage patterns in SONiC showtech archives based on intelligence from 15 real-world executions.

## Known Patterns
### Success Patterns Identified
- **memory_growth_pattern**: Discovered in 2026-04-24 with 0.9 confidence
- **container_restart_pattern**: Discovered in 2026-04-24 with 0.8 confidence
- **threshold_breach_pattern**: Discovered in 2026-04-24 with 0.7 confidence

## Performance Insights
### Execution Time Analysis
- **Average Execution Time**: 41.95s (Recorded: 2026-04-24)
- **Optimization**: Consider caching for large datasets

## Error Handling
### Known Issues and Solutions
- **file_not_found**: Add file existence validation (Added: 2026-04-24)
- **permission_denied**: Add permission checks (Added: 2026-04-24)
```

## 🔧 **Integration with Showtech Ingestion**

### **1. Showtech Extraction Integration**
```python
# When showtech archive is processed
with integrator.intercept_invocation('show_tech_extractor', {'archive_path': archive_path}) as ctx:
    result = extract_showtech_archive(archive_path)
    ctx.record_result(result)

# Automatically captures:
# - Extraction success/failure patterns
# - File access issues
# - Performance bottlenecks
# - New archive formats discovered
```

### **2. Skill Chain Intelligence**
```python
# When multiple skills are invoked on same showtech
for skill_name in skill_chain:
    with integrator.intercept_invocation(skill_name, shared_context) as ctx:
        result = invoke_skill(skill_name, showtech_path)
        ctx.record_result(result)
        shared_context.update(result.get('context_updates', {}))

# Automatically captures:
# - Skill dependency patterns
# - Context sharing effectiveness
# - Chain optimization opportunities
```

## 📈 **Learning Metrics & Intelligence**

### **1. Pattern Frequency Analysis**
```python
# Automatic pattern ranking
def get_pattern_rankings(self):
    """Get ranked patterns by frequency and confidence"""
    rankings = {}
    
    for pattern_file in self.patterns_dir.glob('*.json'):
        with open(pattern_file, 'r') as f:
            patterns = json.load(f)
        
        for pattern_name, pattern_data in patterns.items():
            rankings[pattern_name] = {
                'frequency': pattern_data['frequency'],
                'confidence': pattern_data['confidence'],
                'skill': pattern_file.stem,
                'impact': self._calculate_pattern_impact(pattern_data)
            }
    
    return dict(sorted(rankings.items(), key=lambda x: x[1]['frequency'], reverse=True))
```

### **2. Skill Performance Optimization**
```python
# Automatic performance optimization suggestions
def _generate_optimization_suggestions(self, skill_name: str):
    """Generate optimization suggestions based on performance data"""
    perf_file = self.performance_dir / f"{skill_name}_performance.json"
    
    if perf_file.exists():
        with open(perf_file, 'r') as f:
            perf_data = json.load(f)
        
        suggestions = []
        
        if perf_data['stats']['avg_time'] > 30:
            suggestions.append("Consider implementing caching for large datasets")
        
        if perf_data['stats']['total_executions'] > 100:
            suggestions.append("High usage skill - consider performance optimization")
        
        return suggestions
    
    return []
```

## 🎯 **Key Intelligence Features**

### **1. Automatic Error Pattern Recognition**
- **File Access Issues**: Automatically detects and learns from file not found, permission errors
- **Performance Bottlenecks**: Identifies slow execution patterns and suggests optimizations
- **Context Dependencies**: Learns which contexts trigger specific issues

### **2. Success Pattern Extraction**
- **Effective Command Sequences**: Learns which command combinations work best
- **Platform-Specific Patterns**: Identifies platform differences and optimal approaches
- **Context Correlations**: Discovers which contexts lead to successful outcomes

### **3. Continuous Skill Improvement**
- **Automatic Documentation Updates**: Skills are updated with new insights automatically
- **Performance Optimization**: Skills are optimized based on execution patterns
- **Error Prevention**: Skills are enhanced with preventive error handling

### **4. Knowledge Persistence**
- **Lesson Storage**: Every lesson is stored in structured JSON format
- **Pattern Databases**: Skill-specific pattern databases track frequency and confidence
- **Performance History**: Complete execution history for optimization

## 🔮 **Future Intelligence Capabilities**

### **1. Predictive Error Prevention**
```python
# Predict likely errors based on context
def predict_errors(self, skill_name: str, context: Dict[str, Any]):
    """Predict likely errors based on historical patterns"""
    error_patterns = self._load_error_patterns(skill_name)
    
    predictions = []
    for pattern in error_patterns:
        if self._context_matches(pattern['contexts'], context):
            predictions.append({
                'error_type': pattern['error_pattern'],
                'probability': pattern['frequency'] / pattern['total_occurrences'],
                'prevention': pattern['prevention']
            })
    
    return predictions
```

### **2. Adaptive Skill Selection**
```python
# Select best skill based on context and success patterns
def select_optimal_skill(self, analysis_type: str, context: Dict[str, Any]):
    """Select optimal skill based on context and historical success"""
    skill_performance = self._load_skill_performance_data()
    
    best_skill = None
    best_score = 0
    
    for skill_name, perf_data in skill_performance.items():
        if analysis_type in perf_data['supported_types']:
            score = self._calculate_context_match_score(skill_name, context)
            if score > best_score:
                best_score = score
                best_skill = skill_name
    
    return best_skill
```

---

## 🔧 **Tool Execution Troubleshooting Insights**

### **Common Tool Hiccups and Solutions**

#### **Archive Format Detection Issues**
```yaml
Problem: "Unsupported archive format" error
Root Cause: Compound extension parsing (.tar.gz)
Solution Implemented: Enhanced archive_ext detection
Code Fix: archive_ext = ''.join(archive_path.suffixes)
Impact: Resolves tar.gz, tgz format recognition
```

#### **Unicode Encoding Issues (Windows)**
```yaml
Problem: 'charmap' codec can't encode emoji characters
Root Cause: Windows command prompt encoding limitations
Solution Implemented: Text-based console output
Code Fix: Replaced emojis with [TAG] format
Impact: Analysis completes successfully despite display issues
```

#### **Path Handling Issues**
```yaml
Problem: Unicode escape errors in Windows paths
Root Cause: Backslash interpretation in strings
Solution Implemented: Raw string support
Code Fix: r'path' format and double backslash handling
Impact: Resolves Windows path compatibility
```

### **Execution Success Indicators**
```yaml
Startup: "[ANALYSIS] Starting Standard Analysis"
Archive Recognition: "[ARCHIVE] Archive: path"
Completion: "[SUCCESS] Standard Analysis Complete!"
Health Score: Numeric score (0-10) displayed
Issue Count: "Total Issues: X" shown
```

### **System Requirements Documentation**
```yaml
Python Version: 3.8+ recommended
System Memory: 4GB minimum, 8GB+ for large archives
Disk Space: 2x archive size for extraction
Platform Support: Windows, Linux, macOS compatible
Archive Formats: .tar.gz, .tgz, .zip supported
```

### **Tool Execution Best Practices**
```yaml
1. Archive Preparation:
   - Verify format compatibility
   - Check file integrity
   - Ensure read permissions

2. Path Handling:
   - Use raw strings on Windows
   - Double backslashes for paths
   - Verify file existence

3. Memory Management:
   - Close other applications
   - Monitor system resources
   - Use smaller archives for testing

4. Error Recovery:
   - Analysis continues despite Unicode issues
   - Results generated successfully
   - Check console output for status
```

---

## 🎯 **Summary**

This intelligence system provides:

1. **Automatic Tool Issue Capture**: Every skill execution is monitored for issues and learning opportunities
2. **Real-Time Documentation Updates**: Skills are automatically updated with new insights
3. **Pattern Recognition**: System learns from every execution and builds pattern databases
4. **Performance Optimization**: Continuous performance tracking and optimization suggestions
5. **Error Prevention**: Predictive error prevention based on historical patterns
6. **Knowledge Persistence**: All learning is stored in structured, queryable formats
7. **Tool Execution Troubleshooting**: Comprehensive hiccup documentation and solutions
8. **Cross-Platform Compatibility**: Windows, Linux, macOS execution insights
9. **Unicode Handling**: Encoding issue resolution and workarounds
10. **System Requirements**: Clear documentation for optimal execution environment

The system creates a **self-improving ecosystem** where every skill execution makes the entire system smarter and more effective, while ensuring smooth operation across different environments and preventing common tool-related hiccups.