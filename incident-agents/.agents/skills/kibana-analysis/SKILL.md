---
name: kibana-analysis
description: Analyze application logs in Elastic/Kibana for error spikes, new exception signatures, and latency changes around an incident. Use when an incident involves errors, failures, or degraded responses.
---
# Kibana / Elastic Analysis

## Inputs
service (elastic.index, service_field, service_value), window, baseline = same-length window before start (and same time yesterday if available)

## Modes
- **Targeted** (service known): procedure below.
- **Discovery** (service unknown): run Steps 3–5 of `incident-scoping` against global indices from `service-map.yaml` → `elastic_global`, return candidate services, not findings.

## Procedure
1. **Error rate**: count of `log.level: error` (or equivalent) per 5 min, window vs baseline.
2. **Onset**: first bucket where errors exceed ~3× baseline → this is the incident start time.
3. **Top signatures**: top 10 by `error.type` / exception class / normalized message; mark signatures **new** (absent in baseline).
4. **HTTP**: status code distribution and p95 latency per bucket if fields exist.
5. **Upstream/downstream**: messages referencing dependencies (timeouts, connection refused, 5xx from X, TLS errors).
6. **Trace pivot**: pick 2–3 trace/correlation IDs from top new signature; pull full path.
7. Raw lines: max 20 per signature, redacted.

## Query templates (ES|QL)
```
FROM <index>
| WHERE @timestamp >= "<start>" AND @timestamp <= "<end>" AND <service_field> == "<service_value>" AND log.level == "error"
| STATS c = COUNT(*) BY bucket = DATE_TRUNC(5 minutes, @timestamp)
| SORT bucket
```
```
FROM <index>
| WHERE @timestamp >= "<start>" AND @timestamp <= "<end>" AND <service_field> == "<service_value>" AND log.level == "error"
| STATS c = COUNT(*) BY error.type
| SORT c DESC | LIMIT 10
```

## Heuristics
- New signature appearing at onset → strongest log signal.
- Only timeout/connection errors toward one dependency → likely upstream; next_check that service.
- Errors across many services at once → infra/network (azure, nginx, k8s nodes).

## Output
`findings-contract`, source: elastic. Evidence = queries + Kibana Discover links.
