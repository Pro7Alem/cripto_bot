# ADR-010: Gestão de carteira e preço médio real

- Status: Proposto
- Data: 2026-07-21

## Contexto

A carteira atual registra saldo de BTC, USDT e custo, mas ainda não representa de forma precisa o preço médio real da posição acumulada. Isso pode levar a decisões de saída e avaliação de lucro inconsistentes.

## Decisão

A gestão da carteira deve evoluir para calcular o preço médio real da posição considerando o BTC recebido após a compra, incluindo os efeitos de fees.

## TODO

- calcular o preço médio real considerando BTC recebido após fee de compra;
- ajustar a lógica de lucro e stop loss para usar esse valor como referência;
- validar o comportamento em cenários com múltiplas compras.

## Consequências

Essa mudança melhora a precisão da avaliação de desempenho e reduz erros de cálculo em operações reais ou simuladas.
