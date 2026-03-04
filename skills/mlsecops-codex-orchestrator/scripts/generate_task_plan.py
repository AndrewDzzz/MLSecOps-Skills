#!/usr/bin/env python3
"""Generate a standalone MLSecOps task plan markdown file."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path


DEFAULT_STAGE_ORDER = [
    "mlsecops-foundation",
    "mlsecops-data-protection",
    "mlsecops-model-assurance",
    "mlsecops-supply-chain",
    "mlsecops-runtime-defense",
    "mlsecops-observability-ir",
    "mlsecops-governance",
]


LIFECYCLE_STAGES = [
    "Business understanding",
    "Data collection and preprocessing",
    "Model design and development",
    "Model training and evaluation",
    "Model deployment",
    "Model monitoring and maintenance",
    "Governance and compliance",
    "Collaboration and communication",
    "Infrastructure and tooling",
    "Incident response and continuous improvement",
]


SKILL_DETAILS = {
    "mlsecops-foundation": {
        "goal": "Establish threat model, trust boundaries, and release security baseline.",
        "domain": "Governance and architecture risk baseline",
        "owner": "Security Architect",
        "activities": [
            "Build an ML/LLM threat register using MITRE ATLAS and OWASP ML/LLM categories.",
            "Map critical assets and trust boundaries across training, registry, and inference.",
            "Set release-blocking criteria for unresolved high/critical threats.",
        ],
        "outputs": [
            "Threat register",
            "Baseline control plan",
            "Deployment security gate checklist",
        ],
        "exit_criteria": [
            "Top risks are mapped to controls with owners.",
            "Release criteria are documented and testable.",
        ],
    },
    "mlsecops-data-protection": {
        "goal": "Secure data confidentiality, integrity, and provenance across lifecycle stages.",
        "domain": "Data security and privacy",
        "owner": "Data Platform Lead",
        "activities": [
            "Enforce dataset lineage, checksums, and schema/drift validation.",
            "Apply least-privilege access and retention/deletion policy controls.",
            "Introduce poisoning detection and quarantine for suspicious batches.",
        ],
        "outputs": [
            "Data control matrix",
            "Ingestion validation policy",
            "Poisoning response workflow",
        ],
        "exit_criteria": [
            "Lineage and access controls are enforced in pipelines.",
            "Poisoning and privacy controls are integrated before training.",
        ],
    },
    "mlsecops-model-assurance": {
        "goal": "Quantitatively validate robustness and abuse resistance prior to release.",
        "domain": "Model and algorithm security",
        "owner": "ML Security Lead",
        "activities": [
            "Run adversarial robustness and out-of-distribution evaluations.",
            "Assess extraction, inversion, and privacy leakage risks.",
            "Execute prompt injection/jailbreak tests for LLM-based systems.",
        ],
        "outputs": [
            "Assurance matrix with pass/fail thresholds",
            "Security evaluation report",
            "Remediation backlog for failed scenarios",
        ],
        "exit_criteria": [
            "Critical abuse paths have passing controls or explicit blockers.",
            "Release decision is evidence-backed and reproducible.",
        ],
    },
    "mlsecops-supply-chain": {
        "goal": "Protect dependencies, build pipelines, and model artifacts from tampering.",
        "domain": "Supply chain and artifact integrity",
        "owner": "DevSecOps Engineer",
        "activities": [
            "Pin dependencies and enforce vulnerability scanning in CI.",
            "Generate SBOMs and sign release artifacts.",
            "Scan model files and avoid unsafe serialization formats.",
        ],
        "outputs": [
            "Supply chain checklist",
            "Artifact signing and verification policy",
            "CI/CD hardening plan",
        ],
        "exit_criteria": [
            "Critical vulnerabilities are gated by policy.",
            "Provenance and signature verification are enforced for promotion.",
        ],
    },
    "mlsecops-runtime-defense": {
        "goal": "Reduce exploitability and blast radius of live inference systems.",
        "domain": "Deployment and runtime defense",
        "owner": "Platform Security Engineer",
        "activities": [
            "Enforce authentication, authorization, and abuse throttling.",
            "Apply runtime isolation and least-privilege identity policies.",
            "Implement fail-closed guardrails and rollback controls.",
        ],
        "outputs": [
            "Runtime hardening baseline",
            "API abuse-defense policy",
            "Safe-failure runbook",
        ],
        "exit_criteria": [
            "Runtime boundaries and guardrails are tested and monitored.",
            "Safe rollback and containment paths are operational.",
        ],
    },
    "mlsecops-observability-ir": {
        "goal": "Detect and contain ML/LLM abuse with measurable response quality.",
        "domain": "Monitoring and incident response",
        "owner": "Security Operations Lead",
        "activities": [
            "Define telemetry schema with model version and policy outcome fields.",
            "Add detections for extraction, prompt injection, and drift anomalies.",
            "Create and exercise incident playbooks for priority abuse cases.",
        ],
        "outputs": [
            "Telemetry specification",
            "Detection backlog and alert tuning plan",
            "Incident response playbooks",
        ],
        "exit_criteria": [
            "Critical abuse scenarios have active detections and runbooks.",
            "Postmortem actions are tracked with ownership and due dates.",
        ],
    },
    "mlsecops-governance": {
        "goal": "Operationalize auditability, control ownership, and policy alignment.",
        "domain": "Governance, risk, and compliance",
        "owner": "GRC Program Owner",
        "activities": [
            "Map controls to target frameworks (SOC2, ISO27001, NIST AI RMF).",
            "Define evidence requirements for each release and exception workflow.",
            "Run periodic reviews for control effectiveness and policy drift.",
        ],
        "outputs": [
            "Control-framework mapping matrix",
            "Evidence register",
            "Risk exception policy with expiry controls",
        ],
        "exit_criteria": [
            "Controls have owners, cadence, and evidence artifacts.",
            "Exceptions are time-bounded with compensating controls.",
        ],
    },
}


RISK_PRIORITY_OVERRIDES = {
    "low": [2, 2, 2, 2, 2, 2, 1],
    "medium": [0, 0, 1, 1, 1, 1, 1],
    "high": [0, 0, 0, 0, 1, 1, 1],
    "critical": [0, 0, 0, 0, 0, 0, 1],
}


@dataclass
class TaskPlanConfig:
    project_name: str
    system_summary: str
    risk_profile: str
    compliance: list[str]
    stages: list[str]
    output: Path


def _parse_csv(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def _resolve_stages(raw_stages: str) -> list[str]:
    if not raw_stages.strip():
        return DEFAULT_STAGE_ORDER[:]
    chosen = _parse_csv(raw_stages)
    invalid = [stage for stage in chosen if stage not in SKILL_DETAILS]
    if invalid:
        valid = ", ".join(DEFAULT_STAGE_ORDER)
        raise ValueError(f"Unknown stages: {', '.join(invalid)}. Valid options: {valid}")
    return chosen


def parse_args() -> TaskPlanConfig:
    parser = argparse.ArgumentParser(description="Generate MLSecOps task plan markdown.")
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--system-summary", required=True)
    parser.add_argument(
        "--risk-profile",
        choices=["low", "medium", "high", "critical"],
        default="medium",
    )
    parser.add_argument("--compliance", default="")
    parser.add_argument("--stages", default="")
    parser.add_argument("--output", default="task.md")
    args = parser.parse_args()

    return TaskPlanConfig(
        project_name=args.project_name.strip(),
        system_summary=args.system_summary.strip(),
        risk_profile=args.risk_profile,
        compliance=_parse_csv(args.compliance),
        stages=_resolve_stages(args.stages),
        output=Path(args.output).expanduser(),
    )


def _priority_for_stage(risk_profile: str, idx: int) -> str:
    level = RISK_PRIORITY_OVERRIDES[risk_profile][idx]
    if level == 0:
        return "P0"
    if level == 1:
        return "P1"
    return "P2"


def _render_stage_block(stage_name: str, stage_index: int, risk_profile: str) -> str:
    detail = SKILL_DETAILS[stage_name]
    priority = _priority_for_stage(risk_profile, stage_index)

    activities = "\n".join(f"- {item}" for item in detail["activities"])
    outputs = "\n".join(f"- {item}" for item in detail["outputs"])
    exit_criteria = "\n".join(f"- [ ] {item}" for item in detail["exit_criteria"])

    return (
        f"## Stage {stage_index + 1}: `{stage_name}` ({priority})\n\n"
        f"- Domain: {detail['domain']}\n"
        f"- Owner Role: {detail['owner']}\n"
        f"- Goal: {detail['goal']}\n\n"
        f"Activities:\n{activities}\n\n"
        f"Deliverables:\n{outputs}\n\n"
        f"Exit Criteria:\n{exit_criteria}\n"
    )


def render_markdown(cfg: TaskPlanConfig) -> str:
    compliance = ", ".join(cfg.compliance) if cfg.compliance else "Not specified"
    lifecycle = "\n".join(f"{idx + 1}. {name}" for idx, name in enumerate(LIFECYCLE_STAGES))

    blocks = [
        _render_stage_block(stage_name, idx, cfg.risk_profile)
        for idx, stage_name in enumerate(cfg.stages)
    ]
    stage_content = "\n".join(blocks)

    return f"""# MLSecOps Task Plan

- Generated: {date.today().isoformat()}
- Project: {cfg.project_name}
- Risk profile: {cfg.risk_profile}
- Compliance targets: {compliance}

## System Summary
{cfg.system_summary}

## AI Lifecycle Coverage
This plan is aligned to a 10-stage AI development lifecycle:
{lifecycle}

## Execution Stages
{stage_content}
"""


def main() -> None:
    cfg = parse_args()
    markdown = render_markdown(cfg)

    output_path = cfg.output.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Wrote {len(cfg.stages)} stages to {output_path}")


if __name__ == "__main__":
    main()
