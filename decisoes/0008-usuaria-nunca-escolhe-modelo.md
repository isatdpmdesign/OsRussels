---
numero: 0008
data: 2026-08-07
status: aceita
escopo: produto
substitui: —
substituida_por: —
---
# A usuária nunca escolhe modelo

## Contexto

Decisão da autora, registrada aqui porque muda o que o motor faz. O
concorrente direto (NovelCrafter) usa chave própria da usuária via
OpenRouter e expõe a escolha de modelo, roteador e janela de contexto. O
diagnóstico dela sobre isso é preciso: **o problema não é o BYOK — é
fazer a romancista escolher modelo, roteador e contexto.** Isso é pedir
que a autora vire engenheira de prompt para conseguir escrever ficção.

## Decisão

O roteamento é por tarefa e invisível: contexto longo e barato (bíblia,
continuidade, cruzamento de capítulos) num motor; prosa e voz em outro.
Nenhum nome de modelo aparece na interface. A conexão de chave própria só
é oferecida quando a usuária encosta no limite da cota gratuita, como um
fluxo de noventa segundos com validação instantânea.

Como consequência direta, as skills de motor não mencionam modelo,
provedor nem janela de contexto — a escolha é do roteador, não do prompt.

## Consequência

O onboarding fica em zero configuração, e a meta de primeiro capítulo em
cinco minutos sem colar chave passa a ser possível. Some a categoria
inteira de decisão que a usuária não tem repertório para tomar e que a
faria desistir na primeira tela.

O custo é que o produto assume a conta e o risco de qualidade: se o
roteador escolher mal, a usuária não tem alavanca nenhuma para corrigir —
ela não sabe o que mudou nem como pedir outra coisa. Isso obriga a manter
avaliação própria de qualidade por tarefa (é para isso que o
`rodadas.jsonl` serve) e torna o cache de prompt obrigatório, já que
reenviar a bíblia a cada chamada é o que de fato custa em ficção, não a
saída.
