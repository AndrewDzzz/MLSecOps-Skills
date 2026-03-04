# Foundation Toolkit

Use this file when selecting frameworks and tools during threat modeling.

| Tool | Use | OSS Quick Start |
|---|---|---|
| OWASP Threat Dragon | Diagram-driven threat modeling with threat suggestions across trust boundaries | `docker run -it --rm -p 8080:3000 owasp/threat-dragon:stable` |
| OWASP pytm | Pythonic threat modeling-to-diagram/JSON workflow for architecture-based models | `tm.py --help` |
| Threagile | Agile threat-model-as-code with YAML, risk rules, and reporting in CI-friendly flows | `docker run --rm -it threagile/threagile --help` |
| threatspec | Threat modeling through code comments and source annotations, with `threatspec run` + `report` | `pip install threatspec && threatspec init` |
| OWASP Threat Model Library | Peer-reviewed open threat models and shared schema direction for reuse | Visit the OWASP page and import compatible JSON outputs |
| OWASP Threat Modeling Project | Curated methodologies and techniques for consistent modeling process selection | Use as baseline process reference before model tool execution |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | Map prompt-injection and jailbreak scenarios into threat classes | `npx promptfoo@latest init` |
| [PyRIT](https://github.com/Azure/PyRIT) | Add attack trees for prompt, tool-call, and policy bypass abuse paths | `python -m pip install pyrit && pyrit --help` |

## Practical Sequence
1. Start with ATLAS for attack classification.
2. Choose one of the OSS tooling tracks: diagram-first (`threat-dragon`), model-first (`threagile`/`pytm`), or code-first (`threatspec`).
3. Run the selected tool in draft mode and map top findings to owner/action/timeline controls.
4. Cross-check against OWASP ML/LLM categories.
5. Convert top risks into control owners and release gates.
