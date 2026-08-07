# ADR-008 — Autenticação do dashboard no ALB com Cognito

**Status:** Accepted for production profile

## Contexto

O dashboard apresenta informações processuais e não deve ser tratado como aplicação pública anônima. Colocar apenas um ALB na frente do Streamlit resolveria roteamento, mas não identidade.

## Decisão

No perfil `prod`, terminar TLS no Application Load Balancer e usar `authenticate-cognito` antes do forward para o target group. O user pool não permite self-signup por padrão; usuários são provisionados administrativamente.

## Consequências

- o container Streamlit não implementa senha própria;
- autenticação ocorre antes do tráfego alcançar o serviço ECS;
- produção exige `certificate_arn` e `app_fqdn`;
- o ambiente `dev` pode operar sem Cognito apenas com dados sintéticos e não deve hospedar dados operacionais reais.
