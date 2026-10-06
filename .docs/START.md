# Squint MCP — Especificação inicial

> *Squint — pra ver o bug que o DOM não mostra.*

Servidor MCP open source que **vê** a página como um usuário e **mede** como um DevTools. Cruza a renderização real (pixels) com os dados do navegador (DOM/CSS) para detectar bugs visuais, extrair specs de design e gerar audits de UX/UI.

- **Repositório:** https://github.com/sh4wty1/squint-mcp
- **Pacote (pretendido):** `squint-mcp` (registro depende da linguagem, ver seção 15)
- **Licença (pretendida):** MIT
- **Status:** ideia validada, especificação inicial. Nenhum código ainda.

---

## 1. Problema

- O DOM pode estar "correto" e o render estar quebrado (texto cortado, sobreposição, fonte fallback, contraste ruim sobre imagem)
- Ferramentas de regressão visual (Percy, Chromatic, `toHaveScreenshot` do Playwright) precisam de **baseline** e não **explicam** o que quebrou
- O `@playwright/mcp` navega e tira print, mas não mede nem diagnostica
- Audits de UX/UI hoje são manuais e inconsistentes

## 2. Proposta de valor

- **Diagnóstico sem baseline**: detectar problemas na primeira visita
- **Pixel ↔ elemento**: todo achado aponta seletor, box, estilos e o crop visual
- **Saída estruturada para LLM**: JSON + crops pequenos, não prints gigantes
- **Audits reproduzíveis**: heurísticas versionadas, com severidade, evidência e fonte
- **Aprende com o ecossistema**: regras de audit baseadas em normas (WCAG), heurísticas publicadas e pesquisa sobre outros MCPs

## 3. Público-alvo

- Devs front-end que querem um "segundo par de olhos" do agente antes do PR
- Designers/QA que precisam comparar implementação com mockup
- Agentes de código (Claude Code, Cursor etc.) que geram UI e precisam verificar o próprio resultado visualmente

## 4. Escopo

### Dentro
- Inspeção de elementos (estilos computados + geometria + crop)
- Extração de design tokens (paleta, tipografia, espaçamentos, raios, sombras)
- Detecção automática de bugs visuais
- Comparação com mockup (PNG do Figma etc.)
- Comparação entre viewports (responsivo)
- Audit de UX/UI com heurísticas (WCAG, Nielsen, consistência)

### Fora (por enquanto)
- Interação complexa / fluxos com login (deixar para o `@playwright/mcp`)
- Testes funcionais
- Sites que exigem bypass de proteção anti-bot

---

## 5. Stack

> **Linguagem ainda não decidida** — é a primeira questão do grill (seção 15, Q1).
> As camadas abaixo valem para qualquer linguagem; a coluna de libs mostra as candidatas.

| Camada | Requisito | Candidatas (Python) | Candidatas (TypeScript) |
|---|---|---|---|
| MCP | SDK oficial, stdio + HTTP | `mcp` (FastMCP) | `@modelcontextprotocol/sdk` |
| Navegador | Playwright oficial, Chromium primeiro | `playwright` (async) | `playwright` |
| Imagem | Crop, resize, amostragem de pixel | `Pillow` + `numpy` | `sharp` |
| Visão | Regiões, bordas, alinhamento | `opencv-python` | — (limitado) |
| Diff | Diff visual + perceptual | `scikit-image` (SSIM) | `pixelmatch` + `pngjs` |
| Cor | Contraste WCAG, ΔE, espaços de cor | `coloraide` | `culori` |
| Acessibilidade | Regras WCAG prontas | `axe-core` injetado na página | `axe-core` injetado na página |
| Modelos/validação | Schemas de input/output | `pydantic` | `zod` |
| Testes | Unit + integração com fixtures | `pytest` | `vitest` |
| Qualidade | Tipos estritos + lint/format | `pyright` strict + `ruff` | `tsc` strict + ESLint/Prettier |
| Distribuição | Instalação em 1 comando | `uvx squint-mcp` (PyPI) | `npx squint-mcp` (npm) |

**Independente da linguagem:** o código que roda dentro da página (`page.evaluate`) é sempre JavaScript. Deve ficar isolado em arquivos `.js` dentro de `collectors/`.

