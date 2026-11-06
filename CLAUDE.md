# Os Russels · OpenBooks — instruções do projeto

Dois projetos no mesmo repositório, de propósito:

- **Os Russels** — quinlogia de romance histórico (Dinamarca, 1830, estilo
  Bridgerton). Autora: **Isadora**. Livro 1, *O Afilhado*: **rascunho
  completo, 39 capítulos, em revisão.**
- **OpenBooks** — o SaaS de escrita de ficção que nasce daqui. Briefing em
  `CONTEXTO-OPENBOOKS.md`.

A estratégia é essa mesma: os agentes se constroem como skills **dentro**
do livro real e provam o valor terminando o livro. O que sobreviver ao uso
vira especificação do produto; o que nunca for usado foi economizado.

---

## A arquitetura: motor × dados

O que é **método** é genérico e mora em `.claude/`. O que é **deste
livro** mora no projeto. Entre os dois há um contrato.

```
.claude/
  skills/        16 skills de motor — não sabem quem é Josh ou Aurora
  agents/         5 subagentes (todos somente leitura)
  tools/          lint.py · estado.py  — determinístico, custo zero

Os Russels/
  livro.yaml     ← O CONTRATO: caminhos, precedência, convenções, regras
  perfil/        voz.md (assinatura da autora) · estilo.md (regras duras)
  biblia-os-russels.md
  notas/         ficha-continuidade · sinopse · decisoes-editoriais · errata
  livro-01-o-afilhado/capitulo-NN-slug-pov.md

decisoes/        decisões de produto e engenharia, numeradas
revisao/         comentarios.jsonl · rodadas.jsonl (as rodadas da autora)
```

**Trocar `livro.yaml` + `perfil/` = trocar de livro.** É isso que
transforma este repositório na especificação do OpenBooks.

---

## Regra de ouro — continuidade

**Nunca afirme nada da história a partir da memória.**

1. Consulte a **`ficha-continuidade.md`** (índice rápido, já cita
   `arquivo:linha`).
2. Para **citação verbatim** ou cena nova que dependa do fato, **abra o
   capítulo e leia o trecho**. O índice localiza; ele não confirma.
3. **O texto dos capítulos é a fonte de verdade suprema.** Precedência em
   `livro.yaml`: `capítulos > decisões > bíblia > sinopse > ficha`. Guia
   que diverge do texto está errado por definição.
4. Antes de escrever, rode a skill **`biblioteca`**.

---

## Leitura e escrita de canon são separadas

| | |
|---|---|
| **Leem** | `biblioteca`, `auditoria-de-canon`, e todo o resto |
| **Escreve** | **só** `escriba-de-canon`, e sempre por diff aprovado |

Um agente que lê e escreve canon fecha um ciclo: aluciona um fato, grava
na ficha, e na sessão seguinte lê a própria alucinação como fonte. Já
aconteceu aqui na versão benigna.

**Nenhuma alteração de canon acontece em silêncio.** Nem para consertar um
número óbvio.

---

## Subagentes

Os cinco de `.claude/agents/` **não têm ferramenta de escrita** — o pior
que fazem é uma resposta errada, não uma resposta errada gravada. Some-se
a isso a regra de citação obrigatória e o problema antigo (subagente
inventando idade, descrição e número de linha) fica contido pelo desenho,
não pela vigilância.

Ainda assim: **fato canônico que vai entrar em texto novo passa por
`grep` + leitura antes de ser escrito.**

---

## O ciclo de um capítulo

Skill **`rodada`** orquestra. Resumo:

```
biblioteca → capitulo → [confirmar com a autora] → prosa
  → revisao-voz → revisao-sentimental → revisao-de-pov
  → revisao-de-linha → revisao-mecanica → auditoria-de-canon
  → escriba-de-canon → registrar rodada → commit + push
```

A ordem importa: os passes que **mudam texto** vêm antes dos que só
**conferem**. Caçar vírgula em parágrafo que ainda vai ser reescrito é
trabalho jogado fora.

**Rodada de revisão da autora:** ela comenta pelo app; os comentários
chegam em `revisao/comentarios.jsonl`. Colete **todos**, aplique um a um,
rode os passes de novo por cima, registre em `rodadas.jsonl` com `antes`,
`depois` e **`porque`**.

Comentário do tipo **`regra`** não é correção de trecho: é lei nova. Vira
entrada em `decisoes-editoriais.md` e, se for verificável por máquina,
vira regra no `livro.yaml`. **Regra que a autora precisa repetir duas
vezes é falha do sistema.**

---

## Ferramentas antes de modelo

```bash
python3 .claude/tools/lint.py   --projeto "Os Russels" --resumo
python3 .claude/tools/estado.py --projeto "Os Russels"
```

Tudo que é verificável por máquina não passa por modelo: custa zero e
nunca alucina. O `lint.py` trabalha por **parágrafo**, não por linha —
senão perde tudo em capítulo com hard wrap, que é o livro do cap 25 em
diante.

O `estado.py` é o painel de produção **calculado**. Não existe mais
MANIFESTO mantido à mão: seis documentos de estado escritos com cuidado
divergiram mesmo assim, chegando a doze capítulos de defasagem.

---

## Decisões

- **Da obra** (voz, canon, estilo) → `Os Russels/notas/decisoes-editoriais.md`,
  em tabela, datadas. **Anulam qualquer instrução genérica de skill.**
- **De produto e engenharia** → `decisoes/NNNN-slug.md`, uma por arquivo,
  três parágrafos (contexto, decisão, consequência). Nunca se edita uma
  decisão aceita: cria-se outra que a substitui.

Critério para morar no repo: **algum agente precisa ler para trabalhar.**
Roadmap, preço e entrevistas não precisam.

---

## Branch e merge

- Escrita do livro: `claude/book-writing-workflow-LnfjM`.
- A autora **não faz git** — Claude commita, pusha e faz merge.
- **Sem merge automático em `main`** sem pedido explícito dela. `main` é o
  ponto de release que ela controla.

---

## Tom

Fogo baixo, slow burn, tensão sensorial. Bússola: Bridgerton/Julia Quinn e
Sarah J. Maas. **Mais voltagem = mais tensão e subtexto, não mais
explícito.** A contenção é proposital.
