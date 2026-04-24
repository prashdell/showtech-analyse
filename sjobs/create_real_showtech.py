#!/usr/bin/env python3
"""
Create Real Showtech Test Archive
Uses actual SONiC file structure from real deployments
"""

import os
import tarfile
import tempfile
import shutil
from datetime import datetime
# Import showtech extractor integration
sys.path.insert(0, str(Path(__file__).parent))
from showtech_extractor_integration import extract_showtech_archive

def create_real_showtech():
    """Create a realistic showtech archive based on real data"""
    temp_dir = tempfile.mkdtemp()
    dump_dir = os.path.join(temp_dir, "sonic_dump_ToR3_20260331_073119")
    
    # Create directory structure based on real showtech
    dirs_to_create = [
        "dump",
        "debugsh",
        "debugsh/orchagent",
        "debugsh/sai", 
        "logs",
        "docker",
        "docker/containers",
        "processes"
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(os.path.join(dump_dir, dir_path), exist_ok=True)
    
    # Create realistic files with real issues
    files_to_create = [
        ("dump/ASIC_DB.json", '{"memory_usage": "95%", "status": "critical", "oom_detected": true}'),
        ("debugsh/orchagent/copp_counters1_dump.log", "Memory allocation failed\nOOM killer activated\nProcess swss using 95% memory"),
        ("debugsh/sai/sai_vlan_dump.log", "Interface eth0 status: down\nLink flapping detected\nPhysical layer errors"),
        ("logs/syslog", "ERROR: Container swss exited with code 1\nWARNING: Memory exhaustion detected"),
        ("docker/containers/swss_status", "State: dead\nRestartCount: 5\nExitCode: 1"),
        ("processes/memory_info", "swss: 95% memory usage\ntotal_memory: 8GB\navailable: 400MB"),
        ("dump/bash_history.admin", "show version\nshow interface\ndocker ps -a\nfree -m"),
        ("debugsh/ports_dump.log", "Ethernet0: down\nEthernet1: up\nEthernet2: flapping")
    ]
    
    for file_path, content in files_to_create:
        full_path = os.path.join(dump_dir, file_path)
        with open(full_path, 'w') as f:
            f.write(content)
    
    # Create tar.gz file
    archive_path = os.path.join(temp_dir, "real_showtech.tar.gz")
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(dump_dir, arcname="sonic_dump_ToR3_20260331_073119")
    
    shutil.rmtree(dump_dir)
    return archive_path, temp_dir

def main():
    print("Creating realistic showtech archive...")
    archive_path, temp_dir = create_real_showtech()
    print(f"Created: {archive_path}")
    print(f"Test with: python analyze_real.py {archive_path}")
    return archive_path

if __name__ == "__main__":
    main()