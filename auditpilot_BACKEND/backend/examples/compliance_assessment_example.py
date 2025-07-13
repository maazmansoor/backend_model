"""
Example usage of AuditPilot AI Compliance Assessment
"""
import sys
import os

# Add the parent directory (backend) to the Python path to resolve the import error
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auditpilot.core.ai_analyzer import AIComplianceAnalyzer, AISecurityAssessment
from pprint import pprint

def run_example_assessment():
    """
    An example to test the full AuditPilot system, from AI analysis to final scoring.
    """
    # Initialize both components of our system
    # The AI 'Thinker' that makes judgments
    ai_thinker = AIComplianceAnalyzer()
    # The 'Calculator' that does the math
    score_calculator = AISecurityAssessment()

    # --- Test Case 1: A NEW, "in-between" piece of evidence for control AC-6 ---
    control_id_1 = "AC-6"
    # evidence_1 = "All our AI agents use the 'standard-agent' role. This role has read/write access to the main patient database and read-only access to the billing system. We lock it down more if we see a problem."
    evidence_1 = "Our Identity and Access Management (IAM) policy, 'POL-IAM-002', reviewed on 2025-05-20, explicitly defines roles for all human and non-human users, including AI agents. Production agents operate under the 'prod-agent-readonly' role, which grants read-only access to specific, anonymized patient data partitions required for their analysis function. Any request for elevated privileges, such as write access or access to raw PII, requires a JIRA service ticket using the 'Privilege-Escalation-Request' workflow. This workflow requires two-factor approval from both the Data Governance Lead and the CISO and is logged in our immutable SIEM for audit purposes."
    enhancement_level_1 = "moderate" # A sample enhancement level for this control

    print(f"--- Running Full Test for Control: {control_id_1} ---")
    print(f"Analyzing Evidence: \"{evidence_1}\"\n")

    # Step 1: Get the 'base_score' from the AI Thinker
    analysis_result_1 = ai_thinker.analyze_control_evidence(
        evidence=evidence_1,
        control_id=control_id_1
    )
    base_score_1 = analysis_result_1.get('base_score', 0)

    print("--- AI Analysis Result (The 'Thinker') ---")
    pprint(analysis_result_1)
    
    # Step 2: Calculate the 'final_score' using the Score Calculator
    final_score_1 = score_calculator.calculate_control_score(base_score_1, enhancement_level_1)
    
    print("\n--- Final Score Calculation (The 'Calculator') ---")
    print(f"Base Score from AI: {base_score_1}")
    print(f"Enhancement Level: '{enhancement_level_1}' (Multiplier: {score_calculator.enhancement_multipliers[enhancement_level_1]})")
    print(f"==> Final Calculated Score: {final_score_1:.2f}\n")
    print("--------------------------------------------\n")


    # --- Test Case 2: A "good" piece of evidence for control IA-2 ---
    control_id_2 = "IA-2"
    evidence_2 = "Attached is the configuration for our service mesh, which shows that all agent-to-agent communication is authenticated using mTLS with X.509 certificates. The certificate authority is configured to use the CRYSTALS-Dilithium signature scheme."
    enhancement_level_2 = "significant" # A different sample enhancement level

    print(f"--- Running Full Test for Control: {control_id_2} ---")
    print(f"Analyzing Evidence: \"{evidence_2}\"\n")
    
    # Step 1: Get the 'base_score' from the AI Thinker
    analysis_result_2 = ai_thinker.analyze_control_evidence(
        evidence=evidence_2,
        control_id=control_id_2
    )
    base_score_2 = analysis_result_2.get('base_score', 0)

    print("--- AI Analysis Result (The 'Thinker') ---")
    pprint(analysis_result_2)
    
    # Step 2: Calculate the 'final_score' using the Score Calculator
    final_score_2 = score_calculator.calculate_control_score(base_score_2, enhancement_level_2)

    print("\n--- Final Score Calculation (The 'Calculator') ---")
    print(f"Base Score from AI: {base_score_2}")
    print(f"Enhancement Level: '{enhancement_level_2}' (Multiplier: {score_calculator.enhancement_multipliers[enhancement_level_2]})")
    print(f"==> Final Calculated Score: {final_score_2:.2f}\n")
    print("--------------------------------------------\n")


if __name__ == '__main__':
    run_example_assessment()