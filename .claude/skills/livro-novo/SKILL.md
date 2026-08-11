---
name: livro-novo
description: Começa um projeto de livro do zero e o deixa pronto para as outras skills. Cria o livro.yaml, a pasta perfil/ e o esqueleto de canon a partir de uma conversa com a autora. Use quando alguém quiser escrever um livro e ainda não houver estrutura nenhuma, ou para adaptar um projeto existente ao formato que o motor entende.
---

# Livro novo — do zero ao primeiro capítulo

Todo o resto do motor pressupõe um `livro.yaml` e uma pasta `perfil/`.
Esta skill os cria — **conversando, não com formulário.**

## Princípio

A autora não escolhe modelo, não escreve prompt, não configura nada. Ela
responde perguntas sobre o livro dela, que é o assunto que ela domina.
Tudo que for estrutura, você infere e propõe.

**Meta: primeiro capítulo em uma sessão.** Se a conversa inicial passar de
uns quinze minutos, você está perguntando demais.

## O que perguntar — e o que não perguntar

Pergunte só o que **muda o que o motor faz**:

1. **De que é o livro?** Uma ou duas frases. Não peça sinopse.
2. **Gênero e tom.** E uma bússola: *"que livros você quer que o seu
   lembre?"* — vale mais que qualquer adjetivo.
3. **Quem são as pessoas?** Duas ou três principais, com o que cada uma
   quer e o que atrapalha.
4. **Onde e quando.**
5. **Como você quer contar?** Primeira ou terceira pessoa, um POV ou
   vários.
6. **Tem coisa escrita?** Qualquer coisa — capítulo, conto, post. É a
   matéria-prima do perfil de voz.

**Não pergunte:** número de capítulos, estrutura de atos, arco completo,
nomes de todo mundo. Ela ainda não sabe, e fingir que sabe cria canon
falso que vai atrapalhar depois. Estrutura é trabalho da skill `arco`,
quando houver com o que trabalhar.

## O que criar

```
projeto/
├── livro.yaml           ← o contrato
├── perfil/
│   ├── voz.md           ← via perfil-de-voz, das amostras dela
│   └── estilo.md        ← regras duras (começa mínimo e cresce)
├── canon/               ← ou um arquivo só, se a obra for pequena
│   └── biblia.md
├── notas/
│   ├── decisoes-editoriais.md
│   ├── ficha-continuidade.md
│   └── sinopse-capitulos.md
└── capitulos/
```

Preencha o `livro.yaml` com o que ela disse e **defaults sensatos** para o
resto. Convenção de nome de arquivo, precedência de verdade e template de
capítulo você decide — ela não tem opinião sobre isso e não deveria
precisar ter.

Deixe `revisao.blacklist` **vazia**. Blacklist não se inventa: ela se
acumula conforme a autora recusa coisas. Uma blacklist genérica de
"palavras que a IA usa" só produziria falso positivo em cima do estilo
dela.

## Voz, desde o primeiro capítulo

Se ela tem qualquer coisa escrita, rode **`perfil-de-voz`** antes de
escrever uma linha. Prosa sem perfil sai neutra, e o primeiro capítulo é
onde ela decide se isso presta.

Se não tem nada escrito, diga isso com clareza: o primeiro capítulo vai
sair na voz do gênero, não na dela, e vai afinar conforme ela corrigir.
Cada correção alimenta o perfil (`rodada` → comentário `regra` →
`decisoes-editoriais` → `perfil/voz.md`).

## Depois do esqueleto

1. `arco` — modo desenho, só o suficiente para saber onde o livro começa
2. `capitulo` — beats do primeiro
3. `prosa` — escrever
4. os passes de revisão
5. `escriba-de-canon` — os guias absorvem o que o capítulo estabeleceu

Do capítulo 1 em diante, o canon deixa de ser inventado por você e passa a
ser lido do que já existe. **É por isso que o primeiro capítulo é o mais
perigoso: é o único escrito sem canon para consultar.** Estabeleça pouco,
com intenção, e registre tudo que estabelecer.
