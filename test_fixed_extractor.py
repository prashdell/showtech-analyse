#!/usr/bin/env python3
"""
Test script for Fixed Show Tech Extractor
Demonstrates the standalone functionality
"""

import sys
import json
from pathlib import Path
from datetime import datetime

def test_fixed_extractor():
    """Test the fixed showtech extractor"""
    print("=== Fixed Show Tech Extractor Test ===")
    print()
    
    # Import the fixed extractor
    try:
        from fixed_showtech_extractor import FixedShowTechExtractor
        print("SUCCESS: FixedShowTechExtractor imported successfully")
    except ImportError as e:
        print(f"ERROR: Could not import FixedShowTechExtractor: {e}")
        return
    
    # Initialize extractor
    extractor = FixedShowTechExtractor()
    print("SUCCESS: Extractor initialized")
    print()
    
    # Test extraction
    archive_path = r"C:\Users\Prasanth_Sasidharan\Downloads\sonic_dump_N3248R39-06Apr-Jon_20260326_165720.tar.gz"
    
    if not Path(archive_path).exists():
        print(f"ERROR: Archive not found: {archive_path}")
        return
    
    print(f"Extracting: {archive_path}")
    print()
    
    try:
        result = extractor.extract(archive_path)
        
        if result.get('success'):
            print("SUCCESS: Extraction completed successfully!")
            print(f"Extraction Time: {result.get('extraction_time')}")
            print()
            
            # Display system information
            system_info = result.get('system_info', {})
            print("=== SYSTEM INFORMATION ===")
            for key, value in system_info.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            print()
            
            # Display file inventory summary
            file_inventory = result.get('file_inventory', {})
            total_files = file_inventory.get('total_files', 0)
            file_types = file_inventory.get('file_types', {})
            
            print("=== FILE INVENTORY ===")
            print(f"Total Files: {total_files}")
            print(f"File Types: {len(file_types)}")
            for ext, files in file_types.items():
                print(f"  {ext or 'no_ext'}: {len(files)} files")
            print()
            
            # Display container information
            containers = result.get('docker_containers', {})
            print("=== DOCKER CONTAINERS ===")
            print(f"Total Containers: {containers.get('total_containers', 0)}")
            print(f"Running: {len(containers.get('running_containers', []))}")
            print(f"Stopped: {len(containers.get('stopped_containers', []))}")
            print()
            
            # Display interface statistics
            interface_stats = result.get('interface_stats', {})
            link_status = interface_stats.get('link_status', {})
            print("=== INTERFACE STATISTICS ===")
            print(f"Interfaces with Status: {len(link_status)}")
            
            up_count = sum(1 for status in link_status.values() if status.get('status') == 'up')
            down_count = sum(1 for status in link_status.values() if status.get('status') == 'down')
            print(f"Up Interfaces: {up_count}")
            print(f"Down Interfaces: {down_count}")
            print()
            
            # Display log summary
            log_data = result.get('log_data', {})
            log_summary = log_data.get('log_summary', {})
            print("=== LOG ANALYSIS ===")
            print(f"Log Files: {log_summary.get('total_log_files', 0)}")
            print(f"Critical Errors: {log_summary.get('total_errors', 0)}")
            print(f"Warnings: {log_summary.get('total_warnings', 0)}")
            print(f"Reboot Events: {len(log_data.get('reboot_events', []))}")
            print()
            
            # Save detailed results
            output_file = f"test_extraction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            
            print(f"Detailed results saved to: {output_file}")
            print()
            print("=== TEST COMPLETED SUCCESSFULLY ===")
            
        else:
            print(f"ERROR: Extraction failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"ERROR: Extraction failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fixed_extractor()