# 6. Usage

## Start an investigation
| Situation | Command |
|---|---|
| Have an incident number | `/analyze-incident INC0012345` |
| Know service + time | `/analyze-incident payments-api 2026-09-22T14:00Z` |
| Vague report, no INC | Select `incident-orchestrator`, describe symptoms, URLs, error codes, time |

## Run a single specialist
Select the agent in the dropdown and give service + UTC window:
```
payments-api, 2026-09-22T13:30Z to 2026-09-22T15:00Z
```
Useful for quick checks ("any deploys?", "any OOMs?").

## Give good input
The more clues, the faster scoping works:
- Exact error message or code
- URL or screen/feature name
- Transaction / correlation ID
- Start time with timezone
- What changed recently, if known

## Reading the report
```
## Incident INC0012345 — payments-api — RCA draft
Summary: ...
Onset: 14:05Z   Detected: 14:12Z
Most likely cause (confidence 0.8): release 1.8.3 lowered DB pool size
  Evidence: MR !482 diff; Hikari pool exhausted errors from 14:05; restarts after rev 42
  Confirm by: compare pool metrics before/after 14:03
Alternatives: core-banking-gateway latency (lower: no timeout errors)
Timeline: ...
Checked clean: nodes, HPA, Azure activity log
Suggested actions (approval required): roll back to 1.8.2
Gaps: no APM data
```
| Part | How to use it |
|---|---|
| Confidence | < 0.5 = lead, not conclusion |
| Evidence | Click through; verify the top items |
| Confirm by | Fastest way to prove or disprove |
| Checked clean | Rules out areas — saves time |
| Gaps | Data it couldn't see |

## After the investigation
1. Verify the cause.
2. If asked, approve posting the RCA draft as a ServiceNow work note.
3. Approve or edit the proposed notes-file MR.
4. Review any proposed service-map additions.

## Tips
- Ask follow-ups in the same chat: "check auth-service too", "extend window to 24h".
- If it picks the wrong service, tell it the right one; add the missing hint to service-map.
- Keep windows tight; wide windows cost more and add noise.
