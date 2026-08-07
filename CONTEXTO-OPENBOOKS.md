# CONTEXTO — OpenBooks (handoff para o Claude Code)

> Este documento é o briefing inicial do projeto. Leia inteiro antes de propor qualquer arquitetura ou escrever código.

---

## 1. Quem sou eu

Isadora — designer de experiência (UX/UI), empreendedora e autora. Escrevo ficção de romance histórico. Trabalho sozinha, sem capital para investir, com CLT em paralelo. Sou usuária avançada de IA e desenho todos os meus próprios ativos visuais.

Sou **usuária zero** deste produto. Tudo que for construído aqui precisa primeiro me servir para terminar meu próprio livro.

## 2. O que estou construindo

**OpenBooks** — um SaaS de escrita de livros com IA, voltado para ficção em português.

**Romance no Bolso** (romancenobolso.com.br) — meu app de leitura, onde os livros construídos no OpenBooks ficam hospedados. Escritor publica direto lá com login único, ou exporta EPUB/PDF e publica onde quiser.

São os dois lados do mesmo mercado: OpenBooks é a oferta (escritores), Romance no Bolso é a demanda (leitores).

## 3. Contexto competitivo

- **NovelCrafter** (americano): plataforma de escrita que usa OpenRouter com chave do usuário. Escrevi meu primeiro livro nele e vendo na Amazon. **O problema dele não é o BYOK — é fazer a romancista escolher modelo, roteador e contexto.** Isso é pedir para autora virar engenheira de prompt.
- **SuperCool**: plataforma genérica "faz tudo" vendida via webinar. Livro é um módulo. O produto forte deles é o funil, não a ferramenta.

**Meu diferencial:** o vertical (ficção/romance em PT-BR), o método de repositório que já uso, e simplificação radical da experiência. O usuário nunca escolhe modelo. Eu escolho.

## 4. Decisões já tomadas

| Tema | Decisão | Motivo |
|---|---|---|
| Motor por assinatura via CLI | **Descartado para o SaaS** | Assinatura só funciona com software rodando na máquina do usuário. Web não tem esse caminho. O device-code do Codex existe mas é risco de ToS; Anthropic fechou para terceiros. |
| Modelo | **Roteamento por tarefa, invisível ao usuário** | Contexto longo e barato (bíblia, continuidade, cruzamento de capítulos) num motor; prosa e voz em outro. Nunca expor nome de modelo na interface. |
| Onboarding | Login social + cota gratuita, **zero configuração** | Meta: primeiro capítulo em 5 minutos sem colar chave. Conexão de chave própria só quando encostar no limite — fluxo de 90 segundos, uma vez, com validação instantânea. |
| Plano gratuito | **Qualidade total em escopo pequeno** | Nunca degradar qualidade no free. Dar ~3 capítulos com qualidade cheia. Free ruim mata o produto. |
| Monetização | **Preço por obra, não por token** | Escritor paga pelo livro pronto, como paga revisor e ilustrador. Cobrar nos momentos de valor: EPUB/PDF diagramado, capa, audiobook, publicação no Romance no Bolso. Créditos genéricos que acabam no meio do capítulo fazem o usuário desistir. |
| Custo | **Cache de prompt é obrigatório** | Ficção é barata na saída (~4k tokens/capítulo). O que custa é reenviar a bíblia a cada chamada. |

## 5. Estratégia de construção — LEIA COM ATENÇÃO

**Não comece pelo SaaS. Não construa telas, banco de dados ou autenticação agora.**

A ordem é:

1. **Fase 1 (agora):** construir os agentes como *skills* dentro do repositório do meu livro atual (Os Russels) e terminar o livro usando elas. Sem app, sem interface, sem backend.
2. **Fase 2:** cada skill que sobreviver ao uso real vira especificação do produto. As que eu achar que preciso e nunca usar, economizei de construir.
3. **Fase 3:** o SaaS é a interface por cima de um motor já provado, com um livro pronto como evidência e primeiro item do catálogo.

## 6. O projeto atual — Os Russels

Quinologia de romance histórico, Zelândia rural na década de 1830, estética Bridgerton.

- Fonte canônica: `biblia-os-russels.md`
- 22 capítulos exportados em markdown
- `CONTEXTO-OS-RUSSELS.md` (contexto portátil) e `MANIFESTO.md` (tracker de capítulos)
- Cinco irmãos Russel: Joseph, Josh (protagonista do Livro 1), Meridiana, Dylan, Matias; mãe viúva Casandra
- Livro 1 "O Afilhado": Josh vai a Copenhague estudar com a família do padrinho Raj Svensson; arco enemies-to-lovers com Aurora Svensson
- Livro ainda não finalizado

## 7. Os agentes a construir

Estes são os seis que identifiquei. **Avalie criticamente, proponha outros que julgar necessários, e diga quais destes deveriam ser fundidos ou divididos.**

1. **Bibliotecária** — lê a bíblia, mantém e atualiza fichas de personagem, acusa contradição entre capítulos, responde "o que já foi estabelecido sobre X?". *É o fosso do produto e a primeira a construir.*
2. **Arquiteta** — estrutura de capítulo, beats, arco narrativo, ritmo do livro
3. **Prosa** — escreve a cena na voz da autora; precisa de um perfil de voz por usuário
4. **Revisora** — repetição, ritmo, vício de linguagem, coerência de POV
5. **Diagramadora** — exportação para EPUB e PDF
6. **Narradora** — pipeline de TTS por capítulo, com voz escolhida. Atenção: gerar frase a frase quebra a prosódia; gerar por blocos com contexto e costurar.

## 8. O que eu quero de você agora

1. **Não escreva código ainda.** Comece diagnosticando o repositório atual e me diga o que encontrou.
2. Proponha a estrutura de skills e a divisão de responsabilidades entre os agentes, com sua crítica à minha lista.
3. Proponha a estrutura de registro de decisões: um `CLAUDE.md` na raiz e uma pasta `/decisoes` com um arquivo numerado por decisão (contexto, decisão, consequência — três parágrafos cada). Regra: **se a decisão muda o código, ela mora no repo**; o que é para humano ler (roadmap, entrevistas, preço) fica no Notion.
4. Então construa **apenas a skill da Bibliotecária**, e vamos usá-la de verdade nos 22 capítulos antes de seguir.

Trabalhe em modo diagnóstico e somente leitura primeiro. Nenhuma operação destrutiva sem checkpoint comigo.
