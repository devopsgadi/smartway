# 5. Service onboarding

Each service needs two things:
1. An entry in **`service-map.yaml`** — *where* it lives (identifiers + discovery hints).
2. A **notes file** in `service-knowledge/services/<service>.md` — *how* it behaves and breaks.

## Step 1 — Scaffold
```
/new-service payments-api
```
Creates the notes file from the template and a service-map entry, pre-filled from Helm values, Istio config, and the repo where possible.

## Step 2 — Complete the service-map entry
| Field | Source |
|---|---|
| `snow_ci`, `snow_assignment_groups` | ServiceNow CMDB |
| `k8s.cluster/namespace/deployments/label_selector` | Helm chart / `kubectl get deploy` |
| `gitlab.project/helm_chart_project/deploy_job` | GitLab |
| `elastic.index/service_field/service_value` | Kibana data view |
| `azure.subscription/resource_group/resources` | Azure portal / Terraform |
| `nginx_upstream` | NGINX Plus config |
| `dependencies` | Architecture docs / Istio DestinationRules |

### Discovery hints (for vague tickets)
| Field | Example | Used for |
|---|---|---|
| `aliases` | payments, PAYAPI | Names people write in tickets |
| `business_functions` | bill pay, transfer | Feature words in tickets |
| `keywords` | payment failed | Symptom phrases |
| `hosts`, `url_paths` | /api/v1/payments | URL in ticket or ingress logs |
| `error_codes` | PAY-5003 | Codes users/apps report |
| `log_markers` | com.bank.payments | Logger/package names |

Generate `hosts` / `url_paths` from Istio:
```bash
kubectl get virtualservices -A -o json | python3 scripts/gen_ingress_map.py > ingress-hints.yaml
```
Review and merge into `service-map.yaml`.

## Step 3 — Complete the notes file
| Section | What to write |
|---|---|
| Overview | Purpose, owner, SLO, runtime, replicas/HPA |
| Architecture & dependencies | Upstream/downstream, timeouts/retries, data stores, ingress path, cert names |
| Normal behavior | Expected error noise, batch windows, traffic peaks |
| **Known failure modes** | Symptom → cause → how to confirm → fix. *Most valuable section.* |
| Service-specific queries | Elastic/KQL/kubectl that override generic templates |
| Past incidents | INC, date, root cause, RCA link |
| Runbooks | Links |

Seed Known failure modes from the last 10–20 incidents for the service.

## Step 4 — Validate
Run `/analyze-incident` on a past incident for the service and compare with the known RCA.

## Keeping it current
- The orchestrator proposes service-map additions for clues it couldn't match.
- After each confirmed RCA it proposes a notes-file update as an MR.
- Review both in normal MR flow; owners approve changes to their service.
- Regenerate ingress hints after routing changes.
