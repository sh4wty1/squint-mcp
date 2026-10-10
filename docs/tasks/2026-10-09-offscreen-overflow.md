# Fatia 7: `offscreen-overflow`

**Por quê:** a fatia 7 do `docs/ROADMAP.md` era a primeira pendente da v0.2. Uma página mais larga que o viewport rola na horizontal, e o `detect_visual_bugs` não dizia nada sobre isso nem apontava o elemento responsável.

**O quê:** plano aprovado pelo mantenedor em 2026-10-09 (20 critérios em EARS, duas portas no `Landing`), `checks.md` com C1 a C21 no perfil `light`, e o build: o Check `offscreen-overflow` (categoria `responsive`, severidade sempre `major`), que em cada viewport onde a página rola na horizontal aponta o primeiro elemento, na ordem do documento, que termina na borda direita da página, pela caixa ou pelo próprio texto. Fica em silêncio quando a página esconde o overflow horizontal (`overflow-x: hidden` ou `clip` em `html` ou `body`) e em página da direita para a esquerda. O Capture ganhou o nome da tag de cada elemento. Entrada no CHANGELOG e frase do README atualizadas.

**Como:** a largura da página vem dos `pixels` de página inteira do Capture, sem script novo nem screenshot novo. Antes de escrever os checks, as páginas das fixtures foram medidas contra o Chromium real em `a5013d4`: os `pixels` continuam com a largura do conteúdo mesmo quando a página esconde o overflow, então é a regra do `overflow-x` que decide o silêncio. Arquivos: `src/squint_mcp/checks/offscreen_overflow.py`, `src/squint_mcp/checks/__init__.py`, `src/squint_mcp/js/collect_elements.js`, `src/squint_mcp/models.py`, `src/squint_mcp/config.py`, `src/squint_mcp/tools/detect_visual_bugs.py`, `tests/test_offscreen_overflow.py`, 17 fixtures `tests/fixtures/offscreen-overflow-*.html`, `tests/test_detect_visual_bugs.py`, `CHANGELOG.md`, `README.md`, `.specs/features/offscreen-overflow/`, `.specs/STATE.md`. Branch `feat/offscreen-overflow`, commits `2de1354`, `0529325`, `ea93b48`, `2bd6d5d` e `d84cce9`.

**Verificação:** `validate_checks.py` saiu com 0 erros. Antes da implementação, os testes novos falharam como esperado (`Unknown check "offscreen-overflow"`). Em `d84cce9`: `uv run pytest` com 233 passando, `pyright`, `ruff check` e `ruff format --check` verdes. O Verifier independente deu PASS na rodada 1, 21 de 21 checks com evidência, e `validate_verification.py` saiu com 0. Relatório em `.specs/features/offscreen-overflow/verification.md`.

**Pendências:** push e pull request, quando o mantenedor autorizar. O Verifier deixou três lacunas de precisão, sem falhar nenhum check:

1. C10 a C13 afirmam só `== []`; nenhum teste afirma a pré-condição (a largura da página nos `pixels`), então uma fixture que deixasse de rolar passaria pelo motivo errado. As pré-condições valem hoje, medidas pelo Verifier.
2. O critério 16 diz que o erro termina com a lista de Checks válidos; as quatro asserções testam só que o texto contém a lista.
3. A tolerância de 1px fica presa só entre cerca de 0,41px e 1px (C5 e C6): um valor de 0,5 passaria em todos os testes.

Fechar a 1 e a 2 muda checks aprovados e espera a decisão do mantenedor. O teste `test_a_body_that_hides_its_overflow_under_a_scrolling_html_is_named` cobre o outro lado do critério 11 e não pertence a nenhum check.
