# Instalar skills do manifest fassi-skills

**Por quê:** o `AGENTS.md` roteia pedidos para skills TLC, `the-judge` e `harness-eval`, mas nenhuma estava instalada no projeto.
**O quê:** instaladas em `.claude/skills/`: `tlc-spec-driven`, `tlc-spec-lean`, `tlc-implement`, `the-judge`, `harness-eval` (workflow `tlc` + skills de qualidade). Alvo: claude-code.
**Como:** `/setup-fassi-skills` → `npx --yes @tech-leads-club/agent-skills install -s <skill> -a claude-code`, uma por vez.
**Verificação:** os 5 `SKILL.md` existem em `.claude/skills/*/`.
**Pendências:** nenhuma (workflow `matt-pocock` não instalado por escolha: uma feature fica em um só sistema).

## Atualização: referência `task #N`

`docs/ROADMAP.md` (seção "Como usar"): `task #N` passa a significar a fatia N da tabela, para pedir specs com `specify feature: task #3`.
