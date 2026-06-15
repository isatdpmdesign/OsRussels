---
name: continuidade-os-russels
description: Varre TODA a história de "Os Russels" antes de escrever um capítulo novo OU antes de afirmar/sugerir qualquer fato sobre a história (personagem, evento, objeto, linha do tempo, quem sabe o quê, quem chama quem de quê). Use SEMPRE antes de escrever e sempre que for fazer um apontamento factual. Produz uma ficha de continuidade com fonte (arquivo:linha) e sinaliza divergências entre o texto e a bíblia/sinopse.
---

# Continuidade — Os Russels

A regra que originou esta skill: **nunca afirme nada sobre a história a partir da memória.** A maioria dos erros graves de revisão veio de inventar por cima do que já estava escrito (a cadeira do pai, o afastamento do Erik, o dia da notícia, os nomes dos irmãos). Isso não pode depender da memória da autora para ser pego.

## Princípio da fonte de verdade

1. **O texto dos capítulos é a verdade suprema.** O que está escrito num capítulo publicado manda sobre tudo.
2. **A bíblia (`Os Russels/biblia-os-russels.md`) e a sinopse (`Os Russels/notas/sinopse-capitulos.md`) são guias — e podem estar erradas.** Se um guia divergir do texto, **o texto vence**, e o guia deve ser corrigido. (Já aconteceu: a sinopse dizia "Erik afastado", mas o Cap 17 diz que ele continua visitando às quartas.)
3. **Ao afirmar um fato, cite a fonte:** `arquivo:linha`. Se você não consegue citar a fonte, você não sabe o fato — então vá ler antes de afirmar.

## Quando rodar

- **Antes de escrever qualquer capítulo novo.**
- **Antes de fazer qualquer apontamento ou sugestão factual** sobre a história numa conversa com a autora.
- **Antes de plantar uma informação nova** (confirmar que ela não contradiz nem duplica nada já escrito).

## Onde varrer (TUDO, não só os dois últimos capítulos)

- Todos os capítulos em `Os Russels/livro-01-o-afilhado/capitulo-*.md`
- `Os Russels/biblia-os-russels.md`
- `Os Russels/notas/sinopse-capitulos.md`
- `Os Russels/notas/errata.md` e `Os Russels/notas/diretrizes.md`

## Procedimento

1. **Liste os fatos que o capítulo (ou a afirmação) vai tocar:** personagens presentes, lugares, objetos/símbolos, eventos passados referenciados, idades, relações, quem sabe o quê neste ponto da timeline.
2. **Para cada fato, busque em TODOS os arquivos** (grep por nome/tema + leitura do trecho em volta). Não confie no primeiro resultado: o mesmo fato pode aparecer com formulações diferentes em capítulos diferentes.
3. **Monte a ficha de continuidade** (formato abaixo), cada item com `arquivo:linha`.
4. **Sinalize divergências** entre o texto e a bíblia/sinopse. Quando achar uma, o texto vence; proponha corrigir o guia.

## Checklist do que sempre verificar

- **Linha do tempo:** em que mês/ano estamos; quanto tempo passou desde eventos-chave (a história está em agosto de 1830; a morte de Aarav faz ~18 meses; a prova de ingresso de Josh é em outubro).
- **Idades e descrições físicas:** não mudar nada estabelecido.
- **Nomes:** grafias canônicas (Casandra com um S; Erik com K; Eleonora, não Leonora) e nomes de personagens secundários.
- **Quem sabe o quê:** o conhecimento de cada personagem neste ponto. Ex.: Raj NÃO sabe da carta lacrada; Eleonora e Raj NÃO sabem da festa do celeiro (Aurora foi escondida); Josh nunca abriu a carta.
- **Quem chama quem de quê:** Aurora chama os pais de "papai"/"mamãe", nunca pelos nomes; Josh chama Raj de "padrinho" e Eleonora de "madrinha".
- **Objetos e símbolos:** estado e localização (livro de Oehlenschläger do Aarav com a mancha de tinta; pérgola de glicínias + roseiras no canto direito; banco de ferro que Aarav mandou fazer; a cadeira vazia do Aarav na Bredgade e a do Henrik na fazenda; cheiro de jasmim e canela da Aurora).
- **Relacionamentos atuais:** quem visita quem, quem corteja quem (Erik continua pretendente ativo, visitas de quarta).
- **Voz de cada personagem:** conferir antes de escrever diálogo (ver skill `romance-os-russels`).
- **Fios plantados:** setups que precisam de payoff e payoffs que dependem de setups.

## Formato de saída

```
## Ficha de continuidade — [capítulo/afirmação]

**Fatos canônicos relevantes:**
- [fato] — `arquivo:linha`
- [fato] — `arquivo:linha`

**Quem sabe o quê neste ponto:**
- [personagem]: sabe X, não sabe Y — `arquivo:linha`

**Divergências encontradas (texto vence):**
- [guia] diz A, mas [capítulo:linha] diz B → corrigir o guia

**Sinal verde / pontos de atenção para escrever:**
- [o que respeitar, o que evitar]
```
