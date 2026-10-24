---
name: onda-de-mudanca
description: Propaga uma mudança estrutural por uma obra já escrita. Use quando a autora mudar algo que reverbera — um evento que troca de capítulo, um personagem que muda de função, uma mecânica de enredo que se altera, uma decisão que invalida cenas já escritas. Calcula tudo que a mudança quebra (cenas, plantios, payoffs, guias, referências cruzadas), ordena por gravidade e devolve um plano. Não aplica nada sozinha.
---

# Onda de mudança — quando a história muda de ideia

A história é viva. O que a autora idealizou hoje ela pode mudar amanhã, e
a mudança vai atingir tudo que vem depois — e boa parte do que veio
antes. Isso não é falha de planejamento: **é a natureza do trabalho.** O
sistema é que precisa aguentar.

Esta skill existe porque a operação que mais dói neste projeto é
exatamente essa. Quando o primeiro beijo migrou de um capítulo para outro,
o ato inteiro precisou ser redesenhado — e o rastro daquilo ainda estava
espalhado em quatro documentos meses depois, com ponteiros apontando para
capítulos errados.

**O erro não foi mudar. Foi mudar sem calcular a onda.**

## O que você faz

Recebe uma mudança. Devolve **o que ela quebra**, ordenado por gravidade,
com fonte. Você não conserta — você faz o mapa do estrago.

## Procedimento

### 1. Nomear a mudança com precisão

Antes e depois, em uma frase cada. Vago aqui envenena tudo adiante.

- ❌ "o final vai ser diferente"
- ✅ "a Eleonora deixa de vender as joias; quem cobre o valor que falta
  passa a ser o Erik, por amizade"

### 2. Classificar o tipo — o tipo determina onde procurar

| Tipo | O que costuma quebrar |
|---|---|
| **Evento muda de lugar** | referências temporais, "desde aquela noite", quem sabia o quê em cada ponto, numeração em todos os guias |
| **Personagem muda de função** | falas que só fazem sentido na função antiga, reações de terceiros, plantios de motivação |
| **Mecânica de enredo muda** | toda cena que explica a mecânica, os diálogos que a discutem, a lógica de causa e efeito das cenas seguintes |
| **Fato do mundo muda** | descrições, continuidade física, o que é possível numa cena |
| **Relação muda** | tratamento, tom de diálogo, o que cada um se permite dizer |

### 3. Varrer a obra inteira

Não só os capítulos seguintes. Mudança estrutural quebra para trás
também: plantio que agora não colhe mais, foreshadowing que aponta para
uma coisa que deixou de acontecer.

Para cada capítulo, pergunte:
- **Depende** do fato antigo? (a cena não funciona sem ele)
- **Menciona** o fato antigo? (contradição direta)
- **Planta** o fato antigo? (setup órfão)
- **Colhe** o fato antigo? (payoff sem setup)

E nos guias: bíblia, ficha, sinopse, decisões — toda referência cruzada.

### 4. Classificar cada impacto

| Nível | Significa | Ação |
|---|---|---|
| 🔴 **Quebra** | a cena fica factualmente errada ou logicamente impossível | reescrever |
| 🟠 **Enfraquece** | a cena continua de pé mas perde sentido, ou o plantio fica órfão | revisar |
| 🟡 **Menção** | referência pontual, conserto local | corrigir a linha |
| 🔵 **Oportunidade** | a mudança abre algo que o texto atual não aproveita | sugerir |

### 5. Devolver o plano

```markdown
## Onda de mudança — [nome da mudança]

**Antes:** [uma frase]
**Depois:** [uma frase]
**Tipo:** [classificação]

### 🔴 Quebra ([n] capítulos)
- **`cap N:linha`** — [o que quebra e por quê]
  > "[citação]"
  Ação: [reescrever o quê, em que direção]

### 🟠 Enfraquece ([n])
- ...

### 🟡 Menções ([n])
- `cap N:linha` — trocar "X" por "Y"

### 🔵 Oportunidades
- ...

### Guias a atualizar
- `arquivo:linha` — [o quê] → tarefa do `escriba-de-canon`

### Ordem sugerida
1. [o que fazer primeiro, e por quê essa ordem]

### Custo
[n] capítulos para reescrever, [n] para revisar, [n] linhas pontuais.
```

## O passo que quase todo mundo pula

**A mudança pode não valer a pena.** Parte do seu trabalho é dizer o
custo antes de a autora se comprometer. Uma mudança que melhora uma cena
e quebra onze capítulos é uma informação que ela precisa ter **antes**,
não depois de você ter começado.

Diga o custo com clareza e sem julgamento. A decisão é dela — inclusive a
de pagar caro por uma cena que vale.

## Regras

- **Não aplique nada.** Esta skill produz plano, não diff.
- **Cite fonte** em cada impacto: `arquivo:linha`.
- **Não invente a solução da cena.** Diga em que direção reescrever;
  escrever é trabalho da `prosa`, com a autora decidindo.
- **Depois que a autora aprovar**, os guias vão para o
  `escriba-de-canon` e a mudança vira decisão datada.
