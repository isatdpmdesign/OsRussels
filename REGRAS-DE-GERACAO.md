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

## NOVA REGRA (18/11) — diálogo contínuo

**Diálogo entre dois personagens se gera numa chamada só**, com os dois falantes
(modo multi-speaker do Gemini), e não fala por fala. Gerada isolada, a fala não
sabe a que está respondendo e sai robótica ou "simpática" fora de hora.

- Script: `dialogo-continuo.py`. Uso:
  `GKEY=sua_chave python3 dialogo-continuo.py gemini-2.5-flash-preview-tts saida`
- O texto da chamada tem duas partes:
  1. **Direção de cena** (um parágrafo): onde, que horas, como falam, o estado de
     cada um. Ex.: "É madrugada, numa sala escura, os dois falam baixo para não
     acordar a casa. Josh: voz grave, baixa, aveludada, contida; nunca animado,
     nunca simpático. Aurora: suave, firme, às vezes desafiadora, sem
     infantilidade."
  2. As falas, uma por linha: `Josh: ...` / `Aurora: ...`
- Teste aprovado: **opção A (Flash)**. O Pro saiu "debate", não tensão.
- **A narração continua separada** (voz da narradora), entre os blocos de diálogo.
- Bloco de diálogo ideal: uma troca inteira (6 a 15 falas). Narração curta que
  cai no meio (ex.: "Ele hesitou.") pode virar uma pausa no bloco.

## Regras de voz que continuam valendo

- **Josh**: voz de homem jovem, masculina, nunca fanha, afeminada ou animada.
  Em cena de tensão, prefixo/direção: "voz de homem jovem, grave, baixa e
  aveludada, calma, sem animação". Nunca o "rouco e contido" (fica grosso demais).
- **Josh não é monossílabo**: em momento de sentimento, a fala ganha meia frase.
- **Aurora** em cena tensa: "num tom sincero e contido, sem animação". Sem isso
  sai infantil.
- **"Aurora" dito pelo Josh**: de chamado → take `audio-ref/josh_aurora.wav`;
  de intensidade → take `audio-ref/ref-josh-aurora-intenso.wav`.
- "Baixo" não é "sussurro": se a narração diz "baixou o tom", a narradora
  cochicha. Reescrever a atribuição.
- A emoção vai na atribuição da narradora, não em instrução dentro da fala
  (instrução vaza e é lida em voz alta).
- Falas de uma palavra só falham (finishReason OTHER) ou saem emboladas:
  alongar um pouco.
- Vinheta de abertura: "Você está ouvindo O Afilhado. Uma produção Romance no
  Bolso. Capítulo N: título." Sem "fim do capítulo".
- Abertura de capítulo com contexto ("Este capítulo volta aos olhos de…"),
  primeira aparição de cada pessoa explicada, cartas na voz de quem escreve.

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
