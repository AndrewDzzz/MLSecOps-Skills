# MLSecOps Control Mapping v2

Use this file to map lifecycle steps, threats, controls, and artifacts in one place.

## Lifecycle to Skill and Deliverable Mapping

| AI Lifecycle Stage | Primary Skill | Key Threats | Required Deliverable |
|---|---|---|---|
| Business understanding | `mlsecops-foundation` | Unscoped risk ownership, missing controls | `threat-register.md` |
| Data collection and preprocessing | `mlsecops-data-protection` | Data leakage, poisoning | `data-control-matrix.md` |
| Model design and development | `mlsecops-model-assurance` | Weak robustness and abuse handling | `model-assurance-matrix.md` |
| Model training and evaluation | `mlsecops-model-assurance` | Overfitting to benign data, adversarial fragility | `model-assurance-matrix.md` |
| Model deployment | `mlsecops-runtime-defense` | Prompt injection, misuse, privilege abuse | `runtime-defense-baseline.md` |
| Model monitoring and maintenance | `mlsecops-observability-ir` | Slow detection, poor triage | `incident-playbook.md` |
| Governance and compliance | `mlsecops-governance` | Missing evidence, weak exception handling | `evidence-register.md` |
| Collaboration and communication | `mlsecops-governance` | Unclear owners and escalation paths | `task.md` |
| Infrastructure and tooling | `mlsecops-supply-chain` | Artifact tampering, dependency compromise | `supply-chain-checklist.md` |
| Incident response and continuous improvement | `mlsecops-observability-ir` | Repeat incidents and untracked corrective actions | `incident-playbook.md` |

## Priority Heuristics

- `P0`: externally reachable abuse paths, active incidents, or unverifiable controls.
- `P1`: high-likelihood weaknesses that can become P0 under scale.
- `P2`: process maturity and optimization.

## Exit Gate for Launch

- All `P0` controls assigned and evidenced.
- Threat register has no unowned high/critical risks.
- Assurance matrix thresholds and outcomes are complete.
- Incident playbook includes tested containment and rollback actions.
