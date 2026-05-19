# Retorno `.2PR` Symbolic Names

Section-2 lines in `.2PR` files use symbolic identifiers (not ADVPL expressions) for fields where Protheus auto-maps CNAB retorno positions to internal variables.

Glossary observed in `001PG.2PR`:

| Symbol | Description | Protheus target |
|--------|-------------|-----------------|
| `SEGMENTO` | Segment code (P/Q/A/B/J/N/O) | Internal dispatch |
| `DATA` | Occurrence date (date pagamento, baixa, etc.) | Various depending on segment |
| `DATACREDITO` | Credit date | SE2 / SE5 movements |
| `VALOR` | Value field | SE2->E2_VLRBX, SE2->E2_SALDO, etc. |
| `TITULO` | Document identifier / "seu número" | SE2->E2_IDCNAB / E1_IDCNAB |
| `ESPECIE` | Document species code | SE2/SE1 |
| `OCORRENCIA` | Occurrence code(s) — 10 chars usually | SE2->E2_MOTBX or SE1->E1_MOTBX |
| `ABATIMENTO` | Abatement value | SE2 / SE1 |
| `DESCONTO` | Discount value granted | SE2 / SE1 |
| `MULTA` | Multa value | SE2 / SE1 |
| `RESERVADO` | Placeholder for reserved bank-specific field | (not mapped, kept as bytes) |

The validator allows these in section-2 expressions of `.2PR` files (and ONLY in `.2PR`, not `.2PE`).
