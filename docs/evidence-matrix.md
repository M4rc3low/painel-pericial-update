# Matriz de evidências para portfólio

Este arquivo liga cada habilidade arquitetural a uma evidência concreta do repositório. A intenção é evitar um portfólio baseado apenas em nomes de serviços.

| Competência | Evidência no projeto | O que explicar em entrevista |
|---|---|---|
| Modernização | `docs/architecture.md`, ADR-001/002 | Por que evitar lift-and-shift e separar web, worker e banco |
| Networking | `infra/terraform/network.tf` | Sub-redes públicas/app/db, NAT e trade-off single vs per-AZ |
| Containers | `Dockerfile.*`, `infra/terraform/ecs.tf` | Fargate, health checks, circuit breaker e autoscaling |
| Dados | `migrations/`, `infra/terraform/data.tf` | Migração SQLite -> PostgreSQL, backup, Multi-AZ e segredo gerenciado |
| Event-driven | `infra/terraform/events.tf` | SQS, DLQ, Lambda trigger e EventBridge Scheduler |
| IAM/Security | `infra/bootstrap/`, task roles, `docs/threat-model.md` | OIDC, trust boundary, runtime least privilege e autoridade de Terraform |
| Identity | Cognito + ALB em `ecs.tf` | Autenticar antes do container e exigir TLS no perfil prod |
| Edge security | `infra/terraform/security.tf` | AWS WAF managed rules e rate limit |
| Observability | `monitoring.tf`, `docs/runbook.md` | Métricas, alarmes, logs, dashboard e resposta operacional |
| CI/CD | `.github/workflows/` | Teste, build, Terraform validation e deploy por SHA |
| Supply chain | CodeQL, Dependabot, ECR immutable/scan | Controles no código e na imagem |
| FinOps | `dev.tfvars`, `prod.tfvars`, ADR-006 | Não pagar HA de produção num laboratório; documentar o risco |
| Reliability | DLQ, duplicate-worker guard, Multi-AZ prod | Idempotência, falhas transitórias e concorrência |
| Governance | ADRs, Well-Architected, threat model | Decisões versionadas e trade-offs explícitos |
| Compliance boundary | ADR-004/007 | Por que sessão autenticada e dados reais ficam fora do repo/cloud |

## Evidências que ainda exigem deploy real

Depois do primeiro deploy AWS, adicionar ao portfólio somente evidências reais:
- screenshot sanitizado do CloudWatch dashboard;
- execução de GitHub Actions bem-sucedida;
- `terraform plan`/outputs sem segredos;
- teste de rollback/circuit breaker;
- teste de restore do RDS e RTO observado;
- custo real de 24h/7d no Cost Explorer;
- latência e duração p95 da coleta.

Não inventar números de disponibilidade, economia ou performance antes dessas medições.
