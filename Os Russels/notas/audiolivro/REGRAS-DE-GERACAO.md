# Regras de geração do áudio — O Afilhado

Resumo prático para gerar o áudio de um capítulo em qualquer motor. O histórico
completo das decisões está em `producao-audiolivro.md` (nesta mesma pasta).

## Motor e vozes

- **Gemini 2.5 Flash TTS** (`gemini-2.5-flash-preview-tts`). Cota Tier 1: 100
  requisições/dia por projeto, renova às 05h00 de Brasília.
- Elenco completo usado nos capítulos 1 a 19 (vozes pré-prontas do Gemini, salvo indicação).
  A chave é o código usado nos scripts `gerar-capNN.py`.

| Chave | Personagem | Voz | Caps | Prefixo / observação |
|---|---|---|---|---|
| `N` | Narradora | Vindemiatrix | 1–19 | sempre com o filtro de tom grave: `asetrate=24000*0.88,aresample=24000,atempo=1.1364` |
| `NM` | Memórias (Aarav, falas lembradas) | Vindemiatrix | 6, 10, 16, 19 | narradora + filtro de memória `highpass=f=240,lowpass=f=3200,aecho=0.8:0.6:55:0.3,volume=0.72` |
| `AU` | Aurora | Leda | 1–19 | sempre `BR` ("Diga em português do Brasil, com sotaque brasileiro:"); em tensão/intimidade `AI` ("…num tom sincero e contido, sem animação:") |
| `JOSH` | Josh | Zubenelgenubi | 2–19 | sem prefixo na conversa casual; em tensão `P1` ("Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem animação:"). O antigo `J` ("voz masculina grave e firme…") dos primeiros capítulos foi abandonado: deixava grosso |
| `JOSHW` | Josh em voz baixa/rouca | Zubenelgenubi | 6 | instrução de tom no próprio texto |
| `EL` | Eleonora (mãe) | Gacrux | 1–18 | `ELP` ("Diga com voz de senhora madura, grave e contida:") |
| `RAJ` | Raj (pai) | Algieba | 1–17 | nome falado "Ráge" |
| `DYLAN` | Dylan (irmão do Josh) | Achird | 2 | irônico, seco |
| `HELLE` | Helle (criada) | Achernar | 3, 13 | |
| `LARSEN` | Fru Larsen (cozinheira) | Kore | 3, 13 | |
| `MIK` | Sra. Mikkelsen | Sulafat no script; no áudio final, **ElevenLabs** (voz salva "Eleonora - Os Russels", eleven_v3) | 4 | no Gemini ficava igual à Aurora |
| `FRED` | Frederikke Mikkelsen | Autonoe | 4, 9 | |
| `LOV` | Lovise Mikkelsen | Laomedeia | 4 | |
| `CAS` | Casandra (cartas) | Pulcherrima | 5 | |
| `SOL` | Madame Solberg (modista) | Despina | 6, 14 | |
| `ING` | Ingrid Mortensen | Aoede | 6, 12, 14–16 | `BR` |
| `ERIK` | Erik Mortensen | Iapetus | 10, 15, 16 | `BR` |
| `HJ` | Hjalmar Eriksen ("Iálmar") | Puck | 15 | |
| `LYK` | Lykke Eriksen ("Lúque") | Zephyr | 15 | |
| `VIB` | Vibeke ("Vibêke") | Laomedeia | 17, 18 | `VB` ("…com alegria espontânea:") |
| `LUN` | Sra. Lundgren | Sulafat | 18 | `ELP` |
| `CR1`–`CR3` | vozes de reserva (Erinome, Callirrhoe, Zephyr) | — | — | declaradas, nunca usadas |

- **Takes fixos** (colar o arquivo, não gerar de novo), em `audio-ref/` ou nesta pasta:
  `josh_aurora.wav` ("Aurora" de chamado), `ref-josh-aurora-intenso.wav` ("Aurora" de
  intensidade), `ref-josh-voz-certa.wav` (timbre aprovado do Josh), `ref-josh-tom-intimo.wav`
  e `ref-aurora-tom-intimo.wav` (tom íntimo aprovado dos dois).
