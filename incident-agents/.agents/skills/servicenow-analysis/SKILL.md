---
name: servicenow-analysis
description: Pull incident context, change requests, related incidents, and CMDB relationships from ServiceNow. Use at the start of an incident investigation and to find planned changes in a window.
---
# ServiceNow Analysis

## Procedure
1. **Incident**: number, short_description, priority, cmdb_ci, opened_at, assignment_group, work notes (redacted). Derive window if not given.
2. **Change requests**: `change_request` where cmdb_ci in (CI + dependencies) and planned/actual window overlaps incident window. Include state, type (standard/normal/emergency), implementer.
3. **Related incidents**: open/recent incidents on same CI or dependencies (last 7 days); same symptoms → possible duplicate or recurring.
4. **Problem records** linked to the CI (known errors).
5. **CMDB**: upstream/downstream relationships for the CI.

## Table API hints
- `incident?sysparm_query=number=<INC>`
- `change_request?sysparm_query=cmdb_ci=<sys_id>^start_date<=<end>^end_date>=<start>`
- `cmdb_rel_ci?sysparm_query=child=<sys_id>^ORparent=<sys_id>`

## Heuristics
- Change implemented in window on CI or dependency → high suspicion, flag even if "successful".
- Recurring incidents with same symptom → check linked problem / prior RCA.

## Write-back
Only when user asks: post orchestrator report as a **work note** (never close, reassign, or change state).

## Output
`findings-contract`, source: servicenow.
