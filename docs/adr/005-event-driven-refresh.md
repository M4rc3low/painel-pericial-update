# ADR-005 — SQS + Lambda para atualização manual

**Status:** Accepted

## Contexto

O desktop executava `main.py` como subprocesso a partir da UI. Em cloud isso acoplaria a duração da coleta à sessão do dashboard e exigiria permissão `ecs:RunTask` no container web.

## Decisão

O dashboard envia apenas uma mensagem SQS. Uma Lambda com permissão específica inicia a task Fargate worker. O EventBridge Scheduler reutiliza a mesma Lambda.

## Consequências

- dashboard permanece responsivo;
- burst de solicitações é absorvido pela fila;
- permissão de orquestração fica fora da aplicação web;
- há componentes adicionais a observar (SQS/Lambda/DLQ).
