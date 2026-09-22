# payments-api

## Overview
- Purpose: Payment initiation and status API for digital banking
- Owner / escalation: Payments Platform
- Criticality / SLO: Tier 1 — 99.95% availability, p95 < 300ms
- Runtime: Java/Spring Boot, 6–20 replicas (HPA on CPU 70%)

## Architecture & dependencies
- Upstream: mobile-bff, web-bff
- Downstream:
  - auth-service → HTTP/mTLS → timeout 2s, 1 retry
  - core-banking-gateway → HTTP → timeout 5s, no retry
- Data stores: Azure SQL (payments-db), Service Bus (payments-events)
- Ingress: NGINX Plus `payments_backend` → Istio ingress gateway → payments-api
- Secrets/certs: kv-payments-prod / payments-mtls-cert (90-day rotation)

## Normal behavior (baseline)
- ~0.1% 4xx (validation) is normal; ignore `PaymentValidationException`
- Nightly settlement batch 02:00–03:00 UTC → CPU spike, HPA to max is expected
- Month-end: 3–4× traffic

## Known failure modes
| Symptom | Likely cause | How to confirm | Fix (human-approved) |
|---|---|---|---|
| Spike in `SQLTransientConnectionException` | DB connection pool exhausted | Hikari pool metrics; active = max | Rollback pool config / scale DB |
| 503s + `upstream connect error` | Istio sidecar not ready after deploy | Pod events, `istioctl proxy-status` | Restart pods |
| TLS handshake failures to auth-service | mTLS cert rotated, pods not reloaded | Key Vault cert version vs pod start time | Rolling restart |
| Timeouts to core-banking-gateway | Upstream latency | Check core-banking-gateway file + its logs | Escalate upstream |

## Service-specific queries
### Elastic
```
FROM logs-payments-*
| WHERE service.name == "payments-api" AND @timestamp >= "<start>"
| WHERE error.type != "PaymentValidationException"
| STATS c = COUNT(*) BY error.type | SORT c DESC | LIMIT 10
```
### Kubernetes
`kubectl get pods -n payments -l app.kubernetes.io/name=payments-api -o wide`

## Past incidents
| INC | Date | Root cause | Link to RCA |
|---|---|---|---|
| REPLACE_ME | | | |

## Runbooks
- REPLACE_ME (Confluence/GitLab wiki link)
