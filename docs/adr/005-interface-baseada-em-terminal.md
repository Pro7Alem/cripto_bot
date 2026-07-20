# ADR-005: Interface baseada em terminal

- Status: Aceito
- Data: 2026-07-19

## Contexto

O projeto é um protótipo de observação e validação de sinais de mercado. Em um estágio inicial, uma interface visual completa não é prioridade, mas é necessário exibir informações de forma contínua e simples.

## Decisão

Construir a interface principal como um dashboard no terminal, com atualização em tempo real das informações mais relevantes: preço atual, saldos, volatilidade e classificação do mercado.

## Consequências

A interface terminal é simples de manter e executa bem em ambientes sem dependências gráficas. No entanto, ela oferece menos experiência visual e flexibilidade do que uma interface web ou desktop.
