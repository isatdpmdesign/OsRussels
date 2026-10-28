# Produção do audiolivro — regras e decisões

> Banco de dados do pipeline de áudio de "O Afilhado". Atualizar a cada decisão.

## Método de roteiro de áudio (vale pra qualquer motor)

- **Não é leitura literal.** Adaptação estilo Audible: narradora principal +
  vozes de personagem.
- **Toda fala é atribuída pela narração** ("Aurora respondeu, a voz fria:",
  "o pai interveio, num tom de aviso:"). O ouvinte nunca fica sem saber quem
  fala e com que emoção.
- **A emoção vai na voz da narradora** (na atribuição), NÃO em prefixo na fala
  do personagem — prefixo de instrução vaza (o modelo lê em voz alta).
- **Personagens mortos / memórias** (Aarav; falas lembradas de Casandra, Matias)
  ficam na **narradora**, com moldura ("ele costumava dizer, ainda vivo:") e,
  no caso do Aarav, filtro de eco/memória.
- Pausas entre falas; silêncio tem peso.
- Scripts por capítulo: `gerar-cap01.py`, `gerar-cap02.py` (resumíveis, salvam
  cada fala em cache e só regeram o que muda; a unificação é ffmpeg, custo zero).

## Elenco de vozes

| Personagem | Gemini (testado) | Observação |
|---|---|---|
| Narradora | Vindemiatrix + tom baixado (grave) | distinta da Aurora e da mãe |
| Aurora | Leda | 16, fria por fora |
| Eleonora | Gacrux | mãe, madura |
| Raj | Algieba | pai, barítono contido |
| Josh | Zubenelgenubi | 21, do campo, caloroso |
| Dylan | Achird | 19, irônico, seco |
| Aarav (morto) | narradora + filtro memória | só em lembrança |

> Ao trocar de motor (Cartesia/ElevenLabs), reescolher vozes equivalentes.

## Mapa de pronúncia (escrever como se fala)

| Nome | Grafia no áudio | Por quê |
|---|---|---|
| Raj | **Ráge** (fala); na narração, usar "o pai"/"o padrinho" | "Raj"/"Ráje" saía "rais/raigue/rague" |
| Bredgade | **Brédigueide** | saía "bredegaige" |
| Sorø | **Sorô** | — |
| "jardim" | conferir take (saiu "jédim") | — |

## Decisão de motor (28/out/2026)

- **Gemini 2.5 Flash TTS: descartado para o produto final.** Barato, mas:
  (1) teto de 100 requisições/dia no Tier 1 → livro levaria ~40 dias;
  (2) **não-determinístico** — cada geração troca erros antigos por erros novos
  de pronúncia/sotaque (verrdê, tchertamente, arowrua, Josh→"jóde", rápido→"rapto").
  Nunca converge. Serve pra rascunho, não pra vender.
- **Caminho escolhido: testar Cartesia** (sem teto diário de requisições, cobra
  por caractere; Startup US$49/mês ≈ 1,25M chars = livro inteiro num mês).
  Confirmar PT-BR + qualidade de emoção antes de migrar. Alternativa segura em
  emoção/consistência: ElevenLabs (mais caro).
- **Tiers do Gemini:** limite é por gasto acumulado (Tier 2 ~US$100, Tier 3
  ~US$1000), não por saldo. Por isso no começo do ano (R$1000 gastos) rendia
  mais/dia. Rotação de chave/conta pra driblar = violação de ToS, descartada.

## Capítulos prontos (áudio Gemini — provisório)

- **Cap 1** — fechado em `cap01-completo-v3` (aprovado com ajustes).
- **Cap 2** — gerado, mas com erros residuais de pronúncia do Gemini (verrdê,
  tchertamente, adapto rapto, arowrua, Josh→jóde). A refazer no motor novo.
