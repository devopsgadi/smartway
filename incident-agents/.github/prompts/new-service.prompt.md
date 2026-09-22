---
description: Scaffold a service knowledge file and service-map entry for a new service
argument-hint: <service-key>
---
Create a service knowledge file for: ${input:service:service key}

1. Copy `.agents/skills/service-knowledge/services/_template.md` to `services/<service-key>.md`.
2. Pre-fill what can be derived from this repo and connected tools (read-only): Helm chart values (replicas, limits, HPA), Istio VirtualService/DestinationRule timeouts and retries, GitLab project, dependencies from config.
3. Add the identifiers entry to `.agents/skills/service-map/service-map.yaml`.
4. Leave REPLACE_ME for anything unknown. Do not guess failure modes.
