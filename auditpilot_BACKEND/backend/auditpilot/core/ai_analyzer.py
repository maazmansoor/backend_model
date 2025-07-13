"""
AI-powered analyzer for AuditPilot Compliance Assessment with enhanced accuracy and effectiveness
"""
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import precision_score, recall_score, f1_score
# import pandas as pd
from typing import Dict, List, Tuple, Any
import datetime
import json
import logging
import google.generativeai as genai
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the Gemini API client
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    logger.info("Gemini API key configured successfully.")
except KeyError:
    logger.error("FATAL: GEMINI_API_KEY environment variable not set.")
    raise

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
        """Determine organizational maturity level with corrected, inclusive ranges."""
        if overall_score > 85:
            return 'Level 4 - Advanced'
        elif overall_score > 70:
            return 'Level 3 - Mature'
        elif overall_score > 50:
            return 'Level 2 - Developing'
        elif overall_score >= 0:
            return 'Level 1 - Basic'
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

class AIComplianceAnalyzer:
    """
    Uses a generative AI model to analyze evidence against compliance controls.
    """

    def __init__(self, model_name="gemini-1.5-flash", controls_file=None):
        """
        Initializes the analyzer with a specific model and controls file.

        Args:
            model_name (str): The name of the Gemini model to use.
            controls_file (str): The path to the JSON file with control questions and examples.
                                 Defaults to the path relative to this file.
        """
        self.model = genai.GenerativeModel(model_name)
        if controls_file is None:
            # Assumes controls.json is in the same directory
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.controls_file = os.path.join(base_dir, 'controls.json')
        else:
            self.controls_file = controls_file
        
        self.controls = self._load_controls()
        logger.info(f"AIComplianceAnalyzer initialized with model: {model_name}")

    def _load_controls(self) -> Dict:
        """Loads control data from the JSON file."""
        try:
            with open(self.controls_file, 'r') as f:
                controls = json.load(f)
                logger.info(f"Successfully loaded {len(controls)} controls from {self.controls_file}")
                return controls
        except FileNotFoundError:
            logger.error(f"FATAL: Controls file not found at {self.controls_file}")
            raise
        except json.JSONDecodeError:
            logger.error(f"FATAL: Could not decode JSON from {self.controls_file}")
            raise

    def _build_prompt(self, control_id: str, evidence: str) -> str:
        """
        Builds a detailed few-shot prompt for the AI model.
        """
        control = self.controls.get(control_id)
        if not control:
            raise ValueError(f"Control ID '{control_id}' not found in controls file.")

        question = control.get("question")
        examples = control.get("examples", [])

        prompt_parts = [
            "You are an expert AI compliance auditor. Your task is to assess a piece of evidence against a specific security control and provide a quantitative 'base_score' from 0 to 100, where 0 is non-existent and 100 is perfect implementation.",
            "You must also provide a concise 'justification' for your score. Your entire response must be a single, valid JSON object with the keys 'base_score' and 'justification'.",
            f"\nHere is the control you are assessing (ID: {control_id}):",
            f"'{question}'",
            "\nHere are some examples of how to score evidence for this control:",
            "---"
        ]

        for i, example in enumerate(examples):
            example_evidence = example.get('evidence')
            example_output = json.dumps({
                "base_score": example.get('base_score'),
                "justification": example.get('justification')
            })
            prompt_parts.append(f"EXAMPLE {i+1}:")
            prompt_parts.append(f"Evidence: \"{example_evidence}\"")
            prompt_parts.append(f"Correct Response:\n{example_output}")
            prompt_parts.append("---")
        
        prompt_parts.extend([
            "\nNow, please assess the following new evidence based on the control and examples provided.",
            "NEW EVIDENCE:",
            f"\"{evidence}\"",
            "\nProvide your assessment ONLY as a single, valid JSON object. Do not include any other text or formatting outside of the JSON object."
        ])

        return "\n".join(prompt_parts)

    def analyze_control_evidence(self, evidence: str, control_id: str) -> Dict[str, Any]:
        """
        Analyzes a single piece of evidence for a given control ID.

        Args:
            evidence (str): The evidence to be analyzed.
            control_id (str): The ID of the control to assess against (e.g., 'AC-1').

        Returns:
            A dictionary containing the AI's assessment (base_score, justification).
        """
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError("Evidence must be a non-empty string.")
        
        logger.info(f"Analyzing evidence for control: {control_id}")

        try:
            prompt = self._build_prompt(control_id, evidence)
            logger.info("Sending prompt to Gemini API...")
            
            response = self.model.generate_content(prompt)
            
            # Clean up the response to extract only the JSON part
            raw_response_text = response.text
            logger.info(f"Raw response from API: {raw_response_text}")
            
            json_text = raw_response_text.strip().replace("```json", "").replace("```", "").strip()
            
            # Parse the JSON string from the response
            analysis_result = json.loads(json_text)
            logger.info(f"Successfully parsed AI analysis: {analysis_result}")
            
            # Basic validation of the returned data
            if 'base_score' not in analysis_result or 'justification' not in analysis_result:
                raise ValueError("AI response JSON is missing required keys.")

            return analysis_result

        except Exception as e:
            logger.error(f"An error occurred during AI analysis for control {control_id}: {e}")
            # Return a default error structure
            return {
                "base_score": 0,
                "justification": f"Error during analysis: {e}"
            }