- **No diálogo contínuo** (multi-speaker), as vozes são as mesmas da tabela; o prefixo
  vira a direção de cena no começo do texto.

## Roteiro: como o texto vira áudio

- **Não é leitura literal.** É adaptação estilo Audible: narradora + vozes de
  personagem. Pode cortar enchimento; **não muda trama nem fala**.
- **Ler é diferente de ouvir: mastigar o contexto.** Quem ouve não volta a página.
  - **Vinheta** em todo capítulo: "Você está ouvindo O Afilhado. Uma produção
    Romance no Bolso. Capítulo N: título." Sem "fim do capítulo" no encerramento.
  - **Abertura:** de quem é o POV, onde está e o que aconteceu antes que importa
    ("Este capítulo volta aos olhos de Aurora. No capítulo anterior…").
  - **Primeira aparição** de cada pessoa no capítulo: quem é ("Helle, a criada";
    "Kóngen, o gato de Fru Larsen").
  - **Referência a cena anterior:** dizer qual foi ("na volta do chá, no vidro da
    carruagem").
  - **Troca de POV** no meio do capítulo: anunciar ("Agora, do outro lado da casa…").
  - **Objeto ou lugar** que o ouvinte não visualiza: descrever uma vez (a pérgola).
  - **Cartas:** dizer quem escreve e dar a voz de quem escreveu.
  - Todo contexto acrescentado é **conferido no texto dos capítulos** antes de entrar.
- **Toda fala é atribuída pela narração** ("Aurora respondeu, a voz fria:"). O
  ouvinte nunca fica sem saber quem fala e com que emoção.
- **A emoção vai na atribuição da narradora**, não em instrução dentro da fala.
  Instrução longa dentro da fala vaza e é lida em voz alta.
- **Fala repetida** por um personagem ("Meu problema?") vai na voz dele, num
  trecho próprio, nunca dentro da narração.
- **Mortos e memórias** (Aarav; falas lembradas): na narradora, com moldura ("ele
  costumava dizer:") e o filtro de memória (`NM`).
- **Pausas** (o número no fim de cada linha do roteiro, em segundos):
  - 0,2 entre falas;
  - 0,3 a 0,5 no fim de uma troca ou antes de uma frase que pesa;
  - 1,0 a 1,2 na troca de cena e depois da vinheta;
  - 0,05 entre pedaços do mesmo bloco de diálogo contínuo.
  Silêncio tem peso: não encher.

## Diálogo contínuo (regra de 18/11)

**Diálogo entre dois personagens se gera numa chamada só**, com os dois falantes
(modo multi-speaker do Gemini), e não fala por fala. Gerada isolada, a fala não
sabe a que está respondendo e sai robótica, ou "simpática" fora de hora. É por
isso que a narradora, gerada em blocos longos, sempre teve mais interpretação.

- **Motor:** `gemini-2.5-flash-preview-tts` (opção A, aprovada). O Pro
  (`gemini-2.5-pro-preview-tts`) saiu "debate", não tensão. Não usar.
- **Scripts:** `dialogo-continuo.py` (teste de um bloco) e `blocos18.py` (capítulo
  inteiro: gera cada bloco, transcreve com marcação de tempo, recorta cada fala
  de volta para o seu `{slug}.seg.wav`, e o `gerar-capNN.py` costura com a
  narração no meio).
- **Máximo de dois falantes por bloco.** Cena com três (ex.: Lundgren, Eleonora e
  Vibêke) vira dois blocos, separados pela narração.
- **O nome do falante** nas linhas tem que ser exatamente o configurado na
  chamada (`Josh:`, `Aurora:`, `Vibêke:`, `Senhora Lundgren:`).
- **Tamanho:** uma troca inteira, de 2 a 15 falas. Narração curta no meio ("Ele
  hesitou.") continua separada, entre dois pedaços do bloco.
- **As falas vão limpas**, sem prefixo "Diga…": o tom inteiro vai na direção de cena.
- **Pronúncia** segue o mapa abaixo também dentro do bloco (Rássel, Vibêke…).
- **Conferir o recorte:** transcrever cada pedaço. Se uma fala sair embolada,
  troca-se a frase e regera-se **o bloco inteiro** (não a fala solta).

### Atualizações de 18/11 (retomada pelo cap 18)

- **Bug corrigido no recorte:** o `blocos18.py` passava ao faster-whisper o áudio de
  24 kHz como se fosse de 16 kHz, e as marcações de tempo saíam 1,5× deslocadas
  (os recortes caíam no lugar errado). Agora o áudio é reamostrado para 16 kHz
  antes de transcrever. `--recortar` refaz só o recorte, sem gastar cota.
- **Cap 18:** a cena da janela (Josh e Aurora, `i076`–`i124`) saiu da geração fala
  por fala e entrou em dois blocos contínuos (`B6a`, `B6b`), com direção de cena
  de tensão e ciúme. O "Aurora" de intensidade (`i098`) continua sendo o take colado.
- **Cap 19:** `blocos19.py` monta os blocos direto do `gerar-cap19.py` (faixas
  `A1a`…`S5`, cada uma com a direção do momento emocional). `--takes N` gera N
  versões de cada bloco para a autora escolher.
- **Caminhos:** os scripts gravam em `$GTTS_BASE` (padrão `/tmp/gtts`), não mais
  num scratchpad fixo de outra sessão.
- **Cota esgotada:** o gerador para com `COTA_ESGOTADA` e a continuação fica
  agendada para depois das 05h00 de Brasília. **Não trocar de chave/projeto para
  furar a cota** (ver `producao-audiolivro.md`, decisão de motor).

- **Volume normal na conversa (autora, 18/11):** a regra é só a fala contínua, não
  cochicho. Conversa entre Josh e Aurora vai em volume **normal, médio, no mesmo
  nível dos dois**: "não sussurram, não cochicham, não falam alto". Nada de "voz
  baixa", "tom mais baixo" ou "para ninguém ouvir" na direção: o Gemini cochicha.
  Tensão se pede pela emoção, não pelo volume.

- **Blocos curtos (autora, 19/11):** de 4 a 8 falas. Bloco longo faz o Gemini
  "derivar": o Josh vira voz de moça no meio. O `blocos18.py` mede o tom de cada
  fala do Josh e **refaz o bloco sozinho** se passar de 130 Hz (ele fica em ~100).
- **"Aurora" na boca do Josh nunca é gerado, nem dentro do bloco:** no bloco saiu
  "orora" e "oraurora". A fala vira take colado (`josh_aurora.wav` ou
  `ref-josh-aurora-intenso.wav`) + o resto da frase no bloco.

- **Vibêke e as senhoras ficam fora do diálogo contínuo (autora, 19/11):** no
  bloco a Vibêke perdeu o prefixo "com alegria espontânea" e ficou igual à
  Aurora, e diferente do cap 17. Elas voltam ao método do cap 17: fala por fala,
  com prefixo. O diálogo contínuo fica nas cenas do Josh.
- **Ritmo:** falas de bloco entram a 0,92 da velocidade (`atempo=0.92`) e com
  as pausas do roteiro; a direção de cena pede "ritmo calmo, com pausas entre as
  falas".

- **"Aurora" do Josh = só o chamado padrão `josh_aurora.wav` (autora, 19/11).** O
  take `ref-josh-aurora-intenso.wav` saiu "oraroura" na escuta do cap 18: não usar.
- **Take de outra geração pode ser colado** quando a autora aprovar a fala (ex.:
  `take-cap18-i077-aurora.wav`, entra como `CLIP:take-cap18-i077-aurora`).

- **Josh sem "grave" afina (autora, 19/11):** tirar "grave e aveludada" da direção
  (para corrigir o cochicho) fez o Josh afinar fala a fala até soar feminino. A
  direção dele leva sempre: "grave e aveludada, voz de peito, a mesma do começo ao
  fim, nunca fina, nunca fanha, nunca feminina" + volume normal. A checagem de Hz
  não pega fanho: só a escuta pega.
- **Pausa interna longa:** fala de bloco passa por `silenceremove` (pausa interna
  no máximo ~0,4 s). O "Por quê?" do cap 18 veio depois de um silêncio enorme.

### Como escrever a direção de cena

Um parágrafo antes das falas, sempre com estas peças:

1. **Abertura fixa:** "Leia em português do Brasil, com sotaque brasileiro, como
   uma cena de audiolivro de romance de época, interpretada por [dois atores /
   duas atrizes / um ator e uma atriz], com naturalidade, como conversa de
   verdade, sem ler."
2. **Onde e quando:** "Fim de tarde, no quarto de Aurora." / "Dentro da carruagem,
   a caminho do baile." / "Madrugada, numa sala escura."
3. **Volume:** "falam num tom mais baixo, sem sussurrar" (sala cheia, para não
   ser ouvida), ou "falam baixo para não acordar a casa" (madrugada). Nunca só
   "baixo": vira cochicho.
4. **Cada personagem: idade, voz e estado naquela cena.** Ex.: "Vibêke, a prima de
   dezenove anos, alegre, espontânea, fala com entusiasmo. Aurora responde seca,
   rápida, mas com carinho escondido."
5. **O que NÃO fazer**, quando há risco conhecido: "nunca animado, nunca
   simpático, nunca leve" (Josh em tensão); "sem nenhuma infantilidade" (Aurora).
6. **Um detalhe de corpo**, se ajudar: "ele respira entre as frases".

Exemplos que funcionaram (cap 18):
- *Família/leve:* "Dentro da carruagem, a caminho do baile. Eleonora, a tia,
  senhora madura, voz grave e contida, elegante, com humor seco. Vibêke, a
  sobrinha, alegre e sincera, sem filtro."
- *Contido/observação:* "No salão, sentadas lado a lado, falando num tom mais
  baixo, sem sussurrar, para ninguém ouvir. Eleonora, a mãe, grave, contida,
  observadora, sem olhar para a filha. Aurora, a filha, disfarçando o incômodo,
  respostas curtas e educadas."

## Tom de cada voz

### Josh
- Voz de homem jovem, de rapaz, **masculina**. NUNCA fanha, afeminada ou animada.
  Take de referência do timbre certo: `ref-josh-voz-certa.wav`.
- **Conversa casual** (flerte bem-humorado, família, irmãos): sem prefixo, está bom.
- **Tensão, atração, contenção, desejo:** "voz de homem jovem, grave, baixa e
  aveludada, calma, sem animação" (`P1`). Sem isso ele sai animado, mecânico ou
  robótico. O "Aurora" de advertência também vai nesse tom.
- **Não usar:** "rouca e contida" (P2) fica grosso demais; "voz masculina grave e
  firme, de um homem de vinte e um anos" (`J`, dos primeiros capítulos) também.
- **Fala baixa/sussurrada:** "Diga em voz baixa e grave, quase num sussurro:"
  funciona sem vazar (cap 5).
- **Escorregou para português de Portugal:** prefixo "Diga em português do
  Brasil, com sotaque brasileiro:" (resolveu no cap 11).
- **Josh não é monossílabo:** em momento de sentimento, a fala ganha meia frase
  ("Tudo bem. Você não tem culpa de nada."), nunca uma palavra solta.
- **"Aurora" dito por ele:** de chamado → colar `josh_aurora.wav`; de intensidade
  (aviso, súplica) → colar `ref-josh-aurora-intenso.wav`. Não gerar. Dentro de
  frase, escrever "Aurôra".
- **Conferir:** tom acima de ~165 Hz pode ser take feminino; ouvir.

### Aurora
- Sempre "em português do Brasil, com sotaque brasileiro" (`BR`).
- **Cena tensa ou íntima:** "num tom sincero e contido, sem animação" (`AI`). Sem
  isso sai "animada demais" ou "criança de dez anos" (ex.: o "Mentira sua" do
  cap 15 saiu infantil).
- Tom aprovado: suave, às vezes tensa, com dúvida quando pergunta e com afronta
  quando questiona. Referência: `ref-aurora-tom-intimo.wav`.

### Narradora
- Vindemiatrix com o filtro grave, sempre.
- Narra a emoção na atribuição ("disse, a voz fria:"), e é ela quem dá contexto.
- Se o texto da narração disser "baixou o tom", "baixinho" ou "sussurrou", **ela**
  cochicha: reescrever ("disse, sem levantar a voz").
- "Josh" na narração às vezes sai errado: usar "ele" ou "o afilhado".

### Os outros
- **Eleonora, Sra. Lundgren:** senhora madura, grave e contida (`ELP`).
- **Vibêke:** alegria espontânea, sem filtro, entusiasmo (`VB`).
- **Ingrid, Erik:** `BR`.
- **Sra. Mikkelsen:** ElevenLabs (no Gemini ficava igual à Aurora).

## Efeitos sonoros

**Situação:** só um efeito foi feito até agora, a ambiência da festa no celeiro
(cap 15). A amostra foi **aprovada pela autora** ("tá legal"), mas tem só 2 segundos
e **ainda não foi encaixada** no capítulo 15. Arquivo: `efeitos/celeiro-amostra.mp3`.

- **Motor:** ElevenLabs, efeito sonoro (`eleven_text_to_sound_v2`). O Gemini não
  gera efeito.
- **Prompt em inglês**, descrevendo época, lugar, fontes de som e o que evitar.
  O do celeiro, aprovado:
  > 1830s Danish barn party ambience heard from inside: lively folk fiddle and
  > accordion playing a fast country dance, boots stomping on wooden floor, crowd
  > chatter and laughter, warm and festive, no modern sounds
- **Sempre** terminar o prompt com "no modern sounds" (é 1830).
- **Para ambiência**, gerar com duração de ~30 s e em loop (`loop: true`); a
  amostra de 2 s não serve de fundo.
- **Efeito é ambiência, não protagonista:** entra por baixo da cena, nunca por
  cima de fala. Só em cena que pede lugar (festa, baile, carruagem, chuva), não
  em todo capítulo.

**Como encaixar (planejado, ainda não testado com a autora):**
- mixar por baixo da narração e das falas da cena, em volume baixo (cerca de
  -20 dB abaixo da voz), em loop pela duração da cena;
- entrada e saída em fade (2 a 3 s), sem corte seco;
- primeiro mandar só a cena com o efeito, para a autora aprovar o volume, antes de
  aplicar no capítulo inteiro.

**Ideias levantadas e ainda não feitas:** ambiência do baile dos Lundgren (cap 18:
orquestra de salão, conversa, taças), carruagem na pedra da Brédigueide, e o
degrau que range (cap 19).

## Ciclo de correção com a autora

1. Gerar o capítulo, conferir (transcrição + tom do Josh), refazer o que falhou.
2. Mandar `capNN-completo.mp3` com os **minutos de cada cena**.
3. A autora ouve e aponta o minuto e o problema.
4. Regerar **só o trecho** (3 takes, escolher o melhor), mandar em áudio separado.
5. Com aprovação, encaixar no capítulo e salvar como `capNN-completo-final.mp3`.
6. Regra nova da autora vira linha neste arquivo e em `producao-audiolivro.md`.

## Pronúncia (escrever como se fala)

Mapa completo do que foi usado nos capítulos 1 a 19. A coluna da esquerda é como
está no livro; a do meio é como se escreve no roteiro de áudio.

### Nomes de pessoas

| No livro | No áudio | Observação |
|---|---|---|
| Raj | **Ráge** | "Raj"/"Ráje" saía "rais", "raigue". Na narração, preferir "o pai" / "o padrinho" |
| Aarav | **Aráve** | "Arav" saía "Arrav"; "Aarav" saía embolado |
| Aurora (dita pelo Josh, dentro da frase) | **Aurôra** | sozinha saía "auraa", "aurowruwa"; na narração, se embolar, também "Aurôra" |
| Aurora, como chamado isolado do Josh | colar o take `josh_aurora.wav` ou `ref-josh-aurora-intenso.wav` | não gerar |
| Russel / Russels | **Rássel / Rássels** | na boca da Lúque, trocado por "Rapaz" |
| Vibeke | **Vibêke** | |
| Bjerg | **Bierg** | |
| Erik | **Érik** | |
| Eriksen | **Ériksen** | |
| Hjalmar | **Iálmar** | |
| Lykke | **Lúque** | |
| Oehlenschläger | **Ólenchlêguer** | nunca sozinho numa fala ("Isso é Ólenchlêguer.") |
| Montesquieu | **Montesquiê** | |
| Kongen (o gato) | **Kóngen** | |
| Christian VI | **Cristiano Sexto** | |

### Lugares

| No livro | No áudio |
|---|---|
| Bredgade | **Brédigueide** |
| Sorø | **Sorô** |
| Christianshavn | **Kristiánshaun** |
| Kastellet | **Kástelet** |
| Aalborg | **Ólborg** |
| Aarhus | **Órus** |

### Palavras comuns

| Palavra | No áudio | Por quê |
|---|---|---|
| certamente | **Sertamenti** | saía "tchertamente" |
| naturalmente | trocar por **certamente** (Sertamenti) | L espanhol |
| rápido | trocar por **depressa** / **ágil** | saía "rapto" |
| desceram | **desseram** | |
| pelos (do corpo) | **pêlos** | saía "pélos" |
| robe | **róbe** | |
| igreja | **igrêja** | |
| cor | **cór** | |
| cerca | **cêrca** | |
| seca (adjetivo) | **sêca** | |
| buffet | **bufê** | |
| Sirva / "Servi" (fala curta) | **Sérvi** | |
| "Josh emendou" | **"Josh consertou"** | "emendou" e "corrigiu" embolavam |
| "vou ser direta" | **"eu vou ser direta"** | saía "vousê" |
| madrugadora | evitar ("que também acordava muito cedo") | saía "madrigadora" |
| "dar cobertura" | **"Te dar cobertura?"** | saía com sotaque espanhol |
| "Está verde" | **"Seu rosto está meio verde"** | frase curta falhava |
| "Para." (Aurora) | **"Para, Aurora."** | sozinha saía "parami" |
| "Útil por quê?" | **"E por que seria útil?"** | "útil" sozinho embolava |

### Regras gerais de pronúncia

- Fala de uma palavra só falha (finishReason OTHER) ou sai embolada: alongar com
  meia frase ("Josh." → "Josh. Olha pra mim."; "Sim." → "Sim, Josh.").
- Nome estrangeiro nunca sozinho numa fala curta: sempre dentro de uma frase.
- Se a narração disser "baixou o tom" / "baixinho", a narradora cochicha: reescrever
  a atribuição ("disse, sem levantar a voz").
- "Josh" na narração às vezes sai errado: usar "ele" ou "o afilhado".
- Depois de gerar, transcrever e procurar o nome: se o nome não aparece na
  transcrição, quase sempre saiu errado (foi assim que se achou o "aurara" e o "Arrav").

## Conferência

Antes de mandar, transcrever com faster-whisper (modelo small, int8) e comparar
com o texto; razão abaixo de 0,85 = ouvir e refazer. Tom do Josh acima de
~165 Hz = conferir se não saiu feminino.

## Arquivos desta pasta

- `capitulo-19-a-madrugada-aurora.md` — o capítulo (Aurora com 18 anos).
- `gerar-cap19.py` — o roteiro de áudio atual, fala por fala (o que você ouviu).
- `dialogo-continuo.py` — o gerador de diálogo contínuo.
- `producao-audiolivro.md` — histórico completo de decisões de voz.
- `audio-ref/` — takes aprovados de referência.
