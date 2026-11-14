---
numero: 0006
data: 2026-08-07
status: aceita
escopo: produto
substitui: —
substituida_por: —
---
# Diagramadora e narradora saem da Fase 1, e não são agentes

## Contexto

Dois dos seis agentes do briefing eram a **Diagramadora** (exportar EPUB e
PDF) e a **Narradora** (pipeline de TTS por capítulo). Eles não são da
mesma natureza dos outros quatro: exportar EPUB é pandoc mais CSS mais
validação, e TTS é chamada de API mais concatenação de blocos. Não há
julgamento a delegar — há um passo determinístico a executar igual toda
vez. Chamá-los de agentes injeta não-determinismo exatamente onde se quer
reprodutibilidade: ninguém quer que a diagramação do capítulo 12 saia
diferente na segunda exportação.

Além disso, nenhum dos dois ajuda a terminar o livro, que é o teste
declarado da Fase 1 no próprio briefing.

## Decisão

Os dois são fundidos numa etapa única de **Produção** — um pipeline de
build, não um agente — e ficam para a Fase 3. Fica registrado desde já o
requisito técnico já identificado pela autora: **gerar TTS frase a frase
quebra a prosódia; gerar por blocos com contexto e costurar.**

Fica registrado também um pré-requisito descoberto no diagnóstico: os
capítulos 30 a 39 usam um cabeçalho diferente dos anteriores e o capítulo
21 tem um `#` indentado que o Markdown lê como bloco de código. É do
cabeçalho que a exportação deriva o sumário, então a normalização do
template é trabalho de revisão, não de produção — e precisa acontecer
antes.

## Consequência

Sobram recursos para as quatro peças que efetivamente terminam o livro, e
o produto não carrega código de exportação antes de existir um livro para
exportar. A Diagramadora deixa de ser bloqueada por decisão de design e
passa a ser bloqueada apenas pela higiene do template — que é barata.

O custo é que o OpenBooks fica, por enquanto, sem os dois momentos de
cobrança mais óbvios do modelo "preço por obra": EPUB diagramado e
audiobook. A receita da Fase 3 depende de construí-los, e adiar demais
adia a monetização inteira.
