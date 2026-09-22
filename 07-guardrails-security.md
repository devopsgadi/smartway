# 7. Guardrails & security

## Hard rules (from `AGENTS.md`)
1. **Read-only.** No apply, delete, edit, patch, scale, rollout undo/restart, exec, port-forward, merge, or record updates.
2. **One write exception:** ServiceNow work notes, only when the user explicitly asks.
3. **UTC** for all timestamps.
4. **Resolve services** via service-map / scoping; never guess.
5. **Evidence** for every claim; otherwise labeled hypothesis.
6. **Redaction** before reasoning or output.
7. **Aggregate first**; raw lines only for specific failing entities.
8. **Common output** format.
9. **Correlation ≠ causation**; state confidence and how to confirm.

## Defense in depth
Rules in prompts are not enough. Enforce at the access layer:

| Layer | Control |
|---|---|
| Credentials | Dedicated read-only identities per system |
| Kubernetes | ClusterRole get/list/watch; exclude Secrets |
| Azure | Reader role only |
| GitLab | `read_api` token |
| ServiceNow | Read-only role + work-note write (or none) |
| Elastic | Read on required indices only |
| MCP servers | Expose only read tools; no generic "run command" |
| Secrets | Prompted inputs or a vault; never committed |

## Data protection
- `log-redaction` scrubs account/card numbers, SSNs, emails, phones, tokens, customer names, client IPs.
- Secrets and Key Vault values are referenced by name only.
- Confirm your organization's policy on sending log excerpts to the Copilot model.

## Human in the loop
- All remediation is suggested, never executed.
- ServiceNow posting requires confirmation.
- Notes-file and service-map updates go through GitLab MR review.

## Audit
- Copilot chat history shows every tool call.
- Use service-specific identities so system audit logs attribute activity to the agent.
