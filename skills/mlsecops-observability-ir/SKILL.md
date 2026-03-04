---
name: mlsecops-observability-ir
description: Build ML and LLM security monitoring and incident response capability. Use when defining telemetry schemas, detection rules, abuse monitoring, and incident playbooks for model or agentic systems.
---

# MLSecOps Observability and Incident Response

## Goal
Create measurable detection and response for ML/LLM abuse and operational failures.

## Use this skill for
- Telemetry schema design and alert rule engineering.
- ML-specific incident playbooks and on-call readiness.
- Detection quality and response process measurement.

## Required Inputs
- Current logging/metrics/tracing stack details
- On-call model and incident escalation policy
- Priority abuse hypotheses and model runbook expectations
- Rollback, throttling, and kill-switch mechanisms

## Step-by-step workflow
1. Standardize telemetry.
   - Build event schema with model version, environment, policy action, and actor metadata.
   - Output: schema draft and event contract.
2. Add prioritized detections.
   - Create rules for prompt abuse, extraction scraping, poisoning, and anomalous model drift.
   - Output: detections with severity and ownership.
3. Design response playbooks.
   - Define triage, containment, recovery, and communication templates.
   - Output: incident playbook per threat class.
4. Run exercises.
   - Validate alert-to-containment path with synthetic abuse scenarios.
   - Output: exercise notes and improvement actions.
5. Close the loop.
   - Map closed incidents to control backlog and regression tests.
   - Output: MTTR, precision/recall trend notes, and prevention backlog.

## What this skill can detect
- Prompt injection/exfiltration attempts and prompt-tool misuse.
- Extraction scraping spikes and unusual query volume.
- Policy bypass at runtime and anomaly indicators before incidents.
- Missing rollback/kill-switch execution during abuse events.

## Outputs
- `incident-playbook.md` (service + scenario template)
- Detection backlog and rule owner matrix
- Incident drill outcomes and quality trend notes

## Quality Gates
- [ ] Events are queryable by model version and environment.
- [ ] Every priority threat hypothesis has at least one detection path.
- [ ] Exercise results include measurable MTTR/precision/recall updates.
- [ ] Closeout actions are tied to remediation tasks.

## Bundled Resources
- References:
  - `references/toolkit.md`: telemetry and incident tooling map.
  - `references/playbook-template.md`: IR template sections.
- Scripts:
  - `scripts/generate_ir_playbook.py`: produce service-specific playbook.

## Tool Usage
Generate an incident playbook:

```bash
python skills/mlsecops-observability-ir/scripts/generate_ir_playbook.py \
  --service-name "inference-api" \
  --incident-type "prompt-injection-bypass" \
  --output incident-playbook.md
```

```bash
otelcol --config observability/otel-collector.yaml
prometheus --config.file=observability/prometheus.yml
```
