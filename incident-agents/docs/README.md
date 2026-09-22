# Incident Analysis Agents — Documentation

AI agents that investigate production incidents across **GitLab, Kibana/Elastic, ServiceNow, Kubernetes, and Azure** and produce an evidence-backed root-cause (RCA) draft. They run in **VS Code with GitHub Copilot**; the repo lives in **GitLab**.

| # | Document | Read when |
|---|---|---|
| 1 | [Overview](01-overview.md) | You're new — what it is and why |
| 2 | [How it works](02-how-it-works.md) | You want the plain-language walkthrough |
| 3 | [Architecture](03-architecture.md) | You need the layers, agents, skills, and data flow |
| 4 | [Setup](04-setup.md) | You're installing it |
| 5 | [Service onboarding](05-service-onboarding.md) | You're adding a service |
| 6 | [Usage](06-usage.md) | You're running an investigation |
| 7 | [Guardrails & security](07-guardrails-security.md) | You're reviewing access and risk |
| 8 | [Troubleshooting](08-troubleshooting.md) | Something isn't working |
| 9 | [Extending](09-extending.md) | You're adding skills, agents, or automation |
| 10 | [FAQ](10-faq.md) | Quick answers |

## Quick start
1. Clone the repo and open in VS Code.
2. Fill `.vscode/mcp.json` with read-only MCP servers ([Setup](04-setup.md)).
3. Add one service to `service-map.yaml` ([Service onboarding](05-service-onboarding.md)).
4. Run `/analyze-incident INC0012345` in Copilot Chat ([Usage](06-usage.md)).
