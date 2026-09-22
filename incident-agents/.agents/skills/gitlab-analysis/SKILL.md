---
name: gitlab-analysis
description: Find code, config, Helm, and pipeline changes that could explain an incident. Use for deploy correlation, suspect MRs, and failed pipelines for a service and time window.
---
# GitLab Analysis

## Inputs
service (resolved via service-map), window_start, window_end (UTC)

## Procedure
1. **Deploys in window**: pipelines on the default/release branch for `gitlab.project`; list `deploy_job` runs with status, sha, finished_at.
2. **Helm/values changes**: commits to `helm_chart_project` touching this service's chart/values in window.
3. **Merged MRs** between last good deploy sha and current deployed sha. Title, author, merged_at, labels.
4. **Suspect MR diff**: for top 1–3 MRs, summarize the diff focusing on config, dependencies, DB migrations, timeouts, retries, feature flags, resource limits.
5. **Failed pipelines** in window (may indicate partial deploy).
6. Extend back to T−24h if nothing found in window (slow-burn changes).

## Heuristics
- Deploy finished 0–30 min before error onset → high suspicion.
- Changes to timeouts, pool sizes, limits, TLS, env vars → prioritize over pure code.
- Dependency version bumps → check changelog notes.
- No deploy in window → record in `checked_clean`; points to infra/upstream.

## Output
`findings-contract`, source: gitlab. Evidence = MR/pipeline URLs, commit shas.
