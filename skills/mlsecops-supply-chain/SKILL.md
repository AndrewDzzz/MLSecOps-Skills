---
name: mlsecops-supply-chain
description: Harden ML supply chain integrity across dependencies, model artifacts, and CI/CD pipelines. Use when securing build and release workflows, reducing serialization and dependency risk, and enforcing provenance, signing, and policy gates.
---

# MLSecOps Supply Chain

## Goal
Stop tampering and high-risk dependency drift before model release or runtime rollout.

## Use this skill for
- Dependency and lockfile hardening.
- ML artifact inspection and promotion controls.
- CI/CD trust boundary and provenance validation.

## Required Inputs
- Package manifests and lockfiles (`pyproject.toml`, `uv.lock`, container definitions)
- Model artifact types and registry/promotion workflow
- CI/CD YAML and approval policy requirements

## Step-by-step workflow
1. Baseline dependency control.
   - Enforce lockfile policy and deterministic install mode.
   - Output: package manager and lockfile policy statement.
2. Scan for vulnerabilities and secrets.
   - Run dependency vulnerability and secret scanning profiles.
   - Output: scan report with severity gating.
3. Inspect model artifacts.
   - For pickles or executable-format models, run static opcode checks.
   - Prefer non-executable formats (`safetensors`) where feasible.
   - Output: artifact verdict and required remediation.
4. Enforce integrity and provenance.
   - Generate SBOM + signatures and verify before deploy.
   - Output: provenance evidence and policy checks.
5. Reduce CI/CD blast radius.
   - Restrict workflow permissions, prefer OIDC and short-lived credentials.
   - Output: trusted promotion and exception process.
6. Verify end-to-end with tool-driven scans.
   - Generate supply checklist and run supported scanners in dry-run or execute mode.
   - Output: `supply-chain-checklist.md` and scan report.

## What this skill can detect
- Unpinned dependencies and hidden drift risk.
- CVE and secret exposure in source/build artifacts.
- Malicious or unsafe serialized artifacts.
- Weak release approvals or unverifiable artifact promotion.

## Outputs
- `supply-chain-checklist.md`
- `open-source-scan-report.md` (or JSON/markdown report from scanner runner)
- Signed/provenance policy notes for promotion.

## Quality Gates
- [ ] Lockfile and dependency pinning is enforced.
- [ ] Scan profile blocks critical/high vulnerabilities and leaks by policy.
- [ ] All promoted artifacts have scan evidence and signature checks.
- [ ] CI/CD approvals are protected and time-bounded.

## Bundled Resources
- References:
  - `references/toolkit.md`: control stack for scanning, signing, and provenance.
  - `references/checklist-template.md`: artifact hardening baseline.
  - `references/open-source-tool-runners.md`: scan command profiles.
- Scripts:
  - `scripts/generate_supply_chain_checklist.py`: generate a project-specific checklist.
  - `scripts/run_open_source_scans.py`: orchestrate scanner plans/executions.

## Tool Usage
Generate a tailored checklist:

```bash
python skills/mlsecops-supply-chain/scripts/generate_supply_chain_checklist.py \
  --project-name "fraud-detector" \
  --package-manager uv \
  --ci-platform github-actions \
  --output supply-chain-checklist.md
```

Run a scanner dry-run first:

```bash
python skills/mlsecops-supply-chain/scripts/run_open_source_scans.py \
  --target . \
  --tools "semgrep,bandit,trivy,grype,syft,gitleaks,modelscan,trufflehog,osv-scanner" \
  --output open-source-scan-report.md
```

Execute strict promotion checks for model formats:

```bash
python3 -m pickletools dis suspect-model-file.pickle
python -m zipfile --testzip artifact.zip
```
