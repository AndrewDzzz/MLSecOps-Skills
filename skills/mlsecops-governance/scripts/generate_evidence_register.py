#!/usr/bin/env python3
"""Generate governance evidence register markdown."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import BaseModel, Field


class EvidenceRequest(BaseModel):
	"""Input contract for evidence register generation."""

	frameworks: list[str] = Field(min_length=1)
	output: Path = Field(default=Path('evidence-register.md'))


def _parse_csv(value: str) -> list[str]:
	return [item.strip() for item in value.split(',') if item.strip()]


def parse_args() -> EvidenceRequest:
	parser = argparse.ArgumentParser(description='Generate evidence register markdown.')
	parser.add_argument('--frameworks', required=True, help='Comma-separated frameworks')
	parser.add_argument('--output', default='evidence-register.md')
	args = parser.parse_args()
	return EvidenceRequest(frameworks=_parse_csv(args.frameworks), output=Path(args.output).expanduser())


def render_markdown(req: EvidenceRequest) -> str:
	header = (
		'# Evidence Register\n\n'
		'| Control ID | Framework | Evidence Artifact | Owner | Frequency | Last Updated | Status |\n'
		'|---|---|---|---|---|---|---|\n'
	)
	rows = '\n'.join(
		f'| GOV-{index:03d} | {fw} | define artifact |  | define cadence |  | open |'
		for index, fw in enumerate(req.frameworks, start=1)
	)
	return f'{header}{rows}\n'


def main() -> None:
	req = parse_args()
	output_path = req.output.resolve()
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(render_markdown(req), encoding='utf-8')
	print(f'Wrote evidence register with {len(req.frameworks)} frameworks to {output_path}')


if __name__ == '__main__':
	main()
