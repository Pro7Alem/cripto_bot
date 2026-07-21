# ADR-007: Estratégia de trading baseada em regime de mercado

- Status: Aceito
- Data: 2026-07-21

## Contexto

O bot precisa tomar decisões de compra e venda automaticamente, mas ainda é um protótipo. Sem uma estratégia mínima bem definida, as operações podem ser inconsistentes e difíceis de avaliar.

## Decisão

Adotar uma estratégia simples baseada em três regras principais:

- comprar quando a carteira estiver vazia e o mercado estiver em regime lateral;
- vender para obter lucro quando a posição atingir um ganho mínimo;
- vender também em cenários de perda relevante ou quando o mercado deixa de ser lateral.

## Consequências

Essa estratégia oferece um ponto inicial claro para teste e evolução, embora seja limitada e possa ser substituída por uma abordagem mais robusta no futuro.
