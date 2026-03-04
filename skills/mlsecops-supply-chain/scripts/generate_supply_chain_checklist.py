#!/usr/bin/env python3
"""Generate a supply-chain hardening checklist markdown file."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import BaseModel, Field


class ChecklistRequest(BaseModel):
	"""Input contract for supply-chain checklist generation."""

	project_name: str = Field(min_length=1)
	package_manager: str = 'uv'
	ci_platform: str = 'github-actions'
	output: Path = Field(default=Path('supply-chain-checklist.md'))


def parse_args() -> ChecklistRequest:
	parser = argparse.ArgumentParser(description='Generate supply-chain checklist markdown.')
	parser.add_argument('--project-name', required=True)
	parser.add_argument('--package-manager', default='uv')
	parser.add_argument('--ci-platform', default='github-actions')
	parser.add_argument('--output', default='supply-chain-checklist.md')
	args = parser.parse_args()
	return ChecklistRequest(
		project_name=args.project_name.strip(),
		package_manager=args.package_manager.strip(),
		ci_platform=args.ci_platform.strip(),
		output=Path(args.output).expanduser(),
	)


def render_markdown(req: ChecklistRequest) -> str:
	return (
		f'# Supply Chain Checklist: {req.project_name}\n\n'
		f'- Package manager: `{req.package_manager}`\n'
		f'- CI platform: `{req.ci_platform}`\n\n'
		'- [ ] Dependency pinning and lockfile enforcement enabled\n'
		'- [ ] CVE scanning runs in CI and blocks critical findings\n'
		'- [ ] Model artifact scanning is mandatory before promotion\n'
		'- [ ] SBOM generation step exists for release artifacts\n'
		'- [ ] Artifact signing and verification checks are enforced\n'
		'- [ ] Secrets and credentials are short-lived and scoped\n'
	)


def main() -> None:
	req = parse_args()
	output_path = req.output.resolve()
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(render_markdown(req), encoding='utf-8')
	print(f'Wrote checklist to {output_path}')


if __name__ == '__main__':
	main()
