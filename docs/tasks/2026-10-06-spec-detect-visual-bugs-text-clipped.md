# Spec da fatia 3: `detect_visual_bugs` + `text-clipped`

**Por quê:** a fatia 3 do `docs/ROADMAP.md` é a próxima pendente com dependências concluídas; ela precisa de uma spec aprovada antes de Design, Tasks e implementação.
**O quê:** spec com 68 requisitos (`DVB-01` a `DVB-68`) em EARS, cobrindo a tool, o modelo Finding, o Check `text-clipped`, a geração de seletor, o limite de 5 crops, múltiplos viewports, erros e o contrato de Check. Quatro decisões tomadas com o mantenedor registradas em `context.md`; as demais ambiguidades estão na tabela de Assumptions com default e justificativa.
**Como:** skill `tlc-spec-driven`, fase Specify (com discuss). Arquivos criados: `.specs/features/detect-visual-bugs-text-clipped/spec.md` e `context.md`. Nenhum código alterado.
**Verificação:** `validate_spec.py` → 0 erros, 0 avisos.
**Pendências:** ver a atualização abaixo.

## Atualização: Design

**O quê:** spec aprovada pelo mantenedor. `design.md` escrito (arquitetura, componentes, modelos, erros, riscos, decisões) e decisão de projeto AD-003 registrada em `.specs/STATE.md`: o Capture carrega todos os elementos com campos genéricos e seletor; um Check é uma função `Capture -> list[Finding]` registrada por nome.
**Como:** dois spikes em Chromium real (fora do repositório, no scratchpad) validaram fonte Ahem por `file://`, larguras exatas, ordem dos elementos, combinador `>` atravessando shadow root e validação de lista vazia pelo SDK. Os spikes pediram quatro correções na spec: linha de 30px nas fixtures (caixa do `h1` com `h: 30`, crops de 182×62, amostra em (20, 31)); `#blank-tail` com espaços comuns sob `white-space: pre`; CSS path atravessando shadow com ` > ` (`[data-testid="card"] > h3`); premissa da Ahem marcada como verificada.
**Verificação:** `validate_spec.py` de novo → 0 erros, 0 avisos. Nenhum código de produção alterado.
**Pendências:** aprovação do design; depois Tasks. `uv` não está instalado nesta máquina (os spikes rodaram com `pipx run uv`, que recriou o `.venv`); a execução vai precisar dele.

## Atualização: pausa

**O quê:** trabalho pausado para continuar em outra máquina. Handoff gravado em `.specs/STATE.md`, andamento anotado na seção da fatia 3 de `docs/ROADMAP.md` (a tabela segue `pendente`, para a regra de "próxima tarefa" continuar valendo), tudo commitado na branch `feat/detect-visual-bugs-text-clipped` e enviado ao remoto.
**Pendências:** aprovação do design; Tasks; Execute. Na outra máquina: instalar as skills (`.claude/` é ignorado pelo git), ter `uv` no `PATH`, `uv sync` e `uv run playwright install chromium`.
