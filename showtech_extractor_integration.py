#!/usr/bin/env python3
"""
Show Tech Extractor Integration Module
Invokes the show_tech_extractor skill for consistent data extraction
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

class ShowTechExtractorIntegration:
    """Integration layer for show_tech_extractor skill"""
    
    def __init__(self):
        self.skill_path = Path(r"C:\Users\Prasanth_Sasidharan\.codeium\windsurf\skills\show_tech_extractor")
        self.extractor_script = self.skill_path / "extractor.py"
        
    def extract_showtech(self, archive_path, output_dir=None):
        """
        Extract showtech using the show_tech_extractor skill
        
        Args:
            archive_path: Path to showtech archive
            output_dir: Optional output directory (auto-generated if None)
            
        Returns:
            dict: Extracted data structure
        """
        if not os.path.exists(archive_path):
            raise FileNotFoundError(f"Archive not found: {archive_path}")
        
        # Create output directory if not provided
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="showtech_extracted_")
        
        # Use the show_tech_extractor skill
        try:
            # Try to import and use the extractor directly
            if os.path.exists(self.extractor_script):
                return self._extract_with_skill(archive_path, output_dir)
            else:
                # Fallback to basic extraction
                return self._extract_basic(archive_path, output_dir)
        except Exception as e:
            print(f"Warning: show_tech_extractor skill failed ({e}), using fallback extraction")
            return self._extract_basic(archive_path, output_dir)
    
    def _extract_with_skill(self, archive_path, output_dir):
        """Extract using the fixed show_tech_extractor skill"""
        try:
            # Import the fixed extractor
            from fixed_showtech_extractor import FixedShowTechExtractor
            
            # Initialize and use extractor
            showtech_extractor = FixedShowTechExtractor()
            extracted_data = showtech_extractor.extract(archive_path)
            
            if extracted_data.get('success', False):
                # Save extracted data
                output_file = os.path.join(output_dir, "extracted_data.json")
                with open(output_file, 'w') as f:
                    json.dump(extracted_data, f, indent=2, default=str)
                
                return {
                    'success': True,
                    'output_dir': output_dir,
                    'extracted_data': extracted_data,
                    'method': 'fixed_show_tech_extractor',
                    'extraction_time': datetime.now().isoformat()
                }
            else:
                raise Exception(f"Fixed extractor failed: {extracted_data.get('error', 'Unknown error')}")
                
        except ImportError as e:
            raise Exception(f"Could not import fixed extractor: {e}")
        except Exception as e:
            raise Exception(f"Fixed show tech extractor failed: {e}")
    
    def _extract_basic(self, archive_path, output_dir):
        """Basic extraction fallback"""
        import tarfile
        import zipfile
        
        try:
            if archive_path.endswith('.tar.gz') or archive_path.endswith('.tgz'):
                with tarfile.open(archive_path, 'r:gz') as tar:
                    tar.extractall(output_dir)
            elif archive_path.endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(output_dir)
            else:
                raise ValueError(f"Unsupported archive format: {archive_path}")
            
            # Create basic file inventory
            file_inventory = self._create_file_inventory(output_dir)
            
            return {
                'success': True,
                'output_dir': output_dir,
                'file_inventory': file_inventory,
                'method': 'basic_extraction',
                'extraction_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'basic_extraction_failed'
            }
    
    def _create_file_inventory(self, output_dir):
        """Create inventory of extracted files"""
        inventory = {
            'total_files': 0,
            'directories': [],
            'files': [],
            'file_types': {},
            'key_files': {}
        }
        
        for root, dirs, files in os.walk(output_dir):
            inventory['directories'].append(root)
            
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, output_dir)
                
                inventory['total_files'] += 1
                inventory['files'].append(rel_path)
                
                # File type analysis
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext not in inventory['file_types']:
                    inventory['file_types'][file_ext] = []
                inventory['file_types'][file_ext].append(rel_path)
                
                # Identify key files
                if any(keyword in file.lower() for keyword in 
                      ['asic', 'memory', 'interface', 'bgp', 'docker', 'log', 'config']):
                    inventory['key_files'][file] = rel_path
        
        return inventory
    
    def get_available_parsers(self):
        """Get list of available parsers from the skill"""
        parsers_dir = self.skill_path / "parsers"
        
        if not os.path.exists(parsers_dir):
            return ['basic_fallback']
        
        parsers = []
        for file in os.listdir(parsers_dir):
            if file.endswith('.py') and not file.startswith('__'):
                parser_name = file.replace('.py', '')
                parsers.append(parser_name)
        
        return parsers if parsers else ['basic_fallback']
    
    def validate_extraction(self, extracted_data):
        """Validate extraction results"""
        if not isinstance(extracted_data, dict):
            return False, "Invalid extraction data format"
        
        if 'success' not in extracted_data:
            return False, "Missing success flag"
        
        if not extracted_data['success']:
            return False, extracted_data.get('error', 'Extraction failed')
        
        return True, "Extraction successful"

# Global extractor instance
_extractor_instance = None

def get_showtech_extractor():
    """Get global showtech extractor instance"""
    global _extractor_instance
    if _extractor_instance is None:
        _extractor_instance = ShowTechExtractorIntegration()
    return _extractor_instance

def extract_showtech_archive(archive_path, output_dir=None):
    """Convenience function to extract showtech archive"""
    extractor = get_showtech_extractor()
    return extractor.extract_showtech(archive_path, output_dir)