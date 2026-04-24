#!/usr/bin/env python3
"""
Steve Jobs SONiC Analyzer - Launcher Test Suite
Tests all scenarios to ensure it just works
"""


# Import showtech extractor integration
sys.path.insert(0, str(Path(__file__).parent))
from showtech_extractor_integration import extract_showtech_archive
import os
import sys
import subprocess
import tempfile
import shutil
import tarfile
from pathlib import Path

def run_test(test_name, command, expected_exit_code=0):
    """Run a test and check results"""
    print(f"Testing: {test_name}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == expected_exit_code:
            print("PASS")
            if result.stdout:
                print(f"Output: {result.stdout[:200]}...")
        else:
            print(f"FAIL - Exit code: {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
        
        print("-" * 50)
        return result.returncode == expected_exit_code
        
    except subprocess.TimeoutExpired:
        print("FAIL - Timeout")
        print("-" * 50)
        return False
    except Exception as e:
        print(f"FAIL - Exception: {e}")
        print("-" * 50)
        return False

def create_test_archive():
    """Create a test archive with various issues"""
    temp_dir = tempfile.mkdtemp()
    
    # Create directory structure
    dump_dir = os.path.join(temp_dir, "test_dump")
    os.makedirs(dump_dir, exist_ok=True)
    
    # Create test files with issues
    with open(os.path.join(dump_dir, "memory.log"), "w") as f:
        f.write("Memory usage: 95% - OOM detected\nHigh memory consumption")
    
    with open(os.path.join(dump_dir, "interface.log"), "w") as f:
        f.write("Interface eth0 is down\nFlapping detected on port1")
    
    with open(os.path.join(dump_dir, "docker.log"), "w") as f:
        f.write("Container swss exited with code 1\nRestart required")
    
    with open(os.path.join(dump_dir, "healthy.log"), "w") as f:
        f.write("All systems operational\nNo issues detected")
    
    # Create tar.gz file
    archive_path = os.path.join(temp_dir, "test_showtech.tar.gz")
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(dump_dir, arcname="test_dump")
    
    shutil.rmtree(dump_dir)
    return archive_path, temp_dir

def main():
    """Run all tests"""
    print("=== Steve Jobs Analyzer Launcher Test Suite ===")
    print()
    
    # Get current directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: No arguments
    total_tests += 1
    if run_test("No arguments", "python analyze.py", expected_exit_code=1):
        tests_passed += 1
    
    # Test 2: Non-existent file
    total_tests += 1
    if run_test("Non-existent file", "python analyze.py nonexistent.tar.gz", expected_exit_code=1):
        tests_passed += 1
    
    # Test 3: Valid archive
    archive_path, temp_dir = create_test_archive()
    total_tests += 1
    if run_test("Valid archive analysis", f"python analyze.py {archive_path}", expected_exit_code=0):
        tests_passed += 1
    
    # Test 4: Help/usage (should fail gracefully)
    total_tests += 1
    if run_test("Help flag", "python analyze.py --help", expected_exit_code=1):
        tests_passed += 1
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    # Summary
    print(f"=== Test Results ===")
    print(f"Passed: {tests_passed}/{total_tests}")
    print(f"Success Rate: {tests_passed/total_tests*100:.1f}%")
    
    if tests_passed == total_tests:
        print("ALL TESTS PASSED - Steve Jobs would be proud! ")
        print("It just works.")
    else:
        print("Some tests failed - needs refinement")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)