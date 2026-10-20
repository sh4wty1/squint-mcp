# Say when a page has no style of its own (`authorStyles`)

Issue [#36](https://github.com/sh4wty1/squint-mcp/issues/36).

## Problem

`extract_tokens` reports every value the elements of a page compute, whoever set it. On a page with no style of its own every value comes from the browser's default stylesheet, and the result reads like a design system: `Times New Roman`, `#efefef` and `13.333px` come back as the tokens of the project. An agent that reads them as the page's choices proposes a palette and a type scale that nobody chose.

Evidence: one report, from an agent reviewing Squint on an unstyled page with no author style rule. No figure.

When this ships: the result says whether the page has any style of its own, and on a page with none the summary says that the values are the browser's defaults.

## Flow

Reuses the Capture that `extract_tokens` already takes on every call (AD-009) and the walk over open shadow roots the page scripts already make: no second page load, no per-element question to the browser.

1. a call -> `tools/extract_tokens.py` (exists) - takes its Capture as today
2. `capture.capture` (exists) - runs one page script over the document and every open shadow root, and holds on `Capture` (exists) whether the page has an Author style
3. `tools/extract_tokens.py` (exists) - copies it into the result as `authorStyles` (door 1) and, when it is false, ends the summary with the sentence of AC 2
4. out: the result with `authorStyles`, and the summary

## Impact

| Front | What changes |
| --- | --- |
| domain | new term: Author style - a rule in a style sheet of the document or of an open shadow root, or a declaration in a `style` attribute. Lives in `capture.py` and `extract_tokens` |
| Capture | one more fact, read on every call for every tool, as AD-009 already does for what `extract_tokens` reads; one page script, no screenshot. Conforms to AD-009, no new decision |
| contract | the `extract_tokens` result gains one field; nothing is renamed or removed. `inspect_element` and `detect_visual_bugs` results are unchanged |
| existing tests | none asserts the full set of keys of the `extract_tokens` result (`test_extract_tokens.py` checks the input names and that an output schema exists); none changes |
| stored data | nothing to migrate - nothing is persisted |

## Relations

`None - no stored-data shape change`

## Surface

`None - no HTTP route: extract_tokens is an MCP tool over stdio whose only outcomes are a result or a ToolError (AD-002). The field it gains is door 1; its outcomes are AC 1 to 13`

## Landing

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| 1. The field | `authorStyles: bool` on the `extract_tokens` result, beside `stabilized`; `false` only when the page has no Author style | `notice: str \| None` - prose a consumer has to parse to branch on. `origin: "author" \| "user-agent"` per token - decided against on issue #36: exact only with one CDP `CSS.getMatchedStylesForNode` per element, and a heuristic (compare with a blank page's defaults) otherwise. It stays open for a later slice: a per-token field can be added beside this one without renaming it |

- Nothing else in this change is hard to reverse: the summary sentence is text, and where the fact is measured is internal to the Capture

## Criteria

### S1: the result says whether the page styles itself (P1)

On an unstyled page the result and its summary say that its values are the browser's defaults; any Author style turns the notice off.

**Acceptance Criteria**

1. The system SHALL return `authorStyles`, a boolean, in the structured result of every `extract_tokens` call, and publish it in the tool's output schema
2. WHEN `extract_tokens` is called on a page with no `<style>`, no `<link rel="stylesheet">`, no adopted style sheet and no `style` attribute THEN the system SHALL return `authorStyles: false` and end the summary with ` The page has no style of its own: these values are the browser's defaults.`
3. WHEN the page's only Author style is a `<style>` element with one rule THEN the system SHALL return `authorStyles: true` and a summary without that sentence
4. WHEN the page's only Author style is a `<link rel="stylesheet">` to a same-origin sheet with one rule THEN the system SHALL return `authorStyles: true`
5. WHEN the page's only Author style is one `style` attribute with one declaration THEN the system SHALL return `authorStyles: true`
6. WHEN the page's only Author style is a style sheet of one rule adopted by the document (`document.adoptedStyleSheets`) THEN the system SHALL return `authorStyles: true`
7. WHEN the page's only Author style is a `<style>` element with one rule inside an open shadow root THEN the system SHALL return `authorStyles: true`
8. WHEN the page's only Author style is a style sheet of one rule adopted by an open shadow root THEN the system SHALL return `authorStyles: true`
9. WHEN the page's only Author style is a `<link rel="stylesheet">` to a sheet of another origin, whose rules the page cannot read THEN the system SHALL return `authorStyles: true`
10. IF the page's only `<style>` element holds no rule THEN the system SHALL return `authorStyles: false`
11. IF the page's only `style` attribute is empty (`style=""`) THEN the system SHALL return `authorStyles: false`
12. IF the page's only `<link rel="stylesheet">` answers 404 THEN the system SHALL return `authorStyles: false`
13. WHILE `scope` is given the system SHALL return `authorStyles` for the whole page: a page whose only rule styles an element outside `scope` SHALL give `authorStyles: true`
14. The `inspect_element` and `detect_visual_bugs` results SHALL hold no `authorStyles` and no other field they did not hold before

**Independent test:** call `extract_tokens` on an HTML fixture with no style and on the same fixture with one `<style>` rule; compare `authorStyles` and the summary.

### S2: the record (P2)

**Acceptance Criteria**

15. The docstring of `extract_tokens` SHALL describe `authorStyles`: what counts as an Author style, that it describes the whole page whatever `scope` is, and that `false` means the values are the browser's defaults
16. The `extract_tokens` paragraph of the README SHALL say that `authorStyles` is false on a page with no style of its own, and that a page with some style still reports the defaults of the elements it does not style, such as a default `<button>`
17. The `[Unreleased]` section of `CHANGELOG.md` SHALL have an `Added` entry for `authorStyles` that links issue #36

**Independent test:** read the three places.

## Out of scope

| Excluded | Why |
| --- | --- |
| Which origin set each value (`origin` per token) | decided against on issue #36 (door 1); a page with some style still reports the defaults of what it leaves unstyled |
| Leaving default values out of the tokens | needs the per-value origin above |
| Styles inside iframes and closed shadow roots | a Capture reads neither |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| What counts as a rule | any entry of a sheet's `cssRules`: a style rule, `@media`, `@import`, `@font-face` alike | one count, no walk into grouping rules; a sheet that holds only an empty `@media` is too rare to pay for | n |
| A sheet that is `disabled`, or whose `media` does not match the screen | a `disabled` sheet does not count; a sheet of another medium does | `disabled` is the page turning its style off; a print sheet is still the page's own style, and telling media apart is a second rule nobody asked for | n |
| Presentational attributes (`bgcolor`, `<font color>`, `align`) | not an Author style | they are not CSS; an unstyled page in 2026 rarely uses them, and counting them means listing every one | n |
| A sheet whose `cssRules` throws (another origin) | counts as an Author style | it loaded, so the page has style; its rules are only unreadable | n |
| An Author style that matches nothing on the page | still `authorStyles: true` | the field says whether the page has a style of its own, not whether each value came from it; per-value is the excluded `origin` | n |
| Fixture of AC 9 | a page on `127.0.0.1` linking a sheet on `localhost` of the same `local_server` | two origins with one server; Chromium refuses `cssRules` across origins | n |

**Open questions:** none - all resolved or logged above.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| tool `extract_tokens` | response shape | AC 1 - one boolean beside `stabilized` |
| tool `extract_tokens` | summary text | AC 2, AC 3 |
| tool `extract_tokens` | error shape and codes | n/a - no new failure: the page script cannot fail on a page the Capture already loaded |
| tool `extract_tokens` | who may call, rate limits | n/a - a local stdio server, as before |
| tool `extract_tokens` | versioning | AC 17 - a field is added, nothing breaks |
| tools `inspect_element`, `detect_visual_bugs` | response shape | AC 14 - unchanged |
| document `README.md` | what the reader does next | AC 16 - knows a true `authorStyles` does not clear every value |
| document `CHANGELOG.md` | structure | AC 17 - one entry under `[Unreleased]`, in the form of the existing ones |

## Sources

- [Issue #36](https://github.com/sh4wty1/squint-mcp/issues/36) - the report and the two shapes; the notice was chosen by the maintainer on 2026-10-19
- `.specs/STATE.md` AD-009 - the Capture reads what `extract_tokens` needs on every call
