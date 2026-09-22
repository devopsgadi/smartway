#!/usr/bin/env python3
"""Generate url_paths/hosts discovery hints per service from Istio VirtualServices.
Read-only. Usage: kubectl get virtualservices -A -o json | python3 gen_ingress_map.py > ingress-hints.yaml
Merge output into .agents/skills/service-map/service-map.yaml (review first)."""
import json, sys, collections

vs = json.load(sys.stdin)["items"]
out = collections.defaultdict(lambda: {"hosts": set(), "url_paths": set(), "namespaces": set()})

for v in vs:
    ns = v["metadata"]["namespace"]
    hosts = v["spec"].get("hosts", [])
    for route in v["spec"].get("http", []):
        paths = []
        for m in route.get("match", []) or [{}]:
            uri = m.get("uri", {})
            paths.append(uri.get("prefix") or uri.get("exact") or uri.get("regex") or "/")
        for dest in route.get("route", []):
            svc = dest["destination"]["host"].split(".")[0]
            out[svc]["hosts"].update(h for h in hosts if "." in h)
            out[svc]["url_paths"].update(paths)
            out[svc]["namespaces"].add(dest["destination"]["host"].split(".")[1] if "." in dest["destination"]["host"] else ns)

print("services:")
for svc in sorted(out):
    d = out[svc]
    print(f"  {svc}:")
    for k in ("hosts", "url_paths", "namespaces"):
        print(f"    {k}: [{', '.join(sorted(d[k]))}]")
