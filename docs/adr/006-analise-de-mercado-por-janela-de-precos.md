# ADR-006: Análise de mercado por janela de preços

- Status: Aceito
- Data: 2026-07-19

## Contexto

Para classificar o mercado, o bot precisa interpretar movimentos recentes de preço. Uma análise baseada em uma janela curta de dados permite observar comportamento local sem adicionar complexidade desnecessária.

## Decisão

Usar uma janela fixa de 20 preços recentes para calcular volatilidade e classificar o regime de mercado em lateral, moderado ou em tendência.

A análise considera:

- amplitude do intervalo de preços;
- variação entre o primeiro e o último preço da janela;
- classificação do comportamento em tempo real.

## Consequências

Essa abordagem é simples e eficiente para um protótipo, mas pode ser limitada em cenários com ruído de mercado ou mudanças rápidas de regime.