---

## 6. Arquitetura

```
┌──────────────┐   stdio/HTTP   ┌──────────────────────────────────────┐
│ Cliente MCP  │ ─────────────▶ │  server (registro de tools)          │
│ (Claude etc.)│ ◀───────────── │                                      │
└──────────────┘                │  ┌────────────┐   ┌───────────────┐  │
                                │  │ BrowserPool│──▶│ PageSession   │  │
                                │  └────────────┘   │ (viewport,    │  │
                                │                   │ estabilização)│  │
                                │                   └──────┬────────┘  │
                                │        ┌─────────────────┼────────┐  │
                                │        ▼                 ▼        ▼  │
                                │   collectors/        vision/   audits/
                                │   (DOM, CSS,         (crop,    (regras
                                │    fontes, a11y)     cor, diff) + score)
                                │        └────────┬────────┘        │  │
                                │                 ▼                 │  │
                                │        Finding[] (modelo único) ◀─┘  │
                                └──────────────────────────────────────┘
```

### Pipeline padrão de uma análise
1. Abrir página em `BrowserContext` isolado
2. **Estabilizar**: `networkidle`, `document.fonts.ready`, desativar animações/transições, esconder caret de input
3. Coletar DOM/CSS (`collectors/`)
4. Capturar pixels (página + crops por elemento)
5. Cruzar dados (`vision/` + `detectors/`)
6. Gerar `Finding[]` e, se for audit, consolidar em relatório

---

## 7. Estrutura de pastas (proposta, agnóstica de linguagem)

```
squint-mcp/
├── src/squint/                # (ou src/ em TS)
│   ├── entrypoint             # Sobe o servidor via stdio
│   ├── server                 # Cria o servidor MCP, registra tools
│   ├── config                 # Todos os limiares e defaults
│   ├── tools/                 # 1 arquivo por tool (schema + handler)
│   ├── browser/
│   │   ├── pool               # Reuso de browser, limite de concorrência
│   │   └── stabilize          # Fontes, animações, lazy-load, scroll
│   ├── collectors/            # Coleta de DOM/CSS
│   │   └── js/                # Scripts JS executados via page.evaluate
│   ├── vision/
│   │   ├── crop
│   │   ├── color              # Amostragem, cor dominante, contraste real
│   │   └── diff               # Diff visual + heatmap
│   ├── detectors/             # 1 arquivo por tipo de bug visual
│   ├── audits/
│   │   ├── rules/             # Regras de UX/UI (1 arquivo por regra)
│   │   └── report             # Agregação, score, Markdown/JSON
│   ├── tokens/                # Extração e clusterização de design tokens
│   └── models/finding         # Modelo único de achado
├── fixtures/                  # HTMLs com bugs plantados (para testes)
├── tests/
├── docs/
│   ├── SPEC.md
│   └── research/              # Pesquisa: outros MCPs, heurísticas, normas
├── .github/                   # CI, templates de issue/PR
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── SECURITY.md
└── LICENSE
```

---

## 8. Modelo de dados central

Formato do `Finding` (JSON, agnóstico de linguagem). Todo detector e toda regra de audit devolve isto.

```jsonc
{
  "id": "text-clipped",              // detector/regra que gerou o achado
  "category": "visual-bug",          // visual-bug | a11y | consistency | ux | responsive
  "severity": "major",               // critical | major | minor | info
  "message": "Texto cortado em 14px pela largura do container",
  "selector": "[data-testid=hero-title]", // opcional: seletor estável
  "box": { "x": 120, "y": 340, "w": 480, "h": 56 }, // opcional, px CSS
  "viewport": { "width": 1440, "height": 900 },
  "evidence": {
    "computed": { "overflow": "hidden", "font-size": "48px" }, // estilos relevantes
    "measured": { "overflowPx": 14 },                          // valores medidos
    "cropPath": "crops/hero-title.png"                         // crop com margem
  },
  "suggestion": "Permitir quebra de linha ou reduzir font-size em telas menores", // opcional
  "source": "Squint heuristic"       // opcional: norma/heurística (ex: "WCAG 2.2 SC 1.4.3")
}
```

---

## 9. Tools MCP

