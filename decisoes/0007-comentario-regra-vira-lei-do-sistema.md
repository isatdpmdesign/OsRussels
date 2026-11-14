---
numero: 0007
data: 2026-08-07
status: aceita
escopo: processo
substitui: —
substituida_por: —
---
# Comentário do tipo "regra" vira lei do sistema

## Contexto

A autora revisa pelo celular, comentando linha a linha, e os comentários
chegam estruturados em `revisao/comentarios.jsonl` com um campo `tipo`
que distingue `correcao` de `regra`. A diferença é enorme e estava sendo
tratada igual. Quando ela escreve *"mais uma vez frases monossilábicas,
já conversamos que esse tipo de diálogo não pode existir"*, ela não está
corrigindo um parágrafo — está repetindo uma lei que o sistema não
aprendeu. O "mais uma vez" é o sintoma.

O `rodadas.jsonl` guarda, para cada mudança, `antes`, `depois` e
`porque`. Isso é um registro rotulado do julgamento editorial dela: não
"a IA escreveu X", mas "a IA escreveu X, a autora recusou, virou Y, por
este motivo". É o ativo mais valioso do repositório para o produto, e não
estava no briefing.

## Decisão

Todo comentário do tipo `regra` vira entrada datada em
`decisoes-editoriais.md`, via `escriba-de-canon`. Se for verificável por
máquina, vira também regra no `livro.yaml` para o `lint.py` pegar sozinho
da próxima vez. O `perfil-de-voz` passa a se alimentar do histórico de
rodadas, porque **o que a autora recusa ensina mais sobre a voz dela do
que o que ela escreve**.

## Consequência

O sistema aprende a régua da autora em vez de precisar ser lembrado, e
passa a valer a métrica: **regra que a autora precisa repetir duas vezes é
falha do sistema, não da memória dela.** No OpenBooks, esse mesmo
histórico é o que permite avaliar se um agente está melhorando ou
piorando — nenhum concorrente sem repositório tem esse sinal.

O custo é disciplina de captura: se os comentários deixarem de ser
classificados por tipo, ou se as rodadas forem registradas sem o campo
`porque` preenchido de verdade, o mecanismo inteiro degrada para um log
comum. O campo `porque` precisa ser escrito para alguém entender daqui a
seis meses, sem ter estado na conversa.
