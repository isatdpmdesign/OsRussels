---
name: revisao-pontuacao
description: Revisão mecânica de pontuação e regras duras de estilo para capítulos de "Os Russels". Caça interrogações faltando em falas (o erro mais recorrente), travessão em narração pura (proibido — só fala), vocativo sem vírgula, palavras banidas (peso/pesar, calo da pena fora do canon), referências a número de capítulo dentro da narração, e sujeira mecânica (espaço antes de pontuação, ponto duplicado). Use SEMPRE como passe final antes de entregar um capítulo à autora, depois da voz-isadora e da revisao-sentimental. É barata de rodar — são greps, não releitura.
---

# Revisão de pontuação — passe mecânico final

Esta skill é um **checklist mecânico**. Não relê o capítulo inteiro com olho literário — roda buscas direcionadas e revisa só as linhas suspeitas. É o passe mais barato e o que pega os erros que mais irritam a autora.

## Ordem de execução

Rodar DEPOIS de `voz-isadora` e `revisao-sentimental`, ANTES do commit final.

## 1. Interrogações faltando em falas (ERRO Nº 1 DO PROJETO)

A autora já flagrou várias vezes: falas que são perguntas terminando sem `?`.

```bash
grep -nE '^— (Como|Por quê|Por que|Quando|Onde|Quem|O que|Qual|Quanto|Quantos|Quantas|Será|Cadê|Tem certeza|Você acha|Entendeu|Combina|Pode|Posso|Vai|Vamos|Tá|Tem|É|Sabe|Quer|Gosta|Lembra|Conhece|Ouviu|Viu)\b[^?]*[^?!]$' "caminho/do/capitulo.md"
```

Pra cada linha retornada, decidir: é pergunta? → adicionar `?`. É constatação deliberada (princípio "constatação > pergunta" do projeto)? → deixar. **Na dúvida, é pergunta.** O princípio da constatação vale pra frases afirmativas na forma ("Você vai acompanhar Vibeke ao baile"), não pra interrogativas diretas mutiladas ("Tem certeza").

Também procurar perguntas no MEIO da fala:

```bash
grep -nE '— [^—]*\b(o quê|por quê|né|certo|combinado)\.' "caminho/do/capitulo.md"
```

## 2. Travessão em narração pura (PROIBIDO)

Regra dura do projeto: travessão SÓ em fala (e intercalada fala-narração). Narração usa parênteses, dois-pontos, vírgula ou ponto.

```bash
grep -nE '^[^—].*— ' "caminho/do/capitulo.md"
```

Revisar cada ocorrência: se for intercalada de fala (`— disse ele —`), ok. Se for travessão parentético em parágrafo de narração, substituir.

## 3. Palavras banidas (blacklist viva)

```bash
grep -nE 'peso|pesar|pesava|pesad|pesou' "caminho/do/capitulo.md"
grep -nE 'calo da pena' "caminho/do/capitulo.md"
grep -nE 'como quem comenta o (clima|tempo)' "caminho/do/capitulo.md"
```

- **peso/pesar** — banida em qualquer flexão (jargão de IA flagrado pela autora). Exceção: usos literais inevitáveis (pesar um saco de farinha), confirmar com a autora.
- **calo da pena** — só no canon antigo (Caps 1–21); capítulos novos usam as mãos brutas de campo.
- **"como quem comenta o clima/tempo"** — frase do Josh no cap20; não reciclar em outros POVs.

## 4. Cota de fórmulas "como quem / do jeito que"

```bash
grep -cE 'como quem|do jeito que|com a [a-zçãéúíóê]+ de quem|como se' "caminho/do/capitulo.md"
```

**Teto: ~10 por capítulo** de 4-5 mil palavras. Acima disso, reescrever as mais fracas (dizer o que o personagem FAZ, sem moldura).

## 5. Personagem não sabe que está num livro

```bash
grep -niE 'cap [0-9]|capítulo [0-9]|do cap|no cap' "caminho/do/capitulo.md"
```

Únicas ocorrências permitidas: o cabeçalho (`### Capítulo N`) e o rodapé (`*Continua no Capítulo N+1...*`). Qualquer "Cap 19" dentro da narração → substituir por referência interna do mundo ("a madrugada da sala de estar", "o bosque dos Russels", "a noite do pomar").

## 6. Sujeira mecânica

```bash
grep -nE ' [,.;:!?]' "caminho/do/capitulo.md"        # espaço antes de pontuação
grep -nE '\.\.|,,|!!|\?\?' "caminho/do/capitulo.md"   # pontuação duplicada (exceto reticências legítimas "...")
grep -nE '  ' "caminho/do/capitulo.md"                # espaço duplo
grep -nE '\*[^*]*$' "caminho/do/capitulo.md"          # itálico possivelmente não fechado (revisar manualmente)
```

## 7. Vocativo sem vírgula

Procurar nomes próprios colados no fim de fala sem vírgula antes:

```bash
grep -nE '— [^—]*[a-zçãéõ] (Aurora|Josh|Vibeke|Meridiana|Casandra|Joseph|Dylan|Matias)[.?!]' "caminho/do/capitulo.md"
```

Revisar: "Tá com frio Aurora?" → "Tá com frio, Aurora?". (Falsos positivos quando o nome é objeto da frase — revisar caso a caso.)

## 8. Artigo antes de nome em narração

Regra do projeto: sem artigo antes de Josh/Aurora em narração ("Josh desceu", não "o Josh desceu"). EM FALA o artigo é permitido e natural ("o Josh sabe se a mãe dele cavalga").

```bash
grep -nE '^[^—].*\b([Oo] Josh|[Aa] Aurora)\b' "caminho/do/capitulo.md"
```

Revisar cada caso: narração pura → tirar o artigo. Discurso indireto livre muito colado na voz do personagem → tolerável, decidir caso a caso. (Personagens secundários como "a Vibeke", "a Meridiana" têm tolerância maior na narração íntima — manter o padrão do capítulo.)

## Formato de saída

Curto. Tabela ou lista: achado → linha → correção aplicada (ou "falso positivo, mantido"). Aplicar as correções óbvias direto; listar as ambíguas pra autora decidir. Não fazer cerimônia — esta skill é mecânica.
