# Review of the open pull requests 29 and 30

**Por quê:** os PRs #29 (fix/font-name-backslash, issue #20) e #30 (docs/settle-layout-linux, issue #18) estavam abertos sem review.
**O quê:** uma review consolidada da the-judge em cada um. #29: COMMENT com F1 🟠 (Faces adicionadas por `new FontFace` voltam serializadas em CSS de `document.fonts`; uma Face com falha chamada `Script Face` deixa de gerar Finding, regressão em relação ao main) e F2 🟡 (entrada do CHANGELOG). #30: APPROVE sem findings (postado como COMMENT por ser PR do próprio autor).
**Como:** ladder determinístico, pesquisa na spec CSS Font Loading e no CSSOM, probe no Chromium 153 do venv e repro ponta a ponta com fixture e teste temporários em worktrees de `origin/main` e do branch do PR (removidos depois).
**Verificação:** CI `check` verde nos dois; no head do #29 ruff ok, `tests/test_font_fallback.py` 58 passed; repro do F1 passa no main e falha no PR; gate da review com PASS. Reviews: https://github.com/sh4wty1/squint-mcp/pull/29#pullrequestreview-5558996460 e https://github.com/sh4wty1/squint-mcp/pull/30#pullrequestreview-5558996648
**Pendências:** corrigir o F1 no #29 (decisão de como distinguir Faces de script) e rodar a rodada 2 da review.
