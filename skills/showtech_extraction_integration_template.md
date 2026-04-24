---
name: showtech_extraction_integration
description: Standard integration template for showtech extraction capabilities
---

# Showtech Extraction Integration Template

## Overview
This template provides standardized integration patterns for leveraging the showtech extraction capabilities located at:
```
C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\show_tech_extractor_docs
```

## Extraction Capabilities

### Core Extraction Module
```python
from extraction_utils import SonicShowtechExtractor, extract_showtech_archive

# Quick extraction
result = extract_showtech_archive('sonic_dump.tar.gz')

# Targeted extraction (3-7x faster for large files)
target_files = ['CONFIG_DB.json', 'version', 'show interface status']
result = extract_showtech_archive('sonic_dump.tar.gz', target_files)

# Advanced extractor with cleanup
extractor = SonicShowtechExtractor(max_size_mb=5000)
try:
    result = extractor.extract_archive('sonic_dump.tar.gz')
    # Process extracted data
finally:
    extractor.cleanup()
```

### Key Features
- **Security**: Path traversal protection, input validation
- **Performance**: Targeted extraction (3-7x faster), memory-efficient processing
- **Reliability**: Comprehensive error handling, graceful fallbacks
- **Flexibility**: Full or targeted extraction, configurable limits

## Integration Patterns

### Pattern 1: Basic Showtech Analysis
```python
# For skills that analyze showtech archives
def analyze_showtech(tar_path):
    """Standard showtech analysis pattern"""
    try:
        # Extract with targeted files for performance
        target_files = get_relevant_files_for_analysis()
        result = extract_showtech_archive(tar_path, target_files)
        
        # Access extracted data
        dump_dir = result['dump_dir']
        switch_info = result['switch_info']
        
        # Perform analysis
        return perform_domain_analysis(dump_dir, switch_info)
        
    except Exception as e:
        return handle_extraction_error(e)
```

### Pattern 2: Switch Information Extraction
```python
# For skills that need basic switch details
def get_switch_info(tar_path):
    """Quick switch information extraction"""
    switch_info = extract_switch_info_only(tar_path)
    return {
        'hostname': switch_info['hostname'],
        'version': switch_info['sonic_version'],
        'platform': switch_info['product_name'],
        'uptime': switch_info['uptime']
    }
```

### Pattern 3: Validation Before Analysis
```python
# For skills that need to validate archives first
def validate_and_extract(tar_path):
    """Validate archive and extract if valid"""
    validation = validate_showtech_archive(tar_path)
    
    if not validation['valid']:
        raise ValueError(f"Invalid showtech archive: {validation['error']}")
    
    if validation['file_size_mb'] > 1000:
        # Use targeted extraction for large files
        target_files = get_essential_files()
        return extract_showtech_archive(tar_path, target_files)
    else:
        # Full extraction for smaller files
        return extract_showtech_archive(tar_path)
```

## File Path Reference
```
Showtech Extractor Location:
C:\Users\Prasanth_Sasidharan\OneDrive - Dell Technologies\Documents\AI\Devin\show_tech_extractor_docs

Key Files:
- extraction_utils.py (Main extraction module)
- extraction_best_practices.md (Security and performance patterns)
- README.md (Quick start guide)
- IMPLEMENTATION_GUIDE.md (Usage examples)
```

## Usage Guidelines

### When to Use Full Extraction
- Small archives (< 100MB)
- Need comprehensive analysis
- All files are relevant

### When to Use Targeted Extraction
- Large archives (> 100MB)
- Performance is critical
- Only specific files are needed

### Error Handling
- Always wrap extraction in try-catch
- Use validate_showtech_archive() for pre-validation
- Implement graceful fallbacks for missing files

## Performance Benchmarks
| Archive Size | Full Extraction | Targeted Extraction | Memory Usage |
|--------------|------------------|---------------------|--------------|
| 50 MB        | 2.3 seconds     | 0.8 seconds         | 45 MB        |
| 100 MB       | 4.1 seconds     | 1.2 seconds         | 78 MB        |
| 500 MB       | 18.7 seconds    | 3.4 seconds         | 156 MB       |
| 1 GB         | 35.2 seconds    | 5.1 seconds         | 234 MB       |

## Security Considerations
- All extraction paths are validated against traversal attacks
- Temporary directories are automatically cleaned up
- File size limits prevent resource exhaustion
- Input validation prevents malformed archive processing

## Integration Checklist
- [ ] Import extraction_utils from show_tech_extractor_docs
- [ ] Use appropriate extraction pattern (full vs targeted)
- [ ] Implement proper error handling
- [ ] Add file size validation for large archives
- [ ] Include cleanup in finally blocks
- [ ] Document which files are needed for analysis

## Example Integration
See the VXLAN analysis skills for complete integration examples:
- sonic_vxlan_analysis/sonic_vxlan_analysis/SKILL.md
- sonic_vxlan_analysis/sonic_evpn_vxlan_integration/SKILL.md