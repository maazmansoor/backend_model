"""
Test module demonstrating AuditPilot AI Scorecard usage
"""
import json
from auditpilot.core.assessment import AISecurityAssessment

def main():
    # Create an instance of the assessment system
    assessor = AISecurityAssessment()

    # Sample assessment data - this would normally come from actual system evaluation
    sample_data = {
        'AC': [  # Access Control family
            {'control': 'AC-1', 'base_score': 75, 'enhancement': 'significant'},
            {'control': 'AC-2', 'base_score': 85, 'enhancement': 'transformational'},
            {'control': 'AC-3', 'base_score': 80, 'enhancement': 'significant'}
        ],
        'IA': [  # Identification and Authentication family
            {'control': 'IA-1', 'base_score': 90, 'enhancement': 'transformational'},
            {'control': 'IA-2', 'base_score': 95, 'enhancement': 'transformational'}
        ],
        'SC': [  # System and Communications Protection family
            {'control': 'SC-1', 'base_score': 85, 'enhancement': 'transformational'},
            {'control': 'SC-8', 'base_score': 90, 'enhancement': 'transformational'},
            {'control': 'SC-12', 'base_score': 88, 'enhancement': 'transformational'}
        ]
    }

    # Generate assessment report
    report = assessor.generate_assessment_report(sample_data)

    # Print the report in a readable format
    print("\n=== AuditPilot AI Scorecard Assessment Report ===\n")
    print(f"Assessment Date: {report['assessment_date']}")
    print(f"Overall Score: {report['overall_score']}%")
    print(f"Maturity Level: {report['maturity_level'].upper()}\n")
    
    print("=== Control Family Scores ===")
    for family_id, score in report['family_scores'].items():
        family_name = assessor.control_families[family_id]['name']
        print(f"{family_name} ({family_id}): {score}%")
    
    print("\n=== Recommendations ===")
    for rec in report['recommendations']:
        print(f"- {rec}")

if __name__ == "__main__":
    main() 