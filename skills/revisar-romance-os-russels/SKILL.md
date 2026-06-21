---
name: revisar-romance-os-russels
description: Revisa "Os Russels" e outros romances da autora em duas etapas: parecer editorial global e revisão capítulo a capítulo. Use para diagnosticar naturalidade, marcas de IA, voz, ritmo, diálogo, POV, emoção, estrutura, continuidade e qualidade de prosa; comparar alternativas comerciais; ou preparar versões revisadas sem sobrescrever originais.
---

# Revisar romance — Os Russels

Trabalhar como editora literária, não como ghostwriter automático. Preservar a decisão da autora e demonstrar toda crítica com evidência textual.

## Preparação obrigatória

1. Ler `references/fontes-do-projeto.md` e localizar a versão canônica.
2. Ler a bíblia, decisões editoriais, diretrizes, sinopse e errata.
3. Para um capítulo, ler também os 2–3 anteriores por inteiro.
4. Aplicar `humanizar-romance` quando houver escrita ou reescrita.
5. Usar `references/rubrica-editorial.md` como régua.

## Etapa 1 — Parecer global

Ler o manuscrito inteiro antes de recomendar mudanças estruturais. Entregar:

- reação editorial em até cinco linhas;
- forças que devem ser preservadas, com exemplos;
- problemas prioritários por impacto no leitor;
- mapa dos capítulos: função, temperatura, risco e ação;
- padrões de prosa automatizada com frequência e linhas;
- dilemas de voz versus mercado em duas alternativas;
- ordem de revisão recomendada.

Classificar cada apontamento como **objetivo**, **estético**, **comercial** ou **canônico**. Não apresentar preferência como regra.

## Etapa 2 — Revisão por capítulo

Só iniciar após a autora aprovar o diagnóstico ou pedir diretamente a revisão. Para cada intervenção:

1. citar trecho e linha;
2. explicar o efeito sobre a leitura;
3. propor direção ou versão curta;
4. verificar voz, informação disponível e continuidade;
5. manter o original e criar `-v2`, `-v3` etc. quando houver arquivo alternativo.

Não “embelezar” tudo. Cortar explicações que repetem um gesto, variar cadência, permitir banalidade e preservar frases fortes mesmo que não sejam perfeitas.

## Scanner

Executar `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/scan-style.ps1 -Path <arquivo-ou-pasta>` como triagem. O bypass vale apenas para o processo e não muda a política do Windows. O resultado não é diagnóstico: revisar falsos positivos no contexto.

## Saída

Separar sempre **Manter**, **Rever**, **Decisão da autora** e **Canon/continuidade**. Não declarar um capítulo “humano” apenas por ausência de palavras banidas.
