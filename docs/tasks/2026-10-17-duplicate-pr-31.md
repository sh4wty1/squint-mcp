# PR #31 duplica a fatia 7 já mesclada

**Por quê:** a sessão retomou a fatia 7 pelo Handoff do `.specs/STATE.md` do branch local `feat/offscreen-overflow`, sem comparar com `origin/main`. A fatia 7 já tinha sido refeita e mesclada pelo PR #17 (`8aa017c`), e as fatias 8, 9 e 10 também estão no `main`.

**O quê:** o build antigo foi verificado (PASS, `verification.md`), o branch recebeu push em 2026-10-16 e o PR [#31](https://github.com/sh4wty1/squint-mcp/pull/31) foi aberto. Em 2026-10-17 o PR apareceu como `CONFLICTING`: conflita com o `main` em 15 arquivos e desfaria as correções de revisão do #17. Ele não deve ser mesclado.

**Como:** `git fetch`, `git merge-tree --write-tree origin/main HEAD` e `gh pr list --state all` revelaram a duplicação. Nenhum arquivo do projeto mudou por causa disso.

**Verificação:** `gh pr view 31` com `mergeable: CONFLICTING`; o `docs/ROADMAP.md` do `origin/main` marca as fatias 6 a 10 como `concluída`.

**Pendências:** nenhuma da limpeza: o PR #31 foi fechado como duplicata do #17, o branch `feat/offscreen-overflow` foi apagado no remoto e no local, e o local está no `main`. Lição: ao retomar, comparar o Handoff com `origin/main` antes de agir. Próxima fatia no `main`: 11 (release 0.2.0).
