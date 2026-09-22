---
name: service-knowledge
description: Service-specific operational knowledge — architecture, dependencies, known failure modes, past incidents, service-specific queries, runbooks, SLOs. Use after service-map resolves a service, before and during investigation of that service.
---
# Service Knowledge

One file per service in `services/<service-key>.md` (key = service-map key).

## Procedure
1. After `service-map` resolves the service, read `services/<service-key>.md`.
2. Also read files for services listed in `dependencies` if symptoms point upstream.
3. Apply in this order:
   - **Known failure modes** → check these first; match symptoms before generic procedures.
   - **Service-specific queries** → override generic templates in module skills.
   - **Normal behavior** → use as baseline (expected error noise, restarts, batch windows) to avoid false positives.
4. If no file exists: continue with generic skills and list "no service knowledge file" under Gaps.

## Rules
- Service files are knowledge, not identifiers. Identifiers live only in `service-map.yaml`.
- Known failure mode matched → still require live evidence; history is a lead, not proof.
