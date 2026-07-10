---
name: mit-prompt-optimization
description: Optimize a MIT document-generation prompt pipeline (MIT41/45/65/37/43…) against its real Structured Outputs schemas. Use when the user asks to otimizar/auditar os prompts de uma MIT, wants "as mesmas otimizações" applied to another MIT journey, or pastes platform prompts for a new step/journey.
---

# MIT Prompt Pipeline Optimization

Turn a MIT journey's platform prompts (pasted by the user) into a schema-audited, cache-stable, **drop-in** prompt set with two verification layers. The schema is the **contract**; prompt prose is commentary on it — every claim in a body must be checkable against a schema or a decision the user made.

## Working-tree convention

Locate (or create, on first use) a prompts workspace in the project repo:

- `optimized/_shared/_prefix_<mit>.md` (prefixo global por jornada) + `optimized/<mit>/*.md` (corpos por step) → `compile.sh` gera `compiled/` e `paste/` (o que se cola na tela do Editor de Prompts da infra).
- Schemas strict exportados do TS da infra em `<mit>-schemas.md`; originais da plataforma preservados em `MIT<NN>-prompts/`.
- `validation/validate_<mit>.py` (estático, stdlib) e `validation/eval_<mit>.py` (eval real).
- Entregas anteriores (`DELIVERY_*.md`) são o espelho de formato.

Nota de provider (07/2026): a família GPT-5.6 (sol E terra) devolve 500 determinístico no OpenRouter com payload completo system+user+json_schema strict — rode evals 5.6 na API OpenAI direta; quando bloqueado, reporte e entregue o script, nunca troque de modelo silenciosamente.

## 1. Discovery before questions

Internalize the journey before touching prompt text. Look up facts (repo, prior DELIVERYs); grill only decisions. Establish: what the MIT document IS in the methodology chain (which MIT feeds it, what it feeds); cardinality — per módulo or per projeto (decides where cache pays); pipeline steps + StepIds; what the platform injects in each user turn; whether the tela has a global prompt field; whether any "reference material" the prompts cite actually exists (self-references are usually ruído).
**Done when** the pipeline map (steps, inputs, cardinality, tela mechanics) is confirmed by the user.

## 2. Schema-first

Obtain the real strict schemas (infra TS export) before writing any body — optimizing from prose structure alone has produced contract regressions before. Schemas unavailable → two-phase mode with explicit flags, announced as such.
**Done when** every step maps to a named schema that parses and is strict.

## 3. Contract audit — defect classes to hunt

Diff each prompt against its schema:

- **Invented contract** — fields/enums in the prompt that the schema lacks (worst class).
- **Orphan rules** — instructions pointing at fields/documents with no schema home (e.g. "considere nas observações" with no observations field).
- **Enum drift** — prompt teaches values the schema rejects.
- **Forced hallucination** — required fields the generation moment cannot honestly fill: execution results in a planning-time document, minItems:1 on possibly-empty arrays. Fix in the body with explicit planning/initial values from the contract itself ("Pendente" / "" / "Não" / null) + a schema flag for infra.
- **Uncited required keys** — required keys the body never names; target deep coverage N/N.
- **Circular/stale references** and model-unknowable facts — dates and IDs come injected in the user turn.
- **Gems** — rules that are correct and valuable (e.g. client-language rules): keep and condense without losing any prohibition, and say in the delivery that they were kept.

**Done when** every defect is listed D1..Dn with its correction and the keep-list is named.

## 4. Grill the decisions

One question per turn, each with a recommendation. Minimum set: schema availability; scope (drop-in bodies + S-flags vs structural change); global-prefix mechanics when the tela lacks a global field — default is the self-contained paste (prefix compiled into each step; cache outcome identical to a shared field since keys are per-step); date rules; eval scope and model. Pipeline-structure doubts (e.g. "is the audit step consumed at all?") become S-flags for infra, never blockers.

## 5. Rewrite — prefix + lean bodies, compiled

- One shared prefix per journey (`_prefix_<mit>.md`): what the document is, chain table, the journey's own invariant (MIT41: zero-loss preservation; MIT45: coverage — every TO-BE item → ≥1 cycle and ≥1 positive case), evidence rules, ""/null conventions, marker prohibition plus contract-defined exceptions (`"[ ]"`, `"[CRÍTICO]"`), module focus, output rules. The HTML-comment header carries the infra cache rules and is stripped at compile.
- Per-step body: task, instructions per schema node citing EVERY required key, explicit initial values, byte-exact enums, Saída section. Header comment: `prompt_cache_key` `mit<NN>-<step>-vN`, effort, corrections vs original.
- Extend the compile script; each paste must exceed 1024 tokens (~4K chars) to be cacheable.

**Done when** compile runs and every body cites 100% of deep required keys.

## 6. Verify — two layers, evidence before claims

1. **Static validator** (stdlib, CI; separate script per journey so existing validators stay untouched): schema parse/strict; regression asserts — defect pattern present in original = confirmed, present in optimized = FAIL; deep required-key coverage; ```json fence ban; paste integrity (prefix inlined, no HTML comments, size).
2. **Live eval**: chained fixture run where every planted **trap** maps to one assert — coverage of each TO-BE item, honest planning fields (no invented execution/volumetry), jargon regex on client-facing fields (`MATA\d|SIGA[A-Z]{3}|RN\d|MV_`), injected date echoed back, enum exactness, only-existing IDs referenced. Iterate bodies until green; provider blocked → preserve the runnable script in `validation/` and flag it in the DELIVERY.

**Done when** the validator is green and the eval is green or explicitly blocked-with-handoff.

## 7. Deliver

Preserve originals; write the DELIVERY doc mirroring prior ones (§paste table, §config per step incl. 5.6 `prompt_cache_options`+breakpoint, §user-turn table, §defects D-n, §flags S-n — none blocking, §verification, §maintenance loop); ADR for architecture decisions. Close by telling the user exactly which file(s) go to infra.
