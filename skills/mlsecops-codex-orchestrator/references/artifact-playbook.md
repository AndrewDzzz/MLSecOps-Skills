# MLSecOps Artifact Playbook

Use this reference to standardize what "done" means for each MLSecOps stage.

## Required Artifacts

| Artifact | Stage | Primary Owner | Review Cadence | Generator Script |
|---|---|---|---|---|
| `task.md` | Cross-stage plan | Security Program Lead | Each planning cycle | `scripts/generate_task_plan.py` |
| `threat-register.md` | Foundation | Security Architect | Weekly during rollout | `../mlsecops-foundation/scripts/generate_threat_register.py` |
| `data-control-matrix.md` | Data Protection | Data Platform Lead | Every data source change | `../mlsecops-data-protection/scripts/generate_data_control_matrix.py` |
| `model-assurance-matrix.md` | Model Assurance | ML Security Lead | Per model release | `../mlsecops-model-assurance/scripts/generate_assurance_matrix.py` |
| `supply-chain-checklist.md` | Supply Chain | DevSecOps Engineer | Per CI/CD change | `../mlsecops-supply-chain/scripts/generate_supply_chain_checklist.py` |
| `runtime-defense-baseline.md` | Runtime Defense | Platform Security Engineer | Monthly or before major launch | `../mlsecops-runtime-defense/scripts/generate_runtime_baseline.py` |
| `incident-playbook.md` | Observability and IR | Security Operations Lead | Quarterly tabletop | `../mlsecops-observability-ir/scripts/generate_ir_playbook.py` |
| `evidence-register.md` | Governance | GRC Owner | Monthly evidence sync | `../mlsecops-governance/scripts/generate_evidence_register.py` |

## Minimum Evidence Expectations

- `task.md`: explicit P0/P1/P2 priorities and owner role per stage.
- `threat-register.md`: risk likelihood and impact fields completed.
- `data-control-matrix.md`: provenance, poisoning, and privacy controls declared.
- `model-assurance-matrix.md`: thresholds and pass/fail outcomes filled.
- `supply-chain-checklist.md`: gating items mapped to CI policy.
- `runtime-defense-baseline.md`: auth, isolation, and fail-safe controls assigned.
- `incident-playbook.md`: trigger, containment, and postmortem owners defined.
- `evidence-register.md`: control-to-framework mapping with cadence and ownership.

## Fast Execution

Generate the full pack with one command:

```bash
python skills/mlsecops-codex-orchestrator/scripts/bootstrap_mlsecops_artifacts.py \
  --project-name "my-project" \
  --system-summary "Public ML API with batch retraining" \
  --output-dir mlsecops-artifacts
```

Then score release readiness:

```bash
python skills/mlsecops-codex-orchestrator/scripts/score_release_readiness.py \
  --artifact-dir mlsecops-artifacts \
  --output mlsecops-artifacts/release-readiness.md
```
