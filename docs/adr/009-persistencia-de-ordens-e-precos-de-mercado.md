# ADR-009: Persistência de ordens e preços de mercado

- Status: Aceito
- Data: 2026-07-21

## Contexto

Para analisar o comportamento do bot, é importante registrar não apenas a carteira, mas também as operações realizadas e as condições de mercado observadas ao longo do tempo.

## Decisão

Registrar em banco SQLite:

- ordens de compra e venda;
- preço de mercado em cada atualização relevante;
- volatilidade, tipo de mercado e força estimada.

## Consequências

A persistência passa a servir como histórico de operação e base para futura análise de desempenho, debugging e evolução da estratégia.
