---
name: estado-do-projeto
description: Responde "onde o livro está?" com números derivados dos arquivos, não de documento mantido à mão. Roda o estado.py e interpreta - quantos capítulos, ritmo por ato, distribuição de POV, alertas de template e comprimento, e quais guias ficaram para trás. Use ao retomar o projeto depois de um tempo, antes de planejar um bloco de trabalho, ou quando desconfiar que a documentação divergiu do texto.
---

# Estado do projeto — a verdade calculada

```bash
python3 .claude/tools/estado.py --projeto "Os Russels"
```

## Por que isto não é um arquivo

Este projeto manteve, à mão, seis documentos de estado: MANIFESTO,
RETOMADA, ficha, bíblia, sinopse e diretrizes. Todos foram escritos com
cuidado. Todos divergiram. Em determinado momento o painel de controle do
livro descrevia um livro com doze capítulos a menos do que o que existia.

A lição não é "faltou disciplina" — a disciplina existia e era boa. É que
**estado de produção não sobrevive à manutenção manual.** Quem escreve
prefere escrever, e deve mesmo.

Então: o que é calculável é calculado, toda vez. O que sobra de julgamento
— o que ainda falta decidir — é a única parte que merece um arquivo.

## O que o relatório traz

| Seção | Para quê |
|---|---|
| **Totais** | tamanho real da obra |
| **Ritmo por ato** | média, mínimo e máximo de palavras — onde a obra afina |
| **POV por ato** | quem some, e em que altura do livro |
| **Alertas** | template fora do padrão, wrap estourado, capítulo curto ou longo demais |
| **Frescor dos guias** | capítulo mais alto citado em cada guia × o que existe |

## Como interpretar

**Ritmo.** Um livro saudável fica mais denso perto do fim. Se a média cai
no desfecho, cenas que mereciam ser encenadas foram resumidas — é o
defeito mais comum de rascunho terminado, e o mais barato de consertar.
Queda de 40% ou mais entre a subida e o desfecho é alarme.

**POV.** Conte por ato, nunca só no total. Um protagonista pode ter 40%
do livro e mesmo assim sumir inteiro no clímax — o total esconde
exatamente o que importa.

**Frescor.** Um guia muito atrás não está "desatualizado": está
**mentindo**, e alguém vai consultá-lo achando que é fonte. É trabalho
para o `escriba-de-canon`, e é urgente na proporção de quem lê aquele
arquivo.

**Alertas de template** parecem cosméticos e não são: é do cabeçalho que
a exportação de EPUB deriva a estrutura do sumário.

## Limites

Isto conta e compara. **Não lê.** Ele diz que o capítulo tem 2.304
palavras; não diz se são boas. Para julgar a forma, use `arco`; para
julgar a cena, `revisao-sentimental`.

Número serve para saber **onde olhar** — não substitui olhar.

## Saída esperada

Reporte os números e depois **2 a 3 conclusões**, cada uma ancorada num
número, com o que fazer. Sem conclusão, é só uma tabela.
