---
name: perfil-de-voz
description: Constrói o perfil de voz de uma autora a partir de amostras da escrita dela, e o mantém atualizado conforme ela corrige o texto. Gera o perfil/voz.md que a prosa e a revisao-voz consomem. Use ao começar um projeto com uma autora nova, quando a voz do texto parecer neutra ou genérica, ou periodicamente para absorver o que as rodadas de revisão revelaram sobre a régua dela.
---

# Perfil de voz — descobrir a assinatura

O `perfil/voz.md` é o que impede a prosa de sair correta e sem dono.
Sem ele, tirar os tiques de máquina produz texto neutro — que é só outro
jeito de soar como máquina.

**Ninguém escreve esse arquivo do zero num formulário.** O deste projeto
levou meses e nasceu de erro corrigido. Esta skill é o caminho curto.

## Onde a voz aparece

Duas fontes, e a segunda é melhor que a primeira:

**1. Amostras da autora.** Qualquer coisa escrita por ela: capítulo
antigo, conto, post longo, e-mail comprido. Ficção é ideal; primeira
pessoa informal serve muito bem, porque a voz fica mais exposta.

**2. As correções dela.** Muito mais revelador. Em `revisao/rodadas.jsonl`
cada mudança tem `antes`, `depois` e `porque` — ou seja, **um texto que
ela recusou ao lado do texto que ela aceitou.** Isso é o negativo da voz,
e o negativo ensina mais que o positivo: o que ela corta é mais
característico do que o que ela escreve.

Se o projeto tem histórico de rodadas, **comece por ele.**

## O que procurar

Não catalogue tudo. Procure o que se **repete** e o que é **incomum**.
Voz é o cruzamento dos dois: um traço frequente e banal não é assinatura,
um traço único e isolado é acidente.

| Eixo | Perguntas |
|---|---|
| **Emoção** | Ela nomeia o sentimento ou põe no corpo? Qual parte do corpo? |
| **Ritmo** | Frases longas ou curtas? Onde ela quebra? Usa frase curta como soco? |
| **Ironia** | Contra quem — os personagens, o narrador, ela mesma? |
| **Clareza** | Ela explica ou deixa em subtexto? (divide autoras ao meio) |
| **Clichê** | Foge ou abraça quando o clichê é como gente sente? |
| **Concretude** | Detalhe mundano específico ou descrição genérica? |
| **Pontuação** | Padrão literário ou cadência de fala? |
| **Imperfeições recorrentes** | O que ela faz "errado" **sempre**? Isso é assinatura, não erro. |

Esse último item é o mais importante e o mais fácil de estragar. Uma
vírgula que separa sujeito de verbo, repetida em cinco textos, é a
respiração dela. Corrigir isso é apagar a autora.

## Método

1. **Leia as amostras inteiras** antes de anotar. Impressão geral primeiro.
2. **Colete evidência literal.** Todo traço vem com citação. Traço sem
   citação é você projetando.
3. **Filtre por recorrência.** Aparece em pelo menos duas amostras? Se
   só em uma, é acidente daquele texto.
4. **Cruze com as correções.** O que ela recusou repetidamente é regra
   negativa e vale ouro.
5. **Traduza para o projeto.** Amostra em primeira pessoa contemporânea
   e livro em terceira pessoa histórica não têm a mesma superfície — diga
   o que atravessa e como.
6. **Devolva para ela confirmar.** A autora é a autoridade sobre a
   própria voz. Ela vai discordar de coisa, e a discordância é informação.

## Formato

```markdown
# Perfil de voz — [autora]

## Princípio mestre
[a coisa mais característica, em duas frases]

## As N marcas
### 1. [nome curto do traço]
[o que é]
> "[citação]" · "[citação]"
**Aplicar:** [instrução acionável, com exemplo bom × ruim]

## Tradução para [o projeto]
| Marca | No livro |

## O que NÃO corrigir
[as imperfeições que são assinatura]

## Preferências declaradas
[o que ela já disse explicitamente sobre a própria escrita]
```

## Manutenção

O perfil não é ativo fixo. **Reveja depois de cada bloco de rodadas.**
Se a autora corrigiu a mesma coisa três vezes e isso não está no perfil,
o perfil está incompleto — e o custo dessa lacuna é ela repetir a
correção uma quarta vez.

## No produto

Esta skill é o onboarding do OpenBooks. A usuária cola dois textos dela e
sai com um perfil de voz — sem escolher modelo, sem escrever prompt, sem
saber que existe um perfil. É o que faz a prosa soar como ela desde o
primeiro capítulo.
