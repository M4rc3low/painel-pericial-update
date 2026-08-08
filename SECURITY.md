# Security policy

## Sensitive data

Do not open a public issue containing process data, client information, browser cookies, authentication sessions, AWS credentials or database secrets.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting/security advisory flow when available. If the finding is only about architecture documentation and contains no sensitive material, a normal issue is acceptable.

## Repository hygiene

Before every public release, verify that no `.env`, SQLite database, real CSV export, browser profile, debug HTML or screenshot was added to Git history. `.gitignore` prevents common mistakes but does not remove data already committed.
