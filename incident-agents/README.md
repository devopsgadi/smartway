# Incident Analysis Agents

Full documentation: [docs/README.md](docs/README.md)


1. Fill `.vscode/mcp.json` with your MCP server commands (read-only creds).
2. Populate `.agents/skills/service-map/service-map.yaml`.
3. Confirm Agent Skills + subagents are enabled in VS Code settings; verify tool names in the agent tool picker (`tools:` frontmatter).
4. Open Copilot Chat → select `incident-orchestrator` or run `/analyze-incident INC0012345`.
5. Test each investigator standalone first, then the orchestrator.
6. Build an eval set: 10–20 past incidents with known RCA; replay and tune skill heuristics.

## Layout
- `.agents/skills/` — portable Agent Skills (auto-discovered by VS Code; reusable by other agent runtimes, e.g. from GitLab CI)
- `.github/agents/`, `.github/prompts/` — VS Code Copilot config paths (naming convention only; works on GitLab-hosted repos)
- `.agents/skills/service-knowledge/services/<service>.md` — per-service knowledge (failure modes, baselines, queries, past incidents). Scaffold with `/new-service <key>`.
- `scripts/gen_ingress_map.py` — generate url_paths/hosts hints from Istio VirtualServices.
- `incident-scoping` skill — finds the affected service when INC lacks CI/service info.
