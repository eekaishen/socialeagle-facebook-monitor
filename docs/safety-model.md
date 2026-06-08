# Safety Model

SocialEagle uses a fail-closed model for public-page monitoring.

## Complete Means Verified

A run is complete only when the safety verifier returns:

```json
{"ok": true}
```

Any unresolved access issue, timeout, failed page check, missing metric, or partial row keeps the run incomplete.

## Why Fail Closed

Public monitoring outputs are often used for marketing, compliance, and operations decisions. A partial result can still be useful, but it should not be relabeled as complete.

The safer behavior is:

- show what was verified
- show what was blocked
- preserve status reasons
- wait for a verified rerun or focused repair before claiming full coverage

## Privacy Boundaries

The public repository should never include:

- passwords
- cookies
- browser storage-state files
- private target lists
- generated private reports
- raw account data
- environment variable exports

## Human Review

This project is product and operations guidance, not legal advice. Formal use should be reviewed against platform terms, data policies, and local counsel requirements.
