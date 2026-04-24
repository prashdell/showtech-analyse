# Show Tech Analyzer Skills Collection

## Overview
This collection contains 6 specialized skills for analyzing SONiC show tech-support archives, developed through deep forensic analysis of real-world customer deployments.

## Skills Included

### 1. SONiC Resource Exhaustion Triage
- **Domain:** Memory
- **Focus:** CPU and memory utilization analysis
- **Files:** processes/*, system/load, docker/containers
- **Confidence:** HIGH

### 2. SONiC Interface Connectivity Triage
- **Domain:** Forwarding
- **Focus:** Interface state and connectivity issues
- **Files:** network/interfaces/*, network/routes, network/bgp
- **Confidence:** HIGH

### 3. SONiC Container Health Triage
- **Domain:** Platform
- **Focus:** Docker container status and health
- **Files:** docker/containers/*, logs/*
- **Confidence:** HIGH

### 4. SONiC Version Compatibility Check
- **Domain:** Platform
- **Focus:** Version and platform compatibility
- **Files:** system/version, system/platform
- **Confidence:** MEDIUM

### 5. SONiC Log Analysis
- **Domain:** Debug
- **Focus:** Error detection and log pattern analysis
- **Files:** logs/*
- **Confidence:** HIGH

### 6. SONiC Core Dump Analysis
- **Domain:** Kernel
- **Focus:** Core dump and crash analysis
- **Files:** core/*
- **Confidence:** HIGH

## Usage
These skills can be invoked individually or as a comprehensive analysis suite when processing SONiC show tech-support archives.

## Validation
All skills have been validated against real customer data (SERIAL-REDACTED-SERIAL-REDACTED) and demonstrate high confidence in pattern recognition and issue identification.

## Coverage
- **Total Files Analyzed:** 2,158 files
- **Source Instance:** Mobily Saudi Arabia ToR3
- **Registry Version:** 2026-04-21_1
- **Confidence Distribution:** 5 HIGH, 1 MEDIUM

## Integration
These skills integrate with the SONiC Principal Intelligence Agent framework and can be extended with additional show tech instances for continuous learning.