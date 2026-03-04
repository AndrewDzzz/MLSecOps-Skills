# Stage Selection Guide

Use this file when ordering or trimming stages for a specific project.

## Default Skill Order
1. `mlsecops-foundation`
2. `mlsecops-data-protection`
3. `mlsecops-model-assurance`
4. `mlsecops-supply-chain`
5. `mlsecops-runtime-defense`
6. `mlsecops-observability-ir`
7. `mlsecops-governance`

## AI Lifecycle Mapping
This pack is aligned to a 10-stage AI development lifecycle:
1. Business understanding
2. Data collection and preprocessing
3. Model design and development
4. Model training and evaluation
5. Model deployment
6. Model monitoring and maintenance
7. Governance and compliance
8. Collaboration and communication
9. Infrastructure and tooling
10. Incident response and continuous improvement

Map lifecycle to skills:
- Stages 1 and 7: `mlsecops-foundation`, `mlsecops-governance`
- Stages 2 and 4: `mlsecops-data-protection`, `mlsecops-model-assurance`
- Stages 3 and 5: `mlsecops-model-assurance`, `mlsecops-runtime-defense`
- Stage 6 and 10: `mlsecops-observability-ir`
- Stage 8 and 9: `mlsecops-supply-chain`, `mlsecops-governance`

## Fast-path Variants
- LLM app with public API: prioritize `runtime-defense` and `model-assurance` early.
- Internal batch ML: prioritize `data-protection` and `supply-chain`.
- Audit-driven sprint: run `governance` in parallel with the first two stages.

## Priority Rules
- `P0`: direct exploit paths, release blockers, active incidents.
- `P1`: hardening items reducing near-term risk.
- `P2`: maturity improvements.
