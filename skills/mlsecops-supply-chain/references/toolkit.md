# Supply Chain Toolkit

| Tool | Use |
|---|---|
| [ModelScan](https://github.com/protectai/modelscan) | Scan ML model files for risky payloads |
| [OSV-Scanner](https://github.com/google/osv-scanner) | Dependency vulnerability scanning from source and lockfiles |
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | High-confidence secret discovery and validation |
| [in-toto](https://github.com/in-toto/in-toto) | Software supply chain attestation framework |
| [SLSA GitHub Generator](https://github.com/slsa-framework/slsa-github-generator) | Build provenance generation in GitHub Actions |
| [Sigstore Cosign](https://github.com/sigstore/cosign) | Artifact signing and signature verification |
| [Syft](https://github.com/anchore/syft) / [Grype](https://github.com/anchore/grype) | SBOM generation and vulnerability matching |
| [SafeDep vet](https://github.com/safedep/vet) | Package risk vetting, including MCP mode (`vet server mcp`) |
| safetensors | Safer model serialization format |

## Execution Pattern
1. Pin and scan dependencies.
2. Scan model artifacts before promotion (`modelscan`).
3. Run secret and dependency scans (`trufflehog`, `osv-scanner`).
4. Generate SBOM + signatures.
5. Enforce attestation and verification in deployment workflow.

## Artifact Inspection
| Tool | Use |
|---|---|
| Python Pickletools | Disassemble pickled model artifacts and inspect unsafe opcodes before promotion |
