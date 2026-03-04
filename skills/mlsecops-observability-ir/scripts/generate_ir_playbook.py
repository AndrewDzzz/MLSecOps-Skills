#!/usr/bin/env python3
"""Generate an incident response playbook markdown template."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import BaseModel, Field


class PlaybookRequest(BaseModel):
	"""Input contract for IR playbook generation."""

	service_name: str = Field(min_length=1)
	incident_type: str = Field(min_length=1)
	output: Path = Field(default=Path('incident-playbook.md'))


def parse_args() -> PlaybookRequest:
	parser = argparse.ArgumentParser(description='Generate incident response playbook markdown.')
	parser.add_argument('--service-name', required=True)
	parser.add_argument('--incident-type', required=True)
	parser.add_argument('--output', default='incident-playbook.md')
	args = parser.parse_args()
	return PlaybookRequest(
		service_name=args.service_name.strip(),
		incident_type=args.incident_type.strip(),
		output=Path(args.output).expanduser(),
	)


def render_markdown(req: PlaybookRequest) -> str:
	return (
		f'# Incident Playbook: {req.service_name}\n\n'
		f'- Incident type: `{req.incident_type}`\n\n'
		'## Detection\n'
		'- Trigger rule: \n'
		'- Alert severity: \n'
		'- Initial hypothesis: \n\n'
		'## Triage\n'
		'- Confirm indicators: \n'
		'- Scope and blast radius: \n'
		'- Escalation owner: \n\n'
		'## Containment\n'
		'- Throttle or deny actions: \n'
		'- Rollback or kill-switch action: \n\n'
		'## Recovery\n'
		'- Service restore criteria: \n'
		'- Post-incident validation: \n\n'
		'## Postmortem\n'
		'- Root cause: \n'
		'- Preventive action: \n'
		'- Due date and owner: \n'
	)


def main() -> None:
	req = parse_args()
	output_path = req.output.resolve()
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(render_markdown(req), encoding='utf-8')
	print(f'Wrote IR playbook to {output_path}')


if __name__ == '__main__':
	main()
