# Roteiro de Áudio — Capítulo 1 "O lugar que ficou vazio"

> Adaptação para audiolivro. **Não é leitura literal.** O ouvinte não vê quem
> fala nem quando aquilo aconteceu — então toda fala precisa de âncora de
> **quem / quando / emoção**. Fonte: `capitulo-01-o-lugar-que-ficou-vazio-aurora.md`.
> Canon conferido em `ficha-continuidade.md` e `decisoes-editoriais.md`.

## Elenco de vozes

| Papel | Voz | ID ElevenLabs | Observação |
|---|---|---|---|
| **Narradora** | narradora sintética ElevenLabs v3 (a escolher: narr-1/2/3) | a salvar | **DECIDIDO: não é mais a Kokoro.** A Kokoro soou mecânica; a narração precisa da mesma emoção v3 das falas |
| **Aurora** | Aurora – Os Russels | `6eGtBXZMHHv8fKtkcMol` | 16 anos; contida, afiada, luto por baixo |
| **Eleonora** | Eleonora – Os Russels | `X8aTW3lPzhPDbbM4lmko` | mãe; precisão nórdica, límpida, sem crueldade |
| **Raj** | **a desenhar** | — | pai; 52, indo-dinamarquês, barítono medido, sem sotaque, propósito contido |
| **Aarav** (memória) | Aarav – Os Russels | `b7Gtpz8G4BMXBeI4yDwe` | **morto há 18 meses**; só em lembrança, tratamento "memória" (ver regra 3) |

## Regras globais de adaptação (o que diferencia áudio de texto)

1. **SEMPRE nomear quem fala.** (Regra corrigida — a anterior cortava as
   tags e o ouvinte se perdia.) O ouvinte não vê a mesa: a narração tem que
   dizer **quem** diz **cada** fala, e na primeira vez de cada personagem na
   cena, **quem ele é** ("disse Eleonora, a mãe de Aurora"; "respondeu Aurora").
   A tag pode vir antes (prepara) ou logo depois da fala (confirma), nunca
   ausente. Só se dispensa numa troca rápida de 2 falas já ancoradas logo
   acima, e mesmo aí com cautela. Enquanto as vozes forem próximas, pecar por
   excesso de clareza, não por elegância.
2. **Tempo verbal escancarado.** Lembrança e presente não se confundem no
   ouvido. Antes de qualquer fala do passado, a narração crava "naquela tarde",
   "fazia dezoito meses", "ele costumava dizer".
