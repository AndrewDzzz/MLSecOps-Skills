# Runtime Defense Toolkit

| Tool | Use |
|---|---|
| [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | Input/output guardrails for LLM apps |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | Prompt abuse and policy compliance tests |
| [Open Policy Agent](https://github.com/open-policy-agent/opa) | Fine-grained runtime policy authorization |
| [ModSecurity](https://github.com/SpiderLabs/ModSecurity) | WAF policy enforcement for APIs |
| [OWASP CRS](https://github.com/coreruleset/coreruleset) | Managed WAF rulesets for attack class coverage |
| [Envoy](https://github.com/envoyproxy/envoy) | Edge policy enforcement and request controls |
| [Kong Gateway](https://github.com/Kong/kong) | API auth, throttling, and plugin-based guardrails |
| [Guardrails AI](https://github.com/guardrails-ai/guardrails) | Runtime structured output and prompt guard checks |
| [Vigil](https://github.com/owasp/vigil) | Prompt injection and security analysis workflows |
| [gVisor](https://github.com/google/gvisor) | Container and syscall isolation for ML runtime workers |
| [YARA](https://github.com/VirusTotal/yara) | Runtime scan rules and threat signature checks on loaded artifacts |

## Execution Pattern
1. Harden endpoint auth and validation.
2. Enforce containment and secret isolation.
3. Test bypass and fail-closed behavior.
