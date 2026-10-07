# Instalar skills do manifest fassi-skills

**Por quê:** o `AGENTS.md` roteia pedidos para skills TLC, `the-judge` e `harness-eval`, mas nenhuma estava instalada no projeto.
**O quê:** instaladas em `.claude/skills/`: `tlc-spec-driven`, `tlc-spec-lean`, `tlc-implement`, `the-judge`, `harness-eval` (workflow `tlc` + skills de qualidade). Alvo: claude-code.
**Como:** `/setup-fassi-skills` → `npx --yes @tech-leads-club/agent-skills install -s <skill> -a claude-code`, uma por vez.
**Verificação:** os 5 `SKILL.md` existem em `.claude/skills/*/`.
**Pendências:** nenhuma (workflow `matt-pocock` não instalado por escolha: uma feature fica em um só sistema).

## Atualização: referência `task #N`

`docs/ROADMAP.md` (seção "Como usar"): `task #N` passa a significar a fatia N da tabela, para pedir specs com `specify feature: task #3`.

## Atualização: segunda análise (manifest com 96 skills)

**Por quê:** o marketplace `fassi-skills` passou de 9 para 96 skills; o mantenedor pediu nova análise do que serve ao projeto.
**O quê:** instaladas em `.claude/skills/`: `gh-address-comments` (par do `the-judge`), `gh-fix-ci` (CI com Chromium) e `security-best-practices` (Python, servidor que abre URLs, publicação no PyPI). Ficaram anotadas para depois: `accessibility` (fatia 4), `docs-writer` (fatia 5), `tlc-discover` e `tlc-plan` (roadmap pós-v0.1).
**Como:** `npx --yes @tech-leads-club/agent-skills install -s <skill> -a claude-code`, uma por vez.
**Verificação:** os 3 `SKILL.md` existem em `.claude/skills/*/`.
**Pendências:** `.claude/` é ignorado pelo git, então as 8 skills precisam ser instaladas em cada máquina. `AGENTS.md` não roteia as três novas. A cópia de `setup-fassi-skills` em `~/.claude/skills/` está desatualizada em relação ao marketplace.
