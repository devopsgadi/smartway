# <service-key>

## Overview
- Purpose:
- Owner / escalation:
- Criticality / SLO: (e.g. 99.95% availability, p95 < 300ms)
- Runtime: (language, framework, replicas, HPA range)

## Architecture & dependencies
- Upstream (calls us):
- Downstream (we call): service → protocol → timeout/retry settings
- Data stores / queues:
- Ingress path: (NGINX Plus upstream → Istio gateway → service)
- Secrets / certs: (names only, rotation cadence)

## Normal behavior (baseline)
- Expected error noise:
- Expected restarts / batch jobs / scheduled windows:
- Traffic pattern: (peak hours, month-end spikes)

## Known failure modes
| Symptom | Likely cause | How to confirm | Fix (human-approved) |
|---|---|---|---|
|  |  |  |  |

## Service-specific queries
### Elastic
### Kubernetes
### Azure / KQL

## Past incidents
| INC | Date | Root cause | Link to RCA |
|---|---|---|---|

## Runbooks
- 
