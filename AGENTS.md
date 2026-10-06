## Agent skills

### Skill routing

Route every request to a skill yourself, and say which one you picked in one line. A skill the user names, or the `Skill` column of the slice in `docs/ROADMAP.md`, wins over the table.

| The request is | Skill |
| --- | --- |
| A feature where what to build is still open, or that spans several modules | `tlc-spec-driven` |
| A feature small enough for one plan: one module, behaviour already clear | `tlc-spec-lean` |
| Work already planned: a spec, ticket or checklist exists and only the build is left | `tlc-implement` |
| A pull request to review | `the-judge` |
| `AGENTS.md` or the skills themselves need an audit | `harness-eval` |

Torn between `tlc-spec-driven` and `tlc-spec-lean`: pick driven when the work needs a task breakdown to stay ordered, lean otherwise.

"The next roadmap task" means the first slice in `docs/ROADMAP.md` still `pendente` whose dependencies are `concluída`.

One feature stays in one system from spec to verification: TLC (`tlc-*`) or Matt Pocock (`to-tickets` → `implement`).

### Issue tracker

Issues live in GitHub Issues for `sh4wty1/squint-mcp` (via the `gh` CLI). See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
