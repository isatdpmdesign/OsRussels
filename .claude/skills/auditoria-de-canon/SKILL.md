---
name: auditoria-de-canon
description: Auditoria pós-escrita. Extrai cada AFIRMAÇÃO de fato de um capítulo recém-escrito (eventos passados, "primeira vez / nunca", quem sabe o quê, idades, datas, distâncias, descrições físicas, localizações, nomes) e cruza com todo o resto da obra. Reporta cada divergência com fonte e propõe correção, sem aplicar. Use como passe final antes de fechar um capítulo. É a irmã pós-escrita da skill biblioteca (que é pré-escrita).
---

# Auditoria de canon — passe pós-escrita

A `biblioteca` roda **antes**: monta a ficha para você não errar.
Esta roda **depois**: assume que você errou mesmo assim e vai atrás.

As duas existem porque capítulo escrito no calor da inspiração afirma
fatos que contradizem o canon sem ninguém perceber. A ficha prévia reduz;
não zera.

## Regra de ouro

**Você não corrige. Você reporta.** Propõe a reescrita, cita o canon que
sustenta a proposta, e a autora decide. Aplicar correção de canon sozinho
é como o modelo se autoriza a reescrever a história.

## Procedimento

### 1. Extrair cada afirmação verificável

Varra o capítulo procurando **fatos**, não impressões. Descrição poética
não se audita; afirmação sim. Categorias, em ordem de risco:

| Risco | Categoria | Exemplo de armadilha |
|---|---|---|
| 🔴 | **"Primeira vez" / "nunca tinham"** | afirmar ineditismo do que já aconteceu |
| 🔴 | **Quem sabe o quê** | personagem usando informação que ainda não recebeu |
| 🔴 | **Localização de evento passado** | "o beijo na biblioteca" quando foi na sala de estar |
| 🟠 | Eventos passados referenciados | "desde X", "há Y meses", "no dia que" |
| 🟠 | Idades, datas, durações | propagação inconsistente ao longo do livro |
| 🟠 | Nomes próprios | livraria, modista, parentes, criadagem |
| 🟡 | Descrição física | cor de cabelo, pele, olhos, altura |
| 🟡 | Inventário de objetos | banco de ferro × banco de madeira |
| 🟡 | Relacionamentos | "afilhado de", "padrinho de", "pretendente de" |
| 🟡 | Maneirismos | "do jeito que ele sempre", "como ela costumava" |
| 🟡 | Mecanismos inventados | regra do mundo que ninguém estabeleceu |

### 2. Cruzar com a obra inteira

Para cada fato: termos-chave → `grep -rni` em todos os caminhos do
`livro.yaml` → **abrir e ler o trecho** → citar `arquivo:linha`.

Não vale "acho que está em algum capítulo". Se não achou, o fato é
**inferido**, não canônico — e isso é uma categoria de saída, não um erro.

### 3. Classificar

- **✓ Canônico** — bate. Só entra no sumário.
- **⚠️ Inferido** — não contradiz nada, mas não tem fonte. Plausível.
  A autora confirma e vira canon, ou corta.
- **🚨 Furo** — contradiz o canon. Reportar com fonte + proposta.

## Formato de saída

```markdown
## Auditoria — Cap N

### 🚨 Furos ([n])

1. **`capN:linha`** afirma:
   > "[citação]"

   **Canon contradiz** (`capX:linha`):
   > "[citação canônica]"

   **Proposta:**
   > "[reescrita que respeita o canon]"

### ⚠️ Inferidos ([n]) — decisão da autora

- "[fato]" (`capN:linha`) — sem fonte no canon. Plausível. Confirmar?

### ✓ Verificados ([n])

- [lista curta, sem detalhar]
```

## Princípios

- **Exaustivo por cima de elegante.** Melhor sinalizar 20 fatos para
  confirmar do que deixar passar um que vire furo três capítulos adiante.
- **Nunca inventar a correção.** A proposta só pode usar o que já é canon.
- **Sempre citar fonte**, dos dois lados: o que o capítulo diz e o que o
  canon diz.

## Quando NÃO usar

Trechos curtos, rascunho ainda aberto, correção de pontuação. Rode com o
capítulo fechado — auditar texto que ainda vai mudar é trabalho jogado
fora.
