# 9. Extending

## Add a skill
1. Create `.agents/skills/<name>/SKILL.md`:
```markdown
---
name: <name>
description: <what it does + when to use it — specific, this drives discovery>
---
# <Title>
## Inputs
## Procedure
## Heuristics
## Output
Conform to findings-contract.
```
2. Add scripts/queries/examples in the same folder if needed.
3. Reference it in the relevant agent's "Use skills".

Keep descriptions specific; every skill's description is loaded to decide which to use.

## Add an agent
Create `.github/agents/<name>.agent.md`:
```markdown
---
name: <name>
description: <role>
tools: ['<server>/*', 'read']
---
Follow AGENTS.md hard rules.
Use skills: service-map, service-knowledge, <module-skill>, findings-contract.
Input: service + UTC window. Return only findings-contract YAML.
```
Add it to the orchestrator's `agents:` list and flow.

Candidates: `nginx-investigator` (NGINX Plus API/logs), `database-investigator`, `apm-investigator`.

## Add a service
See [Service onboarding](05-service-onboarding.md).

## Automate (beyond VS Code)
Skills are portable (`SKILL.md` open format). To run without a person at the keyboard:
1. ServiceNow webhook on P1/P2 → GitLab pipeline trigger.
2. GitLab CI job runs a headless agent runtime with the same skills and read-only credentials.
3. Job posts RCA draft as a work note (or to Slack/Teams) for human review.

## Roadmap
| Phase | Scope |
|---|---|
| 1 | Manual, VS Code, 1–2 services, read-only |
| 2 | All tier-1 services; replay evaluation set |
| 3 | Auto-trigger via GitLab CI on P1/P2 |
| 4 | RAG over past RCAs and runbooks |
| 5 | Proposed remediation (rollback MR, etc.) with approval |

## Evaluation
Keep a set of past incidents with known RCAs. After changing skills, replay them and track:
- Correct top hypothesis (%)
- Correct service identified (%)
- Time to draft
