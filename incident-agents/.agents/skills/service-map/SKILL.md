---
name: service-map
description: Resolve a service, ServiceNow CI, namespace, repo, URL path, error code, or alias into all its cross-system identifiers. Use first in every incident investigation, before querying any system.
---
# Service Map

Source of truth: `service-map.yaml` in this folder.

## Procedure
1. Exact match on: key, snow_ci, k8s namespace/deployment, gitlab project, elastic service_value, nginx_upstream.
2. If no exact match, reverse lookup on discovery hints: aliases, url_paths (longest prefix), hosts, error_codes, log_markers, snow_assignment_groups, business_functions, keywords.
3. Return full record(s) with how each matched.
4. Multiple candidates or none → hand off to `incident-scoping`. Never guess.
