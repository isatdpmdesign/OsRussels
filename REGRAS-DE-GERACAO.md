# Regras de geração do áudio — O Afilhado

Resumo prático para gerar o áudio de um capítulo em qualquer motor. O histórico
completo das decisões está em `producao-audiolivro.md` (nesta mesma pasta).

## Motor e vozes

- **Gemini 2.5 Flash TTS** (`gemini-2.5-flash-preview-tts`). Cota Tier 1: 100
  requisições/dia por projeto, renova às 05h00 de Brasília.
- Elenco (vozes pré-prontas do Gemini):

| Personagem | Voz | Observação |
|---|---|---|
| Narradora | Vindemiatrix + tom baixado (`asetrate=24000*0.88,aresample=24000,atempo=1.1364`) | |
| Aurora | Leda | sempre com prefixo de português do Brasil |
| Josh | Zubenelgenubi | ver regras abaixo |
| Eleonora | Gacrux | "senhora madura, grave e contida" |
| Raj | Algieba | |
| Vibêke | Laomedeia | "com alegria espontânea" |
| Sra. Lundgren | Sulafat | "senhora madura" |
| Helle | Achernar | |
| Fru Larsen | Kore | |
| Erik | Iapetus | |
| Ingrid | Aoede | |
| Iálmar | Puck | |
| Lúque | Zephyr | |
| Arav (memória) | narradora + filtro `highpass=f=240,lowpass=f=3200,aecho=0.8:0.6:55:0.3,volume=0.72` | |

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

| Palavra | Grafia no áudio |
|---|---|
| Raj | Ráge |
| Aarav | Aráve (sai "Arrav" com "Arav") |
| Aurora (na fala do Josh) | Aurôra |
| Bredgade | Brédigueide |
| Russel | Rássel |
| Vibeke | Vibêke |
| Oehlenschläger | Ólenchlêguer |
| Eriksen | Ériksen |
| Hjalmar / Lykke | Iálmar / Lúque |
| Sorø | Sorô |
| Kongen | Kóngen |
| robe, igreja, cor, cerca | róbe, igrêja, cór, cêrca |
| certamente | Sertamenti |

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
