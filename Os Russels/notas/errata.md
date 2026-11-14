# Errata — Os Russels, Livro I: O Afilhado

> Correções pendentes no texto. **Item só sai daqui depois de conferido
> no capítulo**, não depois de alguém lembrar de ter corrigido.

---

## Pendentes

1. **Excesso de "Frederik" no livro (pedido da autora, 08/nov/2026 — para melhorar no futuro).**
   Três nomes quase iguais confundem, principalmente no áudio:
   - **os Frederiksen** — anfitriões do baile de abertura (residência na Kongens Nytorv) e do recital; `cap04:101`, `cap06:35,171,203-213`, `cap12:19`, `cap14:67,249`, `cap31`, `cap37`;
   - **Frederikke Mikkelsen** — a moça que flerta com Josh no baile e dança com ele no sarau dos Holst; `cap04:261-315`, `cap06:239-245`, `cap09:265-311`, `cap15:35`, `cap16:105`;
   - **Frederik Holst** — o pretendente de Aurora, filho mais novo dos Holst, afastado pelos conselhos de Josh; `cap11:87-105`, `cap12:41,101`.
   Também `cap09:169` cita "o mais novo dos Frederiksen". E a rua **Fredericiagade** (`cap14`, ponto de encontro na esquina com a Bredgade) soma mais um "Frederik" — no áudio do cap 14 foi trocada por "na esquina, perto de casa". Decidir com a autora quais nomes trocar; propagar com a skill `onda-de-mudanca`.

---

## Resolvidas

Verificação de agosto de 2026, item por item, contra o texto dos
capítulos. Os oito itens abertos estavam todos resolvidos — dois por
correção aplicada e seis porque os capítulos foram reescritos e o trecho
problemático deixou de existir. O arquivo estava desatualizado desde
então, dizendo "correções aplicadas: nenhuma ainda".

| # | Cap | Problema | Como se resolveu | Verificação |
|---|---|---|---|---|
| 1 | 7 | "dois anos de bailes" antes do debut — o baile dos Frederiksen (Cap 6) é o primeiro dela | correção aplicada: ficaram só chás e jantares | `grep "anos de bailes"` → 0 |
| 2 | 16 | Aurora sabia que Josh escrevia cartas **que não enviava** — informação exclusiva do POV dele | capítulo reescrito; o trecho não existe mais | `grep "não enviava"` → 0 |
| 3 | 16 | Aurora citava o dossel "que Josh reclamava em cartas à mãe" — ela não leu as cartas | capítulo reescrito | `grep "dossel"` → 0 |
| 4 | 14 | casa de Ingrid vazia de adultos sem explicação | correção aplicada: os pais estão em Aabenraa, na Jutlândia | `grep "Aabenraa"` → 2 |
| 5 | 15 | beijo do celeiro podia ser mais visceral | superado: o beijo virou **quase-beijo** na reescrita | — |
| 6 | 16 | Aurora citava Meridiana e as pereiras — ela nunca conheceu Meridiana | capítulo reescrito | `grep "pereira"` → 0 |
| 7 | 17 | Eleonora erguia os olhos **do bordado** na mesa do café | era a versão v3, descartada | `grep "bordado"` → 0 |
| 8 | 18 | "sem a urgência do celeiro" — urgência que nunca existiu | era a versão v2, descartada | `grep "urgência do celeiro"` → 0 |

**Padrão nos itens 2, 3 e 6:** os três são a mesma falha — o personagem
POV sabendo o que não tem como saber. É por isso que existe o passe
`revisao-de-pov`. Eles não foram corrigidos: sumiram junto com a
reescrita, o que é sorte, não processo.

---

## Como usar este arquivo

1. Item novo entra em **Pendentes**, com capítulo, trecho e o porquê.
2. Sai de lá só depois de conferido no texto — e a linha da verificação
   fica registrada.
3. Se um capítulo for reescrito inteiro, revise a errata dele: o problema
   pode ter sumido, e item morto atrapalha tanto quanto item esquecido.
