# 4. Setup

Estimated time: 1–2 days for the first service, then ~1 hour per additional service.

## Prerequisites
- VS Code (recent) with GitHub Copilot Chat, agent mode enabled
- Python 3 (for scripts)
- Network access from your workstation to GitLab, Elastic, ServiceNow, Kubernetes API, Azure

## Step 1 — Put the files in a GitLab repo
Unzip and push to a repo such as `platform/incident-agents`. Keep the dot-folders `.agents`, `.github`, `.vscode` (Finder hides them: `Cmd+Shift+.`).

## Step 2 — Get read-only access
| System | Access | Notes |
|---|---|---|
| GitLab | Project/group token, `read_api` | Scope to relevant groups |
| Elastic | API key, read on `logs-*` | Include NGINX and Istio indices |
| ServiceNow | Read user on incident, change_request, problem, cmdb tables | + work notes write if allowed |
| Kubernetes | ServiceAccount + ClusterRole get/list/watch | Separate kubeconfig, e.g. `~/.kube/readonly-config` |
| Azure | Service principal, Reader | On prod subscriptions |

Example read-only ClusterRole (Secrets deliberately excluded):
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata: { name: incident-agent-readonly }
rules:
  - apiGroups: [""]
    resources: [pods, pods/log, events, services, endpoints, configmaps, nodes, namespaces, resourcequotas]
    verbs: [get, list, watch]
  - apiGroups: [apps]
    resources: [deployments, replicasets, statefulsets, daemonsets]
    verbs: [get, list, watch]
  - apiGroups: [autoscaling]
    resources: [horizontalpodautoscalers]
    verbs: [get, list, watch]
  - apiGroups: [metrics.k8s.io]
    resources: [pods, nodes]
    verbs: [get, list]
  - apiGroups: [networking.istio.io]
    resources: [virtualservices, destinationrules, gateways]
    verbs: [get, list, watch]
```

## Step 3 — Connect the tools (MCP)
Edit `.vscode/mcp.json`; replace each `REPLACE_ME` with the MCP server start command.
- GitLab, Kubernetes, Elastic, Azure: use available MCP servers.
- ServiceNow: likely a small wrapper over the REST Table API (read + work note only).

Verify in VS Code: **MCP: List Servers** → all running.

## Step 4 — Confirm Copilot sees everything
- Copilot Chat → agent dropdown → `incident-orchestrator` + five investigators listed.
- Type `/skills` → all skills listed.
- If missing: enable Agent Skills and subagents in VS Code settings; confirm tool names in each agent's `tools:` match the tool picker.

## Step 5 — Fill the service map
Add one service to `.agents/skills/service-map/service-map.yaml` ([Service onboarding](05-service-onboarding.md)).

## Step 6 — Verify log consistency
In Kibana, confirm every index has the same service field (e.g. `service.name`) and namespace field. If not: ingest pipeline, or record per-index fields in `elastic_global`.

## Step 7 — Write the service notes file
`/new-service payments-api`, then fill Known failure modes from recent incidents.

## Step 8 — Test each specialist
Pick an incident with a known cause. Select `kibana-investigator` → give service + UTC window → check evidence. Repeat for `k8s-investigator`, `gitlab-investigator`.

## Step 9 — Test end to end
`/analyze-incident <old INC>` → compare to the real RCA.

## Step 10 — Tune and expand
Fix wrong conclusions by adjusting the skill heuristics or notes file. Replay 10–20 incidents. Add services one at a time. Go live when old incidents are reliably right.

## Setup checklist
- [ ] Repo in GitLab with dot-folders
- [ ] Read-only credentials for all five systems
- [ ] MCP servers running
- [ ] Agents and skills visible in Copilot
- [ ] First service in service-map.yaml
- [ ] Log fields consistent
- [ ] First service notes file
- [ ] Specialists tested individually
- [ ] End-to-end test on past incident
- [ ] 10–20 incident replay passed
