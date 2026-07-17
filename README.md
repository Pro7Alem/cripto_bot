# Cripto_bot

## Descrição

Protótipo simples de bot de trading para o par BTC/USDT na Binance. O projeto coleta preços em tempo real, analisa o mercado e exibe informações no terminal para apoiar decisões de operação em ambiente controlado.

## Status

Em desenvolvimento.

## Funcionalidades

- Coleta de preços em tempo real via WebSocket da Binance
- Análise do mercado com classificação em regimes como lateral, moderado e tendência
- Cálculo de força de tendência
- Painel live no terminal com preço, saldo e volatilidade
- Persistência local em SQLite para carteira e histórico de ordens
- Integração com a API da Binance para ordens a mercado

## Instalação

Requisitos:
- Python 3.11+
- pip

Passos:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crie um arquivo `.env` com suas credenciais da Binance:

```env
API_KEY=seu_api_key
API_SECRET=seu_api_secret
```

## Execução

Para iniciar o bot:

```bash
python -m core.main
```

O projeto usa a Binance Testnet por padrão, então o fluxo é voltado para testes e validação.

## Estrutura dos módulos

- `core/main.py` — ponto de entrada do bot
- `core/exchange/` — conexão com a Binance, WebSocket e ordens
- `core/strategy/` — lógica de análise e classificação de mercado
- `core/services/` — execução de compras e vendas
- `core/repository/` — acesso ao banco SQLite e persistência de dados
- `core/display/` — painel visual no terminal
- `core/utils/` — helpers auxiliares de trading
- `data/` — diretório para arquivos locais, como o banco de dados

## Observações

- O projeto ainda é experimental e não deve ser usado com capital real sem validação adequada.
- A estratégia atual está mais voltada para análise e testes do que para operação automatizada completa.
- As dependências principais incluem `python-binance`, `python-dotenv`, `requests`, `aiohttp` e `sqlite3` via biblioteca padrão do Python.