| Tool | Input | Output | Fase |
|---|---|---|---|
| `ping` | `message?` | nome, versão, eco | 0 |
| `screenshot` | `url`, `viewport?`, `fullPage?`, `selector?` | PNG + metadados | 1 |
| `inspect_element` | `url`, `selector`, `viewport?` | estilos, box model, crop, cor real amostrada | 1 |
| `detect_visual_bugs` | `url`, `viewports?`, `detectors?` | `Finding[]` + crops | 2 |
| `extract_tokens` | `url`, `scope?` | paleta, escala tipográfica, espaçamentos, raios, sombras | 2 |
| `compare_viewports` | `url`, `viewports[]` | diferenças de layout entre tamanhos | 3 |
| `compare_with_mockup` | `url`, `mockupPath`, `selector?` | diff %, heatmap, regiões divergentes | 3 |
| `audit_ui` | `url`, `profile?` (`wcag`, `nielsen`, `consistency`, `full`) | relatório com score, achados e prioridades | 4 |

### Regras para as tools
- Input sempre validado por schema tipado
- Output estruturado (`structuredContent`) + texto, com no máximo N imagens (configurável)
- Preferir crops a prints de página inteira (custo de token)
- Timeout por tool e erro claro quando a página não estabiliza
- Annotations MCP (`readOnlyHint`, `openWorldHint`) em todas as tools

---

## 10. Detectores visuais (fase 2)

| Detector | Sinal DOM | Confirmação visual |
|---|---|---|
| `text-clipped` | `scrollWidth > clientWidth` com `overflow: hidden` | crop termina em glifo cortado |
| `ellipsis-unintended` | `text-overflow: ellipsis` ativo em texto curto | — |
| `overlap` | interseção de boxes + `elementFromPoint` ≠ elemento | crop mostra conteúdo sobreposto |
| `font-fallback` | `document.fonts` com falha / família não carregada | métrica de largura difere da esperada |
| `low-contrast-real` | cor computada do texto | cor de fundo **amostrada do pixel** (resolve imagem/gradiente) |
| `invisible-content` | visível pelo CSS, dentro do viewport | crop é uniforme (só fundo) |
| `offscreen-overflow` | elemento além da largura do viewport | scroll horizontal na página |
| `broken-image` | `naturalWidth === 0` | placeholder / ícone de quebra |
| `tap-target-small` | box < 24×24 px (mobile) | — |
| `layout-shift` | posição muda entre capturas com intervalo | diff entre capturas |

---

## 11. Audit de UX/UI (fase 4)

### Fontes de regras
- **WCAG 2.2**: contraste, alvos de toque, foco visível, texto alternativo (axe-core + checagens visuais próprias)
- **Heurísticas de Nielsen**: só as verificáveis automaticamente (consistência, feedback visível de estado, prevenção de erro em forms)
- **Consistência de design**: cores/tamanhos de fonte quase iguais, espaçamentos fora de escala, botões com estilos divergentes
- **Responsivo**: quebras entre breakpoints

### Formato do relatório
- Score por categoria (0–100) + geral
- Top 10 problemas por impacto (severidade × ocorrências)
- Cada achado com evidência (crop + valores medidos) e fonte
- Exportável em JSON e Markdown

### Pesquisa contínua (`docs/research/`)
- Mapear MCPs existentes de browser/design e o que cada um faz bem
- Catalogar heurísticas e checklists de audit publicados
- Toda regra nova referencia a fonte no campo `source` do `Finding`

---

## 12. Roadmap

### Fase 0 — Fundação
- [ ] Scaffold na linguagem escolhida + SDK MCP + testes + lint/format/typecheck
- [ ] Arquivos de projeto open source (README, LICENSE, CONTRIBUTING, CHANGELOG, SECURITY, templates do GitHub, CI)
- [ ] Servidor sobe via stdio e responde à tool `ping`
- [ ] `BrowserPool` e `stabilize`

### Fase 1 — Inspeção
- [ ] `screenshot`
- [ ] `inspect_element` (estilos + box + crop + cor amostrada)
- [ ] Fixtures básicas

