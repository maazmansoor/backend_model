"""
Core assessment module for AuditPilot AI Scorecard
"""
from typing import Dict, List, Tuple, Optional
import datetime
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AISecurityAssessment:
    """
    AI Security Assessment Automation Framework
    Supports ARC-AMPE compliance evaluation with NIST SP 800-53 Rev. 5,
    as specified in the client's toolkit.
    """
    def __init__(self):
        self.control_families = {
            'AC': {'weight': 0.08, 'name': 'Access Control'},
            'AU': {'weight': 0.07, 'name': 'Audit and Accountability'},
            'AT': {'weight': 0.03, 'name': 'Awareness and Training'},
            'CA': {'weight': 0.06, 'name': 'Assessment, Authorization, and Monitoring'},
            'CM': {'weight': 0.05, 'name': 'Configuration Management'},
            'CP': {'weight': 0.04, 'name': 'Contingency Planning'},
            'IA': {'weight': 0.08, 'name': 'Identification and Authentication'},
            'IR': {'weight': 0.06, 'name': 'Incident Response'},
            'MA': {'weight': 0.03, 'name': 'Maintenance'},
            'MP': {'weight': 0.04, 'name': 'Media Protection'},
            'PE': {'weight': 0.03, 'name': 'Physical and Environmental Protection'},
            'PL': {'weight': 0.04, 'name': 'Planning'},
            'PS': {'weight': 0.04, 'name': 'Personnel Security'},
            'RA': {'weight': 0.06, 'name': 'Risk Assessment'},
            'SA': {'weight': 0.04, 'name': 'System and Services Acquisition'},
            'SC': {'weight': 0.09, 'name': 'System and Communications Protection'},
            'SI': {'weight': 0.07, 'name': 'System and Information Integrity'}
        }
        self.enhancement_multipliers = {
            'none': 1.0,
            'moderate': 1.1,
            'significant': 1.25,
            'transformational': 1.5
        }
        self.maturity_levels = {
            'Level 1 - Basic': (0, 50),
            'Level 2 - Developing': (51, 70),
            'Level 3 - Mature': (71, 85),
            'Level 4 - Advanced': (86, 100)
        }

    def calculate_control_score(self, base_score: int, enhancement_level: str) -> float:
        """Calculate enhanced control score with AI agent multiplier"""
        multiplier = self.enhancement_multipliers.get(enhancement_level, 1.0)
        return min(base_score * multiplier, 100) # Cap at 100

    def calculate_family_score(self, control_scores: List[Tuple[int, str]]) -> float:
        """Calculate weighted family score"""
        if not control_scores:
            return 0.0
        total_score = sum(self.calculate_control_score(base_score, enhancement) for base_score, enhancement in control_scores)
        return total_score / len(control_scores)

    def calculate_overall_score(self, family_scores: Dict[str, float]) -> float:
        """Calculate weighted overall assessment score"""
        total_weighted_score = 0
        total_weight = 0
        for family_id, score in family_scores.items():
            if family_id in self.control_families:
                weight = self.control_families[family_id]['weight']
                total_weighted_score += score * weight
                total_weight += weight
        
        # Normalize by the sum of weights of families present in the data
        return total_weighted_score / total_weight if total_weight > 0 else 0


    def determine_maturity_level(self, overall_score: float) -> str:
        """Determine organizational maturity level"""
        for level, (min_score, max_score) in self.maturity_levels.items():
            if min_score <= overall_score <= max_score:
                return level
        return 'Unknown'

    def generate_assessment_report(self, assessment_data: Dict) -> Dict:
        """Generate comprehensive assessment report"""
        family_scores = {}
        for family_id, controls in assessment_data.items():
            if family_id in self.control_families:
                control_scores = [(c['base_score'], c['enhancement']) for c in controls]
                family_scores[family_id] = self.calculate_family_score(control_scores)
        
        overall_score = self.calculate_overall_score(family_scores)
        maturity_level = self.determine_maturity_level(overall_score)
        
        return {
            'assessment_date': datetime.datetime.now().isoformat(),
            'overall_score': round(overall_score, 2),
            'maturity_level': maturity_level,
            'family_scores': {self.control_families[k]['name']: round(v, 2) for k, v in family_scores.items()},
            'recommendations': self.generate_recommendations(family_scores, overall_score)
        }

    def generate_recommendations(self, family_scores: Dict[str, float], overall_score: float) -> List[str]:
        """Generate improvement recommendations based on maturity and low scores"""
        recommendations = []
        
        # Maturity-based recommendations from the toolkit, now with stricter levels
        if overall_score <= 50:
            recommendations.append("Priority: Foundational. Focus on basic security controls.")
            recommendations.append("-> Deploy Quantum-Resistant Cryptography for core systems.")
            recommendations.append("-> Establish basic Explainable AI (XAI) for critical decisions.")
        elif overall_score <= 70:
            recommendations.append("Priority: Developing. Focus on fixing core weaknesses and optimizing controls.")
            recommendations.append("-> Integrate Homomorphic Encryption for privacy-preserving analytics.")
            recommendations.append("-> Activate the Self-Healing Policy Synthesis Engine.")
        elif overall_score <= 85:
            recommendations.append("Priority: Mature. Focus on continuous improvement and optimization.")
            recommendations.append("-> Enhance automated monitoring and incident response capabilities.")
            recommendations.append("-> Implement advanced threat detection and analysis.")
        else:
            recommendations.append("Priority: Advanced. Maintain leadership through innovation.")
            recommendations.append("-> Contribute to industry best practices and security standards.")
            recommendations.append("-> Prepare for next-generation regulatory requirements.")

        # Identify low-scoring families
        low_scoring_families = sorted(
            [(family_id, score) for family_id, score in family_scores.items() if score < 75],
            key=lambda x: x[1]
        )
        
        if low_scoring_families:
            recommendations.append("\nSpecific Focus Areas (Scores < 75%):")
            for family_id, score in low_scoring_families:
                family_name = self.control_families[family_id]['name']
                recommendations.append(f"- {family_name} ({family_id}): {score:.1f}% - Requires immediate attention.")
                
        return recommendations 