# Model Assurance Toolkit

| Tool | Use |
|---|---|
| [Garak](https://github.com/NVIDIA/garak) | LLM vulnerability scanning |
| [PyRIT](https://github.com/Azure/PyRIT) | LLM red-team automation |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | Prompt and policy abuse testing |
| [ART (TrustedAI)](https://github.com/Trusted-AI/adversarial-robustness-toolbox) | Classical ML adversarial robustness, poisoning, and evasion |
| [Foolbox](https://github.com/bethgelab/foolbox) | Evasion/adversarial benchmarking |
| [TextAttack](https://github.com/QData/TextAttack) | NLP adversarial examples |
| [OpenAttack](https://github.com/thunlp/OpenAttack) | Adversarial examples and black-box attack evaluation |
| [RobustBench](https://github.com/RobustBench/robustbench) | Leaderboards and scripts for image-robustness benchmarking |
| [OpenAI Evals](https://github.com/openai/evals) | Reusable benchmark scaffolds for behavior and policy scoring |
| [Giskard](https://github.com/Giskard-AI/giskard) | Automated QA and LLM/NLP model testing workflows |
| [Guardrails AI](https://github.com/guardrails-ai/guardrails) | Structured output and input/output safety checks |
| [Python Pickletools](https://docs.python.org/3/library/pickletools.html) | Inspect pickle bytecode (`REDUCE`, `GLOBAL`, and exec-like opcodes) before loading artifacts |

## Execution Pattern
1. Pick attack classes by model type.
2. Run reproducible suites and store evidence.
3. Convert failures into release-gate thresholds.
