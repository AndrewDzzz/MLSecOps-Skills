---
name: mlsecops-governance
description: Operationalize MLSecOps governance, auditability, and compliance mapping. Use when defining control ownership, evidence requirements, risk exceptions, and standards alignment for SOC2, ISO27001, NIST, or internal policy programs.
---

# MLSecOps Governance

## Goal
Turn MLSecOps controls into auditable operations with clear ownership, evidence, and exception control.

## Use this skill for
- Control mapping to SOC2 / ISO27001 / NIST AI RMF and internal frameworks.
- Evidence lifecycle standardization for releases and incidents.
- Exception handling with explicit expiry and compensation.

## Required Inputs
- Compliance and policy scope
- Current threat register and control set
- Change-management process and release approval model
- Incident evidence and audit retention requirements

## Step-by-step workflow
1. Map controls to obligations.
   - Translate each required control to evidence-backed owners and cadences.
   - Output: control-to-framework mapping table.
2. Define evidence contracts.
   - Specify evidence artifacts per control and per release decision.
   - Output: evidence register.
3. Implement exception discipline.
   - Add expiry date, compensating controls, and revalidation trigger.
   - Output: exception register with reviewers and end dates.
4. Standardize policy-as-code checks.
   - Run governance checks where possible (OPA/Inspec/OpenSCAP).
   - Output: policy pass/fail records.
5. Link malicious-prompt/artifact controls to release gates.
   - Ensure model release cannot proceed without supply-chain and assurance evidence.
   - Output: gate checklist for unsafe artifact and prompt-tool use.

## What this skill can detect
- Unowned controls and missing review cadence.
- Controls without evidence or non-traceable model-version mapping.
- Stale exceptions or expired risk waivers.
- Governance blind spots for prompt/skill and artifact loading risks.

## Outputs
- `evidence-register.md`
- control-to-framework matrix
- exception policy and review schedule

## Quality Gates
- [ ] Each control has owner, review cadence, and evidence artifact.
- [ ] Evidence is traceable back to model version and test evidence.
- [ ] All exceptions are time-bounded and revalidated.
- [ ] Release gates explicitly require supply-chain + model-assurance evidence.

## Bundled Resources
- References:
  - `references/toolkit.md`: governance frameworks and OSS tooling.
  - `references/evidence-register-template.md`: evidence table format.
- Scripts:
  - `scripts/generate_evidence_register.py`: generate evidence register scaffold.

## Tool Usage
Generate evidence register:

```bash
python skills/mlsecops-governance/scripts/generate_evidence_register.py \
  --frameworks "SOC2,ISO27001,NIST AI RMF" \
  --output evidence-register.md
```

Validate policy and evidence checks:

```bash
opa test policy/ --output text
inspec exec profiles/ --reporter cli json:governance-evidence-inspec.json
```
