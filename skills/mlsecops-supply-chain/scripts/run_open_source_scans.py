#!/usr/bin/env python3
"""Run open-source security tools with dry-run and execution modes."""

from __future__ import annotations

import argparse
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

Status = Literal['planned', 'skipped', 'passed', 'failed']


class ToolExecution(BaseModel):
	"""Execution record for one tool."""

	tool: str
	status: Status
	command: str
	reason: str | None = None
	returncode: int | None = None
	stdout_excerpt: str | None = None
	stderr_excerpt: str | None = None


class ScanRequest(BaseModel):
	"""Input contract for open-source scan runs."""

	target: Path
	tools: list[str] = Field(default_factory=list)
	execute: bool = False
	timeout_seconds: int = Field(default=300, ge=5, le=3600)
	output: Path = Field(default=Path('open-source-scan-report.md'))


class ScanReport(BaseModel):
	"""Aggregate scan report."""

	target: Path
	execute: bool
	results: list[ToolExecution] = Field(default_factory=list)


def _tool_commands(target: Path) -> dict[str, list[str]]:
	"""Return command templates for supported tools."""
	target_str = str(target)
	return {
		'semgrep': ['semgrep', '--config', 'auto', target_str, '--json'],
		'bandit': ['bandit', '-r', target_str, '-f', 'json'],
		'trivy': ['trivy', 'fs', '--format', 'json', target_str],
		'grype': ['grype', f'dir:{target_str}', '-o', 'json'],
		'syft': ['syft', f'dir:{target_str}', '-o', 'cyclonedx-json'],
		'gitleaks': ['gitleaks', 'detect', '--source', target_str, '--no-git'],
		'modelscan': ['modelscan', '-p', target_str, '-r', 'json'],
		'trufflehog': ['trufflehog', 'filesystem', target_str, '--json'],
		'osv-scanner': ['osv-scanner', 'scan', 'source', '-r', target_str],
	}


def _parse_tools(raw: str) -> list[str]:
	"""Parse comma-separated tool names."""
	default = ['semgrep', 'bandit', 'trivy', 'grype', 'syft', 'gitleaks', 'modelscan', 'trufflehog', 'osv-scanner']
	if not raw.strip():
		return default
	return [item.strip() for item in raw.split(',') if item.strip()]


def _parse_args() -> ScanRequest:
	"""Parse CLI args and validate request model."""
	parser = argparse.ArgumentParser(description='Run or plan open-source MLSecOps scans.')
	parser.add_argument('--target', default='.', help='Directory to scan')
	parser.add_argument('--tools', default='', help='Comma-separated tools')
	parser.add_argument('--execute', action='store_true', help='Run commands (default is dry-run plan)')
	parser.add_argument('--timeout-seconds', type=int, default=300)
	parser.add_argument('--output', default='open-source-scan-report.md')
	args = parser.parse_args()
	return ScanRequest(
		target=Path(args.target).expanduser().resolve(),
		tools=_parse_tools(args.tools),
		execute=args.execute,
		timeout_seconds=args.timeout_seconds,
		output=Path(args.output).expanduser(),
	)


def _run_one(tool: str, command: list[str], execute: bool, timeout_seconds: int) -> ToolExecution:
	"""Run a single tool command or return planned entry."""
	command_text = shlex.join(command)
	if shutil.which(command[0]) is None:
		return ToolExecution(tool=tool, status='skipped', command=command_text, reason='Tool not installed')
	if not execute:
		return ToolExecution(tool=tool, status='planned', command=command_text, reason='Dry-run mode')

	try:
		completed = subprocess.run(
			command,
			check=False,
			capture_output=True,
			text=True,
			timeout=timeout_seconds,
		)
	except subprocess.TimeoutExpired:
		return ToolExecution(tool=tool, status='failed', command=command_text, reason='Timed out')

	status: Status = 'passed' if completed.returncode == 0 else 'failed'
	return ToolExecution(
		tool=tool,
		status=status,
		command=command_text,
		returncode=completed.returncode,
		stdout_excerpt=(completed.stdout or '')[:4000],
		stderr_excerpt=(completed.stderr or '')[:4000],
	)


def _render_markdown(report: ScanReport) -> str:
	"""Render report as markdown."""
	rows = '\n'.join(
		f'| {r.tool} | {r.status} | `{r.command}` | {r.reason or ""} | {r.returncode if r.returncode is not None else ""} |'
		for r in report.results
	)
	sections = []
	for r in report.results:
		section = [f'## {r.tool}', f'- Status: `{r.status}`', f'- Command: `{r.command}`']
		if r.reason:
			section.append(f'- Reason: {r.reason}')
		if r.returncode is not None:
			section.append(f'- Return code: `{r.returncode}`')
		if r.stdout_excerpt:
			section.append('### stdout (excerpt)\n```text\n' + r.stdout_excerpt + '\n```')
		if r.stderr_excerpt:
			section.append('### stderr (excerpt)\n```text\n' + r.stderr_excerpt + '\n```')
		sections.append('\n'.join(section))

	return (
		'# Open-Source Scan Report\n\n'
		f'- Target: `{report.target}`\n'
		f'- Execute mode: `{report.execute}`\n\n'
		'| Tool | Status | Command | Reason | Return Code |\n'
		'|---|---|---|---|---|\n'
		f'{rows}\n\n'
		+ '\n\n'.join(sections)
		+ '\n'
	)


def main() -> None:
	"""CLI entrypoint."""
	request = _parse_args()
	commands = _tool_commands(request.target)
	results: list[ToolExecution] = []
	for tool in request.tools:
		if tool not in commands:
			results.append(
				ToolExecution(
					tool=tool,
					status='skipped',
					command='',
					reason='Unsupported tool profile',
				)
			)
			continue
		results.append(_run_one(tool, commands[tool], request.execute, request.timeout_seconds))

	report = ScanReport(target=request.target, execute=request.execute, results=results)
	output_path = request.output.resolve()
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(_render_markdown(report), encoding='utf-8')
	print(f'Wrote scan report to {output_path}')


if __name__ == '__main__':
	main()
