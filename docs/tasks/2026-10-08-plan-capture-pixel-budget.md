# Plano da fatia 6: orçamento de pixels por Capture

**Por quê:** a fatia 6 do `docs/ROADMAP.md` é a primeira pendente da v0.2. Ela fecha a issue #11: o limite de pixels contados do `low-contrast-real` é por elemento, então uma página de muitos textos sobre milhões de cores passa muito do timeout de 30s; e a amostragem em grade regular perde uma cor em padrões de período 2px.

**O quê:** `plan.md` da fatia, na fase Plan do `tlc-spec-lean`: 15 critérios em EARS, três portas no `Landing` (como o orçamento é dividido, o valor dele, como uma região amostrada escolhe seus pixels) e seis suposições ainda não confirmadas. Nenhum check e nenhum código de produção foram escritos.

**Como:** leitura do roadmap, da issue #11, do `.checks/issue4-pixel-work-bound.md`, do `STATE.md`, das lições confirmadas e do código de `vision.py` e do Check. Três spikes descartáveis (fora do repositório) contra o Chromium real, em `f2c6213`: 55 textos sobre ruído levam 61,8s hoje e 1,0s com o orçamento; uma escala única para o Capture perde 3 de 22 Findings no artigo da WCAG na Wikipedia, e um teto igual por texto não perde nenhum; o jitter determinístico devolve as duas cores de listras de 1px em 0,484 / 0,516. Arquivo: `.specs/features/capture-pixel-budget/plan.md`.

**Verificação:** `validate_plan.py capture-pixel-budget` saiu com 0 erros e 0 avisos.

**Pendências:** revisão do plano pelo mantenedor, em especial o valor do orçamento (262.144 ou o dobro) e a decisão sobre o aliasing (jitter ou manter a grade e documentar). Depois: `checks.md`, build e Verifier. Nada foi commitado.
