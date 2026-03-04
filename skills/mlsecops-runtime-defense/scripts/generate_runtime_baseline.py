#!/usr/bin/env python3
"""Generate a runtime defense baseline markdown file."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import BaseModel, Field


class RuntimeRequest(BaseModel):
	"""Input contract for runtime baseline generation."""

	service_name: str = Field(min_length=1)
	auth_mode: str = 'oidc'
	tenancy: str = 'single-tenant'
	output: Path = Field(default=Path('runtime-defense-baseline.md'))


def parse_args() -> RuntimeRequest:
	parser = argparse.ArgumentParser(description='Generate runtime defense baseline markdown.')
	parser.add_argument('--service-name', required=True)
	parser.add_argument('--auth-mode', default='oidc')
	parser.add_argument('--tenancy', default='single-tenant')
	parser.add_argument('--output', default='runtime-defense-baseline.md')
	args = parser.parse_args()
	return RuntimeRequest(
		service_name=args.service_name.strip(),
		auth_mode=args.auth_mode.strip(),
		tenancy=args.tenancy.strip(),
		output=Path(args.output).expanduser(),
	)


def render_markdown(req: RuntimeRequest) -> str:
	return (
		f'# Runtime Defense Baseline: {req.service_name}\n\n'
		f'- Auth mode: `{req.auth_mode}`\n'
		f'- Tenancy: `{req.tenancy}`\n\n'
		'| Control Area | Requirement | Status | Owner |\n'
		'|---|---|---|---|\n'
		'| AuthN/AuthZ | Enforce tenant-scoped authorization |  |  |\n'
		'| Input validation | Validate and sanitize all request fields |  |  |\n'
		'| Throttling | Per-tenant and per-IP rate controls |  |  |\n'
		'| Containment | Least privilege runtime and network policy |  |  |\n'
		'| Fail-safe | Fail closed on policy and integrity failures |  |  |\n'
	)


def main() -> None:
	req = parse_args()
	output_path = req.output.resolve()
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(render_markdown(req), encoding='utf-8')
	print(f'Wrote runtime baseline to {output_path}')


if __name__ == '__main__':
	main()
