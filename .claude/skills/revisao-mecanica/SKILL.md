---
name: revisao-mecanica
description: Passe mecânico final - roda o lint.py (determinístico, custo zero) e tria os achados. Caça interrogação faltando, travessão em narração, blacklist, fórmulas acima da cota, hard wrap, template de capítulo, eco de palavra e sujeira de digitação. Use como último passe antes de fechar um capítulo, depois da voz, do sentimento e da linha.
---

# Revisão mecânica — o passe que não custa nada

Esta skill **não relê o capítulo**. Ela roda uma ferramenta e tria o
resultado.

```bash
python3 .claude/tools/lint.py --projeto "Os Russels" CAMINHO/DO/CAPITULO.md
```

Regras disponíveis: `template`, `wrap`, `interrogacao`,
`interrogacao-ambigua`, `travessao-narracao`, `blacklist`, `formulas`,
`autorreferencia`, `sujeira`, `vocativo`, `artigo`, `eco`.

```bash
# tudo, resumido por capítulo
python3 .claude/tools/lint.py --projeto "Os Russels" --resumo

# uma regra só
python3 .claude/tools/lint.py --projeto "Os Russels" --regra blacklist

# varredura fina de pergunta sem "?" (muito falso positivo, olho humano)
python3 .claude/tools/lint.py --projeto "Os Russels" --regra interrogacao-ambigua CAP.md
```

## Por que é ferramenta e não prompt

Achar interrogação faltando com `grep` custa zero e nunca alucina. Pedir a
um modelo custa dinheiro e às vezes erra. **Tudo que é verificável por
máquina não deveria passar por modelo.** As regras moram no `livro.yaml`;
o script só executa.

Detalhe que importa: o lint trabalha por **parágrafo**. Os greps por linha
da versão antiga perdiam tudo em capítulo com hard wrap — que, deste
projeto, é o livro do capítulo 25 em diante.

## O seu trabalho: triar

O linter acha candidatos. **Ele não sabe o que é erro.** Você decide, e é
aqui que você ganha o seu salário:

| Regra | Precisão | Como triar |
|---|---|---|
| `blacklist`, `wrap`, `template`, `sujeira`, `autorreferencia` | alta | aplicar direto |
| `interrogacao` | boa | ler a frase; na dúvida **é pergunta** |
| `travessao-narracao` | boa | intercalada de fala é falso positivo |
| `vocativo`, `artigo` | média | discurso indireto livre muito colado na voz do personagem tolera o artigo |
| `eco` | média | repetição enfática deliberada fica |
| `formulas` | é contagem | acima da cota, reescrever as mais fracas |
| `interrogacao-ambigua` | baixa | este livro usa constatação de propósito — a maioria fica |

**Exceção da blacklist:** `peso/pesar` é banido como **metáfora
emocional**. Uso literal (*carregar coisa pesada*, *o peso do braço dela*)
passa. O linter não distingue; você distingue.

## Saída

Curta. Achado → linha → o que foi feito.

```
cap 31:366  interrogacao  "— O quê." → "— O quê?"           aplicado
cap 31:541  interrogacao  "— Como a minha mãe percebeu."     aplicado
cap 33:120  eco           'silêncio' ×3                      mantido (enfático)
cap 29:88   blacklist     "o peso do corpo dela"             mantido (literal)
```

Sem cerimônia. Aplique o óbvio, liste o ambíguo para a autora.

## Ordem no ciclo

Último. Depois de `revisao-voz`, `revisao-sentimental` e
`revisao-de-linha` — não faz sentido caçar vírgula em parágrafo que ainda
vai ser reescrito.
