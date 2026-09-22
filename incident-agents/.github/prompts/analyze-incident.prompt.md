---
description: Run RCA analysis for a ServiceNow incident or a service/time window
agent: incident-orchestrator
argument-hint: INC0012345 | <service> <start UTC> [end UTC]
---
Analyze incident: ${input:target:INC number or service + time}

Follow the incident-orchestrator flow. Produce the RCA draft. Do not post anywhere without confirmation.