### Fase 2 — Detecção e tokens
- [ ] Modelo `Finding`
- [ ] 5 primeiros detectores: `text-clipped`, `overlap`, `font-fallback`, `low-contrast-real`, `offscreen-overflow`
- [ ] `extract_tokens` com clusterização de cores (ΔE) e tamanhos

### Fase 3 — Comparações
- [ ] `compare_viewports`
- [ ] `compare_with_mockup` com alinhamento e heatmap

### Fase 4 — Audit
- [ ] Integração axe-core
- [ ] Regras de consistência
- [ ] `audit_ui` com relatório Markdown/JSON

### Fase 5 — Distribuição
- [ ] Transporte HTTP
- [ ] Imagem Docker com browsers inclusos
- [ ] Publicação no registro de pacotes e em registros de MCP

---

## 13. Convenções de desenvolvimento

- **Código sempre comentado**, explicando o *porquê* das heurísticas e limiares
- Limiares (contraste, tamanho mínimo, ΔE) centralizados no módulo `config`, com a fonte citada
- Tipagem estrita + lint + testes rodando no CI e localmente (feedback rápido para o agente se corrigir)
- Todo detector/regra:
  - 1 arquivo próprio
  - 1 fixture HTML com o bug plantado + 1 sem o bug
  - teste que garante detecção e ausência de falso positivo
- Screenshots de teste com `deviceScaleFactor: 1` e animações desativadas
- JS executado na página fica em arquivos `.js` separados, nunca em strings inline gigantes
- Em stdio, logs só em `stderr`
- Commits pequenos por detector/regra, seguindo Conventional Commits
- Antes de criar regra nova, registrar a fonte em `docs/research/`

---

## 14. Decisões tomadas

- Nome: **Squint**
- Projeto público e open source
- Playwright (Chromium primeiro) + SDK MCP oficial
- Foco do diferencial: diagnóstico explicado **sem baseline**, cruzando pixel e DOM
- Interação/navegação complexa fica fora; o Squint complementa o `@playwright/mcp`
- Código será escrito majoritariamente por agente de IA, em fluxo spec-driven (spec → tickets → implementação, 1 ticket por sessão), com revisão humana dos diffs

### Decididas no grill (2026-10-06)

> Onde estas decisões conflitam com as seções 5–13, **estas valem**. Vocabulário em `CONTEXT.md`, justificativas em `docs/adr/`.

- **Linguagem:** Python 3.12+, `uv`, `pyright` strict, `ruff` (ADR-0001)
- **Vocabulário:** "detector" e "regra" viram um conceito só, **Check**; todo Check consome um **Capture** e devolve **Finding[]**; **Audit** = execução de um **Profile** (conjunto de Checks). `detectors/` + `audits/rules/` viram `checks/`
- **Playwright:** dependência normal, restrita ao código que produz o Capture; Checks nunca importam `playwright` (ADR-0002)
- **Stateless:** cada chamada abre a URL, estabiliza, captura e fecha. Sem `actions`. Só o estado inicial da página; o caminho futuro é anexar a um browser existente via CDP
- **v0.1:** `ping` + `inspect_element` + `detect_visual_bugs` com 2 Checks (`low-contrast-real`, `text-clipped`). Sem tool `screenshot`. Um browser único reutilizado, sem pool
- **Entrada:** `http(s)://` (incluindo `localhost`) e `file://`. Sem HTML bruto. Bloqueio de IPs privados é obrigatório quando o transporte HTTP entrar
- **Navegador:** só local, headless, Chromium
- **Idioma:** inglês em tudo que é público (código, docs, mensagens de Finding). **Licença:** MIT
- **Finding:** campo `id` vira `check`; um Finding = um elemento × um viewport × um Check; sem id próprio; inclui trecho do texto visível (~40 caracteres); `cropPath` vira índice da imagem na resposta
- **Imagens:** inline no MCP, no máximo 5 crops por chamada, por severidade, ~512px no maior lado. Sem escrita em disco
- **Stabilize:** `load` → `document.fonts.ready` → zerar animações/transições → `networkidle` com timeout de ~3s que não falha (registra `stabilized: false` no Capture). Timeout total de 30s por tool. Sem scroll de lazy-load, sem pausar carrossel/vídeo
- **Seletor:** `data-testid` > `id` (pulando ids gerados) > role+nome > CSS path; precisa ser único na página
- **Config:** só parâmetros de tool + defaults no módulo `config`. Sem arquivo de config
- **Shadow DOM aberto:** v0.1. **Iframes:** fora
- **Distribuição:** só PyPI (`uvx squint-mcp`) na v0.1; Docker e registros de MCP na fase 5
- **Versionamento:** 0.x enquanto o schema do Finding mudar. Breaking = remover/renomear campo do Finding, tool ou parâmetro. Mudar limiar ou adicionar Check não é breaking, mas vai no CHANGELOG

