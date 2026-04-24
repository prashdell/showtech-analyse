#!/usr/bin/env python3
"""
Integrated Complete Learning-Enhanced Showtech Processor
Combines Method 1 (Complete Analysis) + Method 3 (Learning-Enhanced)
"""

import sys
import os
import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the showtech_analyse directory to Python path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from sonic_principal_intelligence_complete import SONiCPrincipalIntelligenceComplete
    from knowledge_aware_skill_invoker import KnowledgeAwareSkillInvoker
    from automatic_knowledge_integrator import get_global_integrator
    from enhanced_skill_invoker import EnhancedSkillInvoker
    from automatic_knowledge_system import AutomaticKnowledgeSystem
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Make sure you're running this from the showtech_analyse directory")
    sys.exit(1)

class IntegratedLearningProcessor:
    """Complete analysis with learning-enhanced execution"""
    
    def __init__(self):
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.logger.info("Initializing integrated learning processor...")
        
        try:
            self.complete_analyzer = SONiCPrincipalIntelligenceComplete()
            self.logger.info("✓ Complete analyzer initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize complete analyzer: {e}")
            self.complete_analyzer = None
            
        try:
            self.learning_invoker = KnowledgeAwareSkillInvoker()
            self.logger.info("✓ Learning invoker initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize learning invoker: {e}")
            self.learning_invoker = None
            
        try:
            self.knowledge_integrator = get_global_integrator()
            self.logger.info("✓ Knowledge integrator initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize knowledge integrator: {e}")
            self.knowledge_integrator = None
            
        try:
            self.enhanced_invoker = EnhancedSkillInvoker()
            self.logger.info("✓ Enhanced invoker initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize enhanced invoker: {e}")
            self.enhanced_invoker = None
            
        try:
            self.knowledge_system = AutomaticKnowledgeSystem()
            self.logger.info("✓ Knowledge system initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize knowledge system: {e}")
            self.knowledge_system = None
        
        self.logger.info("Integrated learning processor initialization complete")
    
    def process_showtech_integrated(self, archive_path: str) -> dict:
        """Process showtech with complete analysis + learning enhancement"""
        
        if not os.path.exists(archive_path):
            return {
                'success': False,
                'error': f'Archive not found: {archive_path}',
                'execution_summary': {'total_execution_time': 0}
            }
        
        start_time = time.time()
        self.logger.info(f"Starting integrated processing of {archive_path}")
        
        result = {
            'success': True,
            'execution_summary': {
                'method': 'integrated_complete_learning',
                'total_execution_time': 0,
                'phases_completed': 0,
                'learning_integration': 'active',
                'completeness': 'full'
            },
            'complete_analysis': {},
            'learning_enhancements': {},
            'specialized_analysis': {},
            'knowledge_capture': {},
            'performance_metrics': {},
            'next_steps': {}
        }
        
        try:
            # Phase 1: Learning-Enhanced Context Analysis
            self.logger.info("Phase 1: Learning-enhanced context analysis")
            phase_start = time.time()
            
            learning_context = {}
            if self.learning_invoker and self.knowledge_system:
                try:
                    # Get relevant patterns from knowledge base
                    relevant_patterns = self.knowledge_system.get_relevant_patterns(archive_path)
                    learning_context = {
                        'archive_path': archive_path,
                        'relevant_patterns': relevant_patterns,
                        'analysis_timestamp': time.time()
                    }
                    self.logger.info(f"✓ Found {len(relevant_patterns)} relevant patterns")
                except Exception as e:
                    self.logger.warning(f"Learning context analysis failed: {e}")
                    learning_context = {'archive_path': archive_path}
            else:
                learning_context = {'archive_path': archive_path}
                self.logger.warning("Learning components not available, using basic context")
            
            result['execution_summary']['phases_completed'] = 1
            phase_time = time.time() - phase_start
            self.logger.info(f"Phase 1 completed in {phase_time:.2f} seconds")
            
            # Phase 2: Complete Analysis with Learning Optimization
            self.logger.info("Phase 2: Complete analysis with learning optimization")
            phase_start = time.time()
            
            complete_result = {}
            if self.complete_analyzer:
                try:
                    # Try to use learning context if supported
                    if hasattr(self.complete_analyzer, 'process_showtech_archive'):
                        complete_result = self.complete_analyzer.process_showtech_archive(archive_path)
                    else:
                        self.logger.warning("Complete analyzer doesn't support learning context, using standard analysis")
                        complete_result = {'error': 'Method not available'}
                except Exception as e:
                    self.logger.error(f"Complete analysis failed: {e}")
                    complete_result = {'error': str(e)}
            else:
                self.logger.warning("Complete analyzer not available")
                complete_result = {'error': 'Component not available'}
            
            result['complete_analysis'] = complete_result
            result['execution_summary']['phases_completed'] = 2
            phase_time = time.time() - phase_start
            self.logger.info(f"Phase 2 completed in {phase_time:.2f} seconds")
            
            # Phase 3: Real-Time Learning Integration
            self.logger.info("Phase 3: Real-time learning integration")
            phase_start = time.time()
            
            learning_result = {}
            if self.learning_invoker:
                try:
                    learning_result = self.learning_invoker.execute_with_learning(archive_path)
                    self.logger.info("✓ Learning integration completed")
                except Exception as e:
                    self.logger.error(f"Learning integration failed: {e}")
                    learning_result = {'error': str(e)}
            else:
                self.logger.warning("Learning invoker not available")
                learning_result = {'error': 'Component not available'}
            
            result['learning_enhancements'] = learning_result
            result['execution_summary']['phases_completed'] = 3
            phase_time = time.time() - phase_start
            self.logger.info(f"Phase 3 completed in {phase_time:.2f} seconds")
            
            # Phase 4: Enhanced Skill Execution with Fallbacks
            self.logger.info("Phase 4: Enhanced skill execution with fallbacks")
            phase_start = time.time()
            
            specialized_result = {}
            if self.enhanced_invoker:
                try:
                    specialized_result = self.enhanced_invoker.invoke_skills(archive_path)
                    self.logger.info("✓ Enhanced skill execution completed")
                except Exception as e:
                    self.logger.error(f"Enhanced skill execution failed: {e}")
                    specialized_result = {'error': str(e)}
            else:
                self.logger.warning("Enhanced invoker not available")
                specialized_result = {'error': 'Component not available'}
            
            result['specialized_analysis'] = specialized_result
            result['execution_summary']['phases_completed'] = 4
            phase_time = time.time() - phase_start
            self.logger.info(f"Phase 4 completed in {phase_time:.2f} seconds")
            
            # Phase 5: Integrated Knowledge Capture
            self.logger.info("Phase 5: Integrated knowledge capture")
            phase_start = time.time()
            
            integrated_knowledge = self._capture_integrated_knowledge(
                complete_result, learning_result, specialized_result, learning_context
            )
            
            result['knowledge_capture'] = integrated_knowledge
            result['execution_summary']['phases_completed'] = 5
            phase_time = time.time() - phase_start
            self.logger.info(f"Phase 5 completed in {phase_time:.2f} seconds")
            
            # Phase 6: Comprehensive Reporting with Learning Insights
            self.logger.info("Phase 6: Comprehensive reporting with learning insights")
            phase_start = time.time()
            
            final_result = self._generate_integrated_report(
                complete_result, learning_result, specialized_result, 
                integrated_knowledge, time.time() - start_time
            )
            
            result.update(final_result)
            result['execution_summary']['phases_completed'] = 6
            phase_time = time.time() - phase_start
            self.logger.info(f"Phase 6 completed in {phase_time:.2f} seconds")
            
        except Exception as e:
            self.logger.error(f"Integrated processing failed: {e}")
            result['success'] = False
            result['error'] = str(e)
        
        result['execution_summary']['total_execution_time'] = time.time() - start_time
        self.logger.info(f"Integrated processing completed in {result['execution_summary']['total_execution_time']:.2f} seconds")
        
        return result
    
    def _capture_integrated_knowledge(self, complete_result: dict, learning_result: dict, 
                                   specialized_result: dict, context: dict) -> dict:
        """Capture comprehensive knowledge from all sources"""
        
        knowledge = {
            'complete_analysis_patterns': self._extract_patterns(complete_result),
            'learning_enhanced_patterns': self._extract_patterns(learning_result),
            'specialized_patterns': self._extract_patterns(specialized_result),
            'context_insights': context.get('relevant_patterns', []),
            'performance_metrics': {
                'complete_analysis_time': complete_result.get('execution_time', 0),
                'learning_enhancement_time': learning_result.get('execution_time', 0),
                'specialized_execution_time': specialized_result.get('execution_time', 0)
            },
            'knowledge_gaps': self._identify_knowledge_gaps(complete_result, learning_result),
            'learning_opportunities': self._identify_learning_opportunities(specialized_result),
            'integration_timestamp': time.time()
        }
        
        return knowledge
    
    def _extract_patterns(self, result: dict) -> List[str]:
        """Extract patterns from analysis result"""
        patterns = []
        
        if isinstance(result, dict):
            # Look for common pattern keys
            for key in ['patterns', 'detected_patterns', 'learned_patterns', 'issues']:
                if key in result and isinstance(result[key], list):
                    patterns.extend([str(p) for p in result[key]])
            
            # Look for issues that could be patterns
            if 'issues' in result and isinstance(result['issues'], list):
                for issue in result['issues']:
                    if isinstance(issue, dict) and 'description' in issue:
                        patterns.append(f"issue: {issue['description']}")
                    elif isinstance(issue, str):
                        patterns.append(f"issue: {issue}")
        
        return list(set(patterns))  # Remove duplicates
    
    def _identify_knowledge_gaps(self, complete_result: dict, learning_result: dict) -> List[str]:
        """Identify gaps in knowledge that need learning"""
        gaps = []
        
        complete_patterns = set(self._extract_patterns(complete_result))
        learning_patterns = set(self._extract_patterns(learning_result))
        
        # Patterns found in complete analysis but not in learning
        missing_patterns = complete_patterns - learning_patterns
        gaps.extend([f"learning_gap: {pattern}" for pattern in missing_patterns])
        
        return gaps
    
    def _identify_learning_opportunities(self, specialized_result: dict) -> List[str]:
        """Identify opportunities for new learning"""
        opportunities = []
        
        if isinstance(specialized_result, dict):
            # Look for skills with low confidence
            if 'skills' in specialized_result:
                for skill_name, skill_result in specialized_result['skills'].items():
                    if isinstance(skill_result, dict) and skill_result.get('confidence', 0) < 0.8:
                        opportunities.append(f"improve_skill: {skill_name}")
            
            # Look for novel patterns
            if 'novel_patterns' in specialized_result:
                for pattern in specialized_result['novel_patterns']:
                    opportunities.append(f"new_pattern: {pattern}")
        
        return opportunities
    
    def _generate_integrated_report(self, complete_result: dict, learning_result: dict, 
                                   specialized_result: dict, knowledge: dict, execution_time: float) -> dict:
        """Generate comprehensive integrated report"""
        
        return {
            'complete_analysis': {
                'system_info': complete_result.get('system_info', {}),
                'file_analysis': complete_result.get('file_analysis', {}),
                'issues': complete_result.get('issues', []),
                'success': complete_result.get('success', False)
            },
            
            'learning_enhancements': {
                'applied_patterns': learning_result.get('applied_patterns', []),
                'insights': learning_result.get('insights', []),
                'optimizations': learning_result.get('optimizations', []),
                'success': learning_result.get('success', False)
            },
            
            'specialized_analysis': {
                'memory_analysis': specialized_result.get('memory', {}),
                'bgp_analysis': specialized_result.get('bgp', {}),
                'container_analysis': specialized_result.get('containers', {}),
                'interface_analysis': specialized_result.get('interfaces', {}),
                'success': specialized_result.get('success', False)
            },
            
            'performance_metrics': {
                'execution_time_breakdown': knowledge.get('performance_metrics', {}),
                'learning_overhead': learning_result.get('execution_time', 0),
                'efficiency_score': self._calculate_efficiency_score(execution_time, knowledge),
                'learning_effectiveness': self._calculate_learning_effectiveness(knowledge)
            },
            
            'next_steps': {
                'immediate_actions': self._generate_immediate_actions(complete_result, learning_result),
                'learning_improvements': knowledge.get('learning_opportunities', []),
                'system_updates': self._recommend_system_updates(knowledge)
            }
        }
    
    def _calculate_efficiency_score(self, execution_time: float, knowledge: dict) -> float:
        """Calculate efficiency score based on time and knowledge gained"""
        base_score = 100.0
        
        # Time penalty (slower = lower score)
        if execution_time > 300:  # 5 minutes
            time_penalty = (execution_time - 300) / 60  # 1 point per minute over 5
            base_score -= min(time_penalty, 50)  # Max 50 point penalty
        
        # Knowledge bonus (more learning = higher score)
        patterns_learned = len(knowledge.get('learning_enhanced_patterns', []))
        knowledge_bonus = min(patterns_learned * 2, 30)  # Max 30 point bonus
        
        return max(0, base_score + knowledge_bonus)
    
    def _calculate_learning_effectiveness(self, knowledge: dict) -> float:
        """Calculate learning effectiveness score"""
        patterns_learned = len(knowledge.get('learning_enhanced_patterns', []))
        gaps_identified = len(knowledge.get('knowledge_gaps', []))
        opportunities = len(knowledge.get('learning_opportunities', []))
        
        # Effectiveness based on patterns learned vs gaps
        if gaps_identified == 0:
            return 100.0 if patterns_learned > 0 else 0.0
        
        effectiveness = (patterns_learned / (patterns_learned + gaps_identified)) * 100
        return min(effectiveness + (opportunities * 5), 100.0)
    
    def _generate_immediate_actions(self, complete_result: dict, learning_result: dict) -> List[str]:
        """Generate immediate action items"""
        actions = []
        
        # Critical issues from complete analysis
        if isinstance(complete_result.get('issues'), list):
            for issue in complete_result['issues']:
                if isinstance(issue, dict) and issue.get('severity') == 'CRITICAL':
                    actions.append(f"URGENT: {issue.get('description', 'Critical issue detected')}")
                elif isinstance(issue, str) and 'critical' in issue.lower():
                    actions.append(f"URGENT: {issue}")
        
        # High-confidence learning recommendations
        if isinstance(learning_result.get('recommendations'), list):
            for recommendation in learning_result['recommendations']:
                if isinstance(recommendation, dict) and recommendation.get('confidence', 0) > 0.9:
                    actions.append(f"ACTION: {recommendation.get('description', 'Apply learning recommendation')}")
        
        return actions
    
    def _recommend_system_updates(self, knowledge: dict) -> List[str]:
        """Recommend system updates based on learning"""
        updates = []
        
        # Update skills based on learning opportunities
        for opportunity in knowledge.get('learning_opportunities', []):
            if opportunity.startswith('improve_skill:'):
                skill_name = opportunity.replace('improve_skill: ', '')
                updates.append(f"Update skill: {skill_name} with new patterns")
        
        # Add new patterns to knowledge base
        for pattern in knowledge.get('learning_enhanced_patterns', []):
            updates.append(f"Add pattern to knowledge base: {pattern}")
        
        return updates