3. **Aarav = memória, nunca presença.** A citação das rosas NÃO entra como
   homem falando ao vivo. A narração ancora primeiro ("as roseiras tinham sido
   ideia dele; ele costumava dizer, ainda vivo..."), e só então a voz do Aarav
   entra **baixa, distante, como quem se lembra de um som** — e a narração
   fecha de volta no presente ("ele dizia essas coisas. Aurora cresceu achando
   que o mundo inteiro falava assim"). Tratamento técnico: voz do Aarav com
   leve filtro/eco e volume reduzido, pra soar lembrança, não cena.
4. **Emoção marcada com tags v3** entre colchetes, dentro da fala (o modelo
   `eleven_v3` lê como direção de atuação, não fala em voz alta): `[suspira]`,
   `[baixo]`, `[frio]`, `[quase sorrindo]`, etc.
5. **Pausas (beats)** marcadas com `(pausa curta ~0,6s)` / `(pausa ~1s)` /
   `(silêncio ~1,5s)`. Silêncio tem peso — `decisoes:28`.
6. **Densidade descritiva.** Trechos de descrição longa (ex.: a genealogia do
   Raj) funcionam narrados, mas pedem fôlego. Marcados com ✂️ os cortes
   sugeridos pra versão TEASER (isca de Instagram); a versão AUDIOLIVRO
   mantém tudo.

---

## CENA 1 — A cadeira (café da manhã)

**[NARRADORA]**
A cadeira continuava ali. (pausa ~1s)
À cabeceira esquerda da mesa de jantar, entre o castiçal de prata que a mãe de
Aurora nunca deixava apagar e a janela que dava para os jardins de buxo, a
cadeira de Aarav Svensson permanecia em seu posto como um soldado fiel
esperando o general que jamais voltaria. (pausa curta)
Ninguém se sentava nela. Nem os criados ousavam movê-la.
(pausa curta)
Aurora olhava para a cadeira todas as manhãs. Não com a intenção de olhar —
isso ela jamais admitiria. Eram apenas dois segundos. Às vezes três. O
suficiente para sentir o aperto no peito, respirar fundo, e voltar ao pão com
manteiga. (pausa ~1s)

**[ELEONORA]** `[tom leve, de quem puxa conversa amena]`
Está frio lá fora hoje. (pausa curta) Você deveria usar o xale de lã quando
for ao jardim.

**[NARRADORA]**
disse a mãe, Eleonora, do outro lado da mesa, com aquela voz límpida e nórdica.
*(única tag de identificação da cena; ✂️ no teaser)*

**[AURORA]** `[sem levantar os olhos, seco]`
Não pretendo ir ao jardim.

**[ELEONORA]** `[sem acusar, só constatando]`
Pretendia ontem também. E acabou ficando duas horas entre as roseiras.
(silêncio ~1,5s)

**[NARRADORA]**
Aurora não respondeu. Não porque a mãe estivesse errada — estava, na verdade,
perfeitamente certa, como sempre. Não respondeu porque as roseiras eram o
único lugar da propriedade onde ela ainda conseguia sentir Aarav por perto, e
explicar isso exigiria uma conversa que nenhuma das duas estava preparada pra
ter às oito da manhã de uma terça-feira de março. (pausa ~1s)
As roseiras tinham sido ideia dele. Ele costumava dizer, ainda vivo, quando
convenceu o pai a importar as mudas de um viveiro na Jutlândia... (pausa curta)

**[AARAV]** `[memória — baixo, distante, leve eco, afetuoso]`
Rosas dinamarquesas em solo dinamarquês... plantadas por mãos indianas.

**[NARRADORA]**
Aarav tinha essa mania — transformar qualquer coisa ordinária em poesia.
Aurora cresceu acreditando que o mundo inteiro falava assim. Descobriu que não
quando ele se foi, e de repente tudo ao redor ficou em prosa. (pausa ~1s)
Fazia dezoito meses. (pausa curta)
Dezoito meses desde que o navio que levava Aarav numa expedição ao Ceilão fora
engolido por uma tempestade no Índico. A notícia chegou num envelope preto. O
som do envelope sendo aberto. O silêncio do pai. O grito da mãe — um único
grito agudo que pareceu rasgar o tecido do mundo. (pausa ~1s)
E depois, o vazio. Um vazio tão grande que parecia ter corpo próprio: sentava-se
à mesa com eles, caminhava pelos corredores, respirava dentro das paredes.
Aurora odiava os ecos. (silêncio ~1,5s)

---

## CENA 2 — Quem era Raj Svensson (narração pura) ✂️ condensável

> Toda esta cena é narração. No AUDIOLIVRO entra quase inteira (é o retrato que
> dá peso ao pai). No TEASER, corta-se: vai direto da Cena 1 para o anúncio.

**[NARRADORA]**
Raj Svensson era um homem que parecia ter sido esculpido por duas mãos
diferentes. A primeira, indiana, dera-lhe a pele cor de terra molhada, os olhos
escuros como café sem açúcar, os cabelos negros pratejando nas têmporas. A
segunda, dinamarquesa por décadas de convivência, dera-lhe o porte, a postura,
a forma precisa de falar — cada palavra medida como quem distribui ouro.
(pausa curta)
Filho único dos Kapoor, nobres do Rajastão, mandado a Copenhague aos catorze
anos pra estudar. Raj nunca voltou. Casou-se com Eleonora Bjerg, construiu uma
fortuna no comércio marítimo, ganhou o respeito que o dinheiro compra e a
admiração que a inteligência exige. (pausa curta)
Mas, debaixo de tudo, Raj carregava uma solidão que nem a esposa nem a filha
alcançavam. Uma solidão que Aarav, de alguma forma, preenchia. Porque Aarav era
o filho. O herdeiro. O rapaz que embarcara naquela expedição justamente porque
queria ver com os próprios olhos a terra de onde a família viera. (pausa ~1s)
E agora Raj, que jamais chorava, passava horas trancado no escritório. Aurora
sabia. Sabia pelos olhos vermelhos no jantar, pelo garfo seguro com força
demais, pelo modo como ele não olhava para a cadeira vazia. O pai estava se
despedaçando por dentro, como um navio que afunda sem fazer barulho.
(silêncio ~1,5s)

---

## CENA 3 — O anúncio (café, Joshua)

**[NARRADORA]**
Foi numa dessas manhãs de março que Raj anunciou a notícia durante o café. E
Aurora notou algo diferente na voz do pai. Algo que ela não ouvia há meses. Uma
espécie de propósito.

**[RAJ]** `[contido, mas com um fio de ânimo raro]`
Recebi uma carta de Casandra Russel. (pausa curta) O filho dela, Joshua,
precisa vir a Copenhague para seus estudos na universidade. Eu ofereci nossa
casa.

**[NARRADORA]**
O garfo de Aurora parou no ar. Eleonora pousou a xícara de chá com a delicadeza
calculada de quem precisa de um segundo pra processar.

**[ELEONORA]** `[cuidadosa]`
Joshua. (pausa curta) O segundo filho?

**[RAJ]**
O do meio. Tem vinte e um anos. Quer seguir carreira na academia — ciências
naturais, ou talvez política. Ainda não se decidiu. (pausa curta) Eu sou
padrinho dele, Eleonora. Faz anos que prometo a Casandra que cuidaria da
educação de um dos filhos se fosse necessário.

**[ELEONORA]** `[sem interrogação — afirmação]`
E é necessário agora.

**[RAJ]**
Os Russel são gente de bem. Donos de terras no interior da Zelândia. Casandra é
viúva há quatro anos e administra tudo sozinha. Não têm a vida da cidade. Mas
são educados, decentes.

**[ELEONORA]** `[precisa, sem maldade — só literal]`
Rústicos.

**[RAJ]** `[um olhar de "por favor, não comece"]`
Do campo. O rapaz vai estudar, precisa de um teto e de orientação. Eu posso
oferecer ambos. (silêncio ~1,5s)

**[NARRADORA]**
Aurora não tinha falado. Não porque não tivesse o que dizer — tinha, e muito.
Não falou porque as palavras estavam entaladas entre o peito e a garganta,
disputando espaço com algo quente e afiado que ela reconhecia como raiva. Um
rapaz. Na casa deles. No espaço de Aarav. (pausa curta) Aquele desconhecido
viria morar ali, andar pelos corredores deles, sentar-se à mesa deles. Talvez
até — e o pensamento fez Aurora cerrar os dentes — sentar-se na cadeira.
(pausa ~1s)

**[AURORA]** `[controlada demais, fria demais]`
Por quanto tempo?

**[RAJ]** `[ternura e firmeza inamovível]`
O tempo que for necessário. Pode ser um ano. Podem ser dois. Três. Ele fica até
estar pronto.

**[AURORA]** `[repetindo, apertado]`
Três anos. (pausa curta) Na nossa casa.

**[RAJ]**
Na nossa casa.

**[NARRADORA]**
Aurora olhou para a cadeira de Aarav.

**[AURORA]**
E onde ele vai dormir?

**[NARRADORA]**
O silêncio que se seguiu durou um instante, mas foi o suficiente. Aurora viu a
resposta nos olhos do pai antes que ele a dissesse.

**[RAJ]** `[desviando o olhar pela primeira vez]`
No quarto do andar de cima. O quarto leste.

**[NARRADORA]**
O quarto leste. Não o quarto de Aarav, no lado norte, com vista pro jardim. O
quarto leste era o de hóspedes. Era aceitável. Era suportável. Aurora respirou.

**[AURORA]**
Quando?

**[RAJ]**
Daqui a quinze dias.

**[NARRADORA]**
Quinze dias. Aurora tinha quinze dias pra se preparar pra presença de um
estranho na única fortaleza que lhe restava no mundo.

**[AURORA]** `[levantando-se, cortês de gelo]`
Com licença. (pausa curta) Vou ao jardim.

**[NARRADORA]**
Eleonora olhou para o marido. Raj olhou para a cadeira vazia. Ninguém disse
nada. (silêncio ~1,5s)

---

## CENA 4 — O jardim (promessa à cadeira)

**[NARRADORA]**
O jardim dos Svensson era um retângulo de verde e pedra nos fundos do casarão,
protegido por muros altos cobertos de hera. No canto direito, as roseiras de
Aarav dormiam sob a última geada do inverno, os galhos podados esperando a
primavera. Aurora sentou-se no banco. O frio mordia suas mãos sem luvas, mas ela
não se importava. O frio era honesto. O frio não tentava ocupar o lugar de
ninguém. (pausa ~1s)
Joshua Russel. Ela virou o nome na boca como quem prova algo e não tem certeza
se gosta do sabor. (pausa curta) Viria para Copenhague, tropeçaria nas regras de
etiqueta, usaria o talher errado no jantar. E todos, absolutamente todos na
Bredgade, iriam olhar para ele morando na casa dos Svensson e pensar a mesma
coisa: (pausa curta) o novo filho de Raj. O substituto. (pausa ~1s)
Ninguém substituía Aarav. Ninguém. Aarav era insubstituível como o sol é
insubstituível — pode-se acender mil velas, mas nenhuma delas aquece como ele.
(pausa curta) Aurora olhou para as roseiras adormecidas.

**[AURORA]** `[sussurro, feroz e baixo — [whispers]]`
Ninguém vai sentar na sua cadeira, Aarav. (pausa curta) Eu prometo.

**[NARRADORA]**
O vento de março levou suas palavras, mas Aurora tinha certeza, absoluta,
inabalável, de que o irmão ouvira. (silêncio ~1,5s)

---

## CENA 5 — A véspera (quarto, mãe e filha) ✂️ condensável no teaser

**[NARRADORA]**
Os quinze dias passaram como passam todas as coisas que não queremos que
cheguem: rápido demais. Na véspera da chegada, Eleonora entrou no quarto de
Aurora enquanto ela escovava os cabelos diante do espelho.

**[ELEONORA]** `[baixo, sentando-se na beira da cama]`
Amanhã cedo. A carruagem dele chega antes do meio-dia.

**[AURORA]**
Eu sei.

**[ELEONORA]**
Seu pai espera que você seja cortês.

**[AURORA]** `[meio seca]`
Eu sou sempre cortês, mamãe.

**[ELEONORA]** `[com suavidade, sem acusar]`
Cortês de verdade, Aurora. Não essa sua cortesia gelada que faz as pessoas
sentirem que estão sendo recebidas e expulsas ao mesmo tempo.

**[NARRADORA]**
Aurora quase sorriu.

**[AURORA]** `[um fio de ternura cansada]`
Eu vou me comportar, mamãe. Pode dormir tranquila.

**[NARRADORA]**
Eleonora hesitou. Abriu a boca como se fosse dizer algo mais — algo que talvez
envolvesse Aarav, saudade, a necessidade de seguir vivendo — mas pensou melhor.
Levantou-se, beijou o topo da cabeça da filha, e saiu com o mesmo silêncio com
que entrara. (pausa ~1s)
Aurora ficou olhando o próprio reflexo por um longo tempo.

**[AURORA]** `[pensamento interior — sussurro íntimo, [whispers]]`
Cortês. Eu posso ser cortês. Posso ser a anfitriã mais cortês que Joshua Russel
já encontrou na vida. (pausa curta) Mas isso não significa que vou gostar dele.

**[NARRADORA]**
Pousou a escova. Apagou a vela. Deitou-se na escuridão e ficou ouvindo o vento
da noite empurrar os galhos da tília contra a janela. (pausa curta)
Amanhã tudo mudaria. (pausa curta) Ela só não sabia o quanto. (silêncio ~2s)

**[CARTELA/FIM]** — música sobe. "Os Russels — O Afilhado · Capítulo 1"

---

## Corte TEASER (isca de Instagram ~60–75s)

Hook puro, sem spoiler do Joshua. **Toda fala nomeia quem fala (regra 1).**

1. **NARRADORA:** "A cadeira continuava ali..." (parágrafo da cadeira,
   encurtado) "...Ninguém se sentava nela."
2. **NARRADORA (prepara):** "Do outro lado da mesa, a mãe de Aurora, Eleonora,
   levantou os olhos."
   **ELEONORA:** "Está frio lá fora hoje. Você deveria usar o xale de lã quando
   for ao jardim."
3. **AURORA:** "Não pretendo ir ao jardim." / **NARRADORA (confirma):** "disse
   Aurora, sem levantar os olhos do prato."
4. **NARRADORA (prepara):** "A mãe insistiu."
   **ELEONORA:** "Pretendia ontem também. E acabou ficando duas horas entre as
   roseiras."
5. **NARRADORA (ponte):** "As roseiras eram o único lugar onde Aurora ainda
   sentia o irmão por perto. Tinham sido ideia dele. Aarav costumava dizer,
   ainda vivo:"
   **AARAV (memória):** "Rosas dinamarquesas em solo dinamarquês, plantadas por
   mãos indianas."
6. **NARRADORA:** "Fazia dezoito meses desde que o navio que o levava fora
   engolido por uma tempestade no Índico. E desde então, o vazio."
7. **NARRADORA:** "Agora um estranho viria morar na casa. O substituto. Mas
   Aurora olhou para as roseiras adormecidas, e prometeu:"
   **AURORA (sussurro):** "Ninguém vai sentar na sua cadeira, Aarav. Eu prometo."
8. Cartela + "ouça o capítulo 1 completo no link".

Duração estimada: ~75–80s. É a cena mais forte, ensina o ouvido a distinguir as
vozes, cumpre a regra da atribuição e a regra da memória.

---

## Decisões que preciso de você antes de gerar

1. **Narradora:** mantém Kokoro `pf_dora` (grátis, um pouco robótica) ou eu
   desenho uma narradora sintética no ElevenLabs (mesma pegada, mais encorpada)?
2. **Voz do Raj:** preciso desenhar (barítono indo-dinamarquês, medido, sem
   sotaque). Te mando 3 opções pra escolher, como fiz com as outras.
3. **Escopo primeiro:** gero o **teaser de ~70s** primeiro (barato, pra validar
   o formato no ouvido) e, aprovado, o **capítulo 1 inteiro**? Ou já o capítulo
   inteiro?
