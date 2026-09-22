---
name: azure-diagnostics
description: Investigate Azure platform causes — activity log changes, resource health, AKS node pools, networking, Key Vault, App Gateway. Use when evidence points below the application or across multiple services.
---
# Azure Diagnostics (Reader role)

## Procedure
1. **Activity Log** for resource group(s) in window: write/delete operations, caller, status. Focus: NSG, route tables, firewall, Key Vault access policies/secrets, App Gateway, AKS upgrades/scale, DNS.
2. **Resource Health** for listed resources + AKS cluster.
3. **Service Health** for region incidents in window.
4. **AKS**: node pool upgrades, node image updates, autoscaler events, node NotReady.
5. **Key Vault**: certificate/secret expiry or rotation near window (names only).
6. **Log Analytics KQL** (if workspace available):
```kql
AzureActivity
| where TimeGenerated between (datetime(<start>) .. datetime(<end>))
| where ResourceGroup =~ "<rg>"
| where OperationNameValue endswith "WRITE" or OperationNameValue endswith "DELETE"
| project TimeGenerated, OperationNameValue, Caller, ActivityStatusValue, _ResourceId
| order by TimeGenerated asc
```
```kql
KubeEvents
| where TimeGenerated between (datetime(<start>) .. datetime(<end>))
| where Namespace == "<ns>" and KubeEventType == "Warning"
| summarize count() by Reason, bin(TimeGenerated, 5m)
```

## Heuristics
- Infra write in window not tied to a ServiceNow change → flag high.
- Cert expiry / Key Vault change + TLS errors in logs → strong link.
- Region service health event → note and lower app-level hypotheses.

## Output
`findings-contract`, source: azure.
