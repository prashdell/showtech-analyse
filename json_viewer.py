#!/usr/bin/env python3
"""
JSON Report Viewer - Converts technical JSON to human-readable HTML
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def create_html_report(json_file_path):
    """Convert JSON report to human-readable HTML"""
    
    # Load JSON data
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    # Create HTML content
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SONiC Technical Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; border-bottom: 3px solid #007acc; padding-bottom: 20px; margin-bottom: 30px; }}
        .section {{ margin-bottom: 30px; border: 1px solid #ddd; border-radius: 5px; padding: 15px; }}
        .section h2 {{ color: #007acc; border-bottom: 2px solid #007acc; padding-bottom: 5px; }}
        .critical {{ color: #d32f2f; font-weight: bold; }}
        .warning {{ color: #f57c00; font-weight: bold; }}
        .good {{ color: #388e3c; font-weight: bold; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background-color: #e3f2fd; border-radius: 5px; }}
        .recommendation {{ background-color: #fff3e0; padding: 10px; margin: 5px 0; border-left: 4px solid #ff9800; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #007acc; color: white; }}
        .collapsible {{ background-color: #f1f1f1; cursor: pointer; padding: 10px; border: none; text-align: left; outline: none; font-size: 15px; }}
        .content {{ padding: 0 10px; max-height: 0; overflow: hidden; transition: max-height 0.2s ease-out; }}
        .active {{ max-height: 500px; }}
        .health-score {{ font-size: 24px; font-weight: bold; padding: 10px; border-radius: 5px; text-align: center; }}
    </style>
    <script>
        function toggleSection(id) {{
            var content = document.getElementById(id);
            content.classList.toggle("active");
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SONiC Technical Analysis Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Archive: {Path(json_file_path).parent.name}</p>
        </div>
"""
    
    # System Overview
    if 'system_overview' in data:
        html_content += """
        <div class="section">
            <h2>1. System Overview</h2>
            <table>
"""
        overview = data['system_overview']
        for key, value in overview.items():
            html_content += f"                <tr><td>{key.replace('_', ' ').title()}</td><td>{value}</td></tr>\n"
        html_content += """
            </table>
        </div>
"""
    
    # Memory Analysis
    if 'memory_analysis' in data:
        html_content += """
        <div class="section">
            <h2>2. Memory Analysis</h2>
"""
        memory = data['memory_analysis']
        html_content += f"            <div class='metric'>Total Memory: {memory.get('total_memory', 'Unknown')}</div>\n"
        html_content += f"            <div class='metric'>Available Memory: {memory.get('available_memory', 'Unknown')}</div>\n"
        
        if memory.get('oom_events'):
            html_content += f"            <div class='critical'>OOM Events: {len(memory['oom_events'])}</div>\n"
            html_content += "            <button class='collapsible' onclick=\"toggleSection('oom-details')\">Show OOM Details</button>\n"
            html_content += "            <div id='oom-details' class='content'>\n"
            for event in memory['oom_events']:
                html_content += f"                <p>Line {event['line']}: {event['content']}</p>\n"
            html_content += "            </div>\n"
        
        html_content += "        </div>\n"
    
    # Interface Analysis
    if 'interface_analysis' in data:
        html_content += """
        <div class="section">
            <h2>3. Interface Analysis</h2>
"""
        interfaces = data['interface_analysis']
        total = interfaces.get('total_interfaces', 0)
        up = len(interfaces.get('up_interfaces', []))
        down = len(interfaces.get('down_interfaces', []))
        
        if total > 0:
            health_pct = (up / total) * 100
            health_class = 'good' if health_pct > 80 else 'warning' if health_pct > 60 else 'critical'
            html_content += f"            <div class='health-score {health_class}'>Interface Health: {health_pct:.1f}%</div>\n"
        
        html_content += f"            <div class='metric'>Total Interfaces: {total}</div>\n"
        html_content += f"            <div class='metric'>Up Interfaces: {up}</div>\n"
        html_content += f"            <div class='metric'>Down Interfaces: {down}</div>\n"
        
        if interfaces.get('down_interfaces'):
            html_content += "            <button class='collapsible' onclick=\"toggleSection('down-interfaces')\">Show Down Interfaces</button>\n"
            html_content += "            <div id='down-interfaces' class='content'>\n"
            html_content += "                <ul>\n"
            for intf in interfaces['down_interfaces'][:10]:
                html_content += f"                    <li>{intf}</li>\n"
            if len(interfaces['down_interfaces']) > 10:
                html_content += f"                    <li>... and {len(interfaces['down_interfaces']) - 10} more</li>\n"
            html_content += "                </ul>\n"
            html_content += "            </div>\n"
        
        html_content += "        </div>\n"
    
    # Container Analysis
    if 'container_analysis' in data:
        html_content += """
        <div class="section">
            <h2>4. Container Analysis</h2>
"""
        containers = data['container_analysis']
        total = containers.get('total_containers', 0)
        running = len(containers.get('running_containers', []))
        stopped = len(containers.get('stopped_containers', []))
        
        if total > 0:
            health_pct = (running / total) * 100
            health_class = 'good' if health_pct > 80 else 'warning' if health_pct > 60 else 'critical'
            html_content += f"            <div class='health-score {health_class}'>Container Health: {health_pct:.1f}%</div>\n"
        
        html_content += f"            <div class='metric'>Total Containers: {total}</div>\n"
        html_content += f"            <div class='metric'>Running: {running}</div>\n"
        html_content += f"            <div class='metric'>Stopped: {stopped}</div>\n"
        
        html_content += "        </div>\n"
    
    # BGP Analysis
    if 'bgp_analysis' in data:
        html_content += """
        <div class="section">
            <h2>5. BGP Analysis</h2>
"""
        bgp = data['bgp_analysis']
        neighbors = len(bgp.get('bgp_neighbors', []))
        established = len(bgp.get('established_sessions', []))
        failed = len(bgp.get('failed_sessions', []))
        
        html_content += f"            <div class='metric'>BGP Neighbors: {neighbors}</div>\n"
        html_content += f"            <div class='metric'>Established Sessions: {established}</div>\n"
        html_content += f"            <div class='metric'>Failed Sessions: {failed}</div>\n"
        
        if established + failed > 0:
            success_rate = (established / (established + failed)) * 100
            health_class = 'good' if success_rate > 80 else 'warning' if success_rate > 60 else 'critical'
            html_content += f"            <div class='health-score {health_class}'>BGP Success Rate: {success_rate:.1f}%</div>\n"
        
        html_content += "        </div>\n"
    
    # Performance Indicators
    if 'performance_indicators' in data:
        html_content += """
        <div class="section">
            <h2>6. Performance Indicators</h2>
"""
        perf = data['performance_indicators']
        for key, value in perf.items():
            html_content += f"            <div class='metric'>{key.replace('_', ' ').title()}: {value}</div>\n"
        html_content += "        </div>\n"
    
    # Recommendations
    html_content += """
        <div class="section">
            <h2>7. Technical Recommendations</h2>
"""
    
    recommendations = []
    memory = data.get('memory_analysis', {})
    interfaces = data.get('interface_analysis', {})
    containers = data.get('container_analysis', {})
    bgp = data.get('bgp_analysis', {})
    logs = data.get('log_analysis', {})
    
    if memory.get('oom_events'):
        recommendations.append("CRITICAL: OOM events detected - investigate memory leaks and consider memory optimization")
    
    if interfaces.get('down_interfaces'):
        recommendations.append("Interface(s) down - check physical connections and configuration")
    
    if containers.get('stopped_containers'):
        recommendations.append("Container(s) stopped - restart failed containers and check logs")
    
    if bgp.get('failed_sessions'):
        recommendations.append("BGP session issues - check BGP configuration and network connectivity")
    
    for i, rec in enumerate(recommendations, 1):
        html_content += f"            <div class='recommendation'>{i}. {rec}</div>\n"
    
    if not recommendations:
        html_content += "            <div class='good'>No specific recommendations - system appears healthy</div>\n"
    
    html_content += """
        </div>
    </div>
</body>
</html>
"""
    
    # Save HTML file
    output_path = json_file_path.replace('.json', '.html')
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    return output_path

def main():
    if len(sys.argv) != 2:
        print("Usage: python json_viewer.py <json_report_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    if not json_file.endswith('.json'):
        print("Error: Please provide a JSON file")
        sys.exit(1)
    
    if not Path(json_file).exists():
        print(f"Error: File not found: {json_file}")
        sys.exit(1)
    
    try:
        html_file = create_html_report(json_file)
        print(f"HTML report created: {html_file}")
        
        # Auto-open in browser
        import webbrowser
        webbrowser.open(f'file://{Path(html_file).absolute()}')
        
    except Exception as e:
        print(f"Error creating HTML report: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()