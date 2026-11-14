---
name: revisao-de-linha
description: Edição de linha - o passe que trabalha a frase, não a cena. Caça repetição de palavra e de construção entre parágrafos vizinhos, monotonia de ritmo (toda frase do mesmo tamanho), verbo fraco carregado por advérbio, adjetivo que não trabalha, e parágrafos que começam todos igual. Use depois da revisao-voz e antes da revisao-mecanica. É o passe que faltava - nenhum outro olha a frase como unidade.
---

# Revisão de linha — a frase como unidade

Os outros passes olham a cena (`revisao-sentimental`), a voz
(`revisao-voz`), o fato (`auditoria-de-canon`) e a mecânica (`lint.py`).
**Ninguém olha a frase.** É onde mora a diferença entre prosa publicável e
prosa quase lá.

Este passe não muda o que a cena diz. Muda como ela soa.

## O que caçar

### 1. Eco entre parágrafos vizinhos
A mesma palavra incomum aparecendo duas ou três vezes em meia página. O
`lint.py --regra eco` pega dentro do parágrafo; **você pega entre
parágrafos**, que é onde mais acontece e onde a máquina não chega.

Vale para **construções**, não só palavras: três parágrafos seguidos
abrindo com gerúndio, quatro frases seguidas com a mesma estrutura
`sujeito + verbo + complemento longo`.

### 2. Monotonia de ritmo
Leia em voz alta — de verdade, ou mentalmente com atenção ao fôlego. Se
todas as frases têm o mesmo comprimento, o parágrafo embala e a leitora
desliga.

Prosa boa varia: longa, longa, **curta**. A frase curta é o soco. Se não
existe frase curta na página, não existe ênfase.

Esta autora usa isso: *"Que obra de arte!"*, *"E o corpo, céus, o
corpo!"* — frase curta pontuando no meio. Está em `perfil/voz.md`.

### 3. Verbo fraco com advérbio de muleta
*"andou rapidamente"* → *"correu"*. *"falou baixinho"* → *"sussurrou"*.
*"olhou fixamente"* → *"encarou"*.

Advérbio em `-mente` quase sempre sinaliza que o verbo errado foi
escolhido primeiro. **Não banir** — perguntar, em cada um, se existe um
verbo que já contém aquilo.

### 4. Adjetivo que não trabalha
Adjetivo genérico não descreve, ocupa: *bonito*, *estranho*, *grande*,
*terrível*, *intenso*. Se sai e a frase não perde nada, ele não estava
trabalhando.

O contraponto está em `perfil/voz.md`: **adjetivo triplo quando admira é
assinatura desta autora** e fica. A régua é se ele é específico, não se é
sozinho.

### 5. Aberturas repetidas de parágrafo
Cinco parágrafos seguidos começando com o nome do POV. Ou com "E". Ou com
"Quando". Passe o olho **só nas primeiras palavras** de cada parágrafo da
página — o padrão salta.

### 6. Frase que precisa ser relida
Regra dura deste projeto: **se precisa reler para entender, está errada.**
Vale principalmente para fala. Marque toda frase em que você tropeçou —
seu tropeço é o da leitora.

## Procedimento

Trabalhe por **página**, não por capítulo. Este passe é de proximidade;
em bloco grande você perde o ouvido.

1. Leia o trecho em voz alta.
2. Marque onde tropeçou, onde embalou, onde ouviu eco.
3. Só depois volte e classifique.

Ordem importa: **ouvir antes de analisar.** Quem começa procurando
advérbio acha advérbio e perde o ritmo.

## Formato de saída

```markdown
## Revisão de linha — Cap N, [trecho]

**1. [eixo] — `linha`**
> "[antes]"
→ "[depois]"
[meia linha de porquê, só se não for óbvio]
```

Sem cerimônia. Este passe é volume: muitos ajustes pequenos.

## Regras

- **Não invente fato, objeto nem gesto novo.** Aqui só se mexe em como a
  frase soa. Beat novo é `revisao-sentimental`.
- **Não uniformize a voz.** Personagem que fala torto continua falando
  torto. Você conserta a prosa do narrador, não a boca dos personagens.
- **Não corrija a imperfeição que é assinatura.** Vírgula de cadência,
  parágrafo que termina seco, clichê apaixonado dentro do POV — está tudo
  em `perfil/voz.md` e é para ficar.
- Na dúvida entre elegante e vivo, **fique com vivo**.
