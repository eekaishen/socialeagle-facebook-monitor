# Publishing Checklist

Use this checklist before publishing a SocialEagle-style monitor or skill package.

## Public Files

- README explains the public-page monitoring purpose.
- Screenshots are redacted.
- Links point to public product pages only.
- No private target list appears in marketing material.
- No generated private reports are included.

## Secrets

Confirm the repository does not include:

- `.env` files
- passwords
- password hashes
- cookies
- browser storage-state JSON
- API tokens
- Vercel environment exports
- Google credential files

## Language

Prefer:

- monitor
- public-page evidence
- audit trail
- safety verifier
- coverage status
- blocker reason

Avoid language that overpromises complete coverage when the safety verifier is not `ok=true`.

## Launch Channels

Recommended order:

1. GitHub repository
2. Technical build article
3. LinkedIn post
4. Show HN, if the repo and demo are useful to a technical audience
5. Product Hunt, when product assets and maker comment are ready
