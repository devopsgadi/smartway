---
name: findings-contract
description: Required output schema for every investigation agent's findings. Use whenever returning results to the orchestrator or the user.
---
# Findings Contract

Every specialist returns exactly this YAML (no raw dumps):

```yaml
source: gitlab | elastic | servicenow | k8s | azure
service: <service key from service-map>
window: { start: <UTC ISO>, end: <UTC ISO> }
findings:
  - ts: <UTC ISO>              # when it happened, not when observed
    type: change | error | anomaly | state
    summary: <one line, factual>
    evidence: <query | command | URL | record id>
    severity: high | medium | low
checked_clean: [<things checked with no issue>]   # negative evidence matters
confidence: <0.0-1.0>
next_checks:
  - <agent>: <specific follow-up>
```

## Type definitions
- **change**: deploy, config, infra, cert, secret, scaling change → highest signal
- **error**: failures, exceptions, crashes
- **anomaly**: deviation from baseline (rate, latency, volume)
- **state**: current condition (pending pods, degraded resource)
