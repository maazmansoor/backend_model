# from flask import Flask, request, jsonify
# from flask_cors import CORS
# # Import both of our powerful classes
# from auditpilot.core.ai_analyzer import AIComplianceAnalyzer, AISecurityAssessment
# import os

# # Initialize the Flask application
# app = Flask(__name__)
# # Enable Cross-Origin Resource Sharing (CORS) to allow frontend communication
# CORS(app, resources={r"/api/*": {"origins": "*"}})

# # Instantiate our engines
# # The 'Thinker' that makes judgments
# ai_thinker = AIComplianceAnalyzer()
# # The 'Calculator' that does the math
# score_calculator = AISecurityAssessment()

# @app.route('/api/analyze_and_score', methods=['POST'])
# def analyze_and_score():
#     """
#     A new, powerful endpoint that takes simple, natural language evidence,
#     gets a base_score from the AI, calculates the final score, and returns everything.
#     """
#     try:
#         data = request.get_json()
#         if not data or 'evidence' not in data or 'control_id' not in data or 'enhancement' not in data:
#             return jsonify({"error": "Invalid input: 'evidence', 'control_id', and 'enhancement' are required."}), 400

#         evidence = data['evidence']
#         control_id = data['control_id']
#         enhancement = data['enhancement']

#         # Step 1: Get the 'base_score' and justification from the AI Thinker
#         analysis_result = ai_thinker.analyze_control_evidence(
#             evidence=evidence,
#             control_id=control_id
#         )
#         base_score = analysis_result.get('base_score', 0)
#         justification = analysis_result.get('justification', 'No justification provided.')

#         # Step 2: Calculate the 'final_score' using the Score Calculator
#         final_score = score_calculator.calculate_control_score(base_score, enhancement)
        
#         # Step 3: Return a comprehensive result to the frontend
#         return jsonify({
#             'justification': justification,
#             'base_score': base_score,
#             'final_score': final_score
#         })

#     except Exception as e:
#         # Handle any errors that occur during the process
#         app.logger.error(f"An error occurred: {e}")
#         return jsonify({"error": "An error occurred during analysis", "details": str(e)}), 500

# @app.route('/api/predictive_modeling', methods=['POST'])
# def predictive_modeling():
#     """
#     Runs a predictive simulation based on a baseline and a remediation plan.
#     """
#     try:
#         data = request.get_json()
#         if not data or 'baseline_scores' not in data or 'remediation_plan' not in data:
#             return jsonify({"error": "Invalid input: 'baseline_scores' and 'remediation_plan' are required."}), 400

#         baseline_scores = data['baseline_scores']
#         remediation_plan = data['remediation_plan']

#         # 1. Calculate the 'before' report
#         before_report = score_calculator.generate_assessment_report(baseline_scores)

#         # 2. Apply the remediation plan to a copy of the scores
#         remediated_scores = baseline_scores.copy()
#         for family, remediations in remediation_plan.items():
#             if family in remediated_scores:
#                 for remediation in remediations:
#                     control_id_to_update = remediation.get('control')
#                     new_score = remediation.get('new_score')
#                     for control in remediated_scores[family]:
#                         if control['control'] == control_id_to_update:
#                             control['base_score'] = new_score
#                             break
        
#         # 3. Calculate the 'after' report
#         after_report = score_calculator.generate_assessment_report(remediated_scores)

#         return jsonify({
#             'before_report': {
#                 'overall_score': before_report['overall_score'],
#                 'maturity_level': before_report['maturity_level']
#             },
#             'after_report': {
#                 'overall_score': after_report['overall_score'],
#                 'maturity_level': after_report['maturity_level']
#             }
#         })

#     except Exception as e:
#         app.logger.error(f"An error occurred in predictive modeling: {e}")
#         return jsonify({"error": "An error occurred during predictive modeling", "details": str(e)}), 500

# @app.route('/api/behavioral_analysis', methods=['POST'])
# def behavioral_analysis():
#     """
#     Analyzes log data for anomalies using the BA-1 control.
#     """
#     try:
#         data = request.get_json()
#         if not data or 'log_evidence' not in data:
#             return jsonify({"error": "Invalid input: 'log_evidence' is required."}), 400

#         log_evidence = data['log_evidence']

#         # Use the AI 'Thinker' to analyze the logs against the specific BA-1 control
#         analysis_result = ai_thinker.analyze_control_evidence(
#             evidence=log_evidence,
#             control_id='BA-1' # Hardcoded to the behavioral analysis control
#         )
        
#         return jsonify(analysis_result)

#     except Exception as e:
#         app.logger.error(f"An error occurred in behavioral analysis: {e}")
#         return jsonify({"error": "An error occurred during behavioral analysis", "details": str(e)}), 500

