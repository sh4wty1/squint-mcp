# Roadmap

A v0.1 descrita em [`SPEC.md`](SPEC.md) é entregue em 5 fatias verticais. Cada fatia é testada pela fronteira MCP (o único seam da spec) e é implementada em sua própria sessão.

Épico: issue #1.

## Como usar

- A próxima tarefa é a primeira fatia `pendente` cujas dependências estão `concluída`.
- `task #N` (ou `fatia N`) é a fatia de número N da tabela abaixo. Leia a seção dela aqui antes de começar.
- Peça a spec dela com a skill da coluna `Skill` (por exemplo: `/tlc-spec-driven specify feature: task #3`), uma fatia por sessão.
- Ao fechar uma fatia, o status muda para `concluída` na tabela e na seção dela.
- A v0.1 fechou com a fatia 5. A fila continua na v0.2, mais abaixo.

| # | Fatia | Depende de | Skill | Status |
|---|---|---|---|---|
| 1 | Fundação + `ping` | — | `tlc-spec-driven` | concluída |
| 2 | Capture + `inspect_element` | 1 | `tlc-spec-driven` | concluída |
| 3 | `detect_visual_bugs` + `text-clipped` | 2 | `tlc-spec-driven` | concluída |
| 4 | `low-contrast-real` | 3 | `tlc-spec-lean` | concluída |
| 5 | Publicação no PyPI | 4 | manual (`ready-for-human`) | concluída |

---

## 1. Fundação + `ping`

- **Objetivo:** ter um servidor MCP que sobe via stdio e responde `ping`, com todo o ferramental de qualidade rodando localmente e no CI.
- **Entra:**
  - Scaffold Python 3.12+ com `uv`, `pyright` strict, `ruff`, `pytest`
  - Servidor MCP (SDK oficial, FastMCP), transporte stdio, logs só em stderr
  - Tool `ping` (`message?` → nome, versão, eco) com schema tipado e annotations MCP
  - Módulo `config` (vazio de limiares por enquanto, mas no lugar)
  - Teste pela fronteira MCP com cliente em memória (estabelece o padrão de teste)
  - README, LICENSE (MIT), CONTRIBUTING, CHANGELOG, SECURITY, templates de issue/PR
  - CI: typecheck, lint, format check, testes
- **Não entra:** Playwright, browser, Capture, Finding, qualquer Check, publicação no PyPI.
- **Dependência:** nenhuma.
- **Skill:** `tlc-spec-driven`.
- **Status:** concluída. Spec e relatório de validação em [`.specs/features/foundation-ping/`](../.specs/features/foundation-ping/).

## 2. Capture + `inspect_element`

- **Objetivo:** produzir um Capture estabilizado de uma página e expor a primeira tool que cruza DOM/CSS com pixels.
- **Entra:**
  - Browser único (Chromium headless), lançado sob demanda e reutilizado; contexto isolado por chamada
  - Validação de URL: `http(s)://` (incluindo `localhost`) e `file://`
  - Stabilize: `load` → `document.fonts.ready` → zerar animações/transições → `networkidle` (~3s, não falha, registra `stabilized: false`)
  - Capture: dados DOM/CSS + pixels, `deviceScaleFactor: 1`, atravessando shadow DOM aberto
  - Scripts de página em arquivos `.js` separados
  - Vision: crop com margem, redução para ~512px, amostragem de cor
  - Tool `inspect_element` (`url`, `selector`, `viewport?`): estilos computados, box model, cores amostradas, `stabilized`, um crop
  - Erros claros: seletor com zero ou mais de um match, esquema não suportado, página que não carrega, Chromium não instalado, timeout total de 30s
  - CI passa a instalar o Chromium
  - Fixtures HTML básicas
- **Não entra:** modelo Finding, Checks, geração de seletor estável, limite de 5 crops, múltiplos viewports, iframes, scroll de lazy-load, pool de browsers.
- **Dependência:** fatia 1.
- **Skill:** `tlc-spec-driven`.
- **Status:** concluída. Spec, design e relatório de validação em [`.specs/features/capture-inspect-element/`](../.specs/features/capture-inspect-element/).

