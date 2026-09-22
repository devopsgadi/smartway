# AGENTS.md — Incident Analysis Agents

## Purpose
Read-only, evidence-based root-cause analysis across GitLab, Kibana/Elastic, ServiceNow, Kubernetes, and Azure.

## Layers
- **Tools**: MCP servers in `.vscode/mcp.json` (read-only credentials only).
- **Skills**: `.agents/skills/*/SKILL.md` — how to investigate each system.
- **Agents**: `.github/agents/*.agent.md` — role + skills + tool scope.
- **Entry point**: `/analyze-incident` prompt or the `incident-orchestrator` agent.

## Hard rules (all agents)
1. READ-ONLY. Never run mutating commands (apply, delete, rollout undo, scale, restart, merge, update records) — propose them instead.
2. Exception: ServiceNow work notes, only when the user explicitly asks to post.
3. All timestamps in UTC. Normalize before comparing.
4. If the service is unknown or ambiguous, run `incident-scoping` first. Resolve every service through the `service-map` skill first (if unmapped, stop and ask), then load its `service-knowledge` file.
5. Every claim needs evidence (query, command, URL, record number). No evidence → label as hypothesis.
6. Run `log-redaction` rules on any log/record text before reasoning or output.
7. Aggregate before reading raw data: counts, top-N, deltas. Pull raw lines only for specific failing entities.
8. Return findings in the `findings-contract` shape.
9. Correlation ≠ causation. State confidence and what would confirm/refute.

## Default window
Incident start − 2h → now, unless given.