# if __name__ == '__main__':
#     # It's recommended to use a production-ready WSGI server like Gunicorn or Waitress
#     # instead of Flask's built-in server for deployment.
#     # For Railway, you typically define the start command in a Procfile.
#     # Example Procfile: web: gunicorn app:app
#     app.run(debug=True, port=int(os.environ.get('PORT', 5001))) 







# /////////////////////////


from flask import Flask, request, jsonify
from flask_cors import CORS
# Import both of our powerful classes
from auditpilot.core.ai_analyzer import AIComplianceAnalyzer, AISecurityAssessment
import os

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) to allow frontend communication
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Instantiate our engines
# The 'Thinker' that makes judgments
ai_thinker = AIComplianceAnalyzer()
# The 'Calculator' that does the math
score_calculator = AISecurityAssessment()

@app.route('/api/analyze_and_score', methods=['POST'])
def analyze_and_score():
    """
    A new, powerful endpoint that takes simple, natural language evidence,
    gets a base_score from the AI, calculates the final score, and returns everything.
    """
    try:
        data = request.get_json()
        if not data or 'evidence' not in data or 'control_id' not in data or 'enhancement' not in data:
            return jsonify({"error": "Invalid input: 'evidence', 'control_id', and 'enhancement' are required."}), 400

        evidence = data['evidence']
        control_id = data['control_id']
        enhancement = data['enhancement']

        # Step 1: Get the 'base_score' and justification from the AI Thinker
        analysis_result = ai_thinker.analyze_control_evidence(
            evidence=evidence,
            control_id=control_id
        )
        base_score = analysis_result.get('base_score', 0)
        justification = analysis_result.get('justification', 'No justification provided.')

        # Step 2: Calculate the 'final_score' using the Score Calculator
        final_score = score_calculator.calculate_control_score(base_score, enhancement)
        
        # Step 3: Return a comprehensive result to the frontend
        return jsonify({
            'justification': justification,
            'base_score': base_score,
            'final_score': final_score
        })

    except Exception as e:
        # Handle any errors that occur during the process
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred during analysis", "details": str(e)}), 500

@app.route('/api/predictive_modeling', methods=['POST'])
def predictive_modeling():
    """
    Runs a predictive simulation based on a baseline and a remediation plan.
    """
    try:
        data = request.get_json()
        if not data or 'baseline_scores' not in data or 'remediation_plan' not in data:
            return jsonify({"error": "Invalid input: 'baseline_scores' and 'remediation_plan' are required."}), 400

        baseline_scores = data['baseline_scores']
        remediation_plan = data['remediation_plan']

        # 1. Calculate the 'before' report
        before_report = score_calculator.generate_assessment_report(baseline_scores)

        # 2. Apply the remediation plan to a copy of the scores
        remediated_scores = baseline_scores.copy()
        for family, remediations in remediation_plan.items():
            if family in remediated_scores:
                for remediation in remediations:
                    control_id_to_update = remediation.get('control')
                    new_score = remediation.get('new_score')
                    for control in remediated_scores[family]:
                        if control['control'] == control_id_to_update:
                            control['base_score'] = new_score
                            break
        
        # 3. Calculate the 'after' report
        after_report = score_calculator.generate_assessment_report(remediated_scores)

        return jsonify({
            'before_report': {
                'overall_score': before_report['overall_score'],
                'maturity_level': before_report['maturity_level']
            },
            'after_report': {
                'overall_score': after_report['overall_score'],
                'maturity_level': after_report['maturity_level']
            }
        })

    except Exception as e:
        app.logger.error(f"An error occurred in predictive modeling: {e}")
        return jsonify({"error": "An error occurred during predictive modeling", "details": str(e)}), 500


@app.route('/api/behavioral_analysis', methods=['POST'])
def behavioral_analysis():
    """
    Analyzes log data for anomalies using the BA-1 control.
    """
    try:
        data = request.get_json()
        if not data or 'log_evidence' not in data:
            return jsonify({"error": "Invalid input: 'log_evidence' is required."}), 400

        log_evidence = data['log_evidence']

        # Use the AI 'Thinker' to analyze the logs against the specific BA-1 control
        analysis_result = ai_thinker.analyze_control_evidence(
            evidence=log_evidence,
            control_id='BA-1' # Hardcoded to the behavioral analysis control
        )
        
        return jsonify(analysis_result)

    except Exception as e:
        app.logger.error(f"An error occurred in behavioral analysis: {e}")
        return jsonify({"error": "An error occurred during behavioral analysis", "details": str(e)}), 500


if __name__ == '__main__':
    # It's recommended to use a production-ready WSGI server like Gunicorn or Waitress
    # instead of Flask's built-in server for deployment.
    # For Railway, you typically define the start command in a Procfile.
    # Example Procfile: web: gunicorn app:app
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))