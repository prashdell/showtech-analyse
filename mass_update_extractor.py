#!/usr/bin/env python3
"""
Mass Update Script for Show Tech Extractor Integration
Updates all Python scripts to use show_tech_extractor skill
"""

import os
import re
from pathlib import Path

def update_python_script(script_path):
    """Update a single Python script to use show_tech_extractor integration"""
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if already updated
        if 'showtech_extractor_integration' in content:
            print(f"  Already updated: {script_path.name}")
            return False
        
        # Add import statement
        import_line = "# Import showtech extractor integration\nsys.path.insert(0, str(Path(__file__).parent))\nfrom showtech_extractor_integration import extract_showtech_archive\n"
        
        # Find where to insert import (after existing imports)
        import_pattern = r'(from datetime import datetime)\n'
        if re.search(import_pattern, content):
            content = re.sub(import_pattern, r'\1\n' + import_line, content)
        else:
            # Insert after shebang and docstring
            shebang_pattern = r'(#!/usr/bin/env python3\n"""\n[^"]*"""\n\n)'
            if re.search(shebang_pattern, content):
                content = re.sub(shebang_pattern, r'\1\n' + import_line, content)
            else:
                # Insert at beginning after imports
                lines = content.split('\n')
                import_index = 0
                for i, line in enumerate(lines):
                    if line.startswith('import ') or line.startswith('from '):
                        import_index = i + 1
                    elif line.strip() == '' and import_index > 0:
                        break
                lines.insert(import_index, import_line)
                content = '\n'.join(lines)
        
        # Update extract_archive method
        extract_pattern = r'def extract_archive\(self[^:]*\):\s*"""[^"]*"""\s*(.*?)(?=def|\Z)'
        
        def replace_extract_archive(match):
            method_body = match.group(1)
            new_body = '''print(f"Extracting {archive_path} using show_tech_extractor skill...")
        
        # Use the showtech extractor integration
        extraction_result = extract_showtech_archive(archive_path)
        
        if extraction_result['success']:
            self.temp_dir = extraction_result['output_dir']
            print(f"Extraction completed using {extraction_result['method']}")
            
            # Store extracted data for analysis
            if 'extracted_data' in extraction_result:
                self.extracted_data = extraction_result['extracted_data']
            else:
                self.extracted_data = extraction_result.get('file_inventory', {})
            
            return self.temp_dir
        else:
            raise Exception(f"Extraction failed: {extraction_result.get('error', 'Unknown error')}")'''
            
            return f'def extract_archive(self, archive_path: str) -> str:\n        """Extract archive using show_tech_extractor skill"""\n        {new_body}'
        
        content = re.sub(extract_pattern, replace_extract_archive, content, flags=re.DOTALL)
        
        # Remove tarfile import if no longer needed
        if 'tarfile' in content and 'tarfile.open' not in content:
            content = re.sub(r'import tarfile\n', '', content)
            content = re.sub(r'import tempfile\n', '', content)
            content = re.sub(r'import shutil\n', '', content)
        
        # Write updated content
        if content != original_content:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated: {script_path.name}")
            return True
        else:
            print(f"  No changes needed: {script_path.name}")
            return False
            
    except Exception as e:
        print(f"  Error updating {script_path.name}: {e}")
        return False

def main():
    """Update all Python scripts in the project"""
    print("Mass Update: Show Tech Extractor Integration")
    print("=" * 50)
    
    project_dir = Path(__file__).parent
    python_scripts = list(project_dir.glob("*.py"))
    
    # Also include sjobs directory
    sjobs_dir = project_dir / "sjobs"
    if sjobs_dir.exists():
        python_scripts.extend(sjobs_dir.glob("*.py"))
    
    updated_count = 0
    total_count = len(python_scripts)
    
    for script_path in python_scripts:
        if script_path.name == 'showtech_extractor_integration.py':
            continue  # Skip the integration module itself
        
        print(f"Processing: {script_path.name}")
        if update_python_script(script_path):
            updated_count += 1
        print()
    
    print(f"Update Summary:")
    print(f"  Total scripts: {total_count}")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped: {total_count - updated_count}")
    print(f"Done!")

if __name__ == "__main__":
    main()