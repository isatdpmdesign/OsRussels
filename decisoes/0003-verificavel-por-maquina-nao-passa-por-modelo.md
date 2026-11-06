---
numero: 0003
data: 2026-08-07
status: aceita
escopo: engenharia
substitui: —
substituida_por: —
---
# O que é verificável por máquina não passa por modelo

## Contexto

A skill `revisao-pontuacao` era um checklist de `grep` escrito em
Markdown, executado por um modelo a cada rodada. Custava uma chamada por
capítulo para fazer um trabalho que `grep` faz de graça, e tinha um
defeito silencioso: os padrões eram por **linha**, e a partir do capítulo
25 o livro passou a ter hard wrap de 50 caracteres. Uma fala quebrada em
oito linhas deixava de casar com qualquer padrão. O passe rodava, dizia
que estava tudo bem, e não tinha olhado nada.

## Decisão

Tudo que é verificável por máquina vira código determinístico em
`.claude/tools/`, com as regras declaradas no `livro.yaml`. O `lint.py`
implementa onze regras trabalhando por **parágrafo**, e a skill
`revisao-mecanica` deixa de procurar: ela roda a ferramenta e **tria** o
resultado, que é a parte que exige julgamento (uso literal de "peso"
passa, metafórico não).

## Consequência

O passe mecânico fica gratuito, reproduzível e imune a alucinação, e a
margem do produto melhora na parte mais repetitiva do trabalho. As regras
ficam auditáveis num arquivo só, em vez de espalhadas em prosa dentro de
skills.

O custo aparece na precisão: a lista de aberturas interrogativas herdada
produzia cerca de setenta por cento de falso positivo, porque este livro
usa constatação de propósito ("Você vai casar com o Lauritz."). Foi
preciso medir e dividir a regra em duas — alta confiança no passe padrão,
ambígua sob demanda. **Regra determinística exige calibragem medida antes
de ser ligada;** ligar sem medir produz ruído, e ruído faz a autora parar
de olhar o relatório, que é pior do que não ter relatório.