def main():
    """Main function for command line execution"""
    if len(sys.argv) != 2:
        print("Usage: python integrated_showtech_processor.py <showtech_archive>")
        print("\nExample:")
        print("  python integrated_showtech_processor.py C:\\path\\to\\showtech.tar.gz")
        sys.exit(1)
    
    archive_path = sys.argv[1]
    
    print("🚀 Integrated Showtech Processor")
    print("=" * 50)
    print(f"Processing: {archive_path}")
    print()
    
    # Initialize processor
    processor = IntegratedLearningProcessor()
    
    # Process the archive
    result = processor.process_showtech_integrated(archive_path)
    
    # Display results
    print("\n" + "=" * 50)
    print("📊 INTEGRATED PROCESSING RESULTS")
    print("=" * 50)
    
    if result.get('success'):
        summary = result.get('execution_summary', {})
        metrics = result.get('performance_metrics', {})
        knowledge = result.get('knowledge_capture', {})
        
        print(f"✅ Status: SUCCESS")
        print(f"⏱️  Execution Time: {summary.get('total_execution_time', 0):.2f} seconds")
        print(f"🔄 Phases Completed: {summary.get('phases_completed', 0)}/6")
        print(f"📈 Efficiency Score: {metrics.get('efficiency_score', 0):.1f}")
        print(f"🧠 Learning Effectiveness: {metrics.get('learning_effectiveness', 0):.1f}%")
        print(f"🔍 Patterns Learned: {len(knowledge.get('learning_enhanced_patterns', []))}")
        print(f"⚠️  Critical Issues: {len(result.get('next_steps', {}).get('immediate_actions', []))}")
        
        # Show immediate actions if any
        actions = result.get('next_steps', {}).get('immediate_actions', [])
        if actions:
            print(f"\n🚨 IMMEDIATE ACTIONS REQUIRED:")
            for i, action in enumerate(actions, 1):
                print(f"  {i}. {action}")
        
        # Save detailed results
        output_file = f"integrated_analysis_results_{int(time.time())}.json"
        try:
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"\n💾 Detailed results saved to: {output_file}")
        except Exception as e:
            print(f"\n❌ Failed to save results: {e}")
    
    else:
        print(f"❌ Status: FAILED")
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()