---
numero: 0001
data: 2026-08-07
status: aceita
escopo: engenharia
substitui: —
substituida_por: —
---
# Separar motor de dados

## Contexto

As cinco skills originais do projeto (`continuidade-os-russels`,
`voz-isadora`, `revisao-pontuacao`, `revisao-sentimental`,
`auditoria-continuidade`) misturavam duas coisas: o **método** genérico e
os **dados** de Os Russels. A `continuidade-os-russels` conhecia caminhos
de arquivo específicos; a `voz-isadora` era noventa por cento a voz da
Isadora e dez por cento método anti-IA. Funcionava muito bem para uma
autora, e não escalava para nenhuma outra: cada usuária nova do OpenBooks
exigiria uma skill escrita à mão.

## Decisão

O motor mora em `.claude/` e não sabe quem é Josh ou Aurora. Os dados
moram no projeto: `livro.yaml` (o contrato — caminhos, precedência,
convenções, regras mecânicas) e `perfil/` (`voz.md` com a assinatura da
autora, `estilo.md` com as regras duras). Toda skill lê o contrato para
descobrir onde as coisas estão e quais regras valem. Trocar `livro.yaml` e
`perfil/` equivale a trocar de livro.

## Consequência

O repositório vira a especificação executável do produto: cada skill de
motor é um endpoint do OpenBooks, cada arquivo de projeto é uma linha de
tabela por usuária, e o `livro.yaml` é o registro do projeto no banco. As
skills antigas foram aposentadas e o conteúdo específico migrado para
`perfil/`.

O custo é indireção: para entender por que uma skill se comporta de certo
jeito agora é preciso abrir dois arquivos em vez de um. E há um risco
real de o contrato apodrecer — uma regra que muda no `perfil/estilo.md` e
não muda no `livro.yaml` faz o linter e a skill divergirem em silêncio.
Isso impede que regras de estilo sejam escritas soltas dentro de skills,
que era o caminho mais rápido.
