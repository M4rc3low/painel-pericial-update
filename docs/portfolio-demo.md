# Roteiro de demonstração do case (5–7 min)

## 1. Comece pelo problema, não pelos serviços

“Este sistema começou como uma aplicação desktop funcional. O risco era fazer lift-and-shift e apenas trocar meu notebook por uma EC2. Eu preferi identificar acoplamentos: SQLite local, subprocessos, sessão de navegador, ausência de observabilidade e deploy manual.”

## 2. Mostre a decomposição

Abra `docs/architecture.md` e explique:
- ALB -> ECS Fargate web;
- PostgreSQL em RDS;
- SQS para desacoplar o botão de atualização;
- Lambda com `RunTask` isolado;
- worker Fargate efêmero;
- EventBridge Scheduler reutilizando o mesmo trigger.

## 3. Mostre segurança

Abra `infra/bootstrap/main.tf` e `infra/terraform/ecs.tf`:
- GitHub OIDC restrito ao repositório e aos GitHub Environments `aws-dev`/`aws-prod`; produção pode exigir `main` e aprovação manual nas protection rules;
- runtime roles separadas;
- RDS privado;
- web não recebe `ecs:RunTask`;
- produção exige HTTPS + Cognito e habilita WAF.

## 4. Mostre confiabilidade

- SQS DLQ;
- Lambda impede worker concorrente;
- deployment circuit breaker;
- autoscaling;
- RDS Multi-AZ no perfil prod;
- CloudWatch alarms e runbook.

## 5. Mostre FinOps

Compare `dev.tfvars` e `prod.tfvars`. Explique por que laboratório não precisa pagar a topologia HA 24x7 e por que essa economia não deve ser vendida como arquitetura de produção.

## 6. Feche com o boundary mais importante

“Eu não tentei esconder a parte difícil: o legado usava sessão autenticada de navegador. Eu mantive essa automação fora da arquitetura cloud até existir um mecanismo oficialmente suportado. Arquitetura também é saber o que não automatizar.”
