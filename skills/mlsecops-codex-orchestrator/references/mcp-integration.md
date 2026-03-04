# MCP Integration Notes

Use MCP when you want the skill to access external systems through typed tools.

## Recommended MCP Servers

- GitHub official MCP server (`ghcr.io/github/github-mcp-server`) for repository, issue, PR, and workflow operations.
- MCP reference servers from `modelcontextprotocol/servers` for `filesystem`, `fetch`, `git`, `memory`, `time`, and `sequentialthinking`.
- MCP registry (`registry.modelcontextprotocol.io`) for production-grade community servers.
- SafeDep `vet` MCP server for package-risk vetting before dependency installation.
- Internal security MCP servers for SIEM, vuln databases, ticketing, and evidence APIs.

## Probe Before Usage

Always probe connectivity before using a tool:

```bash
python skills/mlsecops-codex-orchestrator/scripts/mcp_tool_probe.py \
  --transport stdio \
  --command docker \
  --arg run \
  --arg -i \
  --arg --rm \
  --arg -e \
  --arg GITHUB_PERSONAL_ACCESS_TOKEN \
  --arg ghcr.io/github/github-mcp-server \
  --env "GITHUB_PERSONAL_ACCESS_TOKEN=${GITHUB_PERSONAL_ACCESS_TOKEN}" \
  --output mcp-probe.json
```

SafeDep vet MCP probe example:

```bash
python skills/mlsecops-codex-orchestrator/scripts/mcp_tool_probe.py \
  --transport stdio \
  --command vet \
  --arg server \
  --arg mcp \
  --arg --server-type \
  --arg stdio \
  --output vet-mcp-probe.json
```

## Safety Rules

1. Use least privilege credentials/tokens for MCP servers.
2. Keep intended `call_tool` arguments explicit and validated in your probe metadata.
3. Persist probe output for audit and reproducibility.
