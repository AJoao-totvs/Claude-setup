# Protheus SIGACFG `.2PE` / `.2PR` File Format

Reverse-engineered from `001PG.2PE` (BB pagamento remessa) and `001PG.2PR` (BB pagamento retorno) provided by the user, and cross-referenced with the Manual de Importação de Arquivos CNAB 240 v2.11.

## Macro Structure

Each file has two sections, separated implicitly by the change in register prefix:

1. **Section 1** — Register declarations. Registers `10`-`17`. Each line declares "this register type exists, use it when the condition is true".
2. **Section 2** — Field definitions. Registers `20`-`27` (mapping `+10` from section 1). Each line defines one field of one register.

## Line Layout (every line is exactly 500 chars + CRLF)

### Section 1 — Declaration

```
RR T NomeDoRegistro<padding até col 37>CONDIÇÃO<padding até 500>
```

| Cols | Content |
|------|---------|
| 0-1  | Register code (`10`-`17`) |
| 2-3  | Subtype (right-padded if 1 char): `H ` (Header), `T ` (Trailer), `D ` (Detail), `D1` (Detail variant) |
| 4-36 | Free-form name (right-padded with spaces) |
| 37+  | ADVPL condition: `.T.` (always use) or `IIF(<expr>, .T., .F.)` |

### Section 2 — Field Definition

```
RR T NomeCampo<padding até col 20>SSSEEEF<expressão_ADVPL_ou_valor><padding até 500>
```

| Cols | Content |
|------|---------|
| 0-1  | Register code (`20`-`27`) — refers to which register-type this field belongs to |
| 2-3  | Subtype (`H `, `T `, `D `, `D1`) |
| 4-19 | Field name (right-padded with spaces, 16 cols) |
| 20-26 | Position block: `SSSEEEF` — start (3 digits), end (3 digits), flag (1 char, usually `0`, sometimes `2`) |
| 27+   | Expression: ADVPL code (`SE2->E2_VENCTO`, `STRZERO(...)`, `IIF(...)`, `SPACE(N)`), literal constant (e.g., `"001"`, `"M"`), or empty for FILLER |

## Register Mapping (Section 1 → Section 2)

| Section 1 | Section 2 | Function |
|-----------|-----------|----------|
| 10H/T     | 20H/T     | Header / Trailer de Arquivo |
| 11D/H/T   | 21D/H/T   | Lote Segmento A (pagamento crédito em conta / TED) |
| 12D/H/T   | 22D/H/T   | Lote Segmento B (PIX / dados complementares) |
| 13D/D1    | 23D/D1    | Lote Segmento J / J-52 (boleto / boleto > R$250k) |
| 15T       | 25T       | Trailer Segmento J |
| 16D/H/T   | 26D/H/T   | Lote Segmento O (concessionária) |
| 17D/D1/H/T | 27D/D1/H/T | Lote Segmento N (tributo GPS / DARF) |

Note: not every declaration has corresponding definitions in section 2 for every operation. The skill emits only definitions whose declared register has a non-trivial condition (or `.T.`).

## Position Block Flag

The 7th char (`F` in `SSSEEEF`):

- `0` (default) — standard field
- `2` — observed for value fields with implied 2-decimal centavos format (`STRZERO((value*100), N)`). Hypothesis: signals "this field is a monetary value, Protheus may render with cents". Not confirmed; treat as informational. Generator should reproduce whatever flag exists in the spec YAML.

## Encoding

- **Character set:** Windows-1252 (CP-1252, also known as ANSI in Protheus-speak). Latin-1 with the ECU extensions for Brazilian accents (á, é, ç, ã, õ).
- **Line terminator:** CRLF (`\r\n`).
- **Padding:** Spaces (0x20) right-pad each line to exactly 500 chars BEFORE the CRLF.
- **No BOM, no trailing newline beyond the last line's CRLF.**

## ADVPL Expression Conventions

See `advpl-functions.md` for full glossary. Common patterns:

- Date as DDMMAAAA: `SUBS(DTOS(<field>),7,2)+SUBS(DTOS(<field>),5,2)+SUBS(DTOS(<field>),1,4)`
- Date as AAAAMMDD: `SUBS(DTOS(<field>),1,4)+SUBS(DTOS(<field>),5,2)+SUBS(DTOS(<field>),7,2)`
- Numeric value in cents, zero-padded: `STRZERO(INT(<field>*100), <len>)`
- Alpha right-padded with spaces: `PADR(ALLTRIM(<field>), <len>)`
- Alpha left-padded with zeros: `PADL(ALLTRIM(<field>), <len>, "0")`
- Filler with N spaces: `SPACE(N)`
- Filler with N zeros: `REPLICATE("0", N)`
- Sequential counter: `INCREMENTA()` (Protheus-managed)

## Retorno (.2PR) Specifics

The `.2PR` file uses the same line layout. Difference is in section-2 expressions:

- Some lines have **symbolic names** instead of ADVPL: `SEGMENTO`, `DATA`, `DATACREDITO`, `VALOR`, `TITULO`, `ESPECIE`, `OCORRENCIA`, `ABATIMENTO`, `DESCONTO`, `MULTA`, `RESERVADO`. These map positions in the bank retorno CNAB to Protheus internal variables.
- Some lines have empty expressions — used to declare position ranges without specifying a target (Protheus reads the chars at those positions verbatim if needed).
- Header/trailer of arquivo and lote may use full ADVPL expressions to populate Protheus tables from the retorno header.

See `retorno-symbols.md` for the symbolic name glossary.
