---
numero: 0002
data: 2026-08-07
status: aceita
escopo: engenharia
substitui: —
substituida_por: —
---
# Leitura e escrita de canon são agentes diferentes

## Contexto

O briefing descrevia a Bibliotecária com três verbos: lê a bíblia,
**mantém e atualiza** as fichas, e acusa contradição. Um deles é de
escrita, e isso cria um ciclo fechado perigoso: o agente aluciona um fato,
grava na ficha de continuidade, e na sessão seguinte lê a própria
alucinação como fonte confiável. A versão benigna disso já aconteceu aqui
— a ficha esteve um capítulo fora de fase enquanto o `CLAUDE.md` mandava
consultá-la primeiro. O projeto já registrava, por escrito, que subagentes
haviam inventado idades, descrições e números de linha.

## Decisão

A `biblioteca` e a `auditoria-de-canon` são somente leitura e citam
`arquivo:linha` em toda afirmação; sem fonte, a resposta é "não está
estabelecido", nunca uma suposição plausível. O `escriba-de-canon` é o
único que escreve na bíblia, na ficha, na sinopse e nas decisões
editoriais, e sempre por diff proposto e aprovado — inclusive para
corrigir um número óbvio. Os cinco subagentes de `.claude/agents/` não
recebem `Edit` nem `Write`.

## Consequência

O pior que um agente pode fazer passa a ser uma resposta errada, em vez de
uma resposta errada gravada como canon. A contenção é do desenho, não da
vigilância — e é a história comercial do produto: *a IA nunca altera o seu
canon em silêncio*, que é exatamente o medo de quem tem cento e setenta
mil palavras investidas.

O custo é atrito: toda correção de guia passa por aprovação, mesmo as
triviais, e isso torna a reconciliação de documentos mais lenta do que se
o agente pudesse simplesmente consertar. Aceito — a alternativa é um
sistema em que ninguém consegue dizer quem escreveu um fato.
