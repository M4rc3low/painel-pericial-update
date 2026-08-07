# Painel Pericial Cloud

Cloud modernization case study of a Python/Streamlit process-monitoring application, designed as an AWS architecture portfolio project.

> **Important:** deadline classification in this project is heuristic and is not a substitute for validation in the official court system or professional legal deadline controls.

## Why this repository exists

The original solution runs locally with Streamlit, SQLite, Playwright and a Windows/Edge launcher. This repository documents and implements the migration toward a secure, observable and reproducible AWS workload.

## Architecture goals

- Containerize web and collector workloads.
- Replace local SQLite with Amazon RDS for PostgreSQL.
- Run the web workload on Amazon ECS with AWS Fargate.
- Schedule collection with Amazon EventBridge Scheduler.
- Store secrets outside source code with AWS Secrets Manager.
- Add CloudWatch logs, metrics and alarms.
- Use Amazon Cognito + ALB authentication for dashboard access.
- Protect the public entry point with AWS WAF and TLS.
- Deliver through GitHub Actions using AWS IAM OIDC federation.
- Manage infrastructure with Terraform.

See [`docs/architecture.md`](docs/architecture.md) and the ADRs under [`docs/adr`](docs/adr).

## Repository structure

```text
src/painel_pericial/      cloud-ready application skeleton
legacy-src/               source-only snapshot of the desktop implementation
infra/terraform/          AWS infrastructure as code
.github/workflows/        CI and reference AWS deployment workflow
docs/                     architecture and decisions
tests/                    automated tests
sample/                   synthetic demo data only
```

## Security rules

The original installer contains local browser profiles, SQLite databases, CSV exports, build artifacts and debug HTML. None of those belong in a public repository. The `.gitignore` intentionally blocks them.

Never commit:
- browser profiles/cookies/sessions;
- real process/client data;
- `.env` files or AWS credentials;
- SQLite databases;
- scraper debug pages with case data;
- compiled installer/build output.

## Local development

```bash
cp .env.example .env
docker compose up --build
```

Then open the Streamlit service on port `8501`.

## CI/CD strategy

Pull requests run tests and container builds. The reference deployment workflow demonstrates OIDC-based AWS authentication without long-lived access keys. Runtime roles are deliberately narrow. The Terraform deploy role is broader because it creates infrastructure, and its trust is constrained to this repository and approved GitHub Environments; splitting plan/apply permissions is a documented hardening step.

## Migration roadmap

1. **Sanitize and baseline** — isolate source code and remove local/session artifacts.
2. **Containerize** — separate web and collector images.
3. **Data layer** — migrate SQLite schema to PostgreSQL and add migrations.
4. **AWS foundation** — VPC, ECR, ECS, RDS, IAM, CloudWatch, Secrets Manager.
5. **Collector orchestration** — EventBridge Scheduler -> Fargate worker with controlled retry/rate.
6. **Security** — Cognito, HTTPS, WAF, least privilege, backup/restore testing.
7. **CI/CD** — GitHub OIDC -> Terraform/ECR/ECS.
8. **Well-Architected review** — document reliability, security, operations, performance, cost and sustainability trade-offs.

## Portfolio talking points

This project demonstrates application modernization rather than a lift-and-shift migration: workload decomposition, managed data services, container orchestration, infrastructure as code, identity federation, secrets management, observability, cost/reliability trade-offs and explicit handling of an external-system authentication constraint.
