#!/bin/bash
# Quick test script for Steve Jobs Analyzer

echo "Testing Steve Jobs Analyzer..."

# Create a sample showtech file structure for testing
mkdir -p test_dump/logs
mkdir -p test_dump/docker
mkdir -p test_dump/processes

# Create sample files with issues
echo "Memory usage: 95% - OOM detected" > test_dump/processes/memory.log
echo "Interface eth0 is down, flapping detected" > test_dump/logs/interface.log
echo "Container swss exited with code 1" > test_dump/docker/status.log

# Create a tar.gz file
cd test_dump
tar -czf ../sample_showtech.tar.gz .
cd ..
rm -rf test_dump

echo "Created sample_showtech.tar.gz"
echo "Run: python analyze.py sample_showtech.tar.gz"