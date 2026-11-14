# Produção do audiolivro — regras e decisões

> Banco de dados do pipeline de áudio de "O Afilhado". Atualizar a cada decisão.

## Método de roteiro de áudio (vale pra qualquer motor)

- **Não é leitura literal.** Adaptação estilo Audible: narradora principal +
  vozes de personagem.
- **Ler é diferente de ouvir — mastigar o contexto** (regra da autora,
  29/out/2026). Quem ouve não volta a página. Toda vez que algo pode ficar
  solto no áudio, a narração lembra:
  - **abertura de capítulo:** quem é o POV, onde está, o que aconteceu antes
    que importa para este capítulo (modelo: a família do Josh no cap 2, a
    abertura do cap 5);
  - **primeira aparição no capítulo:** quem é a pessoa ("Helle, a criada";
    "Kóngen, o gato de Fru Larsen"; "Matias, o caçula, de treze anos");
  - **referência a cena anterior:** dizer qual foi ("na volta do chá, no vidro
    da carruagem");
  - **troca de POV no meio do capítulo:** anunciar ("Agora, do outro lado da
    casa, Aurora...");
  - **objeto ou lugar que o ouvinte não visualiza:** descrever uma vez (a
    pérgola);
  - **cartas:** dizer quem escreve e dar a voz de quem escreveu.
  Todo contexto acrescentado é **conferido no texto dos capítulos** antes de
  entrar (regra de ouro). Pode cortar enchimento; **não muda trama nem fala.**
- **Vinheta de abertura em todo capítulo** (decisão da autora, 29/out):
  "Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo N:
  <título>." Sem "fim do capítulo" no encerramento.
- **Conferência automática:** `conferir-pronuncia.py` transcreve os trechos
  (faster-whisper, local, custo zero) antes de mandar para a autora; pega
  troca de palavra e instrução lida em voz alta.
- **Voz do Josh (regra do cap 7, revista):** a voz normal (Zubenelgenubi,
  sem prefixo) está boa — a autora aprovou. O prefixo "voz masculina grave"
  deixou ele grosso demais: NÃO usar em tudo. Só conferir o tom depois de gerar
  e corrigir a fala que sair de menino (acima de ~170 Hz), refazendo ou com
  filtro leve.
- **Voz do Josh — o padrão** (autora, 08/nov): voz de homem jovem, de rapaz,
  masculina. NUNCA fanha, afeminada ou animada demais. Referência aprovada:
  `ref-josh-voz-certa.wav` (carta do cap 13, "pereiras"), gerada **sem
  prefixo nenhum**. Take que puxar para fanho/animado → refazer.
- **Tom íntimo (Josh e Aurora) — padrão para intimidade, tensão, atração,
  contenção e desejo** (autora, 08/nov): a voz deles, mas suave, mais baixa,
  levemente rouca, contida. Referências aprovadas: `ref-josh-tom-intimo.wav`
  ("Boa noite, Aurora", cap 13) e `ref-aurora-tom-intimo.wav` ("Boa noite,
  Josh", cap 13).
  - **Aurora:** prefixo "Diga em português do Brasil, com sotaque brasileiro,
    num tom sincero e contido, sem animação:" (é o mesmo do "Obrigada, Josh").
  - **Josh:** SEM prefixo (prefixo de tom deixou ele fanho/afeminado); gerar
    2–3 takes e escolher o mais suave. "Aurora" dentro da frase escrito
    "Aurôra".
  - Aurora sem esse prefixo em cena tensa sai "animada demais" ou "criança de
    10 anos".
- **Josh apaixonado — flerte, tensão, cena íntima** (autora, 13/nov): prefixo
  **"Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem
  animação:"** (teste "P1 aveludada", aprovado: "perfeita"). O "rouco e
  contido" (P2) ficou grosso demais: não usar. Em conversa casual (o flerte
  bem-humorado no caminho da festa) o Josh sem prefixo está bom. Sem prefixo
  em cena de tensão ele sai "animado", "mecânico", "robótico": é o erro a
  evitar. O "Aurora" de advertência (não de chamado) também vai com P1.
- **Josh não pode ser monossílabo no áudio** (autora, 13/nov): em momento de
  sentimento, a fala dele ganha meia frase ("Tudo bem. Você não tem culpa de
  nada."), nunca uma palavra solta.
- **"Aurora" do Josh em momento de intensidade** (aviso, súplica, tensão — autora, 13/nov): usar o take recortado `ref-josh-aurora-intenso.wav` (do "Por favor, Aurora…" aprovado no cap 15). O take de "chamado" (abaixo) fica para quando ele só a chama.
- **"Aurora" chamado pelo Josh** (aprovado pela autora, 06/nov): usar SEMPRE o
  mesmo take — o do cap 12 quando ela entra no quarto (c057, guardado como
  `josh_aurora.wav`). Não gerar de novo; colar o take.
- **Português de Portugal no Josh:** se escorregar, prefixo "Diga em português
  do Brasil, com sotaque brasileiro:" (resolveu na carta do cap 11).
- **Quando a personagem repete uma fala** ("Meu problema?", "Me mostrar?"),
  a repetição vai na VOZ DELA, num trecho próprio — nunca dentro da narração.
- **Falas sussurradas/baixas do Josh:** o prefixo curto "Diga em voz baixa e
  grave, quase num sussurro:" funciona no Gemini sem vazar (testado no cap 5).
- **Toda fala é atribuída pela narração** ("Aurora respondeu, a voz fria:",
  "o pai interveio, num tom de aviso:"). O ouvinte nunca fica sem saber quem
  fala e com que emoção.
- **A emoção vai na voz da narradora** (na atribuição), NÃO em prefixo na fala
  do personagem — prefixo de instrução vaza (o modelo lê em voz alta).
- **Personagens mortos / memórias** (Aarav; falas lembradas de Casandra, Matias)
  ficam na **narradora**, com moldura ("ele costumava dizer, ainda vivo:") e,
  no caso do Aarav, filtro de eco/memória.
- Pausas entre falas; silêncio tem peso.
- Scripts por capítulo: `gerar-capNN.py` (resumíveis, salvam cada fala em
  cache e só regeram o que muda; a unificação é ffmpeg, custo zero).
- **Ciclo de correção:** a autora ouve e aponta o minuto; regeramos só o
  trecho, mandamos em áudio separado, ela aprova, e só então entra no capítulo.

## Elenco de vozes

| Personagem | Voz | Observação |
|---|---|---|
| Narradora | Gemini Vindemiatrix + tom baixado (grave) | distinta da Aurora e da mãe |
| Aurora | Gemini Leda | 16, fria por fora |
| Eleonora | Gemini Gacrux | mãe, madura |
| Raj | Gemini Algieba | pai, barítono contido |
| Josh | Gemini Zubenelgenubi | 21, do campo, caloroso |
| Dylan | Gemini Achird | 19, irônico, seco |
| Helle | Gemini Achernar | criada |
| Fru Larsen | Gemini Kore | cozinheira |
| Sra. Mikkelsen | **ElevenLabs** (voz salva "Eleonora - Os Russels", eleven_v3) | no Gemini (Sulafat) ficava igual à Aurora — trocada no cap 4 |
| Frederikke | Gemini Autonoe | cap 4 |
| Lovise | Gemini Laomedeia | cap 4 |
| Casandra (cartas) | Gemini Pulcherrima | estreia no cap 5 — **a auditar com a autora** |
| Aarav (morto) | narradora + filtro memória | só em lembrança |

## Mapa de pronúncia (escrever como se fala)

| Palavra | Grafia no áudio | Por quê |
|---|---|---|
| Raj | **Ráge** (fala); na narração, usar "o pai"/"o padrinho" | "Raj"/"Ráje" saía "rais/raigue/rague" |
| Bredgade | **Brédigueide** | saía "bredegaige" |
| Sorø | **Sorô** | — |
| certamente | **Sertamenti** | saía "tchertamente" |
| naturalmente | trocar por **certamente** ("Sertamenti") | "naturalmenti"/"naturaomente" saíam com L espanhol |
| desceram | **desseram** | saía errado |
| Kongen | **Kóngen** | — |
| Montesquieu | **Montesquiê** | — |
| "rápido" | trocar por "depressa"/"ágil" | saía "rapto" |
| "Está verde" | "Seu rosto está meio verde" | frase curta falhava |
| "Josh emendou" | **"Josh consertou"** | "emendou" e "corrigiu" saíram embolados |
| "pelos" (do corpo) | **pêlos** | saía "pélos" |
| "vou ser direta" | **"eu vou ser direta"** | saía "vousê" |
| "Para." (Aurora) | **"Para, Aurora."** | sozinha saía "parami" |
| "Aurora" isolado | **"Me chame de Aurora."** / sussurro | saía "auraa", "aurowruwa" |
| madrugadora | evitar ("que também acordava muito cedo") | saía "madrigadora" |
| "jardim" | conferir take (saiu "jédim") | — |

Falas de uma palavra só falham às vezes no Gemini (finishReason OTHER); o
script tenta de novo com a fala entre aspas.

## Decisão de motor

- **29/out/2026 — fica no Gemini 2.5 Flash TTS.** A autora não quer pagar
  outra assinatura. Cartesia testada e descartada (emoção ruim); VoiceStudio
  descartado (robótico, só roda no PC dela). Os erros do Gemini variam de
  geração em geração, então o processo é corrigir trecho a trecho com
  aprovação dela.
- ElevenLabs (plano grátis) entra só pontualmente, para voz que o Gemini não
  diferencia (Mikkelsen).
- **Teto:** 100 requisições/dia no Tier 1 → ~1 capítulo/dia. Tiers sobem por
  gasto acumulado (Tier 2 ~US$100, Tier 3 ~US$1000). Rotação de chave/conta
  para driblar = violação de ToS, descartada.

## Capítulos

- **Cap 1** — fechado (`cap01-completo-v3`).
- **Cap 2** — fechado (com a abertura de contexto da família do Josh).
- **Cap 3** — fechado (29/out, correções aprovadas).
- **Cap 4** — fechado (29/out, correções aprovadas; Mikkelsen no ElevenLabs).
- **Cap 5** — primeiro gerado com a regra de contextualização reforçada.
- **Caps 6–12** — fechados (11 e 12 em 12/nov, após a rodada 2).
- **Cap 13** — fechado (08/nov, correções aprovadas; carta com "pereiras", choro "perdendo a força", "Capítulo dez", boa-noite opção B).
- **Cap 14** — fechado (11/nov, correções aprovadas; "Te dar cobertura?" opção A aprovada).
- **Cap 15** — gerado (12/nov), aguardando a escuta da autora. Vozes novas: Iálmar Eriksen (Puck), Lúque Eriksen (Callirrhoe).
- **Cap 16** — gerado (14/nov), aguardando a escuta da autora.

## Pendências de correção

- Caps 11 e 12: resolvidas e aprovadas (12/nov).

## Regra: "baixo" não é "sussurro"

Quando a fala é baixa, o prefixo diz "num tom mais baixo, sem sussurrar".
"Diga baixo" sozinho faz o Gemini cochichar.
