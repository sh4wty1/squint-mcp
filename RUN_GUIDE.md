# RUN GUIDE

> Documento de uso humano.

## Situação das fatias

| # | Fatia | Depende de | Skill | Situação |
| --- | --- | --- | --- | --- |
| 1 | Fundação + ping | — | `tlc-spec-driven` | concluída |
| 2 | Capture + `inspect_element` | 1 | `tlc-spec-driven` | concluída |
| 3 | `detect_visual_bugs` + text-clipped | 2 | `tlc-spec-driven` | concluída |
| 4 | low-contrast-real | 3 | `tlc-spec-lean` | pendente |
| 5 | Publicação no PyPI | 4 | manual (`ready-for-human`) | pendente |

## Ritual por fatia

Uma sessão por fatia, começando com `/clear`.

1. **Branch:** a partir da `main` atualizada, `feat/<slug>`.
2. **Planejar** com a skill da coluna Skill do roadmap:
   - **Fatia 4:** `/tlc-spec-lean plan feature: task #4`. É um plano único (critérios, caminho, entidades, interface), que você aprova, e depois vêm os checks.
   - **Fatias `tlc-spec-driven`** (se o roadmap pós-v0.1 trouxer alguma): `/tlc-spec-driven specify feature: task #N`, aprovando spec, design e `tasks.md` em sequência.
3. **Construir:** commits atômicos, testes pela fronteira MCP, par de fixtures (bug plantado / sem bug), entrada no CHANGELOG.
4. **Verificar:** verificador independente da própria skill, repetindo até não sobrar lacuna.
5. **Revisar (rodada 1):** abrir o PR e rodar `/the-judge`.
6. **Corrigir o review** com `/tlc-implement`: checklist, fixes e relatório de verificação. Foi assim nos PRs #2, #3, #6 e #7.
7. **Revisar (rodada 2):** `/the-judge` de novo sobre os commits de correção. Se voltar com findings, repete o passo 6.
8. **Fechar:** merge, status `concluída` na tabela e na seção do roadmap, registro em `docs/tasks/`.

## Exceção: fatia 5 (PyPI)

É manual, porque envolve suas credenciais.

- **O agente prepara:** o README, o CHANGELOG da 0.1.0 e a versão, no fluxo acima.
- **Você faz:** o release em si.

Quando ela fechar, cria-se o roadmap pós-v0.1 no mesmo formato e o ritual recomeça.
