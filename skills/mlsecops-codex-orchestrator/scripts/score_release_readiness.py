#!/usr/bin/env python3
"""Score MLSecOps release readiness based on generated artifact quality signals."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ArtifactRule:
    name: str
    path: str
    min_lines: int
    required_signals: list[str]


RULES = [
    ArtifactRule(
        name="Task Plan",
        path="task.md",
        min_lines=40,
        required_signals=["P0", "Stage", "Exit Criteria"],
    ),
    ArtifactRule(
        name="Threat Register",
        path="threat-register.md",
        min_lines=10,
        required_signals=["Likelihood", "Impact", "Owner"],
    ),
    ArtifactRule(
        name="Data Control Matrix",
        path="data-control-matrix.md",
        min_lines=8,
        required_signals=["Provenance Control", "Poisoning Check", "Privacy Control"],
    ),
    ArtifactRule(
        name="Model Assurance Matrix",
        path="model-assurance-matrix.md",
        min_lines=8,
        required_signals=["Threshold", "Severity", "Owner"],
    ),
    ArtifactRule(
        name="Supply Chain Checklist",
        path="supply-chain-checklist.md",
        min_lines=8,
        required_signals=["lockfile", "SBOM", "signing"],
    ),
    ArtifactRule(
        name="Runtime Defense Baseline",
        path="runtime-defense-baseline.md",
        min_lines=8,
        required_signals=["AuthN/AuthZ", "Containment", "Fail"],
    ),
    ArtifactRule(
        name="Incident Playbook",
        path="incident-playbook.md",
        min_lines=12,
        required_signals=["Detection", "Containment", "Postmortem"],
    ),
    ArtifactRule(
        name="Evidence Register",
        path="evidence-register.md",
        min_lines=8,
        required_signals=["Framework", "Evidence Artifact", "Owner"],
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score MLSecOps release readiness.")
    parser.add_argument("--artifact-dir", default="mlsecops-artifacts")
    parser.add_argument("--output", default="release-readiness.md")
    return parser.parse_args()


def evaluate(rule: ArtifactRule, artifact_dir: Path) -> dict[str, object]:
    artifact_file = artifact_dir / rule.path
    exists = artifact_file.exists()
    if not exists:
        return {
            "name": rule.name,
            "path": str(artifact_file),
            "exists": False,
            "line_score": 0,
            "signal_score": 0,
            "total_score": 0,
            "status": "gap",
            "missing_signals": rule.required_signals,
        }

    content = artifact_file.read_text(encoding="utf-8", errors="replace")
    lines = [line for line in content.splitlines() if line.strip()]
    lower = content.lower()

    line_score = 30 if len(lines) >= rule.min_lines else int((len(lines) / max(rule.min_lines, 1)) * 30)

    found = [signal for signal in rule.required_signals if signal.lower() in lower]
    signal_ratio = len(found) / len(rule.required_signals) if rule.required_signals else 1.0
    signal_score = int(30 * signal_ratio)

    total_score = 40 + line_score + signal_score
    if total_score >= 85:
        status = "ready"
    elif total_score >= 60:
        status = "partial"
    else:
        status = "gap"

    return {
        "name": rule.name,
        "path": str(artifact_file),
        "exists": True,
        "line_score": line_score,
        "signal_score": signal_score,
        "total_score": total_score,
        "status": status,
        "missing_signals": [signal for signal in rule.required_signals if signal not in found],
    }


def render_markdown(results: list[dict[str, object]], overall_score: int) -> str:
    rows = "\n".join(
        f"| {r['name']} | {r['status']} | {r['total_score']} | {r['line_score']} | {r['signal_score']} | `{r['path']}` |"
        for r in results
    )

    gaps = [r for r in results if r["status"] != "ready"]
    recommendations = []
    for gap in gaps:
        missing = ", ".join(gap["missing_signals"]) if gap["missing_signals"] else "expand artifact detail"
        recommendations.append(f"- {gap['name']}: fill missing signals ({missing}).")

    if overall_score >= 85:
        verdict = "ready"
    elif overall_score >= 60:
        verdict = "partial"
    else:
        verdict = "gap"

    rec_text = "\n".join(recommendations) if recommendations else "- No major gaps detected."

    return (
        "# MLSecOps Release Readiness\n\n"
        f"- Overall score: **{overall_score}/100**\n"
        f"- Verdict: **{verdict}**\n\n"
        "| Artifact | Status | Score | Content Score | Signal Score | Path |\n"
        "|---|---|---:|---:|---:|---|\n"
        f"{rows}\n\n"
        "## Recommendations\n"
        f"{rec_text}\n"
    )


def main() -> None:
    args = parse_args()
    artifact_dir = Path(args.artifact_dir).expanduser().resolve()
    results = [evaluate(rule, artifact_dir=artifact_dir) for rule in RULES]
    overall_score = int(sum(int(item["total_score"]) for item in results) / len(results))

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown(results, overall_score), encoding="utf-8")
    print(f"Wrote readiness report to {output_path}")


if __name__ == "__main__":
    main()
