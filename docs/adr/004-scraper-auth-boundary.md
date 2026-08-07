# ADR 004 - Treat authenticated browser automation as a security boundary

## Status
Open / requires source-system validation.

## Context
The legacy scraper opens Edge with remote debugging and depends on a manually authenticated browser profile. Copying that browser profile to a public repository or container image would leak session material and create an unsafe deployment pattern.

## Decision
Never commit browser profiles, cookies or authenticated session databases. Prefer public-source collection when functionally sufficient. If authenticated collection is required, bootstrap the session through an approved, controlled process and store only the minimum encrypted secret/session material required.

## Consequences
- Full cloud automation depends on the authentication controls of the external system.
- CAPTCHA/MFA or terms-of-use restrictions must not be bypassed.
