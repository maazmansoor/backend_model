# AuditPilot AI Scorecard

An AI-driven compliance and governance platform that implements the ARC-AMPE framework for healthcare AI systems.

## Features

- Comprehensive AI security assessment based on NIST SP 800-53 Rev. 5
- Quantum-resistant security evaluation
- Automated scoring and maturity assessment
- Intelligent recommendations engine
- Detailed compliance reporting

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

To run a sample assessment:

```bash
cd backend
python -m tests.test_assessment
```

You will see output similar to this:

```
=== AuditPilot AI Scorecard Assessment Report ===

Assessment Date: 2023-11-23T15:30:45.123456
Overall Score: 87.5%
Maturity Level: ADVANCED

=== Control Family Scores ===
Access Control (AC): 92.5%
Identification and Authentication (IA): 95.0%
System and Communications Protection (SC): 91.2%

=== Recommendations ===
- Maintain leadership position through innovation
- Contribute to industry best practices and standards
- Prepare for next-generation regulatory requirements
```

## Project Structure

```
backend/
├── auditpilot/
│   ├── __init__.py
│   └── core/
│       └── assessment.py
├── tests/
│   └── test_assessment.py
├── requirements.txt
└── README.md
```

## Assessment Data Format

The system expects assessment data in the following format:

```python
assessment_data = {
    'FAMILY_ID': [
        {
            'control': 'CONTROL_ID',
            'base_score': SCORE_0_TO_100,
            'enhancement': 'none|moderate|significant|transformational'
        },
        # ... more controls
    ],
    # ... more families
}
```

## Scoring System

- Base scores: 0-100 for each control
- Enhancement levels:
  - none: 1.0x multiplier
  - moderate: 1.1x multiplier
  - significant: 1.25x multiplier
  - transformational: 1.5x multiplier

## Maturity Levels

- Basic: 0-40%
- Developing: 41-60%
- Mature: 61-80%
- Advanced: 81-100% 