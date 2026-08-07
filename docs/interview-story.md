# História do case para entrevista

## Em 30 segundos

“Eu peguei uma aplicação desktop Python que misturava Streamlit, SQLite, subprocessos e uma sessão local de navegador. Em vez de fazer lift-and-shift para EC2, redesenhei os boundaries: web e worker em ECS Fargate, PostgreSQL no RDS, atualização desacoplada com SQS/Lambda, agendamento no EventBridge, observabilidade no CloudWatch e IaC em Terraform. O pipeline usa GitHub OIDC, sem access keys estáticas. Mantive duas topologias, uma econômica para portfólio e outra de referência Multi-AZ para produção, e documentei os trade-offs em ADRs e Well-Architected.”

## Pergunta: por que não EC2?

Porque EC2 preservaria o acoplamento de sistema operacional e o modelo “uma máquina faz tudo”. O objetivo da modernização era separar ciclos de vida, falhas e escala entre UI, coleta e persistência.

## Pergunta: por que Fargate e não Lambda para o scraper?

A coleta é um job com duração e dependências que podem crescer, além de potencialmente exigir browser automation em uma evolução futura. Fargate mantém o packaging em container e evita forçar o workload dentro dos limites de execução/dependências de uma função.

## Pergunta: por que SQS + Lambda antes de RunTask?

Para que o dashboard não tenha `ecs:RunTask` nem `iam:PassRole`. A web só pode publicar na fila; a Lambda concentra a capacidade de orquestração, a DLQ absorve falhas e a mesma entrada é reutilizada pelo Scheduler.

## Pergunta: por que um NAT no dev e dois no prod?

Um NAT reduz custo do laboratório, mas cria dependência de uma única AZ para egress. No perfil de produção eu prefiro NAT por AZ e RDS Multi-AZ. O ponto é demonstrar que custo e disponibilidade são decisões explícitas, não defaults invisíveis.

## Pergunta: a role do GitHub é least privilege?

As roles de runtime são estreitas. A role de Terraform é mais ampla por natureza porque precisa criar infraestrutura. Eu reduzi risco usando credenciais temporárias OIDC, trust limitado ao repositório/environments e documentei como hardening futuro separar plan/apply, permission boundaries e SCPs.

## Pergunta: e a autenticação do e-SAJ?

O legado dependia de uma sessão Edge autenticada. Eu não copiei perfil/cookie para container nem GitHub. O boundary cloud habilita apenas coleta pública. Qualquer automação autenticada só entra com mecanismo oficialmente suportado e controles adequados. Para mim, arquitetura inclui saber onde parar a automação.
