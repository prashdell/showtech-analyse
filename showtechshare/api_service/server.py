#!/usr/bin/env python3
"""
SONiC File Intelligence REST API Server
Provides REST API endpoints for accessing SONiC file intelligence database
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from pathlib import Path
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SONiCKnowledgeAPI:
    """REST API for SONiC file intelligence"""
    
    def __init__(self):
        self.knowledge_dir = Path("./showtechshare/knowledge_database")
        self.file_intelligence = self.load_file_intelligence()
        self.production_patterns = self.load_production_patterns()
        self.customer_insights = self.load_customer_insights()
        self.correlation_matrix = self.load_correlation_matrix()
        
    def load_file_intelligence(self):
        """Load file intelligence database"""
        try:
            with open(self.knowledge_dir / "file_intelligence.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("File intelligence database not found")
            return {}
    
    def load_production_patterns(self):
        """Load production patterns database"""
        try:
            with open(self.knowledge_dir / "production_patterns.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("Production patterns database not found")
            return {}
    
    def load_customer_insights(self):
        """Load customer insights database"""
        try:
            with open(self.knowledge_dir / "customer_insights.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("Customer insights database not found")
            return {}
    
    def load_correlation_matrix(self):
        """Load correlation matrix"""
        try:
            with open(self.knowledge_dir / "correlation_matrix.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("Correlation matrix not found")
            return {}

# Initialize API
api = SONiCKnowledgeAPI()

@app.route('/')
def index():
    """API documentation and status"""
    return jsonify({
        "name": "SONiC File Intelligence API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "/api/files": "List all files with intelligence",
            "/api/files/<filename>": "Get specific file intelligence",
            "/api/categories": "List all categories",
            "/api/categories/<category>": "Get files by category",
            "/api/patterns": "Get production patterns",
            "/api/customers": "Get customer insights",
            "/api/correlations": "Get correlation matrix",
            "/api/search": "Search files by keywords",
            "/api/analyze": "Analyze showtech archive",
            "/api/health": "API health check"
        }
    })

@app.route('/api/health')
def health_check():
    """API health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database_status": "connected" if api.file_intelligence else "disconnected"
    })

