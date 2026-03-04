#!/usr/bin/env python3
"""Generate a starter threat register markdown file."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import BaseModel, Field


class ThreatRow(BaseModel):
	"""One threat-register row."""

	asset: str
	vector: str


class ThreatRegisterRequest(BaseModel):
	"""Input contract for threat register generation."""

	assets: list[str] = Field(min_length=1)
	vectors: list[str] = Field(min_length=1)
	output: Path = Field(default=Path('threat-register.md'))


DEFAULT_VECTORS = [
	'poisoning',
	'prompt injection',
	'model extraction',
	'data exfiltration',
	'denial of service',
]


def _parse_csv(value: str) -> list[str]:
	return [item.strip() for item in value.split(',') if item.strip()]


def parse_args() -> ThreatRegisterRequest:
	parser = argparse.ArgumentParser(description='Generate threat register markdown.')
	parser.add_argument('--assets', required=True, help='Comma-separated assets')
	parser.add_argument('--vectors', default=','.join(DEFAULT_VECTORS), help='Comma-separated attack vectors')
	parser.add_argument('--output', default='threat-register.md')
	args = parser.parse_args()
	return ThreatRegisterRequest(
		assets=_parse_csv(args.assets),
		vectors=_parse_csv(args.vectors),
		output=Path(args.output).expanduser(),
	)


def render_markdown(rows: list[ThreatRow]) -> str:
	header = (
		'# Threat Register\n\n'
		'| Asset | Vector | Likelihood (1-5) | Impact (1-5) | Priority | Owner | Status |\n'
		'|---|---|---:|---:|---|---|---|\n'
	)
	body = '\n'.join(
		f'| {row.asset} | {row.vector} |  |  |  |  | open |'
		for row in rows
	)
	return f'{header}{body}\n'


def main() -> None:
	request = parse_args()
	rows = [ThreatRow(asset=a, vector=v) for a in request.assets for v in request.vectors]
	output_path = request.output.resolve()
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(render_markdown(rows), encoding='utf-8')
	print(f'Wrote {len(rows)} threat rows to {output_path}')


if __name__ == '__main__':
	main()
