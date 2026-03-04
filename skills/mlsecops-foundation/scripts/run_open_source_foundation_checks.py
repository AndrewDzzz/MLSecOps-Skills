#!/usr/bin/env python3
"""Probe common open-source foundation tools used for MLSecOps threat modeling."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
from datetime import datetime, timezone
from pathlib import Path


TOOLS = [
	{
		"name": "threatdragon",
		"module": None,
		"command": "threatdragon",
		"package": None,
		"purpose": "Visual threat modeling workflows and DFD-based analysis.",
	},
	{
		"name": "pytm",
		"module": "threatmodels",
		"command": "tm.py",
		"package": "pytm",
		"purpose": "Pythonic architecture-to-model threat translation.",
	},
	{
		"name": "threagile",
		"module": None,
		"command": "threagile",
		"package": "threagile",
		"purpose": "YAML threat model engine and risk reporting.",
	},
	{
		"name": "threatspec",
		"module": "threatspec",
		"command": "threatspec",
		"package": "threatspec",
		"purpose": "Code-level repository threat specification and reports.",
	},
	{
		"name": "atlas",
		"module": None,
		"command": "python -c 'import json; print(\"atlas helper unavailable in std lib\")'",
		"package": "mitre-atlas",
		"purpose": "Threat ontology alignment reference for AI techniques.",
	},
]


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Smoke-check OSS foundation tools used for threat modeling."
	)
	parser.add_argument(
		"--tools",
		help="Comma-separated tool names to check. Omit for all registered tools.",
	)
	parser.add_argument(
		"--output",
		default="foundation-open-source-checks.json",
		help="Output JSON path",
	)
	parser.add_argument(
		"--fail-on-missing",
		action="store_true",
		help="Exit non-zero when any requested tool is missing.",
	)
	return parser.parse_args()


def _to_bool_path(value: str | None) -> bool:
	return bool(value and value.strip())


def is_command_available(command: str) -> bool:
	try:
		import shutil
		base = command.split()[0]
		return shutil.which(base) is not None
	except Exception:
		return False


def run_probe(tool: dict[str, str | None]) -> dict[str, str | bool | None]:
	mod = tool["module"]
	pkg = tool["package"]
	cmd = tool["command"]
	entry: dict[str, str | bool | None] = {
		"name": str(tool["name"]),
		"status": "missing",
		"purpose": str(tool["purpose"]),
		"version": None,
		"command_available": False,
		"error": None,
	}

	try:
		if mod:
			importlib.import_module(mod)
			entry["command_available"] = is_command_available(cmd) if cmd else False
			if pkg:
				try:
					entry["version"] = importlib.metadata.version(str(pkg))
				except Exception:
					entry["version"] = "unknown"
			else:
				entry["version"] = "module-only"
			entry["status"] = "present"
		elif cmd and is_command_available(cmd):
			entry["command_available"] = True
			entry["status"] = "present"
			try:
				entry["version"] = "available"
			except Exception:
				pass
		else:
			entry["status"] = "missing"
			entry["error"] = f"Module and command not found: {cmd or mod}"
	except Exception as exc:
		entry["error"] = str(exc)
		entry["status"] = "missing"
	return entry


def parse_tool_filter(raw: str | None) -> set[str]:
	if not raw:
		return {tool["name"] for tool in TOOLS}
	return {item.strip() for item in raw.split(",") if item.strip()}


def main() -> None:
	args = parse_args()
	enabled = parse_tool_filter(args.tools)
	selected = [tool for tool in TOOLS if tool["name"] in enabled]

	unknown_names = sorted(enabled - {tool["name"] for tool in selected})
	for unknown in unknown_names:
		print(f'Warning: unknown tool "{unknown}" is not in the foundation registry.')
	if not selected:
		print("No valid tools selected.")
		raise SystemExit(2)

	results = [run_probe(tool) for tool in selected]
	present = [result for result in results if result["status"] == "present"]
	missing = [result for result in results if result["status"] != "present"]

	report = {
		"generated_at": datetime.now(timezone.utc).isoformat(),
		"summary": {
			"requested": len(results),
			"present": len(present),
			"missing": len(missing),
		},
		"results": results,
	}

	output_path = Path(args.output).resolve()
	output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
	print(f"Checked {len(results)} tool probes. Present: {len(present)}. Missing: {len(missing)}.")
	print(f"Report written to: {output_path}")

	if args.fail_on_missing and missing:
		raise SystemExit(1)


if __name__ == "__main__":
	main()
