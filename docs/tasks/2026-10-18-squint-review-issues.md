# Issues from an agent's review of Squint

**Por quê:** um agente usou o Squint numa página sem estilo e listou o que ele errou ou deixou confuso; o maintainer pediu as issues para corrigir uma a uma.
**O quê:** issues #32 (`inspect_element` sem `border-color`/`border-style`, `ready-for-agent`), #33 (borda `outset`/`inset`/`groove`/`ridge` reportada numa cor que não é a pintada, `bug`), #34 (requisição da página que falha no carregamento), #35 (quantos elementos cada Check examinou), #36 (estilo padrão do navegador misturado com token). O alvo de toque (SC 2.5.8) já está no roadmap como `tap-target-small` e não virou issue.
**Como:** cada ponto conferido no código antes (`config.py:46`; probe no Chromium 153: um `<button>` padrão calcula `rgb(0, 0, 0) outset 2px`), issues criadas com `gh issue create` no formato Problem / Measured / Expected / Fix; #32 e #33 se citam.
**Verificação:** `gh issue list` mostra as cinco abertas com os labels certos; as referências cruzadas conferidas.
**Pendências:** corrigir as issues na ordem combinada; triagem de #33 a #36.
