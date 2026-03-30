# Cripto_bot

## Descrição

Protótipo de sistema de trading algorítmico para o par **BTC/USDT** na Binance. O objetivo é explorar a automação de decisões de curto prazo com base em sinais de preço em tempo real — processando um stream contínuo de ticks, classificando o regime de mercado e executando ordens programaticamente. O foco atual é validar a lógica da estratégia em ambiente controlado antes de qualquer operação com capital real.

## Status

Pausado

## Funcionalidades

- **Coleta de preços em tempo real** — conexão via WebSocket com a Binance Trade Stream para ingestão contínua de ticks do par BTCUSDT
- **Análise de mercado** — classificação dinâmica do regime de mercado (lateral, moderado, volatile-uptrend, volatile-downtrend) com base em volatilidade e slope da janela de preços
- **Métrica de força de tendência** — estimativa da intensidade direcional (weak, medium, strong) via slope percentual
- **Estratégia lateral (scalping)** — lógica de entrada e saída para mercados de baixa volatilidade, com take profit em +0,5% e stop loss em -0,3%, descontando fee de 0,2%
- **Cooldown entre trades** — janela mínima de 20 ticks entre operações para reduzir overtrading
- **Buyback automático** — reentrada após take profit quando há saldo USDT disponível
- **Persistência em SQLite** — estado da carteira e histórico de ordens armazenados localmente
- **Log live no terminal** — exibição em tempo real de preço atual, saldo BTC/USDT, volatilidade e regime de mercado via stdout inline (sem scroll)
- **Integração com Binance API** — execução de ordens a mercado via `python-binance` assíncrono

## Tecnologias

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Binance](https://img.shields.io/badge/Binance-FCD535?style=for-the-badge&logo=binance&logoColor=white)

## Observações

- **Protótipo experimental** — a estratégia foi testada na Binance Testnet, mas ainda não obteve resultado positivo consistente. Não validado em cenário real. Sujeito a risco alto e não deve ser usado com capital real no estado atual.
- **Estratégia de scalping lateral** — projetada para mercados com volatilidade abaixo de 0,5% na janela de 20 ticks. Em regimes de tendência forte, o stop é antecipado para preservar capital. Parâmetros ainda em calibração.
- **Gestão de risco embutida** — o cálculo de lucro desconta o fee de 0,2% (taker fee padrão da Binance), garantindo que o take profit só seja acionado com ganho líquido positivo.
- **Arquitetura monolítica** — lógica centralizada em `app.py` para simplicidade na fase inicial. Modularização prevista conforme o projeto amadurece.
- **Melhorias previstas** — backtesting com dados históricos (OHLCV), calibração dos parâmetros de take profit/stop loss, gestão de posição dinâmica. O sistema já classifica todos os regimes de mercado — **lateral**, **moderado**, **volatile-uptrend** e **volatile-downtrend** — mas ainda opera apenas no lateral. A implementação de estratégias dedicadas para os demais regimes é o próximo passo estrutural.