---
numero: 0009
data: 2026-11-18
status: aceita
escopo: produto
substitui: —
substituida_por: —
---
# No áudio, diálogo se gera em bloco contínuo, não fala por fala

## Contexto

O audiolivro de *O Afilhado* foi gerado fala por fala: cada fala de personagem
numa chamada própria ao TTS, com um prefixo de tom. A autora ouviu os capítulos
18 e 19 e definiu o Josh como "um robô": falas sem emoção, ou, quando se pedia
emoção, simpáticas e animadas no meio de uma cena de tensão. Ela mesma apontou a
causa: a narradora, gerada em blocos longos, interpretava; os personagens, gerados
isolados, não sabiam a que estavam respondendo.

## Decisão

Diálogo entre dois personagens é gerado numa chamada só, no modo multi-speaker
(Gemini 2.5 Flash TTS), precedido de uma direção de cena (lugar, hora, volume,
estado de cada um, o que não fazer). A narração continua separada. O bloco é
recortado de volta em falas (transcrição com marcação de tempo) para a narração
entrar entre elas. O modelo Pro foi testado e descartado: interpretou a cena como
debate. Teste aprovado pela autora: "a opção A ficou perfeita, ele fala baixo e
contido".

## Consequência

A narradora do OpenBooks não pode tratar fala como unidade de geração: a unidade
é a troca. O roteiro de áudio precisa marcar blocos de diálogo e carregar uma
direção de cena por bloco, e o limite de dois falantes por bloco vira regra de
montagem (cena com três vira dois blocos). Corrigir uma fala passa a significar
regerar o bloco inteiro. Detalhes operacionais em
`Os Russels/notas/audiolivro/REGRAS-DE-GERACAO.md`.
