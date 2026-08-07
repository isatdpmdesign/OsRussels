# Perfil de estilo — Os Russels

> **O que é este arquivo:** as regras duras de superfície deste livro.
> É *dado*, não método. As skills de revisão leem daqui; o `lint.py`
> executa a parte verificável a partir do `livro.yaml`.
>
> Regra de decisão da autora **anula** qualquer instrução genérica de
> skill. Quando esta pasta discordar de uma skill, esta pasta ganha.

---

## Regras duras

| Regra | Detalhe |
|---|---|
| **Travessão só em fala** | Narração usa parênteses, dois-pontos, vírgula ou ponto. O travessão fica reservado para fala, intercalada fala-narração (`— disse ele —`) e interrupção dramática. |
| **Sem artigo antes de Josh/Aurora em narração** | "Josh desceu", não "o Josh desceu". **Em fala o artigo é permitido e natural** ("o Josh sabe se a mãe dele cavalga"). Personagens secundários ("a Vibeke", "a Meridiana") têm tolerância maior na narração íntima — manter o padrão do capítulo. |
| **PT-BR contemporâneo** | "é sério", "pro/pra", "tá", "a gente". Sem floreio pseudo-época. A imersão vem dos costumes, do vestuário e dos espaços — nunca da gramática arcaica. Sem "tu" + conjugação clássica: sempre "você". |
| **Sem gírias modernas** | Registro literário, leitura fácil. |
| **Hard wrap a 50 caracteres** | A partir do capítulo 25. Cabe sem scroll horizontal no diff do GitHub num iPhone 16 — é assim que a autora revisa. |
| **Diálogo com travessão** | Padrão brasileiro. Sem aspas duplas para fala. |
| **Sem auto-referência a capítulo na narração** | O personagem não sabe que está num livro. Usar referência interna do mundo: "a madrugada da sala de estar", "o bosque dos Russels", "a noite do pomar". |

## Cotas

| Item | Teto |
|---|---|
| Fórmulas `como quem / do jeito que / a forma como / com a X de quem` | ~10 por capítulo de 4–5 mil palavras |
| Pingue-pongue monossilábico | máximo 2 trocas seguidas |
| Repetição da mesma raiz em espaço curto | máximo 3, e só com motivo claro (clímax verbal) |

## Blacklist

| Item | Motivo | Exceção | Desde |
|---|---|---|---|
| **peso / pesar / pesava / pesou / pesad-** como metáfora emocional | Virou jargão de IA | Usos literais (pesar farinha, carregar coisa pesada) — confirmar com a autora | jun/2026 |
| **"calo da pena"** fora do Cap 19 | Canon antigo. Josh tem mãos brutas de campo: calo de machado, nó dos dedos com arranhão antigo da pérgola | Cap 19 | jun/2026 |
| **"como quem comenta o clima/tempo"** | Régua do Josh sobre o Dylan (`cap20:143`). Cada personagem cria a própria | — | jun/2026 |

## Princípios de escrita (o que a autora pede)

- **Claro e escancarado > subjetivo e aberto.** Se o POV entendeu, escreve. Se a fala teve significado, nomeia. Na dúvida entre subtexto literário e clareza explícita, **escolha clareza** — a história ganha em arrasto e emoção porque a leitora sabe o que está em jogo a cada cena.
- **Régua dos personagens.** Cada personagem cria a própria imagem do mundo. Aurora descreve o Dylan com a régua dela, não com eco do que Josh já falou. Observação usada por um POV não se recicla em outro.
- **Anti-aforismo de fechamento.** Parágrafos podem terminar mal, no meio, secos. Não fechar tudo redondo.
- **Mais diálogo.** O livro pende para introspecção narrada quando devia ter troca direta. Cada cena emocional pede diálogo real, não só pensamento interior + síntese do narrador. Cuidar do silêncio (que tem carga) e do falado (que tem mais).
- **Cenas íntimas: a cena do livro.** Sem explícito gráfico ou mecânico, mas com sensorial intenso. Metáfora e ritmo a ponto de arrepiar a leitora. Nada de fade preguiçoso.
- **Slow burn é regra.** A economia do *quase* sustenta a tensão. Mais voltagem significa mais tensão e subtexto, não mais explícito.
- **Não se apegar a número de capítulos.** Se um capítulo pede desdobramento, desdobra.

## Estrutura de capítulo

```
# OS RUSSELS — Livro I

## O Afilhado

*Dinamarca, 1830*

---

### Capítulo [N] — [Título evocativo]

[corpo]

---

*Continua no Capítulo [N+1]...*
```

## POV

Terceira pessoa próxima, alternando entre personagens-foco. Discurso indireto livre permitido e usado bastante.

A alternância estrita capítulo a capítulo **não é mais regra** — foi abandonada na prática a partir do Cap 21 (Sorø inteiro pelos olhos de Aurora, cinco capítulos seguidos). O que vale: cada capítulo tem **um** POV, declarado no nome do arquivo, e não se troca de cabeça dentro do capítulo.

## Vozes

| Personagem | Fala |
|---|---|
| **Aurora** | cortesia afiada como arma — sorriso que inclui e exclui ao mesmo tempo |
| **Josh** | simplicidade direta, arma ofensiva involuntária |
| **Raj** | economia e gravidade |
| **Eleonora** | precisão nórdica, literalidade (não é maldade, é literalidade) |
| **Casandra** | prática, seca, maternal na intenção e não na forma |
| **Vibeke** | espontânea, alegre sem ironia — inteligente disfarçada de espontaneidade |
| **Dylan** | diz o que todos pensam sem parecer afetado |
| **Ingrid** | observadora ácida, diz verdades como quem comenta o tempo |
