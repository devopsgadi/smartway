---
name: incident-correlation
description: Merge findings from all specialist agents into a single UTC timeline, rank root-cause hypotheses, and produce the RCA report. Use in the orchestrator after gathering evidence.
---
# Incident Correlation

## Procedure
1. Collect all `findings-contract` outputs. Normalize timestamps to UTC.
2. Establish **onset** (prefer elastic error onset; else incident opened_at).
3. Build timeline: all findings sorted by ts, marked relative to onset (T−12m, T+3m).
4. Generate hypotheses. Rank by:
   - `change` shortly before onset (0–30 min) > `anomaly` at onset > `error` > `state`
   - Corroboration across ≥2 sources raises confidence
   - Explains *all* symptoms > explains some
   - Contradicting evidence (checked_clean) lowers confidence
5. For top hypothesis, state what would **confirm** and what would **refute**.
6. Execute outstanding `next_checks` once if they could change the ranking.

## Report format
```
## Incident <INC> — <service> — RCA draft
**Summary**: <2 sentences>
**Onset**: <UTC>  **Detected**: <UTC>
**Most likely cause** (confidence X): <hypothesis>
  Evidence: <bullets with links>
  Confirm by: <check>
**Alternatives**: <ranked, with why lower>
**Timeline**: <table ts | source | event>
**Checked clean**: <list>
**Suggested actions** (require human approval): <rollback/scale/etc.>
**Gaps**: <data not available>
```
