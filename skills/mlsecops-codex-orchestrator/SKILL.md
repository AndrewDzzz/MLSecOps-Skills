---
name: mlsecops-codex-orchestrator
description: Orchestrate end-to-end MLSecOps execution across the mlsecops-* skills and produce implementation-ready plans. Use when a user asks for a complete security roadmap, stage prioritization, or a generated task.md from project context, risk profile, and compliance requirements.
---

# MLSecOps Codex Orchestrator

## Goal
Convert security requirements into an ordered execution plan with dependencies, owners, and measurable gates.

## Use this skill for
- Full lifecycle MLSecOps roadmap creation.
- Stage prioritization for a new or risky system.
- Bootstrap and score security artifacts for release readiness.

## Required Inputs
- Project name and concise system summary
- Risk profile (`low|medium|high|critical`)
- Deployment architecture and integration exposure
- Compliance targets and evidence expectations

## Step-by-step workflow
1. Classify project context.
   - Confirm system type, data sensitivity, and external exposure.
   - Output: risk baseline and execution assumptions.
2. Build stage sequence.
   - Start from `mlsecops-foundation` and apply platform-specific sequencing.
   - Route serialized artifact checks through `mlsecops-supply-chain` before runtime/assurance.
3. Generate the task plan.
   - Produce `task.md` with clear ownership, priorities, and exit criteria.
4. Bootstrap artifacts.
   - Generate all stage outputs for the project in one run.
   - Output: complete artifact pack in `--output-dir`.
5. Score and surface gaps.
   - Run readiness score and capture missing controls.
   - Output: `release-readiness.md`.
6. Gate release decisions.
   - Block if P0 gaps remain in critical stages.
   - Confirm malicious prompt/serialization controls are in the evidence chain.

## What this skill can detect
- Missing skills in an execution plan or incorrect sequencing.
- Lack of ownership and evidence links across stages.
- Incomplete release-readiness posture across lifecycle artifacts.
- Security regressions between plan generation and artifact generation runs.

## Outputs
- `task.md` (ordered staged roadmap)
- `threat-register.md`
- `data-control-matrix.md`
- `model-assurance-matrix.md`
- `supply-chain-checklist.md`
- `runtime-defense-baseline.md`
- `incident-playbook.md`
- `evidence-register.md`
- `release-readiness.md`
- bootstrap summary (`bootstrap-summary.md/json`)

## Quality Gates
- [ ] Stage order matches risk profile and architecture.
- [ ] Every P0 item is owned, due-dated, and evidence-linked.
- [ ] All required artifacts exist and pass readiness scoring thresholds.
- [ ] Malicious prompt, jailbreak, and serialization controls are explicit blockers.
- [ ] `bootstrap-summary` documents failures and exceptions.

## Tooling
- References:
  - `references/stage-selection.md`: lifecycle-to-stage mapping.
  - `references/control-mapping-v2.md`: threat-control-deliverable mapping.
  - `references/artifact-playbook.md`: owner/evidence expectations.
  - `references/tooling-map.md`: skill/tool combinations by stage.
  - `references/mcp-integration.md`: MCP probe process.
- Scripts:
  - `scripts/generate_task_plan.py`: create `task.md`.
  - `scripts/bootstrap_mlsecops_artifacts.py`: generate all required artifacts.
  - `scripts/score_release_readiness.py`: compute readiness score.
  - `scripts/mcp_tool_probe.py`: validate MCP connectivity for tool workflows.

## Command Path
Generate one-page task plan:

```bash
python skills/mlsecops-codex-orchestrator/scripts/generate_task_plan.py \
  --project-name "fraud-detector" \
  --system-summary "Real-time transaction fraud scoring API" \
  --risk-profile high \
  --compliance "SOC2,ISO27001" \
  --output task.md
```

Bootstrap all artifacts:

```bash
python skills/mlsecops-codex-orchestrator/scripts/bootstrap_mlsecops_artifacts.py \
  --project-name "fraud-detector" \
  --system-summary "Real-time transaction fraud scoring API" \
  --risk-profile high \
  --output-dir mlsecops-artifacts
```

Score readiness:

```bash
python skills/mlsecops-codex-orchestrator/scripts/score_release_readiness.py \
  --artifact-dir mlsecops-artifacts \
  --output mlsecops-artifacts/release-readiness.md
```

Run MCP probe for control tooling integration:

```bash
python skills/mlsecops-codex-orchestrator/scripts/mcp_tool_probe.py \
  --transport stdio \
  --command docker \
  --arg run \
  --arg -i \
  --arg --rm \
  --arg -e \
  --arg GITHUB_PERSONAL_ACCESS_TOKEN \
  --arg ghcr.io/github/github-mcp-server \
  --env "GITHUB_PERSONAL_ACCESS_TOKEN=${GITHUB_PERSONAL_ACCESS_TOKEN}" \
  --output mcp-probe.json
```
