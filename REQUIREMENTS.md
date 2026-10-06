# Requirements — Agent Skills

Skills e ferramentas usadas no desenvolvimento do Squint. Instale antes de começar a trabalhar no repo.

## Pré-requisitos

- Node.js (para rodar `npx`)
- Um agente compatível com skills (Claude Code, Cursor, Copilot, Windsurf, Cline etc.)
- `gh` CLI autenticado (usado pela the-judge para postar reviews)

---

## Matt Pocock — planejamento

| Skill | Uso no projeto | Instalação |
|---|---|---|
| `grill-with-docs` | Entrevista sobre a spec, fecha questões em aberto e registra decisões | `npx skills@latest add mattpocock/skills --skill=grill-with-docs` |
| `to-spec` | Transforma o resultado do grill na spec refinada | `npx skills@latest add mattpocock/skills --skill=to-spec` |
| `to-tickets` | Quebra a spec em tickets (por fase) | `npx skills@latest add mattpocock/skills --skill=to-tickets` |
| `implement` | Implementa um ticket por sessão | `npx skills@latest add mattpocock/skills --skill=implement` |

Instalar todas as skills do Matt de uma vez:

```bash
npx skills@latest add mattpocock/skills
```

Atualizar:

```bash
npx skills update
```

---

## Tech Leads Club — features, qualidade e harness

| Skill | Uso no projeto | Instalação |
|---|---|---|
| `tlc-spec-driven` | Features grandes: Specify → Design → Tasks → Execute, com Verifier independente | `npx @tech-leads-club/agent-skills install --skill tlc-spec-driven` |
| `tlc-spec-lean` | Features pequenas: plano único com critérios EARS → checks → build → Verifier | `npx @tech-leads-club/agent-skills install --skill tlc-spec-lean` |
| `tlc-implement` | Implementa trabalho já planejado: extrai um checklist, constrói e prova cada item com um Verifier independente | `npx @tech-leads-club/agent-skills install --skill tlc-implement` |
| `the-judge` | Review de PR com evidência, postado no GitHub | `npx @tech-leads-club/agent-skills install --skill the-judge` |
| `harness-eval` | Audit qualitativo do AGENTS.md, regras e skills | `npx @tech-leads-club/agent-skills install --skill harness-eval` |

---

## Ferramentas (CLI, sem instalação)

| Ferramenta | Uso no projeto | Comando |
|---|---|---|
| Harness Score | Mede a maturidade do harness do repo (L0–L4) | `npx harness-score` |

---

## Instalar tudo

```bash
# Matt Pocock — planejamento
npx skills@latest add mattpocock/skills --skill=grill-with-docs
npx skills@latest add mattpocock/skills --skill=to-spec
npx skills@latest add mattpocock/skills --skill=to-tickets
npx skills@latest add mattpocock/skills --skill=implement

# Tech Leads Club — features, qualidade e harness
npx @tech-leads-club/agent-skills install --skill tlc-spec-driven
npx @tech-leads-club/agent-skills install --skill tlc-spec-lean
npx @tech-leads-club/agent-skills install --skill tlc-implement
npx @tech-leads-club/agent-skills install --skill the-judge
npx @tech-leads-club/agent-skills install --skill harness-eval
```

---

## Quando usar cada uma

1. **Visão do projeto:** `grill-with-docs` → `to-spec`
2. **Harness inicial** (AGENTS.md, CI, lint/tipos/testes): `npx harness-score`
3. **Cada feature:** a escolha da skill segue a seção "Skill routing" do [`AGENTS.md`](AGENTS.md), que é a fonte única dessa regra.
4. **PR:** `the-judge`
5. **A cada marco:** `npx harness-score` e, se o AGENTS.md estiver inchando, `harness-eval`