# Prompt da próxima sessão (sessão 6 da fatia 9)

Escrito em 2026-10-13, ao fim da sessão 5. O Handoff de `.specs/STATE.md` diz o mesmo estado; este arquivo guarda o prompt pronto para colar. Se ele fica no branch até o pull request é decisão do mantenedor.

```
/tlc-spec-driven resume: task #9, decisões, push e pull request

Fatia 9 do docs/ROADMAP.md: o Check `font-fallback`. A fatia está fechada localmente: a segunda passada do Verifier é um PASS, o T12 marcou a fatia como concluída e o `validate_state.py font-fallback` sai com 0. Nesta sessão só o que vem depois da quinta: as minhas decisões pendentes, o push dos commits novos e o pull request, cada um com o meu aval.

Antes de começar:
1. Confirme que está no branch `feat/font-fallback`, com a árvore limpa e 8 commits à frente de `origin/feat/font-fallback` (que está em `ab1dbab`). O último commit é o do Handoff, logo depois de `79a929a` (o T12): confira com `git log --oneline -3`. Reconcilie o Handoff de .specs/STATE.md com o git.
2. Se este computador não é o da sessão 5: `uv sync`, `uv run playwright install chromium`, e rode o gate Full da tabela de gates uma vez (53 testes no módulo da fatia). Os finais de linha da árvore seguem o `core.autocrlf` desta máquina: mantenha os que o checkout der em cada arquivo.
3. Leia o Handoff de .specs/STATE.md (o item "Open in slice 9") e, de .specs/features/font-fallback/validation.md, o cabeçalho e as seções "I-1", "The spec edits", "FNT-61 and FNT-62" e "Residuals". Não leia `src/` nem `tests/` na janela principal. O contexto desta sessão deve ficar abaixo de 30%.

Primeiro as decisões, uma pergunta por vez, antes de qualquer push:
- I-1: uma família que falhou e tem barra invertida no nome não recebe Finding (`src/squint_mcp/js/font_widths.js:45`). O Verifier leu como issue e deu PASS; lido como lacuna do FNT-01, a passada falha. Escolho entre uma issue, um critério com o conserto numa rodada própria, ou um limite conhecido (marca `ponytail:` e linha nos Risks do design, como o escape hexadecimal).
- Os oito critérios FNT-55 a FNT-62 e as quatro edições de texto aceito da spec (E1 a E5 do relatório), escritos pela rodada de conserto sem a minha leitura: aceito ou mando reescrever.
- FNT-62 nomeia Calibri e FreeSerif no Tail de `#swift`, e FNT-61 depende do kerning da `serif` da máquina: aceito, ou troco por um arquivo de fonte no repositório, ou tiro `text-rendering` da lista.
- Se o `next-session.md` fica no branch para o pull request, e se `design.md` e a linha 399 do tasks.md são atualizados antes dele.

O que pesa nesta sessão:
- Se eu escolher consertar o I-1, isso muda `src/`: é uma rodada própria. Task de conserto com o teste antes do código (vermelho pelo motivo certo), um commit; o gate Linux rodado de novo e escrito sob o T10; o Build em segundo plano (uns 20 minutos, sem pytest em paralelo); e um Verifier novo sobre a rodada, com o sensor na cópia de `src/squint_mcp` e o `git status --porcelain` igual antes e depois. O `validation.md` e o T12 só valem de novo depois do PASS dessa rodada. Nenhum teste é enfraquecido, pulado ou apagado.
- Se uma edição da spec for recusada, o critério reescrito é verificado de novo antes do push.
- O push e o pull request são dois avais separados: peça cada um. O pull request vai para `main` (o da fatia 8 foi o #19); as issues ficam no GitHub de `sh4wty1/squint-mcp`, via `gh`.
- Depois de abrir o pull request, leia o CI dele: o terceiro Success Criterion da spec (a primeira rodada no Linux do CI passa os testes da fatia sem assertiva mudada) só se vê ali. Se um teste da fatia falhar no CI, é um achado: conserta-se a premissa do fixture, nunca a assertiva.
- Os residuais da fatia 8 e os itens "Found outside" do Handoff seguem sem issue: abrir é decisão minha, não faça por conta própria.
- `docs/ROADMAP.md` e `.specs/STATE.md` são CRLF, os arquivos de .specs/features/font-fallback/ são LF: mantenha e confira por contagem de bytes. Scripts com aspas vão para arquivo, não para heredoc. O `lessons.py` só roda depois de um Verifier terminar, e só para falhas concretas.

Ao terminar: troque o Handoff de .specs/STATE.md, faça o commit dele, e me entregue o prompt da próxima sessão (a fatia 10, `extract_tokens`, ou o que tiver ficado aberto), neste mesmo formato e com o hash do último commit.
```
