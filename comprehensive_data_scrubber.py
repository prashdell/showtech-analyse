#!/usr/bin/env python3
"""
Comprehensive Data Scrubbing Script for SONiC ShowTech Analysis
Removes all sensitive data while preserving technical intelligence
"""

import json
import re
import os
import sys
from datetime import datetime
from pathlib import Path

class DataScrubber:
    def __init__(self):
        self.scrubbing_log = []
        self.preserve_patterns = {
            'technical_metrics': True,
            'confidence_levels': True,
            'analysis_patterns': True,
            'platform_intelligence': True
        }
        
        # Sensitive data patterns
        self.ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        self.mac_pattern = re.compile(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b')
        self.hostname_pattern = re.compile(r'\b[A-Z]{3,}-[A-Z0-9-]+\b')
        self.serial_pattern = re.compile(r'\b[A-Z0-9]{8,}\b')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        
        # Customer name patterns (common patterns found in files)
        self.customer_patterns = [
            r'211453514 KS_Electronics',
            r'Arvato Ireland Limited',
            r'ASSOCIACAO DE POUPANCA E EMPRE',
            r'Healthcare Customer',
            r'University of Cambridge',
            r'VOLTAGE PARK',
            r'WORLD WIDE TECHNOLOGY',
            r'UNIV OF UTAH',
            r'Zoho',
            r'Chubb',
            r'ENBD',
            r'Mobily - Saudi Arabia',
            r'KS_Electronics',
            r'Prasanth_Sasidharan',
            r'OneDrive - Dell Technologies'
        ]
        
        # File path patterns to scrub
        self.path_patterns = [
            r'/c/Users/[^/]+/OneDrive - Dell Technologies/Documents/Customer Documents',
            r'/c/Users/[^/]+/OneDrive[^/]*',
            r'Customer Documents'
        ]
        
    def log_scrubbing_action(self, file_path, data_type, count, action):
        """Log scrubbing actions for audit trail"""
        self.scrubbing_log.append({
            'timestamp': datetime.now().isoformat(),
            'file': str(file_path),
            'data_type': data_type,
            'count': count,
            'action': action
        })
        
    def scrub_ip_addresses(self, text):
        """Replace IP addresses with placeholder"""
        def replace_ip(match):
            return f"IP-ADDRESS-{hash(match.group()) % 1000:03d}"
        
        matches = self.ip_pattern.findall(text)
        if matches:
            self.log_scrubbing_action("current", "IP_ADDRESS", len(matches), "replaced_with_placeholder")
        return self.ip_pattern.sub(replace_ip, text)
        
    def scrub_mac_addresses(self, text):
        """Replace MAC addresses with placeholder"""
        def replace_mac(match):
            return "MAC-ADDRESS-REDACTED"
            
        matches = self.mac_pattern.findall(text)
        if matches:
            self.log_scrubbing_action("current", "MAC_ADDRESS", len(matches), "replaced_with_placeholder")
        return self.mac_pattern.sub(replace_mac, text)
        
    def scrub_hostnames(self, text):
        """Replace hostnames with generic placeholders"""
        def replace_hostname(match):
            hostname = match.group()
            # Preserve the pattern type (leaf, spine, etc.)
            if 'leaf' in hostname.lower():
                return "LEAF-SWITCH-REDACTED"
            elif 'spine' in hostname.lower():
                return "SPINE-SWITCH-REDACTED"
            elif 'tor' in hostname.lower():
                return "TOR-SWITCH-REDACTED"
            else:
                return "HOSTNAME-REDACTED"
                
        matches = self.hostname_pattern.findall(text)
        if matches:
            self.log_scrubbing_action("current", "HOSTNAME", len(matches), "replaced_with_placeholder")
        return self.hostname_pattern.sub(replace_hostname, text)
        
    def scrub_customer_names(self, text):
        """Replace customer names with generic placeholders"""
        for pattern in self.customer_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                self.log_scrubbing_action("current", "CUSTOMER_NAME", len(matches), "replaced_with_placeholder")
                text = re.sub(pattern, "CUSTOMER-REDACTED", text, flags=re.IGNORECASE)
        return text
        
    def scrub_file_paths(self, text):
        """Replace sensitive file paths with generic ones"""
        for pattern in self.path_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                self.log_scrubbing_action("current", "FILE_PATH", len(matches), "replaced_with_placeholder")
                text = re.sub(pattern, "/SANITIZED_PATH/Customer_Documents", text, flags=re.IGNORECASE)
        return text
        
    def scrub_serial_numbers(self, text):
        """Replace serial numbers with placeholders"""
        def replace_serial(match):
            return "SERIAL-REDACTED"
            
        matches = self.serial_pattern.findall(text)
        if matches:
            self.log_scrubbing_action("current", "SERIAL_NUMBER", len(matches), "replaced_with_placeholder")
        return self.serial_pattern.sub(replace_serial, text)
        
    def scrub_emails(self, text):
        """Replace email addresses with placeholders"""
        def replace_email(match):
            return "EMAIL-REDACTED@example.com"
            
        matches = self.email_pattern.findall(text)
        if matches:
            self.log_scrubbing_action("current", "EMAIL", len(matches), "replaced_with_placeholder")
        return self.email_pattern.sub(replace_email, text)
        
    def scrub_json_file(self, file_path):
        """Scrub a JSON file while preserving structure and technical data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_size = len(content)
            
            # Apply all scrubbing functions
            content = self.scrub_ip_addresses(content)
            content = self.scrub_mac_addresses(content)
            content = self.scrub_hostnames(content)
            content = self.scrub_customer_names(content)
            content = self.scrub_file_paths(content)
            content = self.scrub_serial_numbers(content)
            content = self.scrub_emails(content)
            
            # Validate JSON is still valid
            try:
                json.loads(content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                scrubbed_size = len(content)
                self.log_scrubbing_action(file_path, "JSON_FILE", 1, 
                    f"size_changed_from_{original_size}_to_{scrubbed_size}")
                return True
                
            except json.JSONDecodeError as e:
                print(f"Warning: JSON became invalid after scrubbing {file_path}: {e}")
                return False
                
        except Exception as e:
            print(f"Error scrubbing {file_path}: {e}")
            return False
            
    def scrub_markdown_file(self, file_path):
        """Scrub a markdown file while preserving technical content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_size = len(content)
            
            # Apply scrubbing (preserve code blocks with technical info)
            lines = content.split('\n')
            scrubbed_lines = []
            in_code_block = False
            
            for line in lines:
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    scrubbed_lines.append(line)
                    continue
                    
                if in_code_block:
                    # In code blocks, only scrub obvious sensitive data
                    line = self.scrub_ip_addresses(line)
                    line = self.scrub_mac_addresses(line)
                    scrubbed_lines.append(line)
                else:
                    # In regular text, scrub everything
                    line = self.scrub_ip_addresses(line)
                    line = self.scrub_mac_addresses(line)
                    line = self.scrub_hostnames(line)
                    line = self.scrub_customer_names(line)
                    line = self.scrub_file_paths(line)
                    line = self.scrub_serial_numbers(line)
                    line = self.scrub_emails(line)
                    scrubbed_lines.append(line)
                    
            content = '\n'.join(scrubbed_lines)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            scrubbed_size = len(content)
            self.log_scrubbing_action(file_path, "MARKDOWN_FILE", 1,
                f"size_changed_from_{original_size}_to_{scrubbed_size}")
            return True
            
        except Exception as e:
            print(f"Error scrubbing markdown {file_path}: {e}")
            return False
            
    def scrub_python_file(self, file_path):
        """Scrub a Python file while preserving functionality"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_size = len(content)
            
            # Only scrub obvious sensitive data in Python files
            content = self.scrub_ip_addresses(content)
            content = self.scrub_mac_addresses(content)
            content = self.scrub_emails(content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            scrubbed_size = len(content)
            self.log_scrubbing_action(file_path, "PYTHON_FILE", 1,
                f"size_changed_from_{original_size}_to_{scrubbed_size}")
            return True
            
        except Exception as e:
            print(f"Error scrubbing Python file {file_path}: {e}")
            return False
            
    def process_directory(self, directory_path):
        """Process all files in a directory"""
        directory = Path(directory_path)
        processed_files = 0
        failed_files = 0
        
        print(f"Processing directory: {directory}")
        
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                file_ext = file_path.suffix.lower()
                
                if file_ext == '.json':
                    if self.scrub_json_file(file_path):
                        processed_files += 1
                    else:
                        failed_files += 1
                elif file_ext in ['.md', '.txt']:
                    if self.scrub_markdown_file(file_path):
                        processed_files += 1
                    else:
                        failed_files += 1
                elif file_ext == '.py':
                    if self.scrub_python_file(file_path):
                        processed_files += 1
                    else:
                        failed_files += 1
                elif file_ext in ['.sh', '.log']:
                    # Scrub shell scripts and logs
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        content = self.scrub_ip_addresses(content)
                        content = self.scrub_customer_names(content)
                        content = self.scrub_file_paths(content)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        processed_files += 1
                    except Exception as e:
                        print(f"Error scrubbing {file_path}: {e}")
                        failed_files += 1
                        
        return processed_files, failed_files
        
    def generate_scrubbing_report(self):
        """Generate a comprehensive scrubbing report"""
        report = {
            'scrubbing_timestamp': datetime.now().isoformat(),
            'total_actions': len(self.scrubbing_log),
            'actions_by_type': {},
            'files_processed': set(),
            'detailed_log': self.scrubbing_log
        }
        
        for action in self.scrubbing_log:
            data_type = action['data_type']
            if data_type not in report['actions_by_type']:
                report['actions_by_type'][data_type] = 0
            report['actions_by_type'][data_type] += action['count']
            report['files_processed'].add(action['file'])
            
        report['files_processed'] = len(report['files_processed'])
        return report

def main():
    if len(sys.argv) != 2:
        print("Usage: python comprehensive_scrubber.py <directory_path>")
        sys.exit(1)
        
    directory_path = sys.argv[1]
    scrubber = DataScrubber()
    
    print("Starting comprehensive data scrubbing...")
    print(f"Target directory: {directory_path}")
    
    processed, failed = scrubber.process_directory(directory_path)
    
    print(f"\nScrubbing completed:")
    print(f"Files processed successfully: {processed}")
    print(f"Files failed: {failed}")
    
    # Generate report
    report = scrubber.generate_scrubbing_report()
    report_path = Path(directory_path) / "scrubbing_report.json"
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
        
    print(f"Scrubbing report saved to: {report_path}")
    print(f"Total scrubbing actions: {report['total_actions']}")
    
    for data_type, count in report['actions_by_type'].items():
        print(f"  {data_type}: {count} items scrubbed")

if __name__ == "__main__":
    main()