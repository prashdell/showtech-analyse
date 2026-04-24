# Showtech Knowledge Capture & Reuse System

## 🎯 **Executive Overview**

This is the complete intelligence system that captures knowledge when a new showtech is processed and makes it available for reuse across future analyses. It's a **multi-layered learning ecosystem** that transforms every showtech analysis into reusable intelligence.

## 🏗️ **Knowledge Capture Architecture**

### **Layer 1: Showtech Ingestion & Extraction**
```python
# From showtech_extractor_integration.py
class ShowTechExtractorIntegration:
    """Integration layer for show_tech_extractor skill"""
    
    def extract_showtech(self, archive_path, output_dir=None):
        """
        Extract showtech using the show_tech_extractor skill
        Captures extraction metadata and creates intelligent inventory
        """
        # 1. Archive Extraction
        extracted_data = showtech_extractor.extract(archive_path)
        
        # 2. Intelligent File Inventory
        file_inventory = self._create_file_inventory(output_dir)
        
        # 3. Key File Identification
        key_files = self._identify_key_files(file_inventory)
        
        # 4. Metadata Capture
        extraction_metadata = {
            'archive_path': archive_path,
            'extraction_time': datetime.now().isoformat(),
            'method': 'fixed_show_tech_extractor',
            'file_inventory': file_inventory,
            'key_files': key_files
        }
```

### **Layer 2: Intelligent File Classification**
```python
# From showtech_extractor_integration.py (lines 116-147)
def _create_file_inventory(self, output_dir):
    """Create inventory of extracted files with intelligent classification"""
    inventory = {
        'total_files': 0,
        'directories': [],
        'files': [],
        'file_types': {},
        'key_files': {}  # Intelligence-driven identification
    }
    
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, output_dir)
            
            # Intelligent file classification
            if any(keyword in file.lower() for keyword in 
                  ['asic', 'memory', 'interface', 'bgp', 'docker', 'log', 'config']):
                inventory['key_files'][file] = rel_path
    
    return inventory
```

### **Layer 3: Deep Analysis & Pattern Recognition**
```python
# From enhanced_analyzer.py (lines 116-119)
def _deep_analysis(self, temp_dir, file_inventory):
    """Perform deep technical analysis with pattern recognition"""
    results = {
        'system_overview': self._analyze_system_overview(temp_dir),
        'hardware_analysis': self._analyze_hardware_platform(temp_dir),
        'service_health': self._analyze_service_health(temp_dir),
        'network_state': self._analyze_network_state(temp_dir),
        'performance_metrics': self._analyze_performance(temp_dir),
        'error_patterns': self._detect_error_patterns(temp_dir),
        'configuration_analysis': self._analyze_configuration(temp_dir)
    }
```

## 🔄 **Knowledge Capture Process Flow**

### **Step 1: Archive Reception & Metadata Capture**
```python
# When new showtech arrives
archive_path = "/path/to/new_showtech.tar.gz"

# 1. Capture initial metadata
initial_metadata = {
    'archive_name': os.path.basename(archive_path),
    'archive_size': os.path.getsize(archive_path),
    'arrival_time': datetime.now().isoformat(),
    'source_context': self._extract_source_context(archive_path)
}

# 2. Intelligent extraction with knowledge capture
with integrator.intercept_invocation('show_tech_extractor', initial_metadata) as ctx:
    extraction_result = extract_showtech_archive(archive_path)
    ctx.record_result(extraction_result)
```

### **Step 2: Extraction Intelligence Capture**
```python
# Extraction process captures multiple intelligence layers
extraction_intelligence = {
    'extraction_success': extraction_result['success'],
    'method_used': extraction_result['method'],
    'file_count': extraction_result['file_inventory']['total_files'],
    'key_files_identified': extraction_result['file_inventory']['key_files'],
    'file_type_distribution': extraction_result['file_inventory']['file_types'],
    'extraction_duration': extraction_time,
    'platform_indicators': self._detect_platform_indicators(extraction_result)
}
```

