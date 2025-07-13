import sys
import os
from pprint import pprint

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auditpilot.core.ai_analyzer import AIComplianceAnalyzer

def run_behavioral_analysis():
    """
    Demonstrates the Behavioral Analytics capabilities of the AuditPilot system.
    It asks the AI to analyze a log file for suspicious activity.
    """
    print("--- Initializing AuditPilot Behavioral Analytics Engine ---")
    
    ai_analyst = AIComplianceAnalyzer()

    # --- The Input: A New, Unseen Log of User Activity ---
    # This log is moderately suspicious: it's after hours, involves sensitive
    # financial data, and makes an external network connection. It's not as
    # obviously bad as the 'critical alert' example we gave the AI.
    log_evidence = (
        "Timestamp: 2024-10-30 18:30:00, User: m.jones, Action: login_success, Source_IP: 192.168.1.15; "
        "Timestamp: 2024-10-30 18:35:12, User: m.jones, Action: file_read, File: /finance/quarterly_earnings.csv; "
        "Timestamp: 2024-10-30 18:36:05, User: m.jones, Action: network_connect, Destination_IP: 13.107.21.200; "
        "Timestamp: 2024-10-30 19:00:00, User: m.jones, Action: logout_success, Source_IP: 192.168.1.15"
    )
    
    print("Analyzing the following user activity log for anomalies:\n")
    print(f'"{log_evidence}"\n')


    # --- The Analysis ---
    # We ask our AI to act as a security analyst and score the log.
    # For this control, a high score means a high level of suspicion.
    print("--- Requesting AI Analysis ---")
    analysis_result = ai_analyst.analyze_control_evidence(
        evidence=log_evidence,
        control_id="BA-1" # Using our new Behavioral Analytics control
    )


    # --- The Result ---
    # Display the AI's judgment on the suspiciousness of the log.
    anomaly_score = analysis_result.get('base_score', 0)
    
    print("\n\n=======================================================")
    print("=== AuditPilot Behavioral Analysis Results ===")
    print("=======================================================\n")
    
    print(f"Anomaly Score: {anomaly_score}/100")
    print("\nAI Justification:")
    print(f"\"{analysis_result.get('justification', 'No justification provided.')}\"")
    
    if anomaly_score > 85:
        print("\nCONCLUSION: CRITICAL ANOMALY DETECTED. IMMEDIATE ACTION REQUIRED.")
    elif anomaly_score > 50:
        print("\nCONCLUSION: Suspicious Activity Detected. Manual review recommended.")
    else:
        print("\nCONCLUSION: Behavior appears normal.")
        
    print("\n=======================================================")


if __name__ == '__main__':
    run_behavioral_analysis() 