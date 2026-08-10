---
name: revisao-de-logica
description: A cena se sustenta? Caça premissa que não fecha, personagem agindo contra o que ele mesmo sabe, motivo declarado que não é motivo de verdade, e logística impossível (tempo, distância, quem estava onde). Use depois da escrita, junto com a revisão de POV. É o passe que pega o erro que ninguém pega, porque o texto fica bonito e coerente e mesmo assim a cena não faz sentido.
---

# Revisão de lógica — a cena se sustenta?

Este passe existe por causa de um erro real que atravessou cinco outros
passes sem ser pego.

Duas moças cochichavam de madrugada com medo de acordar a criada —
*"Helle ainda não acordou"*, *"conta antes de ela acordar"*. Só que a
criada tinha destrancado a porta para uma delas sair à noite e ficara
acordada esperando ela voltar. **Elas não tinham nada a esconder dela.**
O próprio capítulo dizia isso, seiscentas linhas depois.

Nenhum fato estava errado. O canon estava certo, o POV estava certo, a
voz estava certa, a pontuação estava certa. **A cena é que não fazia
sentido.**

## O que este passe caça

### 1. Personagem agindo contra o que ele sabe
O oposto do furo de POV. Lá o personagem sabe demais; aqui ele age como
se soubesse de menos.

- Esconde de quem já sabe.
- Procura o que já encontrou.
- Se surpreende com o que já lhe disseram.
- Pede o que já lhe ofereceram.

**Pergunta:** *este personagem, com o que ele sabe neste ponto, faria
isso?* Se a resposta depende de ele ter esquecido, é furo.

### 2. Motivo declarado que não é o motivo
O texto diz por que alguém faz algo, e a razão não se sustenta.

Perigoso porque **soa explicativo** — parece que a cena foi pensada. A
frase preenche o buraco em vez de tapá-lo.

**Pergunta:** *se eu apagar o motivo declarado, sobra motivo?* Se não
sobra nada, a cena precisa de outro motivo — não de outra frase.

### 3. Premissa que não fecha
A cena inteira depende de uma condição que não vale.

- A urgência não é urgente (ninguém perde nada se demorar).
- O segredo não é segredo (todo mundo em cena já sabe).
- O obstáculo não obstrui (havia três saídas óbvias).
- A escolha não é escolha (só existe uma opção plausível).

**Pergunta:** *o que acontece se o personagem simplesmente não fizer
isso?* Se nada acontece, não há cena — há coreografia.

### 4. Logística
Tempo, distância, quem estava onde, o que estava aberto ou fechado, quem
podia ouvir de onde.

- Alguém atravessa a cidade em cinco minutos.
- Duas coisas acontecem ao mesmo tempo em lugares diferentes com a mesma
  pessoa.
- Uma conversa privada acontece onde meia casa passa.
- O relógio da cena não bate com o relógio do capítulo.

## Procedimento

1. **Liste as premissas da cena.** O que precisa ser verdade para ela
   funcionar? Normalmente são duas ou três, e normalmente estão
   implícitas.
2. **Teste cada uma contra o canon** — com `grep` e leitura, nunca de
   memória. A premissa "elas precisam esconder isso da Helle" cai no
   segundo em que se lê o que a Helle fez na noite anterior.
3. **Para cada personagem em cena, pergunte o que ele sabe** e se o
   comportamento dele bate.
4. **Puxe o fio da urgência.** Quase toda cena tem um relógio. Confira se
   ele existe de verdade.

## Formato

```markdown
## Revisão de lógica — Cap N

### 🚨 Não se sustenta ([n])

1. **`capN:linha`** — [a premissa]
   > "[citação]"
   **Por que não fecha:** [o fato que derruba, com `arquivo:linha`]
   **O que fazer:** [ou a cena muda de motivo, ou o fato muda — e dizer qual]

### ⚠️ Frágil ([n])
- [premissa que se sustenta, mas por pouco]
```

## Regra

Quando a lógica quebra, **quase nunca a solução é apagar a frase.** A
cena costuma precisar daquela função (urgência, segredo, obstáculo) —
o que ela precisa é de um motivo que valha.

No caso da Helle: a urgência continuou existindo, mas passou a vir da
água quente das cinco e meia, que acaba com o pedaço privado da manhã.
Mesma função, motivo verdadeiro. E de quebra as duas dizem em voz alta
que a criada é cúmplice, o que é melhor do que fingir que não é.