@app.route('/api/files')
def get_all_files():
    """Get all files with intelligence data"""
    try:
        files = []
        for filename, data in api.file_intelligence.get('files', {}).items():
            files.append({
                'name': filename,
                'purpose': data.get('purpose', ''),
                'category': data.get('category', ''),
                'escalation': data.get('escalation', ''),
                'correlation_targets': data.get('correlation_targets', []),
                'key_info': data.get('key_info', ''),
                'production_patterns': data.get('production_patterns', {})
            })
        return jsonify({
            'total_files': len(files),
            'files': files
        })
    except Exception as e:
        logger.error(f"Error getting all files: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/files/<filename>')
def get_file_details(filename):
    """Get specific file intelligence"""
    try:
        file_data = api.file_intelligence.get('files', {}).get(filename)
        if not file_data:
            return jsonify({'error': f'File {filename} not found'}), 404
        
        return jsonify({
            'name': filename,
            'intelligence': file_data
        })
    except Exception as e:
        logger.error(f"Error getting file {filename}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories')
def get_categories():
    """Get all categories"""
    try:
        categories = api.file_intelligence.get('categories', {})
        return jsonify({
            'categories': categories,
            'total_categories': len(categories)
        })
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/<category>')
def get_files_by_category(category):
    """Get files by category"""
    try:
        files = []
        for filename, data in api.file_intelligence.get('files', {}).items():
            if data.get('category') == category:
                files.append({
                    'name': filename,
                    'purpose': data.get('purpose', ''),
                    'escalation': data.get('escalation', ''),
                    'key_info': data.get('key_info', '')
                })
        
        return jsonify({
            'category': category,
            'files': files,
            'total_files': len(files)
        })
    except Exception as e:
        logger.error(f"Error getting files for category {category}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/patterns')
def get_production_patterns():
    """Get production patterns"""
    try:
        return jsonify({
            'production_patterns': api.production_patterns,
            'metadata': {
                'customer_types': list(api.production_patterns.get('customer_patterns', {}).keys()),
                'platform_types': list(api.production_patterns.get('platform_patterns', {}).keys()),
                'temporal_patterns': list(api.production_patterns.get('temporal_patterns', {}).keys())
            }
        })
    except Exception as e:
        logger.error(f"Error getting production patterns: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers')
def get_customer_insights():
    """Get customer insights"""
    try:
        return jsonify({
            'customer_insights': api.customer_insights,
            'metadata': {
                'customer_profiles': list(api.customer_insights.get('customer_profiles', {}).keys()),
                'issue_patterns': list(api.customer_insights.get('issue_resolution_patterns', {}).keys())
            }
        })
    except Exception as e:
        logger.error(f"Error getting customer insights: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/correlations')
def get_correlation_matrix():
    """Get correlation matrix"""
    try:
        return jsonify({
            'correlation_matrix': api.correlation_matrix,
            'metadata': {
                'total_correlations': len(api.correlation_matrix),
                'high_priority_correlations': len([k for k, v in api.correlation_matrix.items() if v.get('priority') == 'HIGH'])
            }
        })
    except Exception as e:
        logger.error(f"Error getting correlation matrix: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search')
def search_files():
    """Search files by keywords"""
    try:
        query = request.args.get('q', '').lower()
        category = request.args.get('category', '')
        priority = request.args.get('priority', '')
        
        if not query:
            return jsonify({'error': 'Search query required'}), 400
        
        results = []
        for filename, data in api.file_intelligence.get('files', {}).items():
            # Apply filters
            if category and data.get('category') != category:
                continue
            if priority and data.get('escalation') != priority.upper():
                continue
            
            # Search in multiple fields
            search_fields = [
                filename.lower(),
                data.get('purpose', '').lower(),
                data.get('used_for', '').lower(),
                data.get('key_info', '').lower(),
                ' '.join(data.get('correlation_targets', [])).lower()
            ]
            
            if any(query in field for field in search_fields):
                results.append({
                    'name': filename,
                    'purpose': data.get('purpose', ''),
                    'category': data.get('category', ''),
                    'escalation': data.get('escalation', ''),
                    'relevance_score': sum(1 for field in search_fields if query in field)
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return jsonify({
            'query': query,
            'filters': {
                'category': category,
                'priority': priority
            },
            'total_results': len(results),
            'results': results
        })
    except Exception as e:
        logger.error(f"Error searching files: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_showtech():
    """Analyze showtech archive (placeholder for future implementation)"""
    try:
        data = request.get_json()
        if not data or 'archive_path' not in data:
            return jsonify({'error': 'Archive path required'}), 400
        
        # This would integrate with the comprehensive file intelligence analyzer
        # For now, return a placeholder response
        return jsonify({
            'message': 'Showtech analysis endpoint - integration with comprehensive analyzer',
            'archive_path': data['archive_path'],
            'status': 'placeholder',
            'integration_required': True
        })
    except Exception as e:
        logger.error(f"Error analyzing showtech: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/metadata')
def get_metadata():
    """Get database metadata"""
    try:
        metadata_path = api.knowledge_dir / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            return jsonify(metadata)
        else:
            return jsonify({
                'error': 'Metadata file not found',
                'message': 'Run knowledge database generator first'
            }), 404
    except Exception as e:
        logger.error(f"Error getting metadata: {e}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting SONiC File Intelligence API Server...")
    print("Available endpoints:")
    print("  GET  /api/files - List all files")
    print("  GET  /api/files/<filename> - Get file details")
    print("  GET  /api/categories - List categories")
    print("  GET  /api/patterns - Get production patterns")
    print("  GET  /api/customers - Get customer insights")
    print("  GET  /api/correlations - Get correlation matrix")
    print("  GET  /api/search?q=<query> - Search files")
    print("  GET  /api/health - Health check")
    print("  GET  /api/metadata - Database metadata")
    print("\nServer starting on http://localhost:5000")
    print("Press Ctrl+C to stop")
    
    app.run(host='IP-ADDRESS-209', port=5000, debug=True)