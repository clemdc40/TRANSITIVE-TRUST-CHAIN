# Transitive Trust Chain Abuse (TTCA)

TTCA is a proof-of-concept tool that detects privilege escalation paths
caused by transitive trust relationships in modern Cloud IAM systems.

## Problem

Cloud IAM systems rely heavily on trust relationships (e.g. role assumption).
These relationships are often transitive and may unintentionally allow
an attacker to reach high-privilege principals indirectly.


## Architecture

IAM Raw Data
   ↓
Ingestion
   ↓
Normalization (TTCA Model)
   ↓
Graph Generation
   ↓
TTCA Detection


## Quick Demo

1. Define IAM relationships:
   iam_raw.json

2. Generate TTCA graph:
   python generate_ttca_graph.py

3. Detect transitive abuse:
   python detector.py ttca_graph_from_raw.json


## Example Output

TTCA detected:
user_james → role_dev → role_admin


## Limitations

- No real cloud API integration
- No policy condition analysis
- No scoring or temporal context
- Focused on structural trust abuse only


## Why It Matters

Transitive trust chains are difficult to audit manually and are often
missed by traditional IAM reviews. TTCA provides a formal and automated
approach to identify such risks.
