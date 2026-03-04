#!/usr/bin/env python3
"""Generate a model assurance matrix markdown file."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import BaseModel, Field


class AttackCase(BaseModel):
	"""Single assurance case row."""

	attack_class: str
	scenario: str
	metric: str
	threshold: str


class AssuranceRequest(BaseModel):
	"""Input contract for assurance matrix generation."""

	cases: list[AttackCase] = Field(min_length=1)
	output: Path = Field(default=Path('model-assurance-matrix.md'))


DEFAULT_CASES = [
	AttackCase(attack_class='prompt injection', scenario='policy bypass attempt', metric='bypass rate', threshold='<= 1%'),
	AttackCase(attack_class='model extraction', scenario='iterative query scraping', metric='extraction success', threshold='<= 5%'),
	AttackCase(attack_class='evasion', scenario='adversarial perturbation', metric='accuracy drop', threshold='<= 10%'),
]


def _parse_cases(raw: str) -> list[AttackCase]:
	"""Parse case list from attack:scenario:metric:threshold entries."""
	if not raw.strip():
		return DEFAULT_CASES
	cases: list[AttackCase] = []
	for item in [part.strip() for part in raw.split(',') if part.strip()]:
		parts = [p.strip() for p in item.split(':')]
		if len(parts) < 4:
			raise ValueError(f'Invalid case: {item}. Expected attack:scenario:metric:threshold')
		cases.append(AttackCase(attack_class=parts[0], scenario=parts[1], metric=parts[2], threshold=parts[3]))
	return cases


def parse_args() -> AssuranceRequest:
	parser = argparse.ArgumentParser(description='Generate model assurance matrix markdown.')
	parser.add_argument('--cases', default='', help='Comma-separated attack:scenario:metric:threshold entries')
	parser.add_argument('--output', default='model-assurance-matrix.md')
	args = parser.parse_args()
	return AssuranceRequest(cases=_parse_cases(args.cases), output=Path(args.output).expanduser())


def render_markdown(req: AssuranceRequest) -> str:
	header = (
		'# Model Assurance Matrix\n\n'
		'| Attack Class | Scenario | Metric | Threshold | Result | Severity | Owner |\n'
		'|---|---|---|---|---|---|---|\n'
	)
	rows = '\n'.join(
		f'| {case.attack_class} | {case.scenario} | {case.metric} | {case.threshold} |  |  |  |'
		for case in req.cases
	)
	return f'{header}{rows}\n'


def main() -> None:
	req = parse_args()
	output_path = req.output.resolve()
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(render_markdown(req), encoding='utf-8')
	print(f'Wrote {len(req.cases)} assurance cases to {output_path}')


if __name__ == '__main__':
	main()
