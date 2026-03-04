---
name: mlsecops-model-assurance
description: Validate model robustness and abuse resistance before release. Use for adversarial testing, extraction and privacy leakage assessment, LLM red-teaming, and defining quantitative release gates for ML or LLM systems.
---

# MLSecOps Model Assurance

## Goal
Produce reproducible evidence that a model is safe enough to release against the approved threat model.

## Use this skill for
- Pre-release model validation.
- LLM jailbreak and policy-abuse resistance checks.
- Classical robustness and extraction resistance testing.

## Required Inputs
- Model artifact path and serving interface
- Attack scope by model type (classical / LLM / agentic)
- Evaluation datasets and policy boundary definitions
- Fallback behavior and rate-limiting requirements

## Step-by-step workflow
1. Define the assurance model.
   - Pick attack families by model type and exposure level.
   - Output: test matrix with owners and severity mapping.
2. Run robustness and quality tests.
   - Evaluate OOD and adversarial degradation by family.
   - Output: per-attack metrics and threshold violations.
3. Run abuse and privacy tests.
   - Test prompt injection, jailbreak, extraction, and query scraping.
   - Output: pass/fail by abuse type and confidence.
4. Validate policy controls.
   - Confirm prompt filters, tool-calling boundaries, and fail-safe actions.
   - Output: bypass test report.
5. Inspect serialized artifacts before load.
   - Run pickle opcode inspection for executable-style formats.
   - Output: artifact acceptance/rejection with reasons.
6. Define release gate and remediation backlog.
   - Set mandatory thresholds for P0/P1 findings.
   - Output: release decision record and ticketed fixes.

## What this skill can detect
- Adversarial fragility (accuracy and confidence collapse).
- Prompt injection and policy bypass behavior.
- Model extraction and scraping indicators.
- Membership inference / privacy leakage risks.
- Unsafe model and skill serialization (e.g., pickle `REDUCE`, `GLOBAL` chains).

## Outputs
- `model-assurance-matrix.md` with severity-ranked coverage
- Security test report and evidence bundle
- Remediation plan for failed attack scenarios

## Quality Gates
- [ ] Each selected attack class has measurable thresholds.
- [ ] Failed critical findings are treated as release blockers.
- [ ] Guardrail bypass tests are reproducible and logged.
- [ ] Artifact abuse findings include clear deny/retry policy.

## Bundled Resources
- References:
  - `references/toolkit.md`: attack-tool and robustness selection.
  - `references/assurance-matrix-template.md`: template for test evidence.
- Scripts:
  - `scripts/generate_assurance_matrix.py`: create release-evidence matrix scaffold.

## Tool Usage
Generate assurance matrix with defaults:

```bash
python skills/mlsecops-model-assurance/scripts/generate_assurance_matrix.py \
  --output model-assurance-matrix.md
```

Run representative OSS suites:

```bash
python -m garak.cli --help
promptfoo test
python -m pytest -q test_assurance.py
```
