# ADR-011: Padrões de `scope` para mensagens de commit

- Status: Aceito
- Data: 2026-07-23

## Contexto

Este projeto utiliza mensagens de commit com escopo (conventional-commits style) em várias mensagens. Ao longo do desenvolvimento surgiram variações próximas entre scopes — isso pode dificultar pesquisa, automações e consistência no histórico.

## Decisão

Definir um conjunto canônico de `scope` a ser usado nas mensagens de commit, listando os scopes já usados no repositório e recomendando manutenção dos mesmos quando o mesmo componente/subsistema for afetado.

Scopes detectados no histórico (ordem por frequência):

- `wallet` (3 ocorrências) — saldo, persistência e operações da carteira
- `strategy` (3 ocorrências) — regras e algoritmos de decisão de trading
- `bot` (3 ocorrências) — orquestração e fluxo principal do bot
- `repository` (2 ocorrências) — camadas de acesso a dados e repositório local
- `config` (2 ocorrências) — parâmetros e configuração do projeto
- `adr` (2 ocorrências) — documentação de decisões arquiteturais (ADRs)
- `trading` (1 ocorrência) — lógica de trading (use `trade` preferencialmente)
- `trade` (1 ocorrência) — execução de ordens e operações de mercado
- `ruff` (1 ocorrência) — correções de estilo/formatador (ruff)
- `readme` (1 ocorrência) — documentação do repositório e README
- `project` (1 ocorrência) — metadados do repositório e infra do projeto
- `exchange` (1 ocorrência) — integração com a exchange (APIs/sockets)
- `dashboard` (1 ocorrência) — interface/visualização no terminal
- `core` (1 ocorrência) — código central/arquitetura do sistema
- `cleanup` (1 ocorrência) — tarefas de limpeza e refatoração

## Guidelines (regras práticas)

- Reutilize exatamente um dos scopes listados acima quando o commit afetar esse componente.
- Evite criar scopes aproximados (por exemplo, use `trade` ou `trading`, escolha apenas um e padronize).
- Para mudanças que tocam múltiplos subsistemas, prefira usar um scope genérico existente como `core` ou `bot`, ou crie commits separados por escopo.
- Para arquivos de documentação, use `adr` ou `readme` conforme o foco da mudança.

## Recomendação de padronização (mapa de alias)

- `trade` ←→ `trading`: escolher `trade` como padrão (exemplo)
- `project` e `core`: reserve `core` para mudanças de arquitetura e `project` para metadados/infra do repositório

Escolha e mantenha o padrão; atualize este ADR se decidir por outro mapeamento.

## Consequências

- Histórico de commits mais consistente; buscas e automações (CI, releases) se tornam mais confiáveis.
- Necessidade de disciplina ao criar commits — pode requerer revisão rápida de mensagens no PR.

## Exemplos de commits sugeridos

- `feat(wallet): initialize wallet table`
- `fix(strategy): correct profit calculation`
- `chore(adr): add ADR for commit scopes`