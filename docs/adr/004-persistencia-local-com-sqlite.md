# ADR-004: Persistência local com SQLite

- Status: Aceito
- Data: 2026-07-19

## Contexto

O projeto precisa armazenar informações básicas como carteira, histórico de ordens e estado local para análise. Não é desejável depender de um banco remoto em uma fase inicial, especialmente em um protótipo simples.

## Decisão

Usar SQLite como mecanismo de persistência local, com arquivo armazenado no diretório data/ do projeto.

A persistência será tratada por módulos de repositório, isolando o acesso ao banco e mantendo o restante do código mais limpo.

## Consequências

Essa escolha mantém a implementação simples e leve, porém oferece limitações em termos de concorrência e escalabilidade para cenários maiores.
