#!/usr/bin/env python3
"""Generate a data control matrix markdown file."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import BaseModel, Field


class DataSource(BaseModel):
	"""A single data source entry."""

	name: str
	sensitivity: str


class MatrixRequest(BaseModel):
	"""Input contract for matrix generation."""

	sources: list[DataSource] = Field(min_length=1)
	output: Path = Field(default=Path('data-control-matrix.md'))


def _parse_sources(value: str) -> list[DataSource]:
	"""Parse source list from name:sensitivity pairs."""
	result: list[DataSource] = []
	for item in [part.strip() for part in value.split(',') if part.strip()]:
		name, sensitivity = (item.split(':', 1) + ['medium'])[:2]
		result.append(DataSource(name=name.strip(), sensitivity=sensitivity.strip() or 'medium'))
	return result


def parse_args() -> MatrixRequest:
	parser = argparse.ArgumentParser(description='Generate data protection control matrix.')
	parser.add_argument('--sources', required=True, help='Comma-separated name:sensitivity pairs')
	parser.add_argument('--output', default='data-control-matrix.md')
	args = parser.parse_args()
	return MatrixRequest(sources=_parse_sources(args.sources), output=Path(args.output).expanduser())


def render_markdown(req: MatrixRequest) -> str:
	header = (
		'# Data Control Matrix\n\n'
		'| Data Source | Sensitivity | Provenance Control | Access Control | Retention Rule | Poisoning Check | Privacy Control |\n'
		'|---|---|---|---|---|---|---|\n'
	)
	rows = '\n'.join(
		f'| {src.name} | {src.sensitivity} | immutable snapshots + hash | RBAC + audit | define policy | anomaly gate | define strategy |'
		for src in req.sources
	)
	return f'{header}{rows}\n'


def main() -> None:
	req = parse_args()
	output_path = req.output.resolve()
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(render_markdown(req), encoding='utf-8')
	print(f'Wrote control matrix for {len(req.sources)} data sources to {output_path}')


if __name__ == '__main__':
	main()
