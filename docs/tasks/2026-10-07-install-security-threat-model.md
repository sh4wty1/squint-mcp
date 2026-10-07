# Instalar a skill security-threat-model

**Por quê:** terceira análise do manifest `fassi-skills` (132 skills). O Squint abre qualquer URL que o agente passar, incluindo `localhost` e `file://`, e a fatia 5 publica no PyPI; essa fronteira de confiança ainda não foi mapeada.
**O quê:** instalada `security-threat-model` em `.claude/skills/`. Alvo: claude-code. As demais skills que servem ao projeto já estavam instaladas.
**Como:** `/fassi-skills:setup-fassi-skills` → `npx --yes @tech-leads-club/agent-skills install -s security-threat-model -a claude-code`.
**Verificação:** `.claude/skills/security-threat-model/SKILL.md` existe e a skill aparece na sessão.
**Pendências:** `.claude/` é ignorado pelo git, então a skill precisa ser instalada em cada máquina. `AGENTS.md` não roteia para ela. Anotadas para depois: `tlc-plan` e `tlc-discover` (roadmap pós-v0.1), `spec-driven-eval`, `create-adr`, `docs-writer` (fatia 5).
