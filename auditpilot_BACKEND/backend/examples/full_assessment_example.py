import sys
import os
from pprint import pprint

# Add the parent directory (backend) to the Python path to resolve the import error
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auditpilot.core.ai_analyzer import AIComplianceAnalyzer, AISecurityAssessment

def run_full_assessment():
    """
    Runs a full, multi-control assessment and generates a final report,
    simulating a complete AuditPilot AI Scorecard generation.
    """
    print("--- Initializing AuditPilot Full Assessment ---")
    # Initialize both the 'Thinker' and the 'Calculator'
    ai_thinker = AIComplianceAnalyzer()
    score_calculator = AISecurityAssessment()

    # 1. Define the full "assessment package" to be tested.
    # This contains evidence for multiple controls across different families.
    assessment_package = {

        
        # "AC-6": {
        #     "evidence": "All our AI agents use the 'standard-agent' role. This role has read/write access to the main patient database and read-only access to the billing system.",
        #     "enhancement": "moderate"
        # },


           "AC-6": {
            "evidence": "Our Identity and Access Management (IAM) policy, 'POL-IAM-002', reviewed on 2025-05-20, explicitly defines roles for all human and non-human users, including AI agents. Production agents operate under the 'prod-agent-readonly' role, which grants read-only access to specific, anonymized patient data partitions required for their analysis function. Any request for elevated privileges, such as write access or access to raw PII, requires a JIRA service ticket using the 'Privilege-Escalation-Request' workflow. This workflow requires two-factor approval from both the Data Governance Lead and the CISO and is logged in our immutable SIEM for audit purposes.",
            "enhancement": "moderate"
        },


        "IA-2": {
            "evidence": "Attached is the configuration for our service mesh, which shows that all agent-to-agent communication is authenticated using mTLS with X.509 certificates. The CA is configured to use CRYSTALS-Dilithium.",
            "enhancement": "significant"
        },
        "SI-7": {
            "evidence": "We do a sha256sum check on the application binary after we build it and compare it to the one we deploy manually.",
            "enhancement": "none"
        },
        "AU-2": {
            "evidence": "The system logs when an agent starts and stops, and logs any critical errors to a local file. It does not log what data was accessed.",
            "enhancement": "none"
        }
    }
    print(f"Loaded assessment package with {len(assessment_package)} controls to test.\n")

    # 2. Loop through the package and get the AI's analysis for each control.
    # This is the "Thinker" phase.
    analyzed_data = {}
    print("--- Starting AI Analysis of All Evidence ---")
    for control_id, data in assessment_package.items():
        print(f"Analyzing control: {control_id}...")
        
        # Get the AI's judgment (the base_score)
        analysis_result = ai_thinker.analyze_control_evidence(
            evidence=data["evidence"],
            control_id=control_id
        )
        
        # Get the family ID from the control ID (e.g., 'AC-6' -> 'AC')
        family_id = control_id.split('-')[0]
        
        # Store the results, grouped by family, in the format the calculator expects
        if family_id not in analyzed_data:
            analyzed_data[family_id] = []
        
        analyzed_data[family_id].append({
            'control_id': control_id,
            'base_score': analysis_result.get('base_score', 0),
            'enhancement': data["enhancement"],
            'justification': analysis_result.get('justification', 'No justification provided.')
        })
    print("--- AI Analysis Complete ---\n")

    # 3. Generate the final, comprehensive report.
    # This is the "Calculator" phase.
    print("--- Generating Final Assessment Report ---")
    final_report = score_calculator.generate_assessment_report(analyzed_data)

    # 4. Display the final report for the user.
    print("\n\n\n=== AuditPilot AI Scorecard: Final Report ===")
    pprint(final_report)
    print("============================================")

if __name__ == '__main__':
    run_full_assessment()
