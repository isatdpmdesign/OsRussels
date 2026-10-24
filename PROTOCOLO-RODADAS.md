# Protocolo de Rodadas — Os Russels

> Reconstruído em sessão a partir do fluxo real de trabalho entre a Isadora e o Claude.
> Se a autora tiver uma versão própria deste arquivo, ela substitui esta.

## O ciclo de cada capítulo (uma "rodada")

1. **Pré-escrita** — Claude consulta `ficha-continuidade.md` + `decisoes-editoriais.md` e roda `continuidade-os-russels` (grep + leitura dos trechos canônicos; nunca de memória).
2. **Escrita** — capítulo novo seguindo `romance-os-russels`, hard wrap 50, todas as regras duras.
3. **Passes obrigatórios, nessa ordem:**
   - `voz-isadora` — caça tiques de IA, puxa a voz da autora.
   - `revisao-sentimental` — profundidade interior, diálogo com troca real, emoção vivida.
   - `revisao-pontuacao` — interrogações, travessão só em fala, blacklist, sujeira mecânica.
   - `auditoria-continuidade` — cada afirmação de fato contra o canon (arquivo:linha).
4. **Atualização das notas** — `sinopse-capitulos.md` (resumo ~150 palavras), `ficha-continuidade.md` (fatos novos), `decisoes-editoriais.md` (se houver decisão nova).
5. **Commit + push** na branch `claude/book-writing-workflow-LnfjM`.

## A rodada de revisão da autora

6. Isadora lê pelo app do GitHub (PR #3) e comenta linha a linha, ou manda observações pelo chat.
7. Claude coleta TODOS os comentários novos (sem perder nenhum), aplica um a um, e roda os 4 passes de novo por cima das mudanças.
8. Commit + push com changelog detalhado do que foi aplicado.
9. Repetir até a autora aprovar o capítulo. Só então começa o próximo.

## Regras duras que valem em toda rodada

- Falas simples — se precisa reler pra entender, está errada.
- Vocativo isolado ("— Aurora." / "— Sim.") só com entonação atribuída ou silêncio dramático narrado.
- "Boa" banida como concordância (não é 1830). "Tá" com moderação.
- Diálogo bate-volta com reações construídas é o padrão; reservado ≠ mudo.
- Travessão SÓ em fala. Sem artigo antes de nome próprio. Sem tu/teu. Sem "peso" metafórico.
- Interrogação em toda pergunta. Exclamação onde há entusiasmo.
- Comentários da autora anulam qualquer instrução genérica de skill.

## Autonomia

Quando a autora disser pra seguir sem revisão dela (ex.: "termina o livro"), Claude executa as rodadas completas sozinho — os 4 passes substituem a leitura dela até ela voltar. Os comentários que ela deixar depois entram como rodada de revisão normal, capítulo por capítulo.
