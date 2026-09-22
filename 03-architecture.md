# 3. Architecture

## Layers
| Layer | Location | Role |
|---|---|---|
| Rules | `AGENTS.md` | Hard rules for all agents |
| Tools | `.vscode/mcp.json` | MCP servers giving read-only access to each system |
| Skills | `.agents/skills/<name>/SKILL.md` | Investigation know-how: procedures, queries, heuristics |
| Agents | `.github/agents/*.agent.md` | Role + skills + allowed tools |
| Entry points | `.github/prompts/*.prompt.md` | `/analyze-incident`, `/new-service` |
| Scripts | `scripts/` | Helpers (e.g. ingress map generator) |

**Tools** = access. **Skills** = know-how. **Agents** = who uses which know-how with which access.

> `.github/` is simply where VS Code Copilot reads config from your local checkout. It works identically on a GitLab-hosted repo.

## Repo layout
```
incident-agents/
├── AGENTS.md
├── README.md
├── docs/
├── scripts/gen_ingress_map.py
├── .vscode/mcp.json
├── .github/
│   ├── agents/
│   │   ├── incident-orchestrator.agent.md
│   │   ├── servicenow-investigator.agent.md
│   │   ├── kibana-investigator.agent.md
│   │   ├── k8s-investigator.agent.md
│   │   ├── gitlab-investigator.agent.md
│   │   └── azure-investigator.agent.md
│   └── prompts/
│       ├── analyze-incident.prompt.md
│       └── new-service.prompt.md
└── .agents/skills/
    ├── service-map/            (SKILL.md, service-map.yaml)
    ├── service-knowledge/      (SKILL.md, services/*.md)
    ├── incident-scoping/
    ├── findings-contract/
    ├── log-redaction/
    ├── gitlab-analysis/
    ├── kibana-analysis/
    ├── servicenow-analysis/
    ├── k8s-triage/
    ├── azure-diagnostics/
    └── incident-correlation/
```

## Skills
| Skill | Type | Purpose |
|---|---|---|
| `service-map` | Shared | Resolve service / CI / URL / error code → identifiers in every system |
| `service-knowledge` | Shared | Per-service notes: failure modes, baselines, queries, past incidents |
| `incident-scoping` | Shared | Find the affected service when the ticket is vague |
| `findings-contract` | Shared | Common output schema |
| `log-redaction` | Shared | Scrub PII, secrets, customer data |
| `servicenow-analysis` | Module | Incident, changes, related incidents, CMDB |
| `kibana-analysis` | Module | Error rate, onset, new signatures, traces (targeted + discovery modes) |
| `k8s-triage` | Module | Rollouts, events, restarts, OOM, HPA, nodes, Istio |
| `gitlab-analysis` | Module | Deploys, MRs, Helm/value changes, failed pipelines |
| `azure-diagnostics` | Module | Activity log, resource/service health, AKS, Key Vault, KQL |
| `incident-correlation` | Orchestrator | Timeline, hypothesis ranking, RCA report |

## Agents
| Agent | Skills | Tools |
|---|---|---|
| `incident-orchestrator` | incident-scoping, service-map, service-knowledge, servicenow-analysis, incident-correlation, findings-contract | subagents, servicenow |
| `servicenow-investigator` | service-map, service-knowledge, servicenow-analysis, log-redaction, findings-contract | servicenow |
| `kibana-investigator` | incident-scoping, service-map, service-knowledge, kibana-analysis, log-redaction, findings-contract | elastic |
| `k8s-investigator` | service-map, service-knowledge, k8s-triage, log-redaction, findings-contract | kubernetes |
| `gitlab-investigator` | service-map, service-knowledge, gitlab-analysis, findings-contract | gitlab |
| `azure-investigator` | service-map, service-knowledge, azure-diagnostics, findings-contract | azure |

## Orchestrator flow
1. Get incident context from ServiceNow (if INC given).
2. Resolve service via `service-map`; if unknown/ambiguous → `incident-scoping`.
3. Load `service-knowledge` file; check known failure modes first.
4. Run kibana, k8s, gitlab investigators in parallel.
5. Add azure if multiple services, node/network/TLS symptoms, or no app cause found.
6. One round of high-value follow-up checks.
7. Correlate → RCA draft.
8. Ask before posting to ServiceNow.
9. Propose service-map additions for unmatched clues.
10. After human confirmation, propose notes-file update via MR.

## Findings contract
Every specialist returns:
```yaml
source: gitlab | elastic | servicenow | k8s | azure
service: payments-api
window: { start: 2026-09-22T13:00:00Z, end: 2026-09-22T15:00:00Z }
findings:
  - ts: 2026-09-22T14:03:11Z
    type: change            # change | error | anomaly | state
    summary: "Rollout rev 41→42 (image 1.8.3)"
    evidence: "kubectl rollout history deploy/payments-api -n payments"
    severity: high
checked_clean: ["no node pressure", "HPA below max"]
confidence: 0.8
next_checks:
  - gitlab: "diff for 1.8.3"
```

## Data sources
| System | Data used | Access |
|---|---|---|
| ServiceNow | incident, change_request, problem, cmdb_rel_ci | Table API, read (+ work notes) |
| Elastic | app, NGINX, Istio log indices | ES\|QL / DSL, read |
| Kubernetes | deployments, pods, events, HPA, nodes, Istio CRDs | get/list/watch |
| GitLab | pipelines, jobs, MRs, commits, diffs | `read_api` |
| Azure | Activity Log, Resource/Service Health, AKS, Log Analytics | Reader |
