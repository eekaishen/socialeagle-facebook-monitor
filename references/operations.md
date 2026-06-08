# SocialEagle Operations Reference

## Product Context

SocialEagle is an evidence-first monitor for approved public-page review workflows.

Public preview:

```text
https://socialeagleph.vercel.app/
```

Project owner:

```text
https://www.hubinasia.com/
```

## Safe Operating Rules

- Use approved public-page monitoring scopes only.
- Keep private sessions, credentials, and generated private reports out of public files.
- Run browser-heavy checks outside the operator work window unless explicitly approved.
- Do not run two collectors against the same browser/session at the same time.
- If access/session health is blocked, ask the user to refresh the dedicated browser profile manually.
- Do not ask for or record passwords.

## Definition Of Complete

Only treat a monitoring report as complete when the safety file says:

```json
{"ok": true}
```

`ok=true` means every active target was checked, every required row has evidence, totals recompute, and there are no unresolved access, timeout, failed, or partial-metric blockers.

If `ok=false`, report blockers exactly from `blocking_targets`.

## Expected Safety File

Default path in compatible projects:

```text
output/reports/daily/facebook_daily_latest_safety.json
```

Expected blocker shape:

```json
{
  "target_name": "ExampleBrand",
  "page_url": "https://www.facebook.com/example",
  "page_status": "not_checked",
  "metric_status": "not_checked",
  "status_reason": "target timeout",
  "automation_attempts": []
}
```

## Recommended Reliability Pattern

For browser-backed monitoring jobs:

- isolate target work into bounded jobs
- preserve per-target timeout
- record timeout/exit/stderr summaries into `status_reason`
- keep successful target evidence
- keep unresolved targets incomplete

## Publishing Rule

Publishing a public dashboard is separate from proving the daily monitor is complete.

The product may display a partial run, but it should clearly identify unresolved blockers unless the safety verifier returns `ok=true`.
