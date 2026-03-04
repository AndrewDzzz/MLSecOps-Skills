---
name: mlsecops-data-protection
description: Secure the ML data lifecycle against leakage, poisoning, and privacy failures. Use when designing ingestion and training controls, handling regulated data, or remediating data integrity and confidentiality risks in ML pipelines.
---

# MLSecOps Data Protection

## Goal
Protect data confidentiality, integrity, and provenance before and during model development.

## Use this skill for
- Intake and preprocessing hardening.
- Controlled processing of regulated datasets.
- Poisoning and data integrity control design.

## Required Inputs
- Data source inventory with owners and owners' risk assumptions
- Field-level sensitivity classification (PII/PHI/credentials/etc.)
- Expected schema, quality rules, and drift expectations
- Retention/deletion constraints and legal obligations

## Step-by-step workflow
1. Build a source baseline.
   - Confirm each source has ownership, retention, and legal basis.
   - Output: approved source list and data handling labels.
2. Add integrity and provenance controls.
   - Require immutable snapshots, checksums, and lineage tags before training.
   - Output: source control policy and checkpoint naming convention.
3. Enforce pre-ingest quality gates.
   - Run schema/range/drift checks and reject failing loads.
   - Output: ingestion policy with blocked/review/retry rules.
4. Add poisoning and label-integrity checks.
   - Add anomaly detection, outlier review, and high-impact change approvals.
   - Output: quarantine queue and approval workflow.
5. Apply privacy minimization.
   - Decide pseudonymization, masking, redaction, and differential privacy where required.
   - Output: privacy control matrix (column-by-column).
6. Add prompt-risk filtering at data intake when free text is stored/used for training.
   - Detect and isolate prompt-like payloads and tool-call patterns.
   - Output: filtered or isolated dataset partitions.
7. Generate data control artifacts.
   - Capture matrix and evidence in versioned markdown.
   - Output: `data-control-matrix.md` and control review notes.

## What problems this skill can detect
- Missing or weak dataset provenance controls.
- Sensitive-column leakage and unauthorized enrichment.
- Poisoning signals: label flip, outlier concentration, duplicate anomalies.
- Privacy violations from unmasked training artifacts.
- Prompt-like attacks embedded in training text sources.

## Outputs
- `data-control-matrix.md` (source-by-source safeguards)
- Ingestion validation policy
- Poisoning response process and quarantine plan

## Quality Gates
- [ ] All sources have immutable provenance and checksum checks.
- [ ] PII/sensitive data handling is explicit in policy and logs.
- [ ] Pre-training checks run automatically on every ingestion.
- [ ] Privacy controls are documented and justified for regulated data.
- [ ] Suspicious prompt-like records are isolated before training.

## Open-Source Stack
- Great Expectations, TFDV, Deepchecks, WhyLogs, Evidently, Pandera
- Presidio Analyzer, OpenDP, Opacus, TensorFlow Privacy, ML Privacy Meter
- ARX for structured anonymization workflows

## Bundled Resources
- References:
  - `references/toolkit.md`: OSS stack and sequence.
  - `references/control-matrix-template.md`: starter control matrix.
- Scripts:
  - `scripts/generate_data_control_matrix.py`: scaffold matrix by data source.
  - `scripts/run_open_source_data_checks.py`: smoke-check OSS tooling availability.

## Tool Usage
Generate a source-level matrix:

```bash
python skills/mlsecops-data-protection/scripts/generate_data_control_matrix.py \
  --sources "transactions:high,events:medium,documents:low" \
  --output data-control-matrix.md
```

Validate readiness of OSS controls:

```bash
python skills/mlsecops-data-protection/scripts/run_open_source_data_checks.py \
  --tools great_expectations,deepchecks,presidio_analyzer,opacus,tensorflow_privacy \
  --output data-protection-open-source-checks.json
```
