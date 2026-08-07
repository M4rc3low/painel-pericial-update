# ADR-007 — Dados reais fora do repositório

**Status:** Accepted

## Contexto

O instalador original continha bancos, CSVs e perfis locais. Esses artefatos podem carregar dados pessoais/processuais ou sessão autenticada.

## Decisão

Somente código-fonte sanitizado e dados sintéticos podem ser publicados. Banco, CSV real, cookies, perfis, HTML e screenshots são bloqueados por `.gitignore` e por processo de revisão.

## Consequências

O repositório público continua útil como portfólio sem transformar dados operacionais em material de demonstração.
