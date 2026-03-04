# Open-Source Tool Runners

Use `run_open_source_scans.py` to execute or plan scans with common security tools.

## Supported Tool Profiles

- `semgrep`: static analysis
- `bandit`: Python security linting
- `trivy`: filesystem/dependency scanning
- `grype`: vulnerability scanning
- `syft`: SBOM generation
- `gitleaks`: secret scanning
- `modelscan`: model artifact security scanning ([protectai/modelscan](https://github.com/protectai/modelscan))
- `trufflehog`: credential discovery and validation ([trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog))
- `osv-scanner`: dependency vulnerability scanning ([google/osv-scanner](https://github.com/google/osv-scanner))

## Dry-Run Example

```bash
python skills/mlsecops-supply-chain/scripts/run_open_source_scans.py \
  --target . \
  --tools "semgrep,bandit,trivy,grype,syft,gitleaks,modelscan,trufflehog,osv-scanner" \
  --output open-source-scan-report.md
```

## Execute Example

```bash
python skills/mlsecops-supply-chain/scripts/run_open_source_scans.py \
  --target . \
  --tools "semgrep,bandit,modelscan,trufflehog,osv-scanner" \
  --execute \
  --output open-source-scan-report.md
```
