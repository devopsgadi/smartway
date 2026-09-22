---
name: k8s-triage
description: Investigate Kubernetes-side causes of an incident — rollouts, pod failures, restarts, OOM, scheduling, HPA, Istio. Use when an incident involves a workload on AKS or on-prem Kubernetes.
---
# Kubernetes Triage (read-only)

## Procedure
1. **Rollout history**: `kubectl rollout history deploy/<d> -n <ns>`; get revision timestamps from ReplicaSet creation. Revision change in window = change finding.
2. **Warning events**: `kubectl get events -n <ns> --field-selector type=Warning --sort-by=.lastTimestamp`
3. **Pod status**: `kubectl get pods -n <ns> -l <selector> -o wide` — restarts, CrashLoopBackOff, OOMKilled, Pending, node placement.
4. **Failing pod detail**: `kubectl describe pod` → last state, exit code, reason; `kubectl logs --previous --tail=100` (redact).
5. **Resources**: requests/limits vs `kubectl top pods`; OOM → compare to limit.
6. **HPA**: `kubectl get hpa -n <ns>`; replica churn, maxed out?
7. **Nodes** (if pods on multiple nodes failing or Pending): `kubectl get nodes`, describe for pressure conditions.
8. **Istio** (if meshed): sidecar readiness, `istioctl proxy-status`, VirtualService/DestinationRule changes.
9. **Config**: ConfigMap/Secret resourceVersion changed? (names only, never values).

## Never
apply, delete, edit, patch, scale, rollout undo/restart, exec, port-forward.

## Heuristics
- Restarts beginning ≤5 min after new ReplicaSet → deploy-induced.
- Exit 137 → OOM/kill; 1 → app error (check logs); 143 → SIGTERM (probe/eviction).
- Pending + FailedScheduling → capacity/quota/affinity.
- Failures across namespaces on same nodes → escalate to azure-diagnostics.

## Output
`findings-contract`, source: k8s. Evidence = exact commands.
