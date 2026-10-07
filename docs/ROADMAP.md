# Roadmap — v0.1 em fatias

A v0.1 descrita em [`SPEC.md`](SPEC.md) é entregue em 5 fatias verticais. Cada fatia é testada pela fronteira MCP (o único seam da spec) e é implementada em sua própria sessão.

Épico: issue #1.

## Como usar

- A próxima tarefa é a primeira fatia `pendente` cujas dependências estão `concluída`.
- `task #N` (ou `fatia N`) é a fatia de número N da tabela abaixo. Leia a seção dela aqui antes de começar.
- Peça a spec dela com a skill da coluna `Skill` (por exemplo: `/tlc-spec-driven specify feature: task #3`), uma fatia por sessão.
- Ao fechar uma fatia, o status muda para `concluída` na tabela e na seção dela.
- Quando a fatia 5 fechar, o roadmap pós-v0.1 é criado neste mesmo formato.

| # | Fatia | Depende de | Skill | Status |
|---|---|---|---|---|
| 1 | Fundação + `ping` | — | `tlc-spec-driven` | concluída |
| 2 | Capture + `inspect_element` | 1 | `tlc-spec-driven` | concluída |
| 3 | `detect_visual_bugs` + `text-clipped` | 2 | `tlc-spec-driven` | pendente |
| 4 | `low-contrast-real` | 3 | `tlc-spec-lean` | pendente |
| 5 | Publicação no PyPI | 4 | manual (`ready-for-human`) | pendente |

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
- **Status:** pendente (em andamento na branch `feat/detect-visual-bugs-text-clipped`).
- **Andamento (2026-10-06):** spec aprovada e design escrito, aguardando aprovação, em [`.specs/features/detect-visual-bugs-text-clipped/`](../.specs/features/detect-visual-bugs-text-clipped/). Nenhum código ainda. Próximo passo: aprovar o design e gerar o `tasks.md`. Para retomar: `/tlc-spec-driven resume`; o ponto de parada está no Handoff de [`.specs/STATE.md`](../.specs/STATE.md).

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
- **Status:** pendente.

## 5. Publicação no PyPI

- **Objetivo:** `uvx squint-mcp` funcionar para qualquer pessoa.
- **Entra:**
  - Release 0.1.0 no PyPI
  - README com a instalação em dois passos (`uvx squint-mcp` + `playwright install chromium`) e configuração em clientes MCP
  - CHANGELOG da 0.1.0
- **Não entra:** Docker, registros de MCP, transporte HTTP (fase 5 do roadmap geral).
- **Dependência:** fatia 4.
- **Skill:** manual (`ready-for-human`), porque envolve credenciais do PyPI.
- **Status:** pendente.
