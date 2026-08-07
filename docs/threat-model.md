# Threat model

## Assets

1. dados de processos e clientes;
2. credenciais de banco;
3. permissões AWS de deploy e runtime;
4. código e pipeline;
5. disponibilidade da coleta e do dashboard.

## Trust boundaries

- internet -> ALB;
- GitHub -> AWS STS/OIDC;
- web task -> SQS/RDS;
- Lambda -> ECS control plane;
- worker -> sistema externo/RDS/SNS/S3;
- Secrets Manager -> task execution.

## Principais ameaças e controles

| Ameaça | Controle |
|---|---|
| credencial AWS vazada no GitHub | OIDC com credenciais temporárias; nenhuma access key no workflow; trust limitado ao repositório e aos GitHub Environments aprovados |
| acesso direto ao banco | RDS privado + SG aceitando apenas web/worker |
| container web comprometido iniciar workloads arbitrários | web só envia SQS; `ecs:RunTask` fica na Lambda |
| abuso do endpoint público | ALB; WAF/rate limit opcional; futura autenticação |
| sessão/cookie do e-SAJ publicada | perfis e cookies bloqueados no Git; caminho autenticado fora do boundary cloud |
| dados reais publicados como sample | apenas CSV sintético e inativo; revisão antes de commit |
| atualização duplicada | constraints únicas para movimentações/alertas; worker idempotente no nível de persistência |
| fila parada | DLQ + CloudWatch alarm para idade da mensagem |
| imagem alterada sob mesma tag | ECR com tags imutáveis e deploy pelo SHA do commit |

## Dados que não devem ser armazenados no S3 de debug

HTML ou screenshot de processo pode conter informação pessoal ou processual. O bucket existe para artefatos operacionais controlados, mas o código não faz upload de HTML bruto por padrão. Qualquer ativação futura precisa definir classificação, minimização e retenção.
