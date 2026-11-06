---
name: capitulo
description: Desenha os beats de UM capítulo antes de escrever - POV, o que a cena precisa entregar, onde começa e onde corta, o que planta e o que colhe. Use antes da skill prosa, depois de saber onde o capítulo cai no arco. Para mudança estrutural que atravessa o livro, use a skill arco.
---

# Capítulo — os beats de uma cena

Escala pequena: **um** capítulo. Estrutura do livro inteiro é `arco`;
propagação de mudança é `onda-de-mudanca`.

## As perguntas, em ordem

### 1. De quem é a cabeça?
POV errado é o erro mais caro do planejamento, porque só aparece com o
capítulo escrito.

A pergunta certa não é "de quem é a vez". É: **quem tem mais a perder
nesta cena?** A cena pertence a quem o evento machuca ou muda mais.

Cuidado com o desequilíbrio de longo prazo: um protagonista que passa o
clímax sendo visto de fora vira coadjuvante do próprio livro. Cheque a
distribuição real em `estado-do-projeto`.

### 2. O que muda entre a primeira e a última linha?
Se nada muda — nem fato, nem relação, nem o que alguém sabe, nem o que
alguém está disposto a fazer — **o capítulo não existe ainda.** É o teste
mais duro e o que mais salva trabalho.

Cotidiano vale, desde que algo se desloque por dentro.

### 3. Onde começa e onde corta?
- **Comece tarde.** Entre na cena o mais perto possível do que importa.
- **Corte cedo.** Saia no beat mais alto que ainda deixa a leitora
  querendo. Capítulo que explica o que acabou de acontecer perde a força
  que acabou de ganhar.

### 4. O que planta, o que colhe?
Todo capítulo devia fazer as duas coisas. Plantio sem colheita vira
promessa esquecida; colheita sem plantio vira coincidência.

Confirme com a `biblioteca` o que já está plantado esperando payoff.

### 5. O que a leitora sabe que o personagem não sabe?
Ironia dramática é o motor mais barato de tensão. Se a leitora sabe algo
que o POV ignora, cada fala dele carrega carga de graça.

### 6. Onde está o corpo?
Cena de romance sem corpo é ata de reunião. Onde estão as mãos, a
distância entre os dois, quem olha primeiro, quem desvia, o que quase
acontece.

## As cinco perguntas da autora — o passe que economiza o capítulo

Antes de escrever, rode estas cinco contra os beats. Elas saem da régua
real da autora (`perfil/regua.md`, extraída dos comentários dela), e são
o que ela mais aponta **depois** que a prosa existe — quando consertar
já custa um capítulo inteiro.

**1. Quem inicia?**
Para cada coisa que alguém concede, entrega ou resolve nesta cena:
quem puxou? Se ninguém puxou, tem um passageiro na cena. A versão certa
quase sempre deixa os dois lados ativos.
> Caso real: a mãe oferecia as joias sem a filha pedir. A autora recusou.
> Virou: a filha sugere, a mãe responde que já tinha pensado nisso.

**2. Essa é a emoção certa?**
Nomeie com precisão o que cada personagem sente em cada beat — e confira
se a reação prevista é daquela emoção. Susto não chora igual tristeza.
> Caso real: *"Ela está surpresa mas não triste. Está com medo, mas não
> triste."*

**3. O personagem pagou por isso?**
Toda concessão grande precisa de uma pergunta antes. Quem cede tem o
direito de querer saber por quê — e a resposta é onde a cena vira boa.
> Caso real: antes de ceder as joias, a mãe pergunta o que a filha viu
> naquele rapaz. A resposta virou o melhor trecho do capítulo.

**4. A leitora tem o que precisa?**
Marque tudo que os personagens entendem por atalho e a leitora não.
Abrir compressão quase sempre vira diálogo, porque força o outro a
reagir.

**5. Isso se sustenta?**
Cada premissa da cena contra o canon (`biblioteca`). É a metade que o
sistema pega sozinho — mas pegar aqui é mais barato que pegar depois.

**Leve as respostas junto com os beats para a autora.** Um capítulo de
cinco mil palavras vira uma página de aprovação. É a diferença entre ela
revisar prosa e ela dirigir a história.

## Antes de fechar os beats

- **`biblioteca`** para a ficha: o que é canon nesta cena, quem sabe o
  quê, o que não pode ser dito como novidade.
- **Cheque a régua de comprimento** (`livro.yaml`). Se os beats não
  chegam ao mínimo, ou falta cena, ou a cena está sendo resumida.
- **Cheque a cota do capítulo anterior.** Dois capítulos seguidos de
  mesma temperatura cansam. Depois de um pico, respire; depois de dois
  capítulos calmos, a leitora precisa de fogo.

## Saída

```markdown
## Beats — Cap N: [título provisório]

**POV:** [personagem] — porque [quem tem mais a perder]
**Quando/onde:** [ponto na timeline, lugar]
**Muda o quê:** [em uma frase]

**Beats:**
1. [abre em] — [o que acontece]
2. ...
N. [corta em] — [o beat alto]

**Planta:** [setup] → colhe em [onde]
**Colhe:** [payoff] ← plantado em `cap X:linha`
**A leitora sabe e o POV não:** [se houver]
**Canon a respeitar:** [da ficha, com fonte]
**Alvo:** ~[n] mil palavras
```

Confirme os beats com a autora **antes** de chamar a `prosa`. Discordar
de um beat custa um minuto agora e um capítulo depois.
