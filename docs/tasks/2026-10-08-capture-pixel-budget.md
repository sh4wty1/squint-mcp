# Fatia 6: orçamento de pixels por Capture

**Por quê:** a fatia 6 do `docs/ROADMAP.md` é a primeira pendente da v0.2. Ela fecha a issue #11: o limite de pixels contados do `low-contrast-real` é por elemento, então uma página de muitos textos sobre milhões de cores passa muito do timeout de 30s; e a amostragem em grade regular perde uma cor em padrões de período 2px.

**O quê:** plano aprovado pelo mantenedor (15 critérios em EARS, três portas no `Landing`), `checks.md` com C1 a C15 no perfil `light`, e o build: os textos de um Capture dividem um orçamento de 262.144 pixels contados (um teto igual por texto, texto pequeno contado inteiro), e uma região amostrada escolhe linhas e colunas com deslocamentos de semente fixa em vez de passo regular. Entrada no CHANGELOG.

**Como:** três spikes descartáveis contra o Chromium real em `f2c6213` decidiram a forma: 55 textos sobre ruído levam 61,8s hoje e 1,0s com o orçamento; uma escala única para o Capture perde 3 de 22 Findings no artigo da WCAG na Wikipedia e o teto por texto não perde nenhum. Arquivos: `src/squint_mcp/vision.py`, `src/squint_mcp/checks/low_contrast_real.py`, `src/squint_mcp/config.py`, `CHANGELOG.md`, `tests/fixtures/pixel-budget.html`, `tests/fixtures/sampled-patterns.html`, `tests/test_low_contrast_real.py`, `tests/test_inspect_element.py`, `.specs/features/capture-pixel-budget/`, `.specs/STATE.md`. Branch `feat/capture-pixel-budget`, commits `af7c4ba` e `920cd29`.

**Verificação:** `validate_plan.py` e `validate_checks.py` saíram com 0 erros. `pyright`, `ruff check` e `ruff format --check` verdes. Antes da implementação, os testes novos de C1 e C7 falharam como esperado. A suíte inteira com a implementação ainda não tinha terminado quando a sessão foi pausada.

**Pendências:** rodar `uv run pytest` até o fim (C15); despachar o Verifier independente sobre `f2c6213..HEAD` e rodar `validate_verification.py`; marcar a fatia 6 como `concluída` no roadmap; push e pull request, que fecha a issue #11. O estado para retomar está no `## Handoff` do `.specs/STATE.md`.
