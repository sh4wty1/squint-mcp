# Spec da fatia 4: low-contrast-real

**Por quê:** a fatia 4 do `docs/ROADMAP.md` é a próxima pendente (a 3 foi mergeada no PR #7). Ela entrega o Check que mostra o diferencial do Squint: contraste contra o fundo amostrado do pixel. A issue #8 (ordem de documento entre Checks) precisa fechar nesta fatia.

**O quê:** spec e contexto da fatia, na fase Specify do `tlc-spec-driven` (skill pedida pelo usuário; a coluna do roadmap indicava `tlc-spec-lean`). 46 requisitos (LCR-01 a LCR-46) em EARS, com fixtures e números exatos. Três decisões tomadas com o mantenedor: pior parte do fundo ignorando 10% de ruído, severidade `critical` abaixo de 3:1 e `major` acima, silêncio para texto com opacidade efetiva abaixo de 1. Nenhum código de produção foi alterado.

**Como:** leitura do roadmap, `docs/SPEC.md`, ADRs, `STATE.md`, lições confirmadas e do código da fatia 3. Spike descartável contra o Chromium real: uma segunda captura com `-webkit-text-fill-color: transparent` devolve o fundo atrás dos glifos sem anti-aliasing, e os estilos computados não mudam. Branch `feat/low-contrast-real` criada a partir de `origin/main`. Arquivos: `.specs/features/low-contrast-real/spec.md`, `.specs/features/low-contrast-real/context.md`.

**Verificação:** `validate_spec.py low-contrast-real` saiu com 0 erros e 0 avisos. As razões de contraste citadas na spec foram calculadas pela fórmula da WCAG.

**Pendências:** nenhuma. A sessão foi interrompida antes do Design; Design, Tasks, Execute e o Verifier foram entregues depois, no PR #9. Este registro e o `context.md` só subiram em 2026-10-08, junto com o parágrafo de retomada de sessão do `RUN_GUIDE.md`; o rascunho local da spec e do `STATE.md` foi descartado, por estar superado pelo que o PR #9 mergeou.