### Adiadas (decidir quando a fase chegar, com fixture real)

- Falsos positivos de `overlap` (fase 2)
- Mockup: só PNG ou Figma (fase 3)
- Fórmula e pesos do score do audit (fase 4)

## 15. Questões em aberto (histórico, resolvidas acima)

### Q1 — Linguagem (resolver primeiro: todas as outras dependem dela)

Contexto:
- O código será escrito por IA e revisado pelo autor
- O autor não gosta de JS/TS, curte Python, conhece Java e nunca usou C#
- O diferencial do projeto é processamento visual (pixel, cor, diff, regiões)

Opções avaliadas até agora:

| Opção | A favor | Contra |
|---|---|---|
| **Python** | Playwright oficial; melhor ecossistema de imagem/visão (OpenCV, NumPy, scikit-image, coloraide); FastMCP simples; `uvx` como distribuição; autor curte e revisa com conforto; modelos de IA muito fortes em Python | Tipagem opcional (mitigar com `pyright` strict); um pouco mais lento que Node em I/O, irrelevante aqui |
| **TypeScript** | Playwright e SDK MCP nativos (features chegam primeiro); `page.evaluate` na mesma linguagem; `npx` é o padrão mais comum de MCPs | Autor não gosta; ecossistema de visão computacional limitado |
| **C#** | Playwright e SDK MCP oficiais; tipagem forte; curva curta vindo de Java | Autor nunca usou; ecossistema de imagem mais fraco; comunidade MCP menor; `dotnet tool` exige SDK instalado |
| **Java/Kotlin** | Playwright e SDK MCP oficiais; autor conhece Java; Spring AI | Distribuição pesada (JAR/Docker); foge do ecossistema de front |
| **Go / Rust** | Binário único, ótima distribuição | Sem Playwright oficial; ecossistema de imagem fraco; muito trabalho para o ganho |

Pergunta-chave para decidir: *o processamento de imagem vai ser simples (crop, amostragem, diff) ou vai evoluir para visão computacional (regiões, alinhamento de mockup, SSIM)?*

Recomendação inicial (a validar no grill): **Python**.

### Demais questões

- **MVP / v0.1**: fases 0+1 sozinhas não mostram diferencial frente ao `@playwright/mcp`. Puxar 1 detector (ex: `low-contrast-real` ou `text-clipped`) para a v0.1?
- **Idioma** do projeto (README, docs, mensagens dos `Finding`): inglês, português ou bilíngue?
- **Licença**: MIT ou Apache-2.0?
- **Onde roda o navegador**: só local na v1, ou já prever execução remota (container/VM)?
- **Entrada de páginas**: só URL, ou também HTML bruto / arquivo local / `localhost`?
- **Imagens na resposta**: base64 inline no MCP, arquivos em disco, ou ambos?
- **Shadow DOM e iframes**: suporte em qual fase?
- **Seletores estáveis**: ordem `data-testid` > `id` > role+nome > CSS path é suficiente?
- **Falsos positivos** em overlap (decorativos, `position: absolute` intencional): lista de ignorados? severidade baixa por padrão?
- **Config do usuário**: arquivo de config, parâmetros de tool, ou ambos?
- **Mockup**: só PNG, ou integração direta com Figma no futuro?
- **Score do audit**: fórmula e pesos por categoria
- **Flakiness**: quão agressivo o `stabilize` deve ser (lazy-load, carrosséis, vídeo)?
- **Distribuição**: só registro de pacotes, ou também Docker e registros de MCP desde a v0.1?
- **Versionamento**: quando sair de 0.x e o que conta como breaking change (schema de `Finding`?)