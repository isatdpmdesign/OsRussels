# Workspace Codex — Os Russels

## Isolamento

- Branch de trabalho: `codex/revisao-marketing-os-russels`.
- Base inicial: `origin/claude/book-writing-workflow-LnfjM` no commit `aab7145` (capítulo 32).
- Nunca fazer commit, push, merge ou checkout sobre `main` ou sobre a branch do Claude.
- Atualizações futuras do Claude entram nesta branch somente por merge ou rebase explícito, depois de confirmação da autora.

## Regra dos manuscritos

- Tratar `Os Russels/livro-01-o-afilhado/` como texto canônico recebido do Claude.
- Não sobrescrever capítulos durante diagnóstico, leitura beta, marketing ou extração de quotes.
- Quando a autora aprovar uma reescrita, criar versão paralela em `Os Russels/revisoes-codex/` ou usar sufixo `-v2-codex`.
- Citar arquivo e linha em todo apontamento editorial.

## Áreas de trabalho

- `skills/` — skills de revisão, leitoras e marketing.
- `Os Russels/notas/editorial/` — pareceres, leitura beta e decisões propostas.
- `Os Russels/marketing/` — quotes, calendário, personas de campanha e briefs visuais.
- `Os Russels/revisoes-codex/` — somente versões aprovadas pela autora.

## Fluxo

1. Atualizar a referência remota do Claude para leitura.
2. Comparar os novos commits e atualizar canon/sinopse antes da análise.
3. Rodar diagnóstico sem editar capítulos.
4. Entregar propostas à autora.
5. Alterar texto apenas após aprovação explícita e somente nesta branch.
