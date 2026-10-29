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
