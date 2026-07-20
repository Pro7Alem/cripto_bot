# ADR-003: Integração com Binance Testnet e WebSocket

- Status: Aceito
- Data: 2026-07-19

## Contexto

O projeto é um protótipo e deve permitir validação segura antes de qualquer uso real. A integração com a Binance exige autenticação e acesso a dados em tempo real, o que aumenta o risco de ações indevidas em ambiente de produção.

## Decisão

Usar a API da Binance com o modo testnet ativo por padrão e consumir preços em tempo real por WebSocket.

Isso permite:

- testar fluxos de conexão e processamento sem risco financeiro;
- observar o comportamento do bot em tempo real;
- manter o projeto alinhado com o cenário de validação inicial.

## Consequências

A abordagem reduz riscos operacionais, mas também limita a execução a um ambiente de simulação e exige cuidado ao migrar para uso real.
