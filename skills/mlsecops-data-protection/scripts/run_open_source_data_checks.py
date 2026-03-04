#!/usr/bin/env python3
"""Run lightweight smoke checks for common OSS data-protection libraries."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
from datetime import datetime, timezone
from pathlib import Path


TOOLS = [
	{
		"name": "great_expectations",
		"module": "great_expectations",
		"package": "great-expectations",
		"purpose": "Data quality and expectation-based assertions",
	},
	{
		"name": "deepchecks",
		"module": "deepchecks",
		"package": "deepchecks",
		"purpose": "Leakage, integrity, and data quality tests",
	},
	{
		"name": "tensorflow_data_validation",
		"module": "tensorflow_data_validation",
		"package": "tensorflow-data-validation",
		"purpose": "Schema validation and drift checks",
	},
	{
		"name": "whylogs",
		"module": "whylogs",
		"package": "whylogs",
		"purpose": "Data profiling and baseline drift tracking",
	},
	{
		"name": "evidently",
		"module": "evidently",
		"package": "evidently",
		"purpose": "Distribution and drift diagnostics",
	},
	{
		"name": "pandera",
		"module": "pandera",
		"package": "pandera",
		"purpose": "Typed dataframe constraints",
	},
	{
		"name": "presidio_analyzer",
		"module": "presidio_analyzer",
		"package": "presidio-analyzer",
		"purpose": "PII detection and text anonymization support",
	},
	{
		"name": "opendp",
		"module": "opendp",
		"package": "opendp",
		"purpose": "Differential privacy primitives",
	},
	{
		"name": "opacus",
		"module": "opacus",
		"package": "opacus",
		"purpose": "PyTorch differential-privacy training",
	},
	{
		"name": "tensorflow_privacy",
		"module": "tensorflow_privacy",
		"package": "tensorflow-privacy",
		"purpose": "TensorFlow differential-privacy training",
	},
	{
		"name": "ml_privacy_meter",
		"module": "ml_privacy_meter",
		"package": "ml_privacy_meter",
		"purpose": "Membership-inference and leakage risk checks",
	},
]


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Smoke-check OSS data-protection tooling.")
	parser.add_argument(
		"--tools",
		help="Comma-separated list of tool names (defaults to all known tools).",
	)
	parser.add_argument("--output", default="data-protection-open-source-checks.json", help="Output JSON path")
	parser.add_argument(
		"--fail-on-missing",
		action="store_true",
		help="Exit non-zero if any requested tool is missing.",
	)
	return parser.parse_args()


def run_probe(tool: dict[str, str]) -> dict[str, str | None]:
	try:
		importlib.import_module(tool["module"])
		version = "unknown"
		try:
			version = importlib.metadata.version(tool["package"])
		except Exception:
			pass
		return {"name": tool["name"], "status": "present", "version": version, "purpose": tool["purpose"], "error": None}
	except Exception as exc:
		return {
			"name": tool["name"],
			"status": "missing",
			"version": None,
			"purpose": tool["purpose"],
			"error": str(exc),
		}


def parse_tool_filter(value: str | None) -> set[str]:
	if not value:
		return {tool["name"] for tool in TOOLS}
	return {item.strip() for item in value.split(",") if item.strip()}


def main() -> None:
	args = parse_args()
	enabled = parse_tool_filter(args.tools)
	selected = [tool for tool in TOOLS if tool["name"] in enabled]
	missing_names = sorted(enabled - {tool["name"] for tool in selected})
	if missing_names:
		for name in missing_names:
			print(f'Warning: requested tool "{name}" is not in registry.')
	if not selected:
		print("No valid tools selected.")
		raise SystemExit(2)

	results = [run_probe(tool) for tool in selected]
	present = [r for r in results if r["status"] == "present"]
	missing = [r for r in results if r["status"] != "present"]

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

	print(f'Checked {len(results)} tools: {len(present)} present, {len(missing)} missing.')
	print(f'Report written to: {output_path}')

	if args.fail_on_missing and missing:
		raise SystemExit(1)


if __name__ == "__main__":
	main()
