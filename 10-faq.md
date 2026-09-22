# 10. FAQ

**Does it change anything in production?**
No. Access is read-only; the only possible write is a ServiceNow work note you approve.

**Why `.github/` if we use GitLab?**
It's where VS Code Copilot reads config locally. The host doesn't matter.

**What if the ticket doesn't say which app?**
`incident-scoping` finds it from clues: transaction IDs, URLs, error codes, error spikes, recent changes.

**Why one skill for all services instead of a skill per service?**
Every skill's description is loaded for selection; dozens of similar ones cause wrong picks. One skill loads only the relevant service file.

**How accurate is it?**
As good as the service map, notes files, and log consistency. Measure with a replay set before going live.

**Can it run automatically?**
Yes, later — via GitLab CI with a headless agent runtime using the same skills ([Extending](09-extending.md)).

**What data goes to the model?**
Aggregated results and redacted log excerpts. Confirm against your data-handling policy.

**Who maintains it?**
Platform team owns skills/agents; service owners own their service-map entry and notes file via MR review.
