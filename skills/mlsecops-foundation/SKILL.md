---
name: mlsecops-foundation
description: Build a threat-model and baseline control plan for ML and LLM systems. Use when starting a new project, re-baselining an existing deployment, or translating MITRE ATLAS and OWASP ML/LLM risks into prioritized controls, owners, and release gates.
---

# MLSecOps Foundation

## Goal
Create the baseline threat architecture for ML systems and define release-blocking security controls before engineering hardening.

## Use this skill for
- New project greenfield security setup.
- Re-baselining an existing ML/LLM service.
- Translating architecture and attack models into concrete controls.

## Required Inputs
- System architecture (training, registry, serving, CI/CD, runtime)
- Data sensitivity assumptions and compliance requirements
- Deployment model and tenant/external exposure
- Top business/security outcomes to protect (integrity, availability, confidentiality)

## Step-by-step workflow
1. Define attack surface and assets.
   - Include: datasets, feature pipelines, training jobs, model registry, prompts/tools, endpoints, IAM, and secrets.
   - Output: asset inventory with confidence on criticality.
2. Draw trust boundaries and transitions.
   - Map how untrusted input can enter each boundary (developer, CI, artifact store, runtime).
   - Output: boundary table with allowed and blocked flows.
3. Run threat classification.
   - Map each boundary to MITRE ATLAS and OWASP ML/LLM threat classes.
   - Output: normalized threat register rows.
4. Score and prioritize risk.
   - Use likelihood, impact, exploit preconditions, and blast radius.
   - Label at least P0/P1/P2 explicitly.
   - Output: priority-order list and owner assignment.
5. Add malicious prompt/skill abuse in the register.
   - Prompt injection, prompt-tool misuse, unsafe artifact loading, and serialized execution chains.
   - Output: explicit control entries for policy/allowlist/containment requirements.
6. Convert top risks into controls and gates.
   - Fill preventive/detective/recovery controls.
   - Add release blocking conditions for unresolved high-risk items.
   - Output: baseline control plan with due dates and owners.
7. Generate artifacts and evidence.
   - Run foundation register generator and OSS availability checks.
   - Output: `threat-register.md` and open-source-check report.

## What problems this skill can detect
- Missing or unclear trust boundaries between training, registry, and serving.
- Threats that bypass architecture approvals (prompt/tool abuse, unsafe imports, remote artifact swaps).
- High-risk exposure with no assigned control owner.
- Compliance gap between required standards and implemented controls.

## Outputs
- `threat-register.md` (scored threat catalog)
- control plan with owners and deadlines
- release gate criteria for P0/P1 risks

## Quality Gates
- [ ] Every critical asset appears in the register.
- [ ] All P0/P1 risks have owners, due dates, and blocking criteria.
- [ ] Malicious prompt/skill abuse scenarios are represented as first-class risks.
- [ ] Release gate criteria are measurable (not descriptive only).
- [ ] Evidence includes tool checks or explicit manual review notes.

## Bundled Resources
- References:
  - `references/toolkit.md`: foundational tool selection and sequencing.
  - `references/threat-register-template.md`: starter threat-register structure.
- Scripts:
  - `scripts/generate_threat_register.py`: scaffold threat register content.
  - `scripts/run_open_source_foundation_checks.py`: verify installed OSS tooling.

## Tool Usage
Generate a threat register from architecture-critical assets:

```bash
python skills/mlsecops-foundation/scripts/generate_threat_register.py \
  --assets "training-data,feature-store,model-registry,inference-api" \
  --vectors "poisoning,prompt injection,model extraction,prompt-tool abuse,data exfiltration" \
  --output threat-register.md
```

Check OSS foundation tooling availability:

```bash
python skills/mlsecops-foundation/scripts/run_open_source_foundation_checks.py \
  --tools threatdragon,pytm,threagile,threatspec \
  --output foundation-open-source-checks.json
```

If you need a quick manual starter workflow:

```bash
tm.py --help
docker run --rm -it threagile/threagile --help
pip install threatspec && threatspec init
```