### **Step 3: Multi-Skill Analysis with Knowledge Sharing**
```python
# Skills are invoked in intelligent sequence with shared context
analysis_context = {
    'extraction_intelligence': extraction_intelligence,
    'platform_detected': platform_indicators,
    'key_files_available': key_files,
    'previous_patterns': self._load_relevant_patterns(platform_indicators)
}

# Sequential skill execution with knowledge accumulation
skill_sequence = [
    'sonic_hardware_platform_analyzer',
    'sonic_container_health_triage', 
    'sonic_memory_exhaustion_triage',
    'sonic_bgp_connectivity_triage',
    'sonic_interface_connectivity_triage'
]

accumulated_knowledge = {}
for skill_name in skill_sequence:
    with integrator.intercept_invocation(skill_name, {
        **analysis_context,
        'accumulated_knowledge': accumulated_knowledge
    }) as ctx:
        result = invoke_skill(skill_name, showtech_path)
        ctx.record_result(result)
        
        # Accumulate knowledge for next skill
        accumulated_knowledge[skill_name] = {
            'findings': result.get('findings', {}),
            'patterns': result.get('patterns', []),
            'confidence': result.get('confidence', 0.0),
            'recommendations': result.get('recommendations', [])
        }
```

## 🧠 **Knowledge Reuse Mechanisms**

### **1. Pattern Database Lookup**
```python
# From automatic_knowledge_integrator.py (lines 423-449)
def _update_pattern_database(self, lesson: LessonLearned):
    """Update pattern database with new patterns for future reuse"""
    pattern_file = self.patterns_dir / f"{lesson.skill_name}_patterns.json"
    
    # Load existing patterns
    patterns = {}
    if pattern_file.exists():
        with open(pattern_file, 'r') as f:
            patterns = json.load(f)
    
    # Add new patterns with frequency tracking
    new_patterns = lesson.lesson_content.get('success_patterns', [])
    for pattern in new_patterns:
        if pattern not in patterns:
            patterns[pattern] = {
                'first_seen': lesson.timestamp.isoformat(),
                'frequency': 1,
                'confidence': lesson.confidence_score,
                'contexts': lesson.applicable_contexts,
                'success_rate': 1.0,
                'applicable_platforms': self._extract_platform_context(lesson)
            }
        else:
            # Update existing pattern with new intelligence
            patterns[pattern]['frequency'] += 1
            patterns[pattern]['last_seen'] = lesson.timestamp.isoformat()
            patterns[pattern]['confidence'] = max(
                patterns[pattern]['confidence'], 
                lesson.confidence_score
            )
```

### **2. Context-Aware Skill Selection**
```python
# Intelligent skill selection based on showtech characteristics
def select_optimal_skills(self, showtech_intelligence):
    """Select optimal skills based on showtech content and historical patterns"""
    selected_skills = []
    
    # Platform-specific skill selection
    if 'z9' in showtech_intelligence.get('platform_indicators', {}).get('model', '').lower():
        selected_skills.extend(['sonic_z_series_analyzer', 'sonic_ai_fabric_optimizer'])
    
    # Issue-type specific selection
    if 'memory' in showtech_intelligence.get('key_files', {}):
        selected_skills.append('sonic_memory_exhaustion_triage')
    
    # Historical pattern matching
    relevant_patterns = self._find_matching_patterns(showtech_intelligence)
    for pattern in relevant_patterns:
        if pattern['confidence'] > 0.8:
            selected_skills.extend(pattern['effective_skills'])
    
    return list(set(selected_skills))  # Remove duplicates
```

### **3. Cross-Showtech Correlation**
```python
# Knowledge reuse across multiple showtech archives
def correlate_showtech_analyses(self, current_analysis, historical_analyses):
    """Correlate current analysis with historical patterns"""
    correlations = {
        'platform_matches': [],
        'issue_patterns': [],
        'configuration_similarities': [],
        'performance_comparisons': []
    }
    
    # Platform correlation
    current_platform = current_analysis.get('hardware_platform')
    for historical in historical_analyses:
        if historical.get('hardware_platform') == current_platform:
            correlations['platform_matches'].append({
                'archive_id': historical['archive_id'],
                'similar_issues': historical.get('issues', []),
                'effective_solutions': historical.get('solutions', [])
            })
    
    # Issue pattern correlation
    current_issues = current_analysis.get('detected_issues', [])
    for issue in current_issues:
        matching_patterns = self._find_similar_issue_patterns(issue, historical_analyses)
        correlations['issue_patterns'].extend(matching_patterns)
    
    return correlations
```

## 📊 **Knowledge Storage Structure**

