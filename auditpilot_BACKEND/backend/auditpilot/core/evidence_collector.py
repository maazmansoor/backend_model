"""
Evidence collector for AuditPilot Compliance Assessment
"""
from typing import Dict, Any, List
import json
import datetime

class EvidenceCollector:
    def __init__(self):
        self.evidence_types = {
            'documentation': self._collect_documentation_evidence,
            'implementation': self._collect_implementation_evidence,
            'risk_assessment': self._collect_risk_evidence,
            'automation': self._collect_automation_evidence,
            'monitoring': self._collect_monitoring_evidence,
            'incidents': self._collect_incident_evidence,
            'updates': self._collect_update_evidence
        }

    def collect_control_evidence(self, control_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect and structure evidence for a specific control
        """
        evidence = {}
        
        # Collect evidence for each type
        for evidence_type, collector_func in self.evidence_types.items():
            if evidence_type in inputs:
                evidence[evidence_type] = collector_func(inputs[evidence_type])
            else:
                evidence[evidence_type] = self._get_empty_evidence(evidence_type)

        # Add metadata
        evidence['metadata'] = {
            'control_id': control_id,
            'collection_date': datetime.datetime.now().isoformat(),
            'collector_version': '1.0.0'
        }

        return evidence

    def _collect_documentation_evidence(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Collect and validate documentation evidence"""
        evidence = {}
        
        # Check policies
        evidence['policies'] = {
            'exists': inputs.get('has_policies', False),
            'quality': self._assess_document_quality(inputs.get('policy_details', {})),
            'last_updated': inputs.get('policy_last_updated', None)
        }
        
        # Check procedures
        evidence['procedures'] = {
            'exists': inputs.get('has_procedures', False),
            'quality': self._assess_document_quality(inputs.get('procedure_details', {})),
            'last_updated': inputs.get('procedure_last_updated', None)
        }
        
        # Check guidelines
        evidence['guidelines'] = {
            'exists': inputs.get('has_guidelines', False),
            'quality': self._assess_document_quality(inputs.get('guideline_details', {})),
            'last_updated': inputs.get('guideline_last_updated', None)
        }
        
        # Check training materials
        evidence['training_materials'] = {
            'exists': inputs.get('has_training', False),
            'quality': self._assess_document_quality(inputs.get('training_details', {})),
            'last_updated': inputs.get('training_last_updated', None)
        }
        
        # Check audit logs
        evidence['audit_logs'] = {
            'exists': inputs.get('has_audit_logs', False),
            'quality': self._assess_document_quality(inputs.get('audit_log_details', {})),
            'last_updated': inputs.get('audit_log_last_updated', None)
        }
        
        return evidence

    def _collect_implementation_evidence(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Collect and validate implementation evidence"""
        evidence = {
            'technical_controls': self._assess_technical_controls(inputs.get('technical', {})),
            'administrative_controls': self._assess_administrative_controls(inputs.get('administrative', {})),
            'physical_controls': self._assess_physical_controls(inputs.get('physical', {})),
            'documented_processes': inputs.get('documented_processes', 0),
            'regular_testing': inputs.get('regular_testing', 0),
            'continuous_monitoring': inputs.get('continuous_monitoring', 0),
            'improvement_process': inputs.get('improvement_process', 0),
            'automation_level': inputs.get('automation_level', 0)
        }
        return evidence

    def _collect_risk_evidence(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Collect and validate risk assessment evidence"""
        return {
            'threat_level': inputs.get('threat_level', 0.5),
            'vulnerability_score': inputs.get('vulnerability_score', 0.5),
            'impact_rating': inputs.get('impact_rating', 0.5),
            'last_assessment': inputs.get('last_assessment', None),
            'assessor': inputs.get('assessor', 'unknown')
        }

    def _collect_automation_evidence(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Collect and validate automation evidence"""
        return {
            'monitoring': {'level': inputs.get('monitoring_automation', 0)},
            'response': {'level': inputs.get('response_automation', 0)},
            'reporting': {'level': inputs.get('reporting_automation', 0)},
            'updates': {'level': inputs.get('update_automation', 0)},
            'validation': {'level': inputs.get('validation_automation', 0)}
        }

    def _collect_monitoring_evidence(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Collect and validate monitoring evidence"""
        return {
            'coverage': inputs.get('monitoring_coverage', 0),
            'alerting': inputs.get('alerting_effectiveness', 0),
            'response_time': inputs.get('response_time_score', 0)
        }

    def _collect_incident_evidence(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Collect and validate incident history evidence"""
        return {
            'history': inputs.get('incidents', []),
            'total_count': len(inputs.get('incidents', [])),
            'severity_distribution': self._calculate_severity_distribution(inputs.get('incidents', []))
        }

    def _collect_update_evidence(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Collect and validate update process evidence"""
        return {
            'frequency': inputs.get('update_frequency', 0),
            'coverage': inputs.get('update_coverage', 0),
            'validation': inputs.get('update_validation', 0)
        }

    def _assess_document_quality(self, details: Dict[str, Any]) -> float:
        """Assess document quality on a 0-1 scale"""
        if not details:
            return 0
            
        quality_factors = {
            'completeness': 0.4,
            'accuracy': 0.3,
            'currency': 0.3
        }
        
        quality_score = 0
        for factor, weight in quality_factors.items():
            quality_score += weight * details.get(factor, 0)
            
        return min(max(quality_score, 0), 1)

    def _assess_technical_controls(self, details: Dict[str, Any]) -> Dict[str, Any]:
        """Assess technical control implementation"""
        return {
            'effectiveness': details.get('effectiveness', 0),
            'validation_evidence': details.get('validation', False),
            'testing_results': details.get('testing', False)
        }

    def _assess_administrative_controls(self, details: Dict[str, Any]) -> Dict[str, Any]:
        """Assess administrative control implementation"""
        return {
            'effectiveness': details.get('effectiveness', 0),
            'validation_evidence': details.get('validation', False),
            'testing_results': details.get('testing', False)
        }

    def _assess_physical_controls(self, details: Dict[str, Any]) -> Dict[str, Any]:
        """Assess physical control implementation"""
        return {
            'effectiveness': details.get('effectiveness', 0),
            'validation_evidence': details.get('validation', False),
            'testing_results': details.get('testing', False)
        }

    def _calculate_severity_distribution(self, incidents: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate distribution of incident severities"""
        distribution = {'high': 0, 'medium': 0, 'low': 0}
        for incident in incidents:
            severity = incident.get('severity', 'low').lower()
            if severity in distribution:
                distribution[severity] += 1
        return distribution

    def _get_empty_evidence(self, evidence_type: str) -> Dict[str, Any]:
        """Get empty evidence structure for a given type"""
        empty_evidence = {
            'documentation': {'policies': {'exists': False, 'quality': 0}},
            'implementation': {'technical_controls': {'effectiveness': 0}},
            'risk_assessment': {'threat_level': 0.5, 'vulnerability_score': 0.5},
            'automation': {'monitoring': {'level': 0}},
            'monitoring': {'coverage': 0, 'alerting': 0},
            'incidents': {'history': [], 'total_count': 0},
            'updates': {'frequency': 0, 'coverage': 0}
        }
        return empty_evidence.get(evidence_type, {}) 