## 3. `detect_visual_bugs` + `text-clipped`

- **Objetivo:** entregar o fluxo completo Capture → Check → Finding[] com o primeiro Check.
- **Entra:**
  - Modelo Finding (schema da spec)
  - Contrato de Check: recebe um Capture, devolve Finding[], nunca importa `playwright` (ADR-0002)
  - Geração de seletor: `data-testid` > `id` (pulando ids gerados) > role+nome > CSS path, único na página
  - Tool `detect_visual_bugs` (`url`, `viewports?`, `checks?`): um Capture por viewport, filtro por nome de Check, erro para Check desconhecido listando os válidos, lista vazia em página limpa
  - Findings ordenados por severidade; no máximo 5 crops por chamada, por severidade; `cropIndex` nulo além do limite
  - Check `text-clipped` com par de fixtures (bug plantado / sem bug)
- **Não entra:** `low-contrast-real`, demais Checks, Profile, Audit, score.
- **Dependência:** fatia 2.
- **Skill:** `tlc-spec-driven`.
- **Status:** concluída. Spec, design e relatório de validação em [`.specs/features/detect-visual-bugs-text-clipped/`](../.specs/features/detect-visual-bugs-text-clipped/).

## 4. `low-contrast-real`

- **Objetivo:** adicionar o Check que mostra o diferencial do Squint: contraste contra o fundo amostrado do pixel.
- **Entra:**
  - Check `low-contrast-real` (categoria `a11y`, fonte WCAG 2.2 SC 1.4.3)
  - Limiares de contraste no `config`, com a fonte citada
  - Par de fixtures, incluindo texto sobre imagem ou gradiente
  - Entrada no CHANGELOG
- **Não entra:** mudanças no Capture, no Finding ou nas tools além do que o Check exigir; axe-core; outras regras WCAG.
- **Dependência:** fatia 3.
- **Skill:** `tlc-spec-lean`.
- **Status:** concluída. Spec, design e relatório de validação em [`.specs/features/low-contrast-real/`](../.specs/features/low-contrast-real/).

## 5. Publicação no PyPI

- **Objetivo:** `uvx squint-mcp` funcionar para qualquer pessoa.
- **Entra:**
  - Release 0.1.0 no PyPI
  - README com a instalação em dois passos (`uvx squint-mcp` + `playwright install chromium`) e configuração em clientes MCP
  - CHANGELOG da 0.1.0
