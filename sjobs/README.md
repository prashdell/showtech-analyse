# Steve Jobs SONiC Analyzer

## The Problem
Too many files. Too much complexity. Too many choices.

## The Solution
One command. Clear results. No complexity.

## Usage
```bash
python analyze.py <showtech_file>
```

## What It Does
1. Opens your show tech file
2. Finds what's wrong
3. Tells you how to fix it
4. Done.

## Example Output
```
=== SONiC Analysis ===

CRITICAL: Memory exhaustion (94% confidence)
   - Fix: Restart swss container

WARNING: Interface flapping (87% confidence)
   - Fix: Check cable connection

FIXES:
  docker restart swss
  check physical connections

Done.
```

## That's It.
No configuration. No options. No complexity.

It just works.