### **1. Individual Showtech Knowledge**
```json
// knowledge_base/showtech_analyses/showtech_20260424_143022.json
{
  "showtech_id": "showtech_20260424_143022",
  "archive_metadata": {
    "name": "sonic_dump_CUSTOMER-SW1_20260424_120000.tar.gz",
    "size": 125829120,
    "extraction_time": "2026-04-24T14:30:22",
    "platform_detected": "S5248F-ON",
    "version": "4.5.1"
  },
  "extraction_intelligence": {
    "file_count": 1247,
    "key_files": {
      "config_db.json": "dump/CONFIG_DB.json",
      "asic_state": "dump/ASIC_DB.json",
      "memory_info": "dump/memory.json"
    },
    "file_type_distribution": {
      ".json": 890,
      ".log": 234,
      ".txt": 123
    }
  },
  "analysis_results": {
    "hardware_analysis": {...},
    "service_health": {...},
    "network_state": {...},
    "detected_issues": [...],
    "recommendations": [...]
  },
  "captured_patterns": [
    "bgp_docker_restart_pattern",
    "memory_growth_pattern",
    "interface_flap_pattern"
  ],
  "correlations": {
    "similar_archives": ["showtech_20260420_091533"],
    "platform_matches": 15,
    "issue_patterns": 7
  }
}
```

### **2. Pattern Database for Reuse**
```json
// knowledge_base/patterns/sonic_memory_exhaustion_triage_patterns.json
{
  "memory_growth_pattern": {
    "first_seen": "2026-04-15T10:30:00",
    "frequency": 23,
    "confidence": 0.92,
    "contexts": ["memory_analysis", "container_health"],
    "success_rate": 0.87,
    "applicable_platforms": ["S5248F", "S5232F", "S5448F"],
    "indicators": [
      "memory_usage > 80%",
      "container_restart_count > 3",
      "swap_usage > 50%"
    ],
    "effective_solutions": [
      "restart affected containers",
      "check for memory leaks",
      "analyze process growth"
    ],
    "related_patterns": [
      "container_restart_pattern",
      "swap_usage_pattern"
    ]
  }
}
```

### **3. Cross-Archive Intelligence**
```json
// knowledge_base/cross_archive_intelligence.json
{
  "platform_behaviors": {
    "S5248F": {
      "common_issues": ["bgp_docker_failure", "memory_exhaustion"],
      "temperature_sensitivity": "high",
      "optimal_version": "4.5.1"
    }
  },
  "version_patterns": {
    "4.5.0": {
      "known_issues": ["ssh_key_sharing", "bgp_stability"],
      "upgrade_path": "4.5.0a recommended"
    }
  },
  "customer_patterns": {
    "NEE-series": {
      "common_topologies": ["spine_leaf", "mclag"],
      "typical_issues": ["bgp_flapping", "interface_connectivity"]
    }
  }
}
```

## 🔄 **Real-Time Knowledge Reuse in Action**

### **Scenario 1: New Showtech Arrives**
```python
# Step 1: Initial extraction and analysis
showtech_path = "/new/archive/sonic_dump_CUSTOMER-SW1_20260424_120000.tar.gz"

# Step 2: Intelligent skill selection based on content
extraction_result = extract_showtech_archive(showtech_path)
platform_detected = detect_platform(extraction_result)
relevant_patterns = load_patterns_for_platform(platform_detected)

# Step 3: Context-aware analysis with historical knowledge
analysis_context = {
    'platform': platform_detected,
    'historical_patterns': relevant_patterns,
    'similar_archives': find_similar_archives(extraction_result),
    'known_issues': load_known_issues(platform_detected, version)
}

# Step 4: Execute skills with accumulated knowledge
for skill in select_optimal_skills(analysis_context):
    result = invoke_skill_with_context(skill, showtech_path, analysis_context)
    
    # Step 5: Capture new knowledge for future reuse
    if result.get('new_patterns'):
        update_pattern_database(skill, result['new_patterns'])
    
    if result.get('new_insights'):
        update_cross_archive_intelligence(result['new_insights'])
```

### **Scenario 2: Pattern Recognition & Reuse**
```python
# When analyzing BGP issues, system automatically reuses knowledge
def analyze_bgp_with_reuse(showtech_path):
    # Load BGP-specific knowledge
    bgp_patterns = load_pattern_database('sonic_bgp_connectivity_triage')
    
    # Check for known patterns in current showtech
    current_bgp_state = extract_bgp_state(showtech_path)
    
    # Pattern matching
    matched_patterns = []
    for pattern_name, pattern_data in bgp_patterns.items():
        if pattern_matches(current_bgp_state, pattern_data['indicators']):
            matched_patterns.append({
                'pattern': pattern_name,
                'confidence': pattern_data['confidence'],
                'solutions': pattern_data['effective_solutions'],
                'success_rate': pattern_data['success_rate']
            })
    
    # Apply most effective solutions first
    sorted_patterns = sorted(matched_patterns, key=lambda x: x['success_rate'], reverse=True)
    
    return {
        'matched_patterns': sorted_patterns,
        'recommended_actions': [p['solutions'][0] for p in sorted_patterns],
        'confidence': max([p['confidence'] for p in sorted_patterns]) if sorted_patterns else 0.0
    }
```

