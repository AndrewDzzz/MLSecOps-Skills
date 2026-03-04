#!/usr/bin/env python3
"""Probe MCP endpoints with zero external Python dependencies."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


def _parse_kv_pairs(raw: str) -> dict[str, str]:
    if not raw.strip():
        return {}
    parsed: dict[str, str] = {}
    for item in [part.strip() for part in raw.split(",") if part.strip()]:
        if "=" not in item:
            raise ValueError(f"Invalid env entry: {item}. Expected key=value.")
        key, value = item.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe MCP server connectivity and capture diagnostics.")
    parser.add_argument("--transport", choices=["stdio", "sse", "streamable-http"], default="stdio")
    parser.add_argument("--command", default=None, help="Required for stdio transport")
    parser.add_argument("--arg", action="append", default=[], help="Repeatable stdio arg (recommended)")
    parser.add_argument("--args", default="", help="Comma-separated stdio args (legacy)")
    parser.add_argument("--url", default=None, help="Required for sse/streamable-http transport")
    parser.add_argument("--env", default="", help="Comma-separated key=value pairs for stdio transport")
    parser.add_argument(
        "--call-tool",
        default=None,
        help="Optional tool name to record in output as the intended follow-up action.",
    )
    parser.add_argument(
        "--call-arguments",
        default="{}",
        help="JSON object of intended tool arguments; stored in output for manual replay.",
    )
    parser.add_argument("--timeout", type=int, default=20, help="Probe timeout in seconds")
    parser.add_argument("--output", default="mcp-probe.json", help="Output JSON path")
    args = parser.parse_args()

    try:
        call_arguments = json.loads(args.call_arguments)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid --call-arguments JSON: {exc}") from exc
    if not isinstance(call_arguments, dict):
        raise ValueError("--call-arguments must be a JSON object")

    args.call_arguments = call_arguments
    args.env = _parse_kv_pairs(args.env)
    args.args = [item.strip() for item in args.args.split(",") if item.strip()]
    args.argv = [*args.arg, *args.args]
    return args


def _probe_stdio(args: argparse.Namespace) -> dict[str, object]:
    if not args.command:
        raise ValueError("--command is required for stdio transport")

    command = [args.command, *args.argv]
    env = {**os.environ, **args.env}

    try:
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=args.timeout,
            env=env,
        )
        return {
            "status": "ok" if proc.returncode == 0 else "error",
            "target": args.command,
            "command": command,
            "return_code": proc.returncode,
            "stdout_preview": proc.stdout[:4000],
            "stderr_preview": proc.stderr[:4000],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timeout",
            "target": args.command,
            "command": command,
            "return_code": None,
            "stdout_preview": (exc.stdout or "")[:4000],
            "stderr_preview": (exc.stderr or "")[:4000],
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "target": args.command,
            "command": command,
            "return_code": None,
            "stdout_preview": "",
            "stderr_preview": f"Command not found: {args.command}",
        }


def _probe_http(args: argparse.Namespace) -> dict[str, object]:
    if not args.url:
        raise ValueError("--url is required for sse/streamable-http transport")

    request = urllib.request.Request(
        args.url,
        method="GET",
        headers={"Accept": "text/event-stream, application/json, */*"},
    )
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            body = response.read(4096).decode("utf-8", errors="replace")
            return {
                "status": "ok",
                "target": args.url,
                "http_status": getattr(response, "status", None),
                "body_preview": body,
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(4096).decode("utf-8", errors="replace")
        return {
            "status": "error",
            "target": args.url,
            "http_status": exc.code,
            "body_preview": body,
        }
    except urllib.error.URLError as exc:
        return {
            "status": "error",
            "target": args.url,
            "http_status": None,
            "body_preview": str(exc.reason),
        }


def main() -> None:
    try:
        args = _parse_args()
    except ValueError as exc:
        raise SystemExit(f"Input error: {exc}") from exc

    if args.transport == "stdio":
        probe = _probe_stdio(args)
    else:
        probe = _probe_http(args)

    result = {
        "transport": args.transport,
        "probe": probe,
        "requested_tool_call": {
            "tool": args.call_tool,
            "arguments": args.call_arguments,
        }
        if args.call_tool
        else None,
        "note": (
            "This lightweight probe validates connectivity and captures diagnostics. "
            "If an MCP Python client is installed, replace with a full MCP session probe."
        ),
    }

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote MCP probe result to {output_path}")


if __name__ == "__main__":
    main()
