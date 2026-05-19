# ADVPL Functions Used in `.2PE` Expressions

Glossary of every ADVPL function observed in `001PG.2PE` plus extensions documented in TDN TOTVS. The skill's validator only allows these in generated expressions.

| Function | Signature | Purpose |
|----------|-----------|---------|
| `STRZERO` | `STRZERO(num, len)` | Convert number to string, zero-pad on left to `len` chars. |
| `INT` | `INT(num)` | Truncate to integer (discards decimals). |
| `ROUND` | `ROUND(num, decimals)` | Round to `decimals` places. |
| `NOROUND` | `NOROUND(num)` | Treat number as truncated (avoid implicit rounding). |
| `PADL` | `PADL(str, len, char)` | Pad `str` on left with `char` to `len`. |
| `PADR` | `PADR(str, len, char?)` | Pad `str` on right (default char is space) to `len`. |
| `SUBS` | `SUBS(str, start, len)` | Substring starting at `start` (1-indexed), of length `len`. |
| `SUBSTR` | Same as `SUBS`. | Alias. |
| `LEFT` | `LEFT(str, len)` | Leftmost `len` chars. |
| `DTOS` | `DTOS(date)` | Date → string "AAAAMMDD". |
| `DAY` | `DAY(date)` | Day component (1-31). |
| `MONTH` | `MONTH(date)` | Month (1-12). |
| `YEAR` | `YEAR(date)` | Year (4 digits). |
| `TIME` | `TIME()` | Current time "HH:MM:SS". |
| `STRTRAN` | `STRTRAN(str, from, to?)` | Replace chars (default removes). |
| `IIF` | `IIF(cond, true_val, false_val)` | Inline if. |
| `EMPTY` | `EMPTY(val)` | True if val is empty/zero/null. |
| `AT` | `AT(needle, haystack)` | 1-indexed position of `needle` in `haystack`, 0 if not found. |
| `ALLTRIM` | `ALLTRIM(str)` | Trim left + right. |
| `UPPER` | `UPPER(str)` | Uppercase. |
| `VAL` | `VAL(str)` | String → numeric. |
| `SPACE` | `SPACE(N)` | N space characters. |
| `REPLICATE` | `REPLICATE(char, N)` | Repeat `char` N times. |
| `INCREMENTA` | `INCREMENTA()` | Protheus-managed counter for sequential record numbering. |
| `GRAVADATA` | `GRAVADATA(date, flag, format)` | TOTVS proprietary: format date according to `format` (e.g., 5 = DDMMAAAA). |

## TOTVS Proprietary Functions

These are Protheus-specific globals/helpers used in CNAB layouts:

| Name | Type | Purpose |
|------|------|---------|
| `DDATABASE` | variable | System date at moment of remessa generation. |
| `NSEQ` | variable | Protheus-managed file sequence number. |
| `NLOTCNAB2` | variable | Current lote being processed. |
| `NSOMAVLLOTE` | variable | Running sum of values in current lote. |
| `NTOTCNAB2` | variable | Total records count. |
| `F420SEQLOT()` | function | Sequential within current lote. |
| `F420LINLOT()` | function | Total lines in current lote. |
| `FNLINCNAB2()` | function | Total lines in arquivo. |
| `U_TTCNABM2(N?)` | function | TOTVS helper (signature varies); used as totalizer. |
| `INCREMENTAL()` | function | Variant of `INCREMENTA()` returning incremented-then-decremented value (observed in 27D1). |
| `SOMAVALOR()` | function | Sums values for trailer. |
| `RESERVADO` | variable | Used as filler placeholder in some retorno fields. |

The validator allows all of the above. Adding a new function requires updating this file AND the validator's allow-list.

## Protheus Table References

See `protheus-tables.md` for the table glossary (SE1, SE2, SA1, SA2, SA6, SEA, SEE, SM0).
