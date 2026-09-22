---
name: incident-scoping
description: Identify the affected service(s) and time window when an incident has missing, generic, or wrong CI/service info. Use before any specialist investigation whenever the service is not confidently known.
---
# Incident Scoping (service discovery)

Goal: turn a vague INC into ranked candidate services + a UTC window. Stop as soon as one candidate is confident.

## Step 1 — Extract clues from the INC (servicenow-analysis)
From short_description, description, work notes, comments, attachments text:
- Error codes / exception names / HTTP status
- URLs, hosts, API paths, screen/feature names ("bill pay page")
- Transaction / correlation / reference IDs (redact customer data)
- Business function words (login, payment, statement)
- Reported time ("since 9:15 ET") → convert to UTC
- Assignment group, caller's app, related INCs
- Affected CI even if generic ("Digital Banking")

## Step 2 — Map clues via service-map reverse lookup
Error code / URL path / host / alias / assignment group → candidate services.
Record which clue matched each candidate.

## Step 3 — Pivot on hard identifiers in logs (strongest)
If a correlation/transaction ID or unique error string exists, search all app logs:
```
FROM logs-*
| WHERE @timestamp >= "<start>" AND @timestamp <= "<end>"
| WHERE trace.id == "<id>" OR transaction.id == "<id>" OR message LIKE "*<id>*"
| STATS c = COUNT(*), first = MIN(@timestamp) BY service.name, kubernetes.namespace
| SORT first ASC
```
The first service to log an error for that ID is usually closest to the cause.

## Step 4 — Ingress-first (URL known, service unknown)
All traffic enters via NGINX Plus / Istio gateway. Map path → upstream → service:
```
FROM logs-nginx-*, logs-istio-*
| WHERE @timestamp >= "<start>" AND @timestamp <= "<end>" AND url.path LIKE "<path>*"
| STATS total = COUNT(*), errors = COUNT(CASE(http.response.status_code >= 500, 1, null)) BY upstream_name, url.path
| SORT errors DESC | LIMIT 10
```

## Step 5 — Estate-wide anomaly sweep (no usable clues)
Rank services by error increase vs baseline (same-length window before):
```
FROM logs-*
| WHERE @timestamp >= "<baseline_start>" AND @timestamp <= "<end>" AND log.level == "error"
| EVAL period = CASE(@timestamp >= "<start>", "incident", "baseline")
| STATS c = COUNT(*) BY service.name, period
```
Compute ratio incident/baseline per service; top 5 with ratio ≥ 3 are candidates.
In parallel (cheap, estate-wide):
- k8s: Warning events + restarts across all namespaces in window
- gitlab: all prod deploys in window
- servicenow: all change requests + other open incidents in window
- azure: activity log writes across prod subscriptions in window

## Step 6 — Rank & decide
Score candidates: hard-ID match (5) > URL/ingress 5xx (4) > error code match (4) > anomaly ratio (3) > deploy/change in window (2) > alias/keyword/assignment group (1).
- One clear winner → proceed with it (note confidence).
- Several close → investigate top 2 in parallel.
- Nothing → ask the human ONE question with top 3 candidates + what evidence would decide.

## Window rules
- Use reported time from INC text if present; else opened_at − 2h → opened_at + 30m.
- Refine to anomaly onset found in Step 3/4/5.

## Output
```yaml
candidates:
  - service: payments-api
    score: 9
    matched_on: [error_code PAY-5003, ingress /api/v1/payments 5xx]
window: { start: <UTC>, end: <UTC>, onset: <UTC|null> }
clues_unmatched: [<clues with no mapping — add to service-map>]
```
Unmatched clues are signals to improve service-map.yaml.
