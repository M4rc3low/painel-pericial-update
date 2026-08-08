# ADR 009 - Separate runtime least privilege from Terraform deployment authority

## Status
Accepted.

## Context
The web and worker containers should have only the permissions required at runtime. Terraform, however, must create and modify networking, ECS, RDS, IAM, observability and security resources. Calling both permission sets “least privilege” would hide an important architectural distinction.

## Decision
- Runtime task roles are narrow and workload-specific.
- GitHub Actions receives short-lived credentials through OIDC; no static AWS access key is stored in GitHub.
- The OIDC trust policy is restricted to this repository and the approved GitHub Environments `aws-dev` and `aws-prod`.
- The Terraform deployment role is intentionally broader than runtime roles because it manages infrastructure.
- Production GitHub Environment protection rules should require the approved branch and reviewer(s).

## Hardening path
For a larger organization, split read-only plan from apply, use permission boundaries/SCPs, scope service actions further, and move sensitive production deployments behind a dedicated platform role.

## Consequences
The portfolio remains truthful about administrative authority while still demonstrating strong identity federation and runtime least privilege.
