# ADR-006 — Perfis separados para portfólio e produção

**Status:** Accepted

## Contexto

Uma arquitetura altamente redundante tem custo fixo desnecessário para um laboratório de portfólio, mas um desenho barato não deve ser apresentado como referência de produção.

## Decisão

Manter `dev` com uma task web, RDS pequeno/Single-AZ e um NAT Gateway. Documentar `prod` com >=2 tasks, RDS Multi-AZ, WAF, TLS, deletion protection e NAT por AZ como evolução necessária.

## Consequências

O case demonstra explicitamente trade-off de custo x disponibilidade em vez de ocultar o risco de SPOFs no ambiente de demonstração.
