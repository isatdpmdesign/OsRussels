# A régua da autora

> **O que é este arquivo:** o que a Isadora caça quando revisa, extraído
> dos comentários reais dela (`revisao/comentarios.jsonl`) e das rodadas
> (`revisao/rodadas.jsonl`). Não é opinião sobre o que ela gosta — é o
> que ela de fato apontou, contado.
>
> No OpenBooks isto é gerado por autora, e é o que faz o sistema parar de
> precisar dela para as mesmas coisas duas vezes.

---

## O achado principal

**Ela não é revisora de linha. É editora de história.**

Distribuição real dos 28 primeiros comentários:

| | |
|---|---|
| 12 | correção pontual |
| 8 | canon / continuidade |
| **4** | **discussão — questiona a escolha e propõe outra** |
| **3** | **cena — redesenha o beat** |
| 1 | regra |

As sete de `discussão` e `cena` são as caras. Não corrigem frase:
perguntam **por que essa pessoa faria isso, agora, desse jeito.**

---

## As cinco perguntas dela

### 1. Quem inicia?
Ela caça personagem recebendo de graça o que devia ter pedido.

> *"Não acha estranho Eleonora já oferecer as joias sem Aurora nem
> sugerir? Não é melhor Aurora sugerir e Eleonora dizer que já tinha
> pensado nisso?"*

**A régua:** quando um personagem cede, entrega ou resolve, pergunte quem
puxou. Se a resposta for "ninguém, aconteceu", a cena tem um passageiro.
A versão certa quase sempre deixa **os dois** ativos.

### 2. Essa é a emoção certa?
Ela não diz "está raso". Ela nomeia o sentimento correto.

> *"Eu não sei se faz sentido Aurora chorar aqui. Ela está surpresa mas
> não triste. Está com medo, mas não triste."*

**A régua:** antes de escrever a reação, nomeie o que a personagem sente
com precisão — e confira se a reação escrita é daquela emoção. Susto não
chora igual tristeza. Alívio não chora igual medo.

### 3. O personagem pagou por isso?
Ela recusa virada que chega barata.

> *"Antes de Eleonora decidir destinar as joias, ela pode questionar o
> que Aurora viu de tão bom no Josh."*

**A régua:** toda concessão grande precisa de uma pergunta antes. Quem
cede tem o direito de querer saber por quê — e a resposta é onde a cena
vira boa.

### 4. A leitora tem o que precisa?
Ela pega o que só faz sentido para quem escreveu.

> *"Não entendi o que quis dizer na mesma cadeira. Trate alternativas."*
> *"Ele tinha pensado a noite inteira, pelos dois, e decidido sozinho"* —
> a autora sabia o que "pelos dois" queria dizer; a leitora não.

**A régua:** se você entende a frase por ter lido os capítulos
anteriores, abra. Abrir compressão quase sempre vira diálogo, porque
força o outro a reagir.

### 5. Isso se sustenta?
> *"Erik nunca esteve nos jantares. Erik ia visitar Aurora à tarde."*
> *"Não sei se Aurora prometeu por carta... não foi presencial?"*

**A régua:** é a `revisao-de-logica` e a `auditoria-de-canon`. Metade dos
comentários dela é isso — e é a metade que o sistema já consegue pegar
sozinho.

---

## Como ela quer ser respondida

> *"Não copie minha frase. Pense em algo melhor para ser descritivo aqui."*

Ela dá **direção, não texto**. Quando sugere uma frase, é exemplo do
registro, não material para colar. Copiar a sugestão dela ao pé da letra
é entender errado o pedido.

---

## O que isso significa na prática

**O que ela aponta divide em duas metades limpas:**

| Metade | O quê | Quem resolve |
|---|---|---|
| ~60% | canon, continuidade, pontuação, monossílabo, repetição | **o sistema**, sozinho, com `lint.py` e os passes |
| ~40% | agência, emoção certa, virada comprada, clareza | **ela** — mas **antes da prosa**, não depois |

A segunda metade não é automatizável: depende de saber para que a
história serve. Mas é **antecipável**. Todos os comentários de discussão
do Cap 33 poderiam ter sido feitos olhando os beats, numa página, em vez
de num capítulo de 4.300 palavras.

**É por isso que as cinco perguntas moram na skill `capitulo`, e não numa
skill de revisão.** Elas valem antes.
