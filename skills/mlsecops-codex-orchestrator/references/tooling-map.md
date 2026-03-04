# Orchestrator Tooling Map

Use this map to choose practical tools while building the cross-skill plan.

| Domain | Tool | Purpose |
|---|---|---|
| Threat model | MITRE ATLAS | Classify AI attack techniques |
| LLM app security | OWASP LLMSVS | Verification requirements for LLM systems |
| Data privacy | OpenDP / TensorFlow Privacy | Differential privacy controls |
| Model testing | Garak / PyRIT / Promptfoo / ART / TextAttack | Abuse, jailbreak, and adversarial testing |
| Supply chain integrity | ModelScan / OSV-Scanner / in-toto / SLSA GitHub Generator / Sigstore Cosign | Model and dependency integrity with provenance |
| Secret leak detection | Gitleaks / TruffleHog | Detect and validate leaked credentials |
| Runtime guardrails | NeMo Guardrails / Falco | Prompt safety and runtime abuse detection |
| Monitoring and telemetry | OpenTelemetry Collector / AVID / incidentdatabase.ai | Security telemetry and incident knowledge |
| MCP ecosystem | GitHub MCP Server / MCP Reference Servers / MCP Registry / SafeDep vet MCP | Typed tool access and package vetting via MCP |
| Malicious artifact defense | ModelScan / YARA / semgrep / bandit / pickletools | Detect payload-capable model files and risky deserialization paths |
