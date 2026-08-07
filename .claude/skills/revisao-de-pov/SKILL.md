---
name: revisao-de-pov
description: Disciplina de ponto de vista. Caça o erro mais silencioso e mais frequente da obra - o personagem POV sabendo, vendo ou sentindo o que ele não tem como saber, ver ou sentir. Também caça troca de cabeça no meio da cena, verbos de filtro que afastam a leitora, e descrição do próprio POV por fora. Use depois da escrita, antes da auditoria de canon.
---

# Revisão de POV — o que essa cabeça pode saber

Este é o furo que mais passa despercebido, porque o texto fica **bonito e
coerente** — só está sendo narrado por alguém que não podia narrar aquilo.

Não é preciosismo técnico. É o que quebra a imersão sem a leitora saber
por quê: ela sente que a cena "não é de ninguém".

A errata deste projeto prova o padrão. Três dos oito itens registrados
são exatamente isto:

> Aurora pensa que Josh *"escrevia cartas que não enviava"* — ela não tem
> como saber que ele não as envia. É informação exclusiva do POV dele.

> *"A cama com o dossel — que Josh reclamava em cartas à mãe"* — Aurora
> não leu as cartas.

> *"como Meridiana falava com as pereiras"* — Aurora nunca conheceu
> Meridiana.

Nenhum dos três é erro de canon: os fatos são todos verdadeiros. **O erro
é de quem sabe.**

## Os quatro eixos

### 1. Conhecimento — o mais grave

O POV afirma, pensa ou sente algo que ele não recebeu em cena.

**Procure por:** verbos de saber (*sabia*, *entendia*, *percebia*,
*lembrava*), atribuição de motivo a terceiros (*porque ele queria*,
*ela estava com medo de*), e qualquer referência a fato que aconteceu
fora da presença do POV.

**A pergunta:** *em que cena, exatamente, esta cabeça recebeu esta
informação?* Se você não consegue citar `arquivo:linha`, é furo.

**Cuidado com a distinção que salva a cena:** o POV pode **observar** e
**supor** à vontade — o que ele não pode é **saber**. "Ele escrevia
cartas todas as noites" (ela ouve a pena, vê a tinta nos dedos) é legal.
"Ele escrevia cartas que não enviava" não é.

Muitas vezes o conserto é uma palavra: trocar *sabia* por *desconfiava*,
ou *porque* por *como se*.

### 2. Percepção

O POV descreve o que não pode perceber da posição em que está: o que
acontece atrás dele, a própria expressão de rosto, o que outro personagem
sente por dentro.

**O caso clássico:** o POV descrevendo o próprio rosto sem espelho. *"Os
olhos dela brilharam"* num capítulo de POV dela é a câmera saindo da
cabeça.

### 3. Troca de cabeça

No meio da cena o acesso interior escorrega para outro personagem, quase
sempre por um parágrafo só. Cada capítulo tem **um** POV, declarado no
nome do arquivo.

### 4. Verbos de filtro

*viu que*, *ouviu que*, *sentiu que*, *notou que*, *percebeu que*,
*pareceu-lhe que*. Em terceira pessoa próxima eles inserem uma camada
entre a leitora e a experiência.

> *Aurora viu que a mão dele tremia.* → *A mão dele tremia.*

Estamos na cabeça dela: se está na página, ela viu.

**Não zere.** O filtro é útil quando o ato de perceber é o que importa —
quando o personagem se dá conta de algo. Corte quando ele só está
atrapalhando.

## Procedimento

1. Confirme o POV do capítulo (nome do arquivo + voz interna).
2. Passe 1 — **conhecimento.** Liste cada afirmação sobre o mundo
   interior de terceiros ou sobre fato fora de cena. Para cada uma,
   procure a fonte. Sem fonte, é furo.
3. Passe 2 — **percepção e troca de cabeça.**
4. Passe 3 — **filtros.** Marque; corte os que só afastam.

## Formato de saída

```markdown
## Revisão de POV — Cap N (POV: [personagem])

### 🚨 Conhecimento ([n])
1. **`capN:linha`**
   > "[citação]"
   [Personagem] não tem como saber: [o porquê].
   Recebeu? Não encontrei fonte / recebeu em `capX:linha`.
   **Correção:** > "[reescrita — observação ou suspeita no lugar do saber]"

### 🟠 Percepção / troca de cabeça ([n])
### 🟡 Filtros ([n])
- `linha` — "viu que a mão tremia" → "a mão tremia"
```

## Regra

**Não corrija sozinho o que for conhecimento.** Furo de conhecimento
costuma ser furo de enredo disfarçado: às vezes a cena precisa daquela
informação, e a solução certa é **plantar antes** em outro capítulo, não
apagar aqui. Isso é decisão da autora.

Filtro você pode aplicar direto — é ajuste de superfície.
