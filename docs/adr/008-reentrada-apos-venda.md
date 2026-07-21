# ADR-008: Reentrada após venda

- Status: Aceito
- Data: 2026-07-21

## Contexto

Após vender uma posição, o bot precisa decidir se deve esperar por nova oportunidade ou tentar recomprar rapidamente. Sem essa regra, o sistema pode agir de forma impulsiva ou perder boas entradas.

## Decisão

Implementar uma lógica de reentrada que inicia após uma venda e monitora o mercado por um número mínimo de observações antes de tentar uma nova compra.

A regra considera:

- preço de venda anterior;
- quantidade de preços observados após a venda;
- se o mercado voltou a um perfil lateral.

## Consequências

A reentrada melhora a capacidade do bot de aproveitar novos movimentos sem depender apenas de uma única entrada. Ainda assim, a regra é conservadora e pode ser refinada com dados reais de desempenho.
