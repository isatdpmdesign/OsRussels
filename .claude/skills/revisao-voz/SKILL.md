---
name: revisao-voz
description: Antídoto contra escrita de IA e calibração para a voz da autora. Use SEMPRE antes de escrever prosa nova e SEMPRE depois, para revisar. Tem dois trabalhos - cortar os tiques que denunciam texto de modelo, e puxar a prosa para a assinatura da autora lida em perfil/voz.md. Sem a segunda metade, tirar o tique só produz prosa neutra, que é outro jeito de soar como máquina.
---

# Revisão de voz — tirar a máquina, pôr a autora

Dois trabalhos, nesta ordem:

**(a)** cortar os tiques que denunciam escrita de modelo;
**(b)** puxar a prosa para a voz da autora — que está em
`perfil/voz.md` (caminho em `livro.yaml → caminhos.voz`).

**Leia `perfil/voz.md` antes de começar.** Fazer só (a) deixa a prosa
limpa e sem dono. Prosa sem dono é o segundo sintoma mais óbvio de texto
de máquina, depois dos tiques.

Você não vai conseguir ser a autora. Precisa parar de ser claramente um
modelo.

---

## PARTE 1 — Os dez tiques

### 1. Antítese simétrica
Frases que se completam em espelho: *"não X, mas Y"*, *"a cabeceira que
ninguém olha de frente e que ninguém consegue não olhar"*.
**Antídoto:** corte um lado. Deixe aberta.

### 2. Paralelo em três tempos
*"Sabia o número exato. Sabia que eram poucos. Sabia que não ia dar
nenhum."*
**Antídoto:** tire um item. O efeito de máquina vem do trino fechado.

### 3. Abstrato por cima do concreto
*"o modo como"*, *"a precisão com que"*, *"a forma como"*, *"do jeito
que"*. O personagem nunca faz: existe *a forma como* ele faz.
**Antídoto:** corte a moldura. Diga o que ele faz.

### 4. Emoção substantivada
*"o querer ainda estava lá"*, *"o calor dela"*. A emoção vira objeto que
o narrador discute de fora.
**Antídoto:** devolva ao corpo. *"Ele ainda queria"* > *"o querer ainda
estava lá"*.

### 5. Aforismo de fechamento
Todo parágrafo termina com chave de ouro.
**Antídoto:** termine parágrafos **mal**. No meio do pensamento. Num beat
seco. Este parágrafo podia ter acabado em "mal".

### 6. Travessão como faca-suíça
**Antídoto:** vírgula, ponto, parêntese. Travessão só para fala e
interrupção. (Neste projeto é regra dura, e o `lint.py` pega.)

### 7. Reformular em variantes
A mesma ideia em três versões para fechar redonda.
**Antídoto:** diga uma vez. Confie na leitora.

### 8. Bonito demais no banal
Todo gesto carrega significado. Vida real não é assim.
**Antídoto:** permita banalidade. O gato pode aparecer e ninguém ter
coragem de tirar, e ponto.

### 9. Ecolalia
Repetir a palavra que acabou de usar, quase sempre colada ao tique 3:
*"guardou, do jeito que ele guardava"*. O ouvido humano reclama antes da
cabeça.
**Antídoto:** troque uma ocorrência ou vire a frase de outro ângulo. Se a
repetição for estilística mesmo, no máximo três e com motivo claro.
(O `lint.py --regra eco` acha as piores.)

### 10. Subtexto vago
*"sem saber ainda o que aquilo significava"*, *"uma coisa que ele ainda
não tinha processado"*. Parece profundo; é trampolim. Pede à leitora que
deduza — e ela deduz errado, ou não deduz, e a cena não pousa.
**Antídoto:** consulte a preferência da autora em `perfil/voz.md`. Neste
projeto ela é explícita: **claro e escancarado > subjetivo e aberto.** Se
o POV entendeu, escreva o que entendeu. Se a fala teve significado,
nomeie.

---

## PARTE 2 — Pôr a autora

Abra `perfil/voz.md` e aplique as marcas de lá. Não é decoração: é a
metade do trabalho. Tique removido sem voz posta no lugar devolve um
texto correto que não é de ninguém.

---

## PARTE 3 — Princípio mestre

**O ser humano erra.** Esta skill não te deixa mais perfeito. Te deixa
**menos perfeito do jeito certo.** A perfeição é o que denuncia.

---

## Como aplicar

**Antes de escrever:** defina registro e POV, releia a PARTE 1 e o
`perfil/voz.md`, lembre que pode errar, escreva.

**Depois de escrever:** cace os dez tiques. Conte-os por parágrafo.
Mais de **dois por parágrafo** e está cheirando a modelo.

Não corte tudo. Alguma simetria é prosa. Nem todo paralelo é máquina.

## Quando NÃO usar

Continuidade, idade, data, fato — é `biblioteca` e `auditoria-de-canon`.
Pontuação e blacklist — é `revisao-mecanica`. Aqui é só voz.
