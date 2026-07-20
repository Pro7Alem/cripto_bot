# ADR-002: Arquitetura modular em Python

- Status: Aceito
- Data: 2026-07-19

## Contexto

O projeto precisa separar responsabilidades claras entre conexão com exchange, análise de mercado, persistência e interface. Sem essa separação, o código tende a crescer de forma pouco manutenível.

## Decisão

Estruturar o projeto em módulos Python com responsabilidades bem definidas:

- core/main.py: ponto de entrada da aplicação
- core/exchange: integração com a exchange e sockets
- core/strategy: lógica de análise de mercado
- core/repository: persistência de dados
- core/display: interface de saída
- core/services: orquestração de operações

## Consequências

A arquitetura modular facilita testes, substituição de componentes e evolução do bot para cenários mais complexos sem reescrever o sistema inteiro.
