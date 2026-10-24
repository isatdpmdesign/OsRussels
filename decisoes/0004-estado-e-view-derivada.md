---
numero: 0004
data: 2026-08-07
status: aceita
escopo: engenharia
substitui: —
substituida_por: —
---
# Estado de produção é view derivada, não arquivo

## Contexto

O projeto mantinha à mão seis documentos de estado: `MANIFESTO.md`,
`RETOMADA.md`, `ficha-continuidade.md`, `biblia-os-russels.md`,
`sinopse-capitulos.md` e `diretrizes.md`. Todos foram escritos com
cuidado. Todos divergiram. Em agosto de 2026 o MANIFESTO — o painel de
controle declarado do livro — descrevia uma obra de dezenove capítulos
com "cap 20 a escrever", enquanto existiam trinta e nove escritos; as
diretrizes estavam dezenove capítulos atrás e a errata, vinte e um.

A leitura errada seria "faltou disciplina". A disciplina existia e era
acima da média: há registro de rodadas, erratas numeradas e decisões
datadas. O que falhou foi o método, não a pessoa. Quem escreve prefere
escrever, e deve mesmo.

## Decisão

O que é calculável passa a ser calculado toda vez, pelo `estado.py`:
contagem de capítulos, ritmo por ato, distribuição de POV, alertas de
template, wrap e comprimento, e o frescor de cada guia (capítulo mais alto
citado versus o que existe). O `MANIFESTO.md` e o `RETOMADA.md` são
aposentados depois de migrado o conteúdo canônico que só existia neles.
Sobra em arquivo apenas o que exige julgamento: o que ainda falta decidir.

## Consequência

O estado deixa de mentir, e a detecção de guia desatualizado passa a ser
automática em vez de depender de alguém desconfiar. No OpenBooks isso é a
tela inicial do projeto, e é uma feature que nenhum concorrente sem
repositório consegue oferecer.

O custo é que o relatório é frio: ele diz que o capítulo 39 tem 2.304
palavras, não que o final está fraco. Número serve para saber **onde
olhar** e não substitui ler — tratar a tabela como juízo literário seria
trocar um erro por outro.
