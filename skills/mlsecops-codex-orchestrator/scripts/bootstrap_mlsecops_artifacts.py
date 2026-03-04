#!/usr/bin/env python3
"""Bootstrap a full MLSecOps artifact pack by chaining stage scripts."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Job:
    name: str
    script_path: Path
    args: list[str]
    output_file: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate all baseline MLSecOps artifacts.")
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--system-summary", required=True)
    parser.add_argument("--risk-profile", choices=["low", "medium", "high", "critical"], default="high")
    parser.add_argument("--assets", default="training-data,model-registry,inference-api")
    parser.add_argument("--data-sources", default="events:medium,customer-profile:high")
    parser.add_argument("--frameworks", default="SOC2,ISO27001,NIST AI RMF")
    parser.add_argument("--service-name", default="inference-api")
    parser.add_argument("--incident-type", default="prompt-injection-bypass")
    parser.add_argument("--package-manager", default="uv")
    parser.add_argument("--ci-platform", default="github-actions")
    parser.add_argument("--output-dir", default="mlsecops-artifacts")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def build_jobs(args: argparse.Namespace, skills_root: Path, output_dir: Path) -> list[Job]:
    orchestrator_dir = skills_root / "mlsecops-codex-orchestrator" / "scripts"
    return [
        Job(
            name="task-plan",
            script_path=orchestrator_dir / "generate_task_plan.py",
            args=[
                "--project-name",
                args.project_name,
                "--system-summary",
                args.system_summary,
                "--risk-profile",
                args.risk_profile,
                "--compliance",
                args.frameworks,
                "--output",
                str(output_dir / "task.md"),
            ],
            output_file=output_dir / "task.md",
        ),
        Job(
            name="threat-register",
            script_path=skills_root / "mlsecops-foundation" / "scripts" / "generate_threat_register.py",
            args=[
                "--assets",
                args.assets,
                "--output",
                str(output_dir / "threat-register.md"),
            ],
            output_file=output_dir / "threat-register.md",
        ),
        Job(
            name="data-control-matrix",
            script_path=skills_root / "mlsecops-data-protection" / "scripts" / "generate_data_control_matrix.py",
            args=[
                "--sources",
                args.data_sources,
                "--output",
                str(output_dir / "data-control-matrix.md"),
            ],
            output_file=output_dir / "data-control-matrix.md",
        ),
        Job(
            name="model-assurance",
            script_path=skills_root / "mlsecops-model-assurance" / "scripts" / "generate_assurance_matrix.py",
            args=[
                "--output",
                str(output_dir / "model-assurance-matrix.md"),
            ],
            output_file=output_dir / "model-assurance-matrix.md",
        ),
        Job(
            name="supply-chain",
            script_path=skills_root / "mlsecops-supply-chain" / "scripts" / "generate_supply_chain_checklist.py",
            args=[
                "--project-name",
                args.project_name,
                "--package-manager",
                args.package_manager,
                "--ci-platform",
                args.ci_platform,
                "--output",
                str(output_dir / "supply-chain-checklist.md"),
            ],
            output_file=output_dir / "supply-chain-checklist.md",
        ),
        Job(
            name="runtime-defense",
            script_path=skills_root / "mlsecops-runtime-defense" / "scripts" / "generate_runtime_baseline.py",
            args=[
                "--service-name",
                args.service_name,
                "--output",
                str(output_dir / "runtime-defense-baseline.md"),
            ],
            output_file=output_dir / "runtime-defense-baseline.md",
        ),
        Job(
            name="observability-ir",
            script_path=skills_root / "mlsecops-observability-ir" / "scripts" / "generate_ir_playbook.py",
            args=[
                "--service-name",
                args.service_name,
                "--incident-type",
                args.incident_type,
                "--output",
                str(output_dir / "incident-playbook.md"),
            ],
            output_file=output_dir / "incident-playbook.md",
        ),
        Job(
            name="governance",
            script_path=skills_root / "mlsecops-governance" / "scripts" / "generate_evidence_register.py",
            args=[
                "--frameworks",
                args.frameworks,
                "--output",
                str(output_dir / "evidence-register.md"),
            ],
            output_file=output_dir / "evidence-register.md",
        ),
    ]


def run_job(job: Job, dry_run: bool) -> dict[str, object]:
    command = [sys.executable, str(job.script_path), *job.args]
    command_text = shlex.join(command)

    if not job.script_path.exists():
        return {
            "name": job.name,
            "status": "failed",
            "command": command_text,
            "output_file": str(job.output_file),
            "reason": "Script file not found",
        }

    if dry_run:
        return {
            "name": job.name,
            "status": "planned",
            "command": command_text,
            "output_file": str(job.output_file),
            "reason": "Dry-run mode",
        }

    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    return {
        "name": job.name,
        "status": "passed" if completed.returncode == 0 else "failed",
        "command": command_text,
        "output_file": str(job.output_file),
        "return_code": completed.returncode,
        "stdout_excerpt": (completed.stdout or "")[:2000],
        "stderr_excerpt": (completed.stderr or "")[:2000],
    }


def render_summary(results: list[dict[str, object]], dry_run: bool) -> str:
    rows = "\n".join(
        f"| {item['name']} | {item['status']} | `{item['output_file']}` | `{item['command']}` |"
        for item in results
    )

    details = []
    for item in results:
        lines = [
            f"## {item['name']}",
            f"- Status: `{item['status']}`",
            f"- Output: `{item['output_file']}`",
            f"- Command: `{item['command']}`",
        ]
        reason = item.get("reason")
        if reason:
            lines.append(f"- Reason: {reason}")
        if item.get("return_code") is not None:
            lines.append(f"- Return code: `{item['return_code']}`")
        if item.get("stdout_excerpt"):
            lines.append("### stdout (excerpt)\n```text\n" + str(item["stdout_excerpt"]) + "\n```")
        if item.get("stderr_excerpt"):
            lines.append("### stderr (excerpt)\n```text\n" + str(item["stderr_excerpt"]) + "\n```")
        details.append("\n".join(lines))

    return (
        "# MLSecOps Bootstrap Summary\n\n"
        f"- Dry-run: `{dry_run}`\n\n"
        "| Job | Status | Output File | Command |\n"
        "|---|---|---|---|\n"
        f"{rows}\n\n"
        + "\n\n".join(details)
        + "\n"
    )


def main() -> None:
    args = parse_args()
    this_file = Path(__file__).resolve()
    skills_root = this_file.parents[2]
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    jobs = build_jobs(args, skills_root=skills_root, output_dir=output_dir)
    results = [run_job(job, dry_run=args.dry_run) for job in jobs]

    summary_md = output_dir / "bootstrap-summary.md"
    summary_json = output_dir / "bootstrap-summary.json"
    summary_md.write_text(render_summary(results, dry_run=args.dry_run), encoding="utf-8")
    summary_json.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote bootstrap summary to {summary_md}")
    print(f"Wrote machine-readable results to {summary_json}")

    failed = any(item["status"] == "failed" for item in results)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
