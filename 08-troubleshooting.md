# 8. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Can't see `.agents`, `.github` after unzip | Hidden dot-folders | Finder `Cmd+Shift+.`, or `ls -la`, or open in VS Code |
| Agents missing from dropdown | Not discovered | Open repo root in VS Code; check `.github/agents/*.agent.md`; reload window |
| `/skills` doesn't list skills | Skills disabled or wrong path | Enable Agent Skills; skills must be `.agents/skills/<name>/SKILL.md` |
| Agent says tool not available | Tool name mismatch or server down | Check `tools:` against tool picker; **MCP: List Servers** |
| MCP server fails to start | Command/env wrong, auth failure | Check output log; test credentials manually |
| "Service unmapped" | No service-map entry | Add entry ([Service onboarding](05-service-onboarding.md)) |
| Picks wrong service | Weak/missing discovery hints | Add aliases, url_paths, error_codes |
| Estate-wide sweep returns nothing | Inconsistent service field in Elastic | Standardize `service.name` or map per index in `elastic_global` |
| Wrong times in timeline | Timezone mismatch | Give times with timezone; verify system clocks/UTC |
| Too much log data / slow | Window too wide | Narrow window; rely on aggregation queries |
| Confident but wrong | Correlation mistaken for cause | Tune heuristics; add failure mode to notes file |
| Tries a mutating command | Tool exposes writes | Remove write tools from MCP server; enforce RBAC |
| ServiceNow post fails | No work-note permission | Grant or keep read-only and copy report manually |
