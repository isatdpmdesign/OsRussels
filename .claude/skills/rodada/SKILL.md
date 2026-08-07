---
name: rodada
description: O ciclo completo de um capítulo, do planejamento ao commit, e a rodada de revisão da autora. Use quando for escrever um capítulo novo, reescrever um existente, ou aplicar os comentários que a autora deixou no app. Orquestra as outras skills na ordem certa e registra cada rodada em revisao/rodadas.jsonl com antes, depois e porquê.
---

# Rodada — o ciclo de um capítulo

Esta skill não faz o trabalho: ela **chama quem faz, na ordem certa, e
registra o que aconteceu.** É o maestro.

## Ciclo A — capítulo novo ou reescrita

```
1. biblioteca            ficha do que é canon nesta cena
2. capitulo              beats, POV, onde abre e onde corta
   → confirmar com a autora antes de escrever
3. prosa                 escrever
4. revisao-voz           tique de máquina + assinatura da autora
5. revisao-sentimental   profundidade, diálogo, emoção vivida
6. revisao-de-pov        o que essa cabeça pode saber
7. revisao-de-linha      a frase
8. revisao-mecanica      lint.py + triagem
9. auditoria-de-canon    cada afirmação contra a obra
10. escriba-de-canon     absorve nos guias (sinopse, ficha, bíblia)
11. registrar a rodada + commit + push
```

A ordem não é arbitrária. Cada passe pressupõe o anterior resolvido, e
caçar vírgula em parágrafo que ainda vai ser reescrito é trabalho jogado
fora. Os passes caros (voz, sentimental) vêm antes dos baratos (linha,
mecânica) porque eles mudam texto; os baratos só confirmam.

## Ciclo B — rodada de revisão da autora

A autora lê pelo app e comenta linha a linha. Os comentários chegam em
`revisao/comentarios.jsonl`:

```json
{"id": "c-...", "capPath": "...", "contexto": "trecho citado",
 "bloco": 143, "tipo": "correcao|regra",
 "texto": "o que ela pediu", "estado": "novo|aplicado",
 "criadoEm": "..."}
```

**Procedimento:**

1. **Colete TODOS os comentários novos do capítulo.** Não perca nenhum —
   é a queixa mais fácil de gerar e a mais difícil de perdoar. Trabalhe da
   lista, não da memória.
2. **Separe por tipo.** `correcao` vale para aquele trecho. **`regra`
   vale para o livro inteiro** e provavelmente é decisão editorial nova —
   veja abaixo.
3. **Aplique um a um**, na ordem do capítulo.
4. **Rode os quatro passes de novo** por cima das mudanças. Comentário
   aplicado é texto novo, e texto novo não passou por passe nenhum.
5. **Registre a rodada** e marque os comentários como `aplicado`.
6. Commit com changelog do que foi aplicado.
7. Repita até a autora aprovar. Só então o próximo capítulo.

### Comentário do tipo `regra` é decisão editorial

Quando a autora diz *"já conversamos que esse tipo de diálogo não pode
existir"*, ela não está corrigindo um parágrafo — está estabelecendo lei.

**Todo comentário `regra` vira entrada em `decisoes-editoriais.md`**
(via `escriba-de-canon`) e, se for verificável por máquina, **vira regra
no `livro.yaml`** para o `lint.py` pegar sozinho da próxima vez.

É assim que o sistema aprende a régua dela em vez de precisar ser
lembrado. Uma regra que a autora precisa repetir duas vezes é uma falha
do sistema, não da memória dela.

## O registro da rodada

Toda rodada entra em `revisao/rodadas.jsonl`, uma linha por rodada:

```json
{"id": "r-capNN-AAAAMMDDHHMMSS",
 "capPath": "...",
 "quando": "ISO-8601",
 "autor": "claude-code",
 "resumo": "uma frase do que a rodada fez",
 "comentarioIds": ["c-...", "c-..."],
 "mudancas": [
   {"antes": "...", "depois": "...",
    "porque": "motivo + fonte canônica + [coment. #N]"}
 ]}
```

**O campo `porque` é o mais importante do arquivo.** Ele é o que
transforma um log em conhecimento: não "a IA escreveu X", mas "a IA
escreveu X, a autora recusou, virou Y, por este motivo". Escreva-o para
ser lido daqui a seis meses por alguém que não estava na conversa.

Cite a fonte canônica quando a mudança for de continuidade
(`cap03:163`), e o número do comentário quando vier da autora.

## Autonomia

Quando a autora disser para seguir sem revisão dela (*"termina o livro"*,
*"pode ir"*), execute as rodadas completas sozinho — os passes substituem
a leitura dela até ela voltar. Os comentários que ela deixar depois entram
como Ciclo B normal, capítulo por capítulo.

Autonomia **não** afrouxa nenhum passe. Ela remove a aprovação, não a
verificação. O terço final deste livro foi escrito em autonomia e é
mensuravelmente mais fino que o resto — capítulos com metade das palavras
dos anteriores. Escrever sozinho é permissão para seguir, nunca para
apressar.
