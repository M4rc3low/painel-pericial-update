# Runbook operacional

## Dashboard indisponível

1. verificar `HTTPCode_Target_5XX_Count` e health do target group;
2. conferir desired/running tasks do serviço ECS `web`;
3. abrir `/ecs/painel-pericial/<env>/web` no CloudWatch Logs;
4. validar conectividade com RDS e secret injection;
5. se a revisão atual estiver quebrada, o deployment circuit breaker deve executar rollback; confirmar eventos do ECS.

## Atualização solicitada e não executada

1. conferir `ApproximateNumberOfMessagesVisible` e idade da fila;
2. revisar logs da Lambda `trigger-worker`;
3. verificar se `RunTask` retornou failures;
4. conferir task worker stopped reason e `/ecs/.../worker` logs;
5. verificar mensagens na DLQ.

## Coleta falhando para todos os processos

1. verificar conectividade de saída/NAT;
2. validar status HTTP e mudanças estruturais da fonte;
3. confirmar que o collector continua usando apenas o caminho público autorizado;
4. suspender schedule se houver erro sistemático para evitar tráfego inútil.

## Banco

- conferir CPU e storage no CloudWatch;
- usar snapshots/automated backups para recovery;
- em produção, testar restore periodicamente e registrar RTO/RPO observado.

## Incidente de segredo

1. impedir novos deploys;
2. rotacionar segredo afetado;
3. revisar CloudTrail/CloudWatch e histórico Git;
4. se o segredo entrou no Git, removê-lo do histórico — `.gitignore` não é remediação retroativa.
