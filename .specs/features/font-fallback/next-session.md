# Prompt da próxima sessão (sessão 5 da fatia 9)

Escrito em 2026-10-13, ao fim da sessão 4, para o mantenedor continuar de outro computador. O Handoff de `.specs/STATE.md` diz o mesmo estado; este arquivo guarda o prompt pronto para colar. Se ele fica no branch até o pull request é decisão do mantenedor.

```
/tlc-spec-driven validate: task #9, fase 5

Fatia 9 do docs/ROADMAP.md: o Check `font-fallback`. Nesta sessão só a sessão 5 da tabela do Execution Plan do tasks.md: o Verifier, as rodadas de conserto se houver, e o T12 num PASS.

Antes de começar:
1. Confirme que está no branch `feat/font-fallback`, com a árvore limpa e igual a `origin/feat/font-fallback` (o branch foi enviado ao remoto em 2026-10-13, sem pull request). O último commit é o que gravou .specs/features/font-fallback/next-session.md, logo depois de `ed5bfee`: confira com `git log --oneline -2`. Reconcilie o Handoff de .specs/STATE.md com o git.
2. Se este computador não é o da sessão 4: `uv sync`, `uv run playwright install chromium`, e rode o gate Full da tabela de gates uma vez antes de qualquer outra coisa (45 testes no módulo da fatia). A imagem do Docker não está nesta máquina: só é preciso baixá-la se uma rodada de conserto mudar `src/` ou `tests/`. Os finais de linha da árvore seguem o `core.autocrlf` desta máquina: mantenha os que o checkout der em cada arquivo.
3. Leia de .specs/features/font-fallback/tasks.md o cabeçalho até o fim do Execution Plan e a fase 5 inteira (T12), sem reler as fases 1 a 4; da spec.md os Goals e os Success Criteria; da skill, o papel do Verifier em sub-agents.md e o validate.md. Não leia `src/` nem `tests/` na janela principal: quem lê é o Verifier. O contexto desta sessão deve ficar abaixo de 30%.
4. Rode o `validate_tasks.py` no tasks.md antes de despachar o Verifier (os três avisos de `Tests: none` em T10 a T12 são esperados).

O que pesa nesta fase:
- O Verifier é um sub-agente novo (autor ≠ verificador), sobre o intervalo `0b9ae25..HEAD`, com a spec.md como fonte da verdade e o validate.md como checklist. Ele cobre 53 critérios, FNT-40 a FNT-45 por evidência de arquivo; o FNT-46 é do T12, depois do PASS.
- O Build da fase 4 passou em `82fa6cc` (2026-10-13: pyright, ruff check, ruff format e 413 testes, 24 min 11 s) e o módulo da fatia passou no Linux (45 testes, registrado sob o T10). São o gate dos Success Criteria: não precisam rodar de novo se `src/` e `tests/` não mudarem. Os commits depois de `82fa6cc` só tocam .specs/.
- O sensor de discriminação roda numa cópia de `src/squint_mcp` num diretório temporário, com `PYTHONPATH` apontando para ela, nunca com `git stash` nem na árvore. Ele não pode deixar vivo nenhum mutante que uma task nomeia (o quarto Success Criterion e a Assumption "When the discrimination sensor is satisfied"). Ao fim, o `git status --porcelain` tem de ser o de antes.
- Sub-agentes não conseguem escrever arquivos `.md` com a ferramenta Write: o Verifier escreve o `validation.md` por script, ou devolve o texto e a janela principal escreve.
- A lacuna do FNT-36 que o Handoff registra (o teste não distingue as duas ordens) é para o Verifier julgar. O comentário de `_settle_layout` é do mantenedor: não toque.
- Um FAIL vira tasks de conserto, cada uma num commit próprio, e o Verifier roda de novo: três rodadas no máximo antes de me perguntar. Nenhum teste é enfraquecido, pulado ou apagado.
- Se uma rodada mudar `src/` ou `tests/`, rode de novo o gate Linux e escreva o resultado sob o T10, e rode de novo o Build em segundo plano (uns 24 minutos), sem pytest em paralelo.
- Num PASS, o T12 marca a fatia 9 como concluída em docs/ROADMAP.md (FNT-46), com a coluna Status da spec atualizada no mesmo commit e a mensagem que a task traz. Confira os finais de linha por contagem de bytes. Scripts com aspas vão para arquivo, não para heredoc.
- A sessão fecha quando o `validate_state.py font-fallback` sai com 0. As lições só são destiladas de falhas concretas (`lessons.py`); um PASS limpo não registra nada.
- O terceiro Success Criterion (a primeira rodada no Linux do CI) só se vê no pull request: o CI roda em push para `main` e em pull_request, e nenhuma rodada dele viu o branch ainda.
- Os commits desta sessão ficam locais: não faça push nem abra pull request sem o meu aval.

Ao terminar: troque o Handoff de .specs/STATE.md, faça o commit dele, e me entregue o prompt da próxima sessão (o push dos commits novos e o pull request, com o meu aval), neste mesmo formato e com o hash do último commit.
```
