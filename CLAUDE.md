# Os Russels — instruções do projeto

Quinlogia de romance histórico (Dinamarca, 1830), estilo Bridgerton. A autora é Isadora. O trabalho de escrita acontece na branch `claude/book-writing-workflow-LnfjM`.

## Onde está cada coisa

- Capítulos: `Os Russels/livro-01-o-afilhado/capitulo-*.md`
- Bíblia (canon): `Os Russels/biblia-os-russels.md`
- Sinopse dos capítulos: `Os Russels/notas/sinopse-capitulos.md`
- **Ficha de continuidade** (índice rápido de fatos): `Os Russels/notas/ficha-continuidade.md`
- **Decisões editoriais** (palavra final da autora, datada): `Os Russels/notas/decisoes-editoriais.md`
- Diretrizes de diálogo e errata: `Os Russels/notas/`
- Skill mestre de escrita: `Os Russels/SKILL.md` (`romance-os-russels`)

## Regra de ouro — continuidade

**Nunca afirme nada da história a partir da memória.** Antes de afirmar um fato:

1. Consulte primeiro a **`ficha-continuidade.md`** (índice rápido). Ela já cita `arquivo:linha`.
2. Para qualquer **citação verbatim** ou cena nova que dependa do fato, **abra o capítulo e leia o trecho** — não confie só no índice.
3. **O texto dos capítulos é a fonte de verdade suprema.** Bíblia, sinopse e ficha são guias; se divergirem do texto, o texto vence e o guia deve ser corrigido.
4. Antes de escrever um capítulo grande, rodar a skill **`continuidade-os-russels`** (varre o canon montando ficha pré-escrita).

## Subagentes — uso restrito

**Subagentes podem alucinar canon** (já aconteceu: idades inventadas, descrições erradas, números de linha falsos).

- ✅ **OK:** triagem ampla, busca exploratória, levantamento de áreas.
- ❌ **NUNCA:** afirmar idade, descrição, evento ou citação canônica direto da resposta do subagente sem grepar e ler o trecho original.
- ✅ **OBRIGATÓRIO:** todo fato canônico que vai entrar em texto novo passa por mim (grep + Read) antes de escrever.

## Decisões editoriais

Toda decisão da autora sobre voz, canon ou estilo entra em `notas/decisoes-editoriais.md`. **Essas decisões anulam qualquer instrução genérica de skill.** Consultar antes de escrever ou revisar.

Inclui a **blacklist** (palavras/frases banidas), as **regras duras de estilo** (travessão só em fala, sem artigo antes de Josh/Aurora etc.) e as **correções de canon** já cimentadas.

## Fluxo ao escrever um capítulo

1. **Antes:** consultar `ficha-continuidade.md` + `decisoes-editoriais.md`. Se for capítulo novo grande, rodar `continuidade-os-russels` pra ficha pré-escrita.
2. **Escrever** seguindo `romance-os-russels` (voz, ritmo de fogo baixo, estrutura).
3. **Depois (passe obrigatório, nessa ordem):**
   - **`voz-isadora`** — caçar tiques de IA + puxar voz da autora.
   - **`revisao-sentimental`** — profundidade interior, diálogo, troca real, emoção vivida × contada.
   - **`revisao-pontuacao`** — passe mecânico (interrogações faltando, travessões em narração, blacklist, sujeira).
   - **`auditoria-continuidade`** — cada afirmação de fato contra o canon.
4. **Atualizar** `sinopse-capitulos.md` (com resumo descritivo do capítulo escrito, ~150 palavras), `ficha-continuidade.md` (se houver fato novo), `decisoes-editoriais.md` (se houver nova decisão da autora).
5. **Commit + push** na branch de trabalho.

## Branch e merge

- Trabalho sempre na branch `claude/book-writing-workflow-LnfjM`.
- A autora **não faz git** — Claude é responsável por commit, push e qualquer merge eventual em `main`.
- Por enquanto **não fazer merge automático em main** sem pedido explícito da autora — manter `main` como ponto de "release oficial" que ela controla.

## Tom

Fogo baixo, slow-burn, tensão sensorial. Bússola: Bridgerton/Julia Quinn e Sarah J. Maas. Mais voltagem = mais tensão e subtexto, não mais explícito — a contenção é proposital.
