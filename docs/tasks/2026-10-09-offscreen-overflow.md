# Fatia 7: Check `offscreen-overflow`

**Por quê:** a fatia 7 do `docs/ROADMAP.md` é a primeira pendente. Uma página mais larga que o viewport rola de lado e o `detect_visual_bugs` hoje não diz qual elemento causa isso.

**O quê:** até aqui, o plano (aprovado pelo mantenedor em 2026-10-09) e o `checks.md`: 23 checks em 4 fatias no perfil `light`, cada um com sua prova, a tabela de `Coverage` e as nove dimensões do `Swept`. Nenhum código ainda.

**Como:** `tlc-spec-lean`. Os checks derivam dos 20 critérios do plano e das duas portas do `Landing`. Dois checks fecham um critério por um lado que o plano não exemplifica: C7 (um elemento a menos de 1px da borda é nomeado, AC 2) e C13 (o `overflow-x` do `body` só vale enquanto o do `html` é `visible`, AC 11). Arquivos: `.specs/features/offscreen-overflow/checks.md`, `.specs/STATE.md`. Branch `feat/offscreen-overflow`.

**Verificação:** `validate_checks.py offscreen-overflow` saiu com 0 erros e 11 avisos, todos de provas que são `grep`, `git diff` ou a suíte inteira (C18, C20, C22, C23), como na fatia 6.

**Pendências:** o build (testes a partir dos checks, o módulo do Check, o campo `tag` no coletor, descrição da tool, CHANGELOG e README), o Verifier independente, e push e pull request quando o mantenedor autorizar.
