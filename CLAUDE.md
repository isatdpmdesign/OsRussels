# Os Russels — instruções do projeto

Quinlogia de romance histórico (Dinamarca, 1830), estilo Bridgerton. A autora é Isadora. O trabalho de escrita acontece na branch `claude/book-writing-workflow-LnfjM`.

## Onde está cada coisa

- Capítulos: `Os Russels/livro-01-o-afilhado/capitulo-*.md`
- Bíblia (canon): `Os Russels/biblia-os-russels.md`
- Sinopse dos capítulos: `Os Russels/notas/sinopse-capitulos.md`
- Diretrizes e errata: `Os Russels/notas/`
- Skill mestre de escrita: `Os Russels/SKILL.md` (`romance-os-russels`)

## Regra de ouro — continuidade

**Nunca afirme, sugira ou escreva nada sobre a história a partir da memória.** Antes de escrever um capítulo, fazer um apontamento factual, ou plantar uma informação nova, **varra TODA a história** — todos os capítulos, a bíblia e a sinopse, não só os dois últimos capítulos. Rode a skill **`continuidade-os-russels`**.

- O **texto dos capítulos é a fonte de verdade suprema.** Bíblia e sinopse são guias e podem estar erradas; se divergirem do texto, o texto vence e o guia deve ser corrigido.
- Ao afirmar um fato, **cite a fonte** (`arquivo:linha`). Se não consegue citar, não sabe — vá ler antes.
- A maioria dos erros graves de revisão veio de inventar por cima do que já estava escrito. Isso não pode depender da memória da autora para ser pego.

## Fluxo ao escrever um capítulo

1. **Antes:** rodar `continuidade-os-russels` — montar a ficha de continuidade (timeline, quem sabe o quê, nomes, objetos, voz dos personagens, fios plantados).
2. **Escrever** seguindo a skill `romance-os-russels` (voz, ritmo de fogo baixo, estrutura).
3. **Depois:** rodar `revisao-sentimental` — revisar o tom humano e emocional (profundidade interior, diálogo, troca real entre personagens, emoção vivida x contada) com olhar de leitora apaixonada + beta-reader sincera.
4. **Atualizar** a sinopse (e a bíblia, se houver fato novo ou correção) e **commitar + push** na branch de trabalho.

## Tom

Fogo baixo, slow-burn, tensão sensorial. Bússola: Bridgerton/Julia Quinn e Sarah J. Maas. Mais voltagem = mais tensão e subtexto, não mais explícito — a contenção é proposital.
