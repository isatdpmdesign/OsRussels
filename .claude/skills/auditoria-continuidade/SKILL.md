---
name: auditoria-continuidade
description: Auditoria sistemática pós-escrita de continuidade para "Os Russels". Pega cada AFIRMAÇÃO de fato no capítulo recém-escrito (eventos passados referenciados, "primeira vez / nunca tinha X", quem sabe o quê, idades, datas, distâncias, descrições físicas, localizações, nomes próprios) e cruza com TODOS os capítulos anteriores, a bíblia e a sinopse. Reporta cada divergência com fonte (arquivo:linha) e propõe correção. Use SEMPRE como passe final antes de fechar um capítulo, depois da voz-isadora e da revisao-sentimental. Diferente da continuidade-os-russels (pré-escrita: monta a ficha antes de afirmar), esta é pós-escrita (audita cada afirmação já escrita).
---

# Auditoria de Continuidade — passe pós-escrita

Esta skill roda DEPOIS que o capítulo está escrito e revisado. É o último passe antes de fechar.

A regra que originou esta skill: capítulo escrito sob pressão de inspiração ou tom afirma fatos que **contradizem o canon sem perceber**. Exemplo real: o Cap 21 afirmou *"Aurora estava entrando numa carruagem com Josh pela primeira vez"* — quando o canon dos `cap04:169`, `cap06:361`, `cap11:93` e `cap18:47` mostra que eles já dividiram carruagem várias vezes.

A skill **`continuidade-os-russels`** é PRÉ-escrita: monta a ficha de continuidade antes de afirmar. **Esta skill** é PÓS-escrita: audita cada afirmação já escrita contra o canon.

## Quando rodar

- Depois que o capítulo está escrito.
- Depois da **`voz-isadora`** (limpeza de tiques) e da **`revisao-sentimental`** (revisão de tom).
- **Antes** de fechar o capítulo como pronto.

## Procedimento

### 1. Extrair cada afirmação de fato

Varrer o capítulo procurando AFIRMAÇÕES — não impressões, não descrições poéticas, mas fatos que podem ser conferidos contra o canon. Categorias a procurar:

- **"Primeira vez" / "Nunca tinham X"** — categoria mais perigosa. Toda afirmação de "nunca" e "primeira" é candidata a furo.
- **Eventos passados referenciados** — "a primeira vez que", "desde X", "há Y meses", "no dia que".
- **Quem sabe o quê** — "ela sabia", "ele não sabia", "nunca tinha contado".
- **Idades, datas, durações** — "X anos", "três semanas", "às 5h45".
- **Localizações de eventos passados** — onde aconteceu o quê (beijo onde? festa onde? chegada como?).
- **Nomes próprios** — livraria, lugares, parentes, criadagem.
- **Relacionamentos** — "afilhado de", "pretendente de", "padrinho de".
- **Distâncias, horários, números** — "oito horas", "quarenta centímetros", "três passos".
- **Voz/maneirismos** — "do jeito que ele sempre", "como ela costumava".
- **Descrição física** — pele, cabelo, olhos, traços.
- **Inventário de objetos** — móveis, ferramentas, livros, presentes.

### 2. Para cada fato, grepar nos arquivos do canon

Arquivos a varrer:
- `Os Russels/livro-01-o-afilhado/capitulo-*.md` (todos os capítulos anteriores).
- `Os Russels/biblia-os-russels.md`.
- `Os Russels/notas/sinopse-capitulos.md`.
- `Os Russels/notas/errata.md` (se existir).
- `Os Russels/notas/diretrizes.md` (se existir).

Procedimento de busca:
1. Identificar 2-3 termos-chave do fato (substantivos + verbo principal).
2. `grep -rni "termo1\|termo2\|termo3" "Os Russels/"` — case-insensitive, em todos os arquivos.
3. Ler trechos retornados em contexto pra confirmar.
4. Citar fonte (arquivo:linha) ao reportar.

### 3. Categorizar cada fato

- **✓ Canônico** — bate com canon estabelecido. Sem ação. (Lista sumária no fim.)
- **⚠️ Inferido** — não contradiz canon, mas não tem fonte explícita. Anotar como assertiva razoável. Sinalizar pra a autora confirmar.
- **🚨 Furo** — contradiz canon. Reportar com fonte do canon + proposta de correção.

### 4. Reportar à autora

**Não corrigir sozinha.** Apresentar:
- Lista de furos (🚨) com canon citado e correção proposta.
- Lista de inferidos (⚠️) pra autora confirmar.
- Sumário dos canônicos (✓), sem detalhar.

## Tipos de furo mais comuns no projeto (do histórico)

1. **"Primeira vez" / "Nunca tinham X"** — afirmar que algo nunca aconteceu quando JÁ aconteceu no canon.
   - Cap 21: *"primeira carruagem juntos"* — eles já dividiram carruagem em cap 04, 06, 11, 18.
2. **Localização de eventos passados** — onde aconteceu o quê.
   - Cap 21: *"beijo na biblioteca"* — foi na sala de estar (cap 19).
3. **Nomes próprios** — livraria, lugares, parentes.
   - Cap 21: *"madame Soulberg"* — canon é *"Herr Møller"* (cap 01:151).
4. **Datas/idades** — propagação inconsistente.
   - Matias 16 vs 13; Henrik "três dias" vs canon "três semanas".
5. **Descrição física** — pele, cabelo.
   - Aurora *"retinta"* vs canon *"âmbar/bronze"* (cap 01:169, cap 02:141).
   - Cabelo do Josh: canon *"loiro-ruivo"*, não só *"loiro"*.
6. **Quem sabe o quê** — Aurora *"já sabia da carta"* cap 20 vs Aurora nunca soube canonicamente.
7. **Inventário de objetos** — banco de ferro vs banco de madeira (Josh envernizou; envernizar pressupõe madeira).
8. **Mecanismos inventados** — "a mãe disse pra guardar a carta até avisar" vs canon "Josh desconfia que é pra ele" (cap03:317).

## Formato de saída

```markdown
## Auditoria do Cap N

### 🚨 Furos confirmados ([número])

1. **`capN:linha`** — afirma:
   > "[citação]"

   **Canon contradiz** (`capX:linha`):
   > "[citação canônica]"

   **Proposta de correção:**
   > "[reescrita que respeita o canon]"

2. ...

### ⚠️ Inferidos (sem fonte canônica)

- "[fato afirmado]" (`capN:linha`) — não tem fonte; plausível. Decisão da autora.

### ✓ OK (sumário)

- [lista curta dos fatos verificados que batem com canon]
```

## Princípio

- **Não inventar correções** — só propor o que respeita o canon.
- **Não impor reescritas** — autora decide.
- **Citar fonte sempre** (arquivo:linha).
- **Se houver dúvida sobre o canon, ler antes de afirmar** — não vale dizer "acho que está em algum capítulo".
- **Lista exaustiva** — é melhor flagar 20 fatos pra confirmar do que pular um que vire furo.

## Quando NÃO rodar

- Pra trechos curtos (uma fala, um parágrafo).
- Pra correções de português / pontuação.
- Pra escrita nova ainda em rascunho — espere o capítulo estar fechado pra rodar.
