# Data Protection Toolkit

| Tool | Use | OSS Quick Check |
|---|---|---|
| Great Expectations | Data schema and expectation-based quality controls | `python -c "import great_expectations; print(great_expectations.__version__)"` |
| TensorFlow Data Validation | Feature schema, distribution shift, and drift checks | `python -c "import tensorflow_data_validation as tfdv; print('tfdv ok')"` |
| Deepchecks | Data integrity, leakage, and suspicious-label detection | `python -c "import deepchecks; print('deepchecks ok')"` |
| WhyLogs | Statistical data profiles and automated baseline checks | `python -c "import whylogs; print('whylogs ok')"` |
| Evidently | Shift and feature monitoring reports | `python -c "import evidently; print('evidently ok')"` |
| Pandera | Type-enforced dataframe validation rules | `python -c "import pandera; print('pandera ok')"` |
| Presidio Analyzer | PII detection and redaction candidates for text | `python -c "import presidio_analyzer; print('presidio ok')"` |
| OpenDP | Formal differential privacy primitives | `python -c "import opendp; print('opendp ok')"` |
| Opacus | DP-SGD and differential-privacy training (PyTorch) | `python -c "import opacus; print('opacus ok')"` |
| TensorFlow Privacy | DP training APIs for TensorFlow | `python -c "import tensorflow_privacy; print('tensorflow_privacy ok')"` |
| ML Privacy Meter | Membership-inference and privacy leakage tests | `python -c "import ml_privacy_meter; print('ml_privacy_meter ok')"` |
| ARX (Java) | De-identification (k-anonymity, l-diversity, t-closeness) | ARX is Java-based; use the published CLI/GUI workflow from upstream documentation |
| [Guardrails AI](https://github.com/guardrails-ai/guardrails) | Guard prompt-like inputs and enforce allowed output formats before training/inference | `python -m guardrails validate` |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | Prompt fuzzing to detect injection patterns in text datasets | `npx promptfoo@latest init` |

## Use Pattern
1. Validate schema/provenance first.
2. Add OSS-based quality and poisoning checks (`Great Expectations` / `Deepchecks` / `TFDV`).
3. Run privacy-risk tooling where regulated workloads exist (`Presidio`, `OpenDP`, `Opacus`).
4. Capture tool outputs and keep them as release evidence in this stage.
