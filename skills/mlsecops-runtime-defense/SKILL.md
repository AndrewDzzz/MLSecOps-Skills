---
name: mlsecops-runtime-defense
description: Secure live ML and LLM serving systems against runtime abuse. Use when hardening inference APIs, enforcing guardrails and containment, implementing safe-failure behavior, or reducing blast radius in production.
---

# MLSecOps Runtime Defense

## Goal
Reduce abuse, contain compromise, and guarantee safe behavior under attack for live ML services.

## Use this skill for
- Production or staging inference hardening.
- LLM tool-calling and function-execution containment.
- Safe-failure and rollback policy testing.

## Required Inputs
- Service API contract and tenancy/rate model
- Runtime isolation model and network policy
- AuthN/AuthZ and secret management setup
- Guardrail and fallback behavior requirements

## Step-by-step workflow
1. Lock request entry points.
   - Confirm authentication, per-tenant authorization, and schema validation.
   - Output: explicit allow/deny policy and validation spec.
2. Enforce abuse limits and isolation.
   - Add request size, concurrency, and burst controls.
   - Reduce runtime privileges and egress paths.
   - Output: hardened runtime profile and limits.
3. Defend prompt and tool behavior.
   - Apply prompt/tool invocation policies.
   - Block prompt-driven unsafe tool chaining and remote code-like payloads.
   - Output: tool and function allowlist with escalation paths.
4. Define fail-closed behavior.
   - Standardize error handling, retries, and kill switches.
   - Output: safe failure matrix and runbook references.
5. Verify runtime evidence.
   - Exercise bypass tests and record observed blocks.
   - Output: blocked/allowed traces for release review.
6. Produce baseline artifact.
   - Generate runtime baseline with owners and control status.

## What this skill can detect
- Prompt injection and tool-invocation abuse at runtime.
- Unsanitized payload and header/input abuse patterns.
- AuthN/AuthZ bypass attempts and abuse-rate anomalies.
- Secret leakage from runtime containers and unsafe privilege use.

## Outputs
- `runtime-defense-baseline.md`
- API abuse-defense policy and safe-failure runbook section
- Runtime validation evidence (logs, test commands, and expected behavior)

## Quality Gates
- [ ] Request validation and auth controls block unauthorized attempts.
- [ ] Prompt/tool abuse bypass attempts are tested and logged.
- [ ] Fail-closed behavior is deterministic under policy/integrity failures.
- [ ] Rollback and circuit-breaker steps are operational and documented.

## Bundled Resources
- References:
  - `references/toolkit.md`: runtime enforcement and containment tools.
  - `references/runtime-baseline-template.md`: baseline control format.
- Scripts:
  - `scripts/generate_runtime_baseline.py`: generate baseline template.

## Security Testing Commands

```bash
opa eval --data runtime/policies --input request.json "data.ml.security.allow"
modsecurity -t -c modsecurity.conf
```

## Tool Usage
Generate a runtime baseline:

```bash
python skills/mlsecops-runtime-defense/scripts/generate_runtime_baseline.py \
  --service-name "inference-api" \
  --auth-mode oidc \
  --tenancy multi-tenant \
  --output runtime-defense-baseline.md
```

```bash
opa eval --data runtime/policies --input request.json "data.ml.security.allow"
```
