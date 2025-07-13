"""
Example usage of the AISecurityAssessment framework based on the client's toolkit.
"""
from auditpilot.core.ai_analyzer import AISecurityAssessment

def main():
    """
    Runs a sample assessment using the data and logic specified
    in the AI Security Assessment Toolkit.
    """
    assessor = AISecurityAssessment()
    
    # New, realistic data for a medium-sized hospital
    hospital_assessment_data = {
        'AC': [ # Access Control
            {'control': 'AC-1', 'base_score': 75, 'enhancement': 'moderate'},
            {'control': 'AC-2', 'base_score': 70, 'enhancement': 'moderate'}
        ],
        'IA': [ # Identification and Authentication
            {'control': 'IA-1', 'base_score': 60, 'enhancement': 'none'},
            {'control': 'IA-5', 'base_score': 65, 'enhancement': 'none'}
        ],
        'SC': [ # System and Communications Protection
            {'control': 'SC-7', 'base_score': 70, 'enhancement': 'moderate'},
            {'control': 'SC-8', 'base_score': 75, 'enhancement': 'moderate'}
        ],
        'RA': [ # Risk Assessment
            {'control': 'RA-3', 'base_score': 40, 'enhancement': 'none'},
            {'control': 'RA-5', 'base_score': 50, 'enhancement': 'none'}
        ],
        'IR': [ # Incident Response
            {'control': 'IR-4', 'base_score': 55, 'enhancement': 'none'},
            {'control': 'IR-6', 'base_score': 60, 'enhancement': 'none'}
        ]
    }
    
    # Example data for a student's report card
    student_report_card_data = {
        'AC': [ # Attendance & Punctuality
            {'control': 'AC-1', 'base_score': 95, 'enhancement': 'significant'}
        ],
        'IA': [ # Identity & Following Rules
            {'control': 'IA-1', 'base_score': 50, 'enhancement': 'moderate'}
        ],
        'RA': [ # Research & Analysis Skills
            {'control': 'RA-3', 'base_score': 20, 'enhancement': 'none'}
        ],
        'IR': [ # Handling Mistakes / Incidents
            {'control': 'IR-4', 'base_score': 55, 'enhancement': 'none'}
        ]
    }
    
    # --- Select which data to run ---
    # report = assessor.generate_assessment_report(hospital_assessment_data)
    report = assessor.generate_assessment_report(student_report_card_data)
    
    # Print the comprehensive report
    print("\n=== AI Security Assessment Report ===\n")
    print(f"Assessment Date: {report['assessment_date']}")
    print(f"Overall Score: {report['overall_score']}%")
    print(f"Maturity Level: {report['maturity_level']}")
    
    print("\n--- Scores by Control Family ---")
    for family_name, score in report['family_scores'].items():
        print(f"- {family_name}: {score}%")
        
    print("\n--- Recommendations ---")
    for recommendation in report['recommendations']:
        print(recommendation)

if __name__ == "__main__":
    main() 