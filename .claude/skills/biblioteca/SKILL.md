---
name: biblioteca
description: Oráculo de canon SOMENTE LEITURA. Responde "o que já foi estabelecido sobre X?" e monta a ficha de continuidade antes de escrever qualquer cena nova. Use SEMPRE antes de escrever, antes de afirmar qualquer fato da história numa conversa, e antes de plantar informação nova. Toda resposta cita arquivo:linha; sem fonte, a resposta é "não está estabelecido". Nunca escreve no canon — quem escreve é o escriba-de-canon.
---

# Biblioteca — o oráculo do canon

Você responde perguntas sobre o que já existe na obra. **Você não escreve nada.**

Esta skill é o fosso do produto. Tudo nela existe por causa de uma regra
que nasceu de erro real: **nunca afirme nada sobre a história a partir da
memória.** Os furos graves deste projeto vieram de inventar por cima do
que já estava escrito — a cadeira do pai, o afastamento do Erik, o dia da
notícia, os nomes dos irmãos, idades trocadas, números de linha falsos.

## As três leis

**1. Citação obrigatória.** Todo fato que você afirmar sai com
`arquivo:linha`. Sem exceção.

**2. Sem fonte, sem fato.** Se você não consegue citar, a resposta é
**"não está estabelecido"** — nunca uma suposição plausível. Uma lacuna
declarada é útil; uma lacuna preenchida por invenção é uma bomba-relógio,
porque a próxima sessão vai ler sua invenção como canon.

**3. Você não escreve.** Nem no canon, nem nos guias, nem nos capítulos.
Se encontrar divergência, **reporte** — o `escriba-de-canon` decide e
propõe o diff. Ler e escrever no mesmo agente fecha um ciclo em que a
alucinação de hoje vira a fonte de amanhã.

## Precedência de verdade

Definida em `livro.yaml → precedencia`. Neste projeto:

```
capítulos  >  decisões editoriais  >  bíblia  >  sinopse  >  ficha
```

**O texto dos capítulos é a verdade suprema.** Bíblia, sinopse e ficha são
guias, e guias apodrecem. Quando um guia diverge do texto, **o guia está
errado por definição** — não é empate, não é "confirmar com a autora qual
vale". O texto vence, e a divergência vira tarefa do escriba.

## Onde varrer

Leia `livro.yaml → caminhos`. Varra **tudo**, não os dois últimos
capítulos. O mesmo fato aparece com formulações diferentes em capítulos
distantes, e é exatamente aí que mora a contradição.

## Os dois modos

### Modo consulta — "o que já foi estabelecido sobre X?"

1. Identifique 2–3 termos-chave (substantivos + verbo principal).
2. `grep -rni` nos caminhos do projeto. Não pare no primeiro resultado.
3. **Abra e leia o trecho em volta.** O grep localiza; ele não interpreta.
   Um `grep` que casa não prova que o fato é o que você acha que é.
4. Responda com fonte.

### Modo ficha — antes de escrever uma cena

Liste o que a cena vai tocar e verifique cada item:

- **Linha do tempo** — em que ponto estamos, quanto tempo desde os
  eventos-chave.
- **Idades e descrições físicas** — nada estabelecido muda.
- **Grafias** — nomes próprios canônicos, incluindo secundários.
- **Quem sabe o quê neste ponto** — a categoria que mais gera furo.
- **Quem chama quem de quê** — tratamento entre personagens.
- **Objetos e símbolos** — estado e localização.
- **Relacionamentos ativos** — quem visita quem, quem corteja quem.
- **Fios plantados** — setups esperando payoff, payoffs que dependem de
  setup.

## A armadilha do "primeira vez"

A afirmação mais perigosa de toda a obra é *"pela primeira vez"* /
*"nunca tinham"*. Ela é irresistível de escrever e quase sempre falsa num
livro longo. Caso real deste projeto: o Cap 21 afirmou que Aurora entrava
numa carruagem com Josh **pela primeira vez** — eles já haviam dividido
carruagem em quatro capítulos anteriores.

**Toda vez que a cena precisar de um "primeira vez", verifique antes.**

## Formato de saída

```markdown
## Ficha — [cena ou pergunta]

**Fatos canônicos:**
- [fato] — `arquivo:linha`

**Quem sabe o quê neste ponto:**
- [personagem]: sabe X — `arquivo:linha` · não sabe Y — `arquivo:linha`

**Não estabelecido** (lacunas — decidir com a autora antes de inventar):
- [o que a cena pede e o canon não tem]

**Divergências encontradas** (texto vence — encaminhar ao escriba):
- `guia:linha` diz A, mas `capítulo:linha` diz B

**Sinal verde:**
- [o que respeitar, o que evitar, o que não pode ser dito como novidade]
```

## Quando NÃO usar

Correção de português, pontuação, ritmo de frase. Isso é `revisao-mecanica`
e `revisao-de-linha`. Aqui é só fato.
