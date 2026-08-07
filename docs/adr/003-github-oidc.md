# ADR 003 - GitHub Actions authenticates to AWS with OIDC

## Status
Accepted.

## Decision
Do not store long-lived AWS access keys in GitHub secrets. GitHub Actions obtains short-lived AWS credentials by assuming a temporary IAM role through OIDC federation. Runtime roles remain least-privilege; the Terraform deployment role has broader infrastructure-management permissions and is constrained at the trust boundary.

## Consequences
- Reduced credential leakage risk.
- Trust policy is scoped to the intended repository and GitHub Environments (`aws-dev`/`aws-prod`). Environment protection rules should gate production to the approved branch/reviewers.
- CloudTrail can audit role usage.
