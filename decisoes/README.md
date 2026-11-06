# Decisões — produto e engenharia

Uma decisão por arquivo, numerada, três parágrafos: **contexto**,
**decisão**, **consequência**.

## Onde cada decisão mora

| Tipo | Onde | Formato |
|---|---|---|
| **Da obra** — voz, canon, estilo, o que um personagem faz | `Os Russels/notas/decisoes-editoriais.md` | tabela datada |
| **De produto e engenharia** — como o sistema funciona | aqui, `NNNN-slug.md` | três parágrafos |

Os dois formatos são diferentes porque os problemas são diferentes.
Cinquenta regras curtas que precisam ser consultadas de relance querem uma
tabela. Uma decisão com raciocínio longo e cadeia de substituições quer um
arquivo com histórico. Converter um no outro seria churn sem ganho.

## Critério para morar no repositório

**Algum agente precisa ler isto para trabalhar?** Se sim, mora aqui.

Roadmap, preço, entrevistas de usuária e material de marketing não
precisam — nenhuma skill os consulta. O corte não é "muda o código": as
decisões mais valiosas deste projeto até hoje não mudaram código nenhum,
mudaram o texto (blacklist, hard wrap, a mecânica da carta da Casandra) e
precisam estar onde o motor lê.

## Regras

1. **Decisão aceita não se edita.** Mudou de ideia? Nova decisão, com
   `substitui: NNNN`, e a antiga vira `status: substituída`. O histórico é
   o ativo — daqui a seis meses você vai querer saber *por que* descartou
   um caminho, e a tabela guarda a escolha mas perde o argumento.
2. **A consequência é obrigatória, e inclui o que a decisão impede.** Uma
   decisão sem custo declarado não foi pensada até o fim.
3. **Quando uma decisão muda uma regra vigente**, o `CLAUDE.md` muda no
   mesmo commit.

## Formato

```markdown
---
numero: 0000
data: AAAA-MM-DD
status: proposta | aceita | substituída
escopo: produto | engenharia | processo
substitui: —
substituida_por: —
---
# Título na voz ativa

## Contexto
## Decisão
## Consequência
```

## Índice

| # | Decisão | Escopo | Status |
|---|---|---|---|
| 0001 | Separar motor de dados | engenharia | aceita |
| 0002 | Leitura e escrita de canon são agentes diferentes | engenharia | aceita |
| 0003 | O que é verificável por máquina não passa por modelo | engenharia | aceita |
| 0004 | Estado de produção é view derivada, não arquivo | engenharia | aceita |
| 0005 | Revisão dividida por tipo de falha, não uma revisora | processo | aceita |
| 0006 | Diagramadora e narradora saem da Fase 1 | produto | aceita |
| 0007 | Comentário do tipo regra vira lei do sistema | processo | aceita |
| 0008 | A usuária nunca escolhe modelo | produto | aceita |
