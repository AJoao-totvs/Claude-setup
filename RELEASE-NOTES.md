## cnab-protheus v1.0.0-a — 2026-05-19

Initial release. First combination supported: **Banco do Brasil (001) — pagamento — remessa**.

### What's in this release

- `.2PE` (remessa) generation from cached YAML spec
- Byte-identical match against the canonical fixture `001PG.2PE` (validated via byte-diff test)
- Validators: line length (500), section structure (10-17 declarations + 20-27 definitions), conditional overlap detection (per register+subtype+flag)
- Curated mapping patterns (`references/mappings/field-patterns.yaml`): dates (DDMMAAAA/AAAAMMDD), values in centavos, alpha padding, fillers, counters, plus `raw` escape hatch
- Curated source mappings (`references/mappings/source-mappings.yaml`): SM0 (empresa), SEE (convênio), SA6 (banco), SE2 (a pagar), SA2 (fornecedor), SEA (modelo)
- Custom agent `cnab-config-reviewer` (in `agents/`) for semantic review (manual dispatch in v1.0-a)
- Encoding: CP-1252 ANSI, CRLF line terminators, 500-char fixed line length

### Not yet (coming in v1.0-b/c/d/e)

- Other banks (Bradesco, Itaú, Santander)
- Other operations (cobrança, folha, tributos)
- `.2PR` (retorno) generation — fixture exists but generator not yet wired
- Online research orchestration for fresh specs (currently a NotImplementedError stub)
- Automatic invocation of `cnab-config-reviewer` agent

### Known limitations

- Only BB pagamento has byte-truth validation
- No round-trip Protheus integration testing (QA must verify manually in Protheus dev env)
- Non-CP1252 characters get replaced with `?` and emit UnicodeWarning (financial-data integrity considered acceptable for v1.0-a)

### Stats

- 53 unit tests, 91% coverage
- ~20 git commits on branch
- Plugin at `plugins/cnab-protheus/` includes skill, references (format docs + mappings + spec + fixtures + manual), scripts (Python), agents, templates, tests
