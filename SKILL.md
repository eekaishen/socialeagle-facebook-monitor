---
name: socialeagle-public-page-monitor
description: Inspect and operate evidence-first public social monitoring workflows. Use when Codex needs to review a monitoring safety result, list blockers, protect off-hours browser-heavy checks, avoid credential leakage, or prepare publish-safe product documentation for SocialEagle-style public-page monitoring.
---

# SocialEagle Public Page Monitor

## Core Rule

Treat public social monitoring as an evidence review workflow, not a best-effort browser task.

Only describe a run as complete when the safety result says `ok=true`. If `ok=false`, report the exact blockers and keep partial coverage visible.

Read `references/operations.md` when you need the operating model, report shape, or publishing guardrails.

## Start Every Task

First identify what the user wants:

- status inspection
- focused diagnostic
- code fix guidance
- product or PRD update
- publish-safe GitHub packaging

If project memory files exist, read them before changing behavior:

```bash
test -f state/current_task.md && sed -n '1,220p' state/current_task.md
test -f state/next_steps.md && sed -n '1,220p' state/next_steps.md
test -f state/decision_log.md && sed -n '1,180p' state/decision_log.md
test -f codex-handoff.md && sed -n '1,220p' codex-handoff.md
```

## Status Inspection

Prefer the bundled read-only inspector:

```bash
python3 scripts/inspect_safety.py --reports-dir output/reports/daily --json
```

Report:

- `ok`
- target date
- latest report path, when available
- `blocking_targets` with `target_name`, `page_url`, `page_status`, `metric_status`, and `status_reason`
- `automation_attempts`
- whether the public site was updated, if deployment metadata is available

Do not run broad browser collection just to answer a status question.

## Work-Hours Safety

Browser-heavy monitoring should run outside the operator's work window unless explicitly approved.

Use local project policy for the exact window. If no project policy exists, ask for the preferred quiet hours before scheduling browser-heavy checks.

If a run records a work-hours cutoff, treat it as intended protection, not a failure to force through.

## Auth And Session Rules

Never ask for or record passwords.

If access/session health is blocked, ask the user to refresh the dedicated browser profile manually. Do not store cookies, passwords, or raw storage-state values in GitHub, Markdown, chat, `.env`, generated bundles, or skill files.

## Focused Diagnostics

When `ok=false`, diagnose the exact blocker first.

Allowed diagnostic pattern:

- inspect safety JSON
- inspect latest dated report JSON
- run project-provided preflight checks, if available
- check only blocking target names when browser-heavy diagnostics are approved

Avoid full reruns until the cause is clear.

## Code Fix Direction

When blockers show worker exits or timeouts, focus on runner reliability:

- isolate each target collection job
- keep hard per-target timeouts
- capture exit code, timeout, and stderr summary into `status_reason`
- preserve successful target rows
- keep unresolved targets incomplete instead of inventing no-post results

After code edits, run targeted non-browser verification first.

## Product And Publishing Work

Keep public language focused on:

- public-page monitoring
- evidence review
- audit trail
- status visibility
- privacy-aware operation

Do not publish credentials, private sessions, private target lists, generated private reports, or raw account data.

## Final Handoff

For meaningful work, update local project memory if it exists. Then report:

- what changed
- what was verified
- current blockers or remaining risk
