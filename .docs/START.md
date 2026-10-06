# Squint MCP — Especificação inicial

> *Squint — pra ver o bug que o DOM não mostra.*

Servidor MCP open source que **vê** a página como um usuário e **mede** como um DevTools. Cruza a renderização real (pixels) com os dados do navegador (DOM/CSS) para detectar bugs visuais, extrair specs de design e gerar audits de UX/UI.

- **Repositório:** https://github.com/sh4wty1/squint-mcp
- **Pacote npm (pretendido):** `squint-mcp`
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

## 5. Stack (proposta)

| Camada | Escolha | Motivo |
|---|---|---|
| Linguagem | TypeScript (Node ≥ 22) | SDK MCP oficial e Playwright nativos |
| MCP | `@modelcontextprotocol/sdk` | Transporte stdio (local) e HTTP (remoto) |
| Navegador | `playwright` (Chromium primeiro) | CDP, screenshots por elemento, emulação |
| Imagem | `sharp` | Crop, amostragem de cor, resize, rápido |
| Diff | `pixelmatch` + `pngjs` | Diff visual e heatmap |
| Acessibilidade | `axe-core` (injetado na página) | Regras WCAG prontas |
| Cor | `culori` | Conversão de espaços, contraste, ΔE |
| Validação | `zod` | Schemas de input/output das tools |
| Testes | `vitest` | Rápido, TS nativo |
| Qualidade | ESLint + Prettier | Padrão de projetos open source TS |

---

## 6. Arquitetura

```
┌──────────────┐   stdio/HTTP   ┌──────────────────────────────────────┐
│ Cliente MCP  │ ─────────────▶ │  server.ts (registro de tools)       │
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

## 7. Estrutura de pastas (proposta)

```
squint-mcp/
├── src/
│   ├── index.ts               # Entrypoint do binário (stdio)
│   ├── server.ts              # Fábrica do McpServer, registra tools
│   ├── config.ts              # Todos os limiares e defaults
│   ├── tools/                 # 1 arquivo por tool (schema + handler)
│   ├── browser/
│   │   ├── pool.ts            # Reuso de browser, limite de concorrência
│   │   └── stabilize.ts       # Fontes, animações, lazy-load, scroll
│   ├── collectors/            # Scripts que rodam via page.evaluate
│   │   ├── styles.ts
│   │   ├── geometry.ts
│   │   ├── fonts.ts
│   │   └── a11y.ts            # Wrapper do axe-core
│   ├── vision/
│   │   ├── crop.ts
│   │   ├── color.ts           # Amostragem, cor dominante, contraste real
│   │   └── diff.ts            # pixelmatch + heatmap
│   ├── detectors/             # 1 arquivo por tipo de bug visual
│   ├── audits/
│   │   ├── rules/             # Regras de UX/UI (1 arquivo por regra)
│   │   └── report.ts          # Agregação, score, Markdown/JSON
│   ├── tokens/                # Extração e clusterização de design tokens
│   └── types/finding.ts       # Modelo único de achado
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

```ts
// Todo detector e toda regra de audit devolve isto
export interface Finding {
  id: string;                    // ex: "text-clipped"
  category: 'visual-bug' | 'a11y' | 'consistency' | 'ux' | 'responsive';
  severity: 'critical' | 'major' | 'minor' | 'info';
  message: string;               // explicação curta, legível por humano e LLM
  selector?: string;             // seletor estável do elemento
  box?: { x: number; y: number; w: number; h: number };
  viewport: { width: number; height: number };
  evidence: {
    computed?: Record<string, string>;          // estilos relevantes
    measured?: Record<string, number | string>; // valores medidos em pixel
    cropPath?: string;                          // crop do elemento com margem
  };
  suggestion?: string;           // correção sugerida
  source?: string;               // norma/heurística de origem (ex: "WCAG 2.2 SC 1.4.3")
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
- Input sempre validado com `zod`
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
- [ ] Scaffold TS + MCP SDK + vitest + ESLint/Prettier
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
- [ ] Publicação no npm e em registros de MCP

---

## 13. Convenções de desenvolvimento

- **Código sempre comentado**, explicando o *porquê* das heurísticas e limiares
- Limiares (contraste, tamanho mínimo, ΔE) centralizados em `src/config.ts`, com a fonte citada
- Todo detector/regra:
  - 1 arquivo próprio
  - 1 fixture HTML com o bug plantado + 1 sem o bug
  - teste que garante detecção e ausência de falso positivo
- Screenshots de teste com `deviceScaleFactor: 1` e animações desativadas
- Em stdio, logs só em `stderr`
- Commits pequenos por detector/regra, seguindo Conventional Commits
- Antes de criar regra nova, registrar a fonte em `docs/research/`

---

## 14. Decisões tomadas

- Nome: **Squint**
- Projeto público e open source
- TypeScript + Playwright + SDK MCP oficial
- Foco do diferencial: diagnóstico explicado **sem baseline**, cruzando pixel e DOM
- Interação/navegação complexa fica fora; o Squint complementa o `@playwright/mcp`

## 15. Questões em aberto

- **Idioma** do projeto (README, docs, mensagens dos `Finding`): inglês, português ou bilíngue?
- **Licença**: MIT ou Apache-2.0?
- **Onde roda o navegador**: só local na v1, ou já prever execução remota (container/VM)?
- **Entrada de páginas**: só URL, ou também HTML bruto / arquivo local / `localhost`?
- **Imagens na resposta**: base64 inline no MCP, arquivos em disco, ou ambos?
- **Shadow DOM e iframes**: suporte em qual fase?
- **Seletores estáveis**: ordem `data-testid` > `id` > role+nome > CSS path é suficiente?
- **Falsos positivos** em overlap (decorativos, `position: absolute` intencional): lista de ignorados? severidade baixa por padrão?
- **Config do usuário**: arquivo (`squint.config.json`), parâmetros de tool, ou ambos?
- **Mockup**: só PNG, ou integração direta com Figma no futuro?
- **Score do audit**: fórmula e pesos por categoria
- **Flakiness**: quão agressivo o `stabilize` deve ser (lazy-load, carrosséis, vídeo)?
- **Distribuição**: só npm, ou também Docker e registros de MCP desde a v0.1?
- **Versionamento**: quando sair de 0.x e o que conta como breaking change (schema de `Finding`?)