### **Scenario 3: Continuous Learning Loop**
```python
# Every analysis contributes to the knowledge base
def continuous_learning_cycle(showtech_path):
    # 1. Extract and analyze
    analysis_results = comprehensive_analysis(showtech_path)
    
    # 2. Capture lessons learned
    lessons = extract_lessons_from_analysis(analysis_results)
    
    # 3. Update knowledge bases
    for lesson in lessons:
        update_pattern_database(lesson.skill_name, lesson.patterns)
        update_performance_data(lesson.skill_name, lesson.performance)
        update_cross_archive_intelligence(lesson.correlations)
    
    # 4. Improve future analyses
    improve_skill_effectiveness(lessons)
    
    # 5. Share knowledge across skills
    distribute_intelligence_to_related_skills(lessons)
```

## 🎯 **Knowledge Reuse Benefits**

### **1. Faster Analysis**
- **Pattern Recognition**: Immediate identification of known issues
- **Solution Reuse**: Apply proven solutions from similar cases
- **Context Awareness**: Skip irrelevant analysis steps

### **2. Higher Accuracy**
- **Historical Validation**: Solutions validated by past successes
- **Platform-Specific Knowledge**: Tailored analysis for each platform
- **Confidence Scoring**: Trust metrics based on historical success rates

### **3. Continuous Improvement**
- **Learning Loop**: Every analysis improves future accuracy
- **Pattern Evolution**: Patterns adapt to new issues and solutions
- **Knowledge Accumulation**: System gets smarter with each analysis

### **4. Consistency & Standardization**
- **Uniform Analysis**: Consistent approach across all showtechs
- **Standardized Solutions**: Proven solutions applied consistently
- **Quality Assurance**: Knowledge base ensures analysis quality

## 🔮 **Advanced Knowledge Features**

### **1. Predictive Analysis**
```python
def predict_issues(showtech_path):
    """Predict likely issues based on historical patterns"""
    extraction_result = extract_showtech_archive(showtech_path)
    
    predictions = []
    
    # Platform-based predictions
    platform = detect_platform(extraction_result)
    platform_issues = load_platform_issue_patterns(platform)
    
    for issue_pattern in platform_issues:
        if pattern_indicators_present(extraction_result, issue_pattern['indicators']):
            predictions.append({
                'issue_type': issue_pattern['issue'],
                'probability': issue_pattern['probability'],
                'recommended_prevention': issue_pattern['prevention'],
                'confidence': issue_pattern['confidence']
            })
    
    return sorted(predictions, key=lambda x: x['probability'], reverse=True)
```

### **2. Automated Solution Recommendation**
```python
def recommend_solutions(detected_issues, platform, version):
    """Automatically recommend solutions based on historical success"""
    recommendations = []
    
    for issue in detected_issues:
        # Find most effective solutions for this issue
        solution_history = load_solution_effectiveness(issue, platform, version)
        
        # Sort by success rate
        effective_solutions = sorted(
            solution_history, 
            key=lambda x: x['success_rate'], 
            reverse=True
        )
        
        recommendations.append({
            'issue': issue,
            'recommended_solution': effective_solutions[0]['solution'],
            'success_rate': effective_solutions[0]['success_rate'],
            'confidence': effective_solutions[0]['confidence'],
            'implementation_steps': effective_solutions[0]['steps']
        })
    
    return recommendations
```

---

## 🎯 **Summary**

The showtech knowledge capture and reuse system creates a **self-improving ecosystem** where:

1. **Every showtech analysis** contributes to collective intelligence
2. **Historical patterns** are automatically applied to new analyses
3. **Cross-archive correlations** provide deeper insights
4. **Continuous learning** improves accuracy and efficiency over time
5. **Knowledge persistence** ensures intelligence is never lost

This transforms showtech analysis from a **manual, repetitive process** into an **intelligent, learning system** that gets smarter with every archive processed.