# 1. Overview

## What it is
A team of AI agents that investigates incidents the way an experienced on-call engineer would: read the ticket, find the affected app, check logs, pods, recent changes, and cloud infrastructure, then build a timeline and name the most likely cause — with evidence.

## The analogy: a detective team
| Role | Agent | Job |
|---|---|---|
| Lead detective | `incident-orchestrator` | Reads the case, picks the app, dispatches specialists, writes the conclusion |
| Records clerk | `servicenow-investigator` | Ticket details, change requests, related incidents, CMDB |
| Log analyst | `kibana-investigator` | Error spikes, new exception types, onset time |
| Scene inspector | `k8s-investigator` | Crashing, restarting, newly deployed pods |
| Change tracker | `gitlab-investigator` | Code, Helm, and config changes before the problem |
| Infrastructure expert | `azure-investigator` | Network, certificates, nodes, platform health |

## What you get
An RCA draft containing:
- Summary and onset time (UTC)
- Most likely cause with confidence and evidence links
- Ranked alternative causes
- Timeline across all systems
- What was checked and found clean
- Suggested actions (for human approval)
- Gaps in available data

## What it does NOT do
- Change anything in production (read-only by design)
- Close, reassign, or update ServiceNow records (it may add a work note only when asked)
- Replace human judgment — every conclusion is a draft for review

## Goals
- Cut time-to-first-hypothesis from hours to minutes
- Make investigations consistent across engineers and shifts
- Capture learnings per service so every incident improves the next one
