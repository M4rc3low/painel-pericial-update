# AWS Well-Architected Review

## Operational Excellence

**Implementado**
- infraestrutura declarada em Terraform;
- CI valida Python, containers e Terraform;
- deploy manualmente promovido via workflow;
- CloudWatch dashboard e logs centralizados;
- runbook e ADRs versionados com o código.

**Próxima maturidade**
- canary/synthetic check do dashboard;
- deploy blue/green via CodeDeploy;
- game day de falha do worker e restore do banco.

## Security

**Implementado**
- tasks em sub-redes privadas;
- RDS sem endpoint público;
- SG-to-SG para banco;
- senha gerenciada pelo Secrets Manager;
- workload roles separadas;
- GitHub OIDC sem credenciais AWS de longa duração;
- ECR scan-on-push e imagens imutáveis;
- WAF opcional;
- CodeQL e Dependabot.

**Próxima maturidade**
- federação do Cognito com um IdP corporativo, se aplicável;
- CMK dedicada para dados classificados;
- AWS Config/Security Hub em conta organizacional;
- permission boundaries/SCPs em ambiente multi-account.

## Reliability

**Implementado**
- worker stateless e efêmero;
- fila com DLQ;
- deployment circuit breaker no ECS;
- autoscaling web;
- backups RDS;
- processos persistidos fora dos containers.

**Trade-off do dev**
Single NAT e RDS Single-AZ reduzem custo, mas são SPOFs. O perfil de produção muda para redundância multi-AZ.

## Performance Efficiency

- Fargate evita dimensionamento de hosts.
- web escala horizontalmente por CPU.
- worker existe apenas durante a coleta.
- PostgreSQL permite índices e concorrência que SQLite local não oferecia.

Próximo passo: medir duração/p95 das coletas e ajustar CPU/memória com dados reais.

## Cost Optimization

- worker on-demand em vez de serviço 24x7;
- dev reduz desired count e tamanho do RDS;
- budget alert opcional;
- lifecycle de imagens ECR e artefatos S3;
- uma arquitetura de produção mais redundante é documentada, mas não ativada sem necessidade.

Principal custo fixo do dev: ALB, NAT Gateway e RDS. Para demonstrações esporádicas, destruir o workload depois da apresentação é uma decisão FinOps legítima; o bootstrap/ECR pode permanecer.

## Sustainability

- compute efêmero para tarefas periódicas;
- autoscaling evita capacidade ociosa excessiva;
- artefatos possuem lifecycle;
- escolha de serviços gerenciados reduz administração de hosts dedicados.