- **Não entra:** Docker, registros de MCP, transporte HTTP (fase 5 do roadmap geral).
- **Dependência:** fatia 4.
- **Skill:** manual (`ready-for-human`), porque envolve credenciais do PyPI.
- **Status:** concluída. `squint-mcp` 0.1.0 está no [PyPI](https://pypi.org/project/squint-mcp/0.1.0/), publicado pela tag `v0.1.0`. Registro em [`docs/tasks/2026-10-08-release-0.1.0.md`](tasks/2026-10-08-release-0.1.0.md).

---

# v0.2 — completar a detecção (proposta)

A v0.2 fecha a fase 2 da especificação inicial ([`.docs/START.md`](../.docs/START.md), seções 10 e 12): os três Checks que faltam dos cinco primeiros e a tool `extract_tokens`. Proposta a revisar: a ordem e o corte são seus.

| # | Fatia | Depende de | Skill | Status |
|---|---|---|---|---|
| 6 | Orçamento de pixels por Capture | — | `tlc-spec-lean` | concluída |
| 7 | `offscreen-overflow` | — | `tlc-spec-lean` | pendente |
| 8 | `overlap` | — | `tlc-spec-driven` | pendente |
| 9 | `font-fallback` | — | `tlc-spec-driven` | pendente |
| 10 | `extract_tokens` | — | `tlc-spec-driven` | pendente |
| 11 | Release 0.2.0 | 6 a 10 | `tlc-implement` | pendente |

## 6. Orçamento de pixels por Capture

- **Objetivo:** uma chamada nunca passar muito de `TOTAL_TIMEOUT_S`, qualquer que seja a página, e a amostragem não perder cores em padrões finos.
- **Entra:**
  - Um orçamento de pixels contados dividido entre os textos de um Capture, no lugar do limite por elemento (issue #11, ponto 1)
  - Decisão sobre o aliasing da amostragem em padrões de período 2px, mantendo o resultado determinístico (issue #11, ponto 2)
  - Entrada no CHANGELOG
- **Não entra:** tornar o trabalho de pixels cancelável; pool de browsers; mudanças no Finding.
- **Dependência:** nenhuma.
- **Skill:** `tlc-spec-lean`.
- **Status:** concluída. Plano, checks e relatório de verificação em [`.specs/features/capture-pixel-budget/`](../.specs/features/capture-pixel-budget/).

## 7. `offscreen-overflow`

- **Objetivo:** apontar o elemento que faz a página rolar na horizontal.
- **Entra:**
  - Check `offscreen-overflow`: elemento além da largura do viewport, confirmado pelo scroll horizontal da página
  - Par de fixtures (bug plantado / sem bug)
  - Entrada no CHANGELOG
- **Não entra:** overflow vertical; scroll dentro de contêineres; `compare_viewports`.
- **Dependência:** nenhuma.
- **Skill:** `tlc-spec-lean`.
- **Status:** pendente.

## 8. `overlap`

- **Objetivo:** apontar conteúdo coberto por outro elemento sem intenção.
- **Entra:**
  - Check `overlap`: interseção de boxes mais `elementFromPoint` diferente do elemento, confirmado no crop
  - A decisão adiada sobre falsos positivos (dropdowns, tooltips, badges, sticky headers), tomada com fixtures reais
  - Par de fixtures, incluindo sobreposições intencionais que não podem ser reportadas
  - Entrada no CHANGELOG
- **Não entra:** estados de interação (hover, modal aberto); iframes.
- **Dependência:** nenhuma.
- **Skill:** `tlc-spec-driven`, porque o critério de falso positivo ainda está em aberto.
- **Status:** pendente.

## 9. `font-fallback`

- **Objetivo:** apontar texto renderizado numa fonte diferente da que o CSS pede.
- **Entra:**
  - Check `font-fallback`: família não carregada em `document.fonts`, confirmada pela métrica de largura
  - O que o Capture precisar expor sobre as fontes carregadas
  - Par de fixtures
  - Entrada no CHANGELOG
- **Não entra:** `layout-shift`; avaliação de qualidade tipográfica.
- **Dependência:** nenhuma.
- **Skill:** `tlc-spec-driven`, porque mexe no Capture e no Check.
- **Status:** pendente.

## 10. `extract_tokens`

- **Objetivo:** devolver os tokens de design que a página de fato usa.
- **Entra:**
  - Tool `extract_tokens` (`url`, `scope?`): paleta, escala tipográfica, espaçamentos, raios e sombras
  - Agrupamento de cores quase iguais (ΔE) e de tamanhos, com os limiares no `config` e a fonte citada
  - Fixtures e testes pela fronteira MCP
  - README e CHANGELOG
- **Não entra:** regras de consistência e score (fase 4); comparação com um design system; `audit_ui`.
- **Dependência:** nenhuma.
- **Skill:** `tlc-spec-driven`.
- **Status:** pendente.

## 11. Release 0.2.0

- **Objetivo:** a v0.2 no PyPI.
- **Entra:**
  - Versão `0.2.0` no `pyproject.toml`, CHANGELOG datado, README com os Checks e a tool novos
  - Tag `v0.2.0`: o workflow `publish.yml` publica, sem credenciais
- **Não entra:** Docker, registros de MCP, transporte HTTP (fase 5).
- **Dependência:** fatias 6 a 10.
- **Skill:** `tlc-implement`.
- **Status:** pendente.

## Depois da v0.2

Sem fatias ainda: os outros Checks da seção 10 (`ellipsis-unintended`, `invisible-content`, `broken-image`, `tap-target-small`, `layout-shift`), a fase 3 (`compare_viewports`, `compare_with_mockup`), a fase 4 (axe-core, Profiles, `audit_ui`) e a fase 5 (HTTP, Docker, registros de MCP).
