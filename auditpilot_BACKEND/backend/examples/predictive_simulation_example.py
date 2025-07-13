import sys
import os
from pprint import pprint
import copy

# Add the parent directory (backend) to the Python path to resolve the import error
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auditpilot.core.ai_analyzer import AISecurityAssessment

def run_predictive_simulation():
    """
    Demonstrates the predictive modeling capabilities of the AuditPilot system.
    It establishes a baseline score and then simulates the impact of a
    remediation plan to forecast a future score.
    """
    print("--- Initializing AuditPilot Predictive Simulation ---")
    
    # We only need the 'Calculator' for this simulation, as we assume the AI 'Thinker'
    # has already provided the base scores.
    score_calculator = AISecurityAssessment()

    # --- INPUT 1: The "Current State" ---
    # This is our baseline data from the previous full assessment.
    # It represents the poor initial compliance posture of the organization.
    baseline_data = {
        'AC': [{'control_id': 'AC-6', 'base_score': 20, 'enhancement': 'moderate'}],
        'IA': [{'control_id': 'IA-2', 'base_score': 90, 'enhancement': 'significant'}],
        'SI': [{'control_id': 'SI-7', 'base_score': 15, 'enhancement': 'none'}],
        'AU': [{'control_id': 'AU-2', 'base_score': 30, 'enhancement': 'none'}]
    }
    print("Loaded baseline data representing the 'Current State'.\n")

    # --- INPUT 2: The "Remediation Plan" ---
    # This represents the user's plan to fix their problems. They believe
    # that by investing resources, they can improve the base scores for their
    # weakest controls.
    remediation_plan = {
        'AC-6': {'new_base_score': 85}, # Drastic improvement in Access Control
        'SI-7': {'new_base_score': 70}, # Significant improvement in System Integrity
        'AU-2': {'new_base_score': 75}  # Significant improvement in Auditing
    }
    print("Defined a 'Remediation Plan' to forecast future improvements.\n")

    # --- "BEFORE" CALCULATION ---
    # Calculate the current score based on the baseline data.
    print("--- Calculating 'Before' Scorecard ---")
    before_report = score_calculator.generate_assessment_report(baseline_data)
    

    # --- "AFTER" CALCULATION (The Prediction) ---
    # Now, we apply the remediation plan to our data to predict the future state.
    predicted_data = copy.deepcopy(baseline_data) # Create a deep copy to avoid changing the original
    
    for family_id, controls in predicted_data.items():
        for control in controls:
            control_id = control['control_id']
            if control_id in remediation_plan:
                control['base_score'] = remediation_plan[control_id]['new_base_score']
    
    print("--- Calculating 'After' Scorecard (Prediction) ---")
    after_report = score_calculator.generate_assessment_report(predicted_data)


    # --- THE RESULT ---
    # Display a clear, side-by-side comparison for the user.
    print("\n\n\n=======================================================")
    print("=== AuditPilot Predictive Modeling Results ===")
    print("=======================================================\n")
    
    print("--- CURRENT STATE ---")
    print(f"Overall Score: {before_report['overall_score']:.2f}")
    print(f"Maturity Level: {before_report['maturity_level']}")
    print("\n--- REMEDIATION PLAN ---")
    print("Applied the following improvements:")
    for control, plan in remediation_plan.items():
        print(f"  - {control}: Improved base score to {plan['new_base_score']}")
        
    print("\n--- PREDICTED FUTURE STATE ---")
    print(f"Predicted Overall Score: {after_report['overall_score']:.2f}")
    print(f"Predicted Maturity Level: {after_report['maturity_level']}")
    
    improvement = after_report['overall_score'] - before_report['overall_score']
    print(f"\nPredicted Improvement: +{improvement:.2f} points")
    print("\n=======================================================")


if __name__ == '__main__':
    run_predictive_simulation()
