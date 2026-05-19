---
name: cnab-protheus
description: >
  Gera arquivos de configuração Protheus SIGACFG (.2PE remessa / .2PR retorno)
  para CNAB 240 dos 4 maiores bancos brasileiros (Banco do Brasil 001, Bradesco 237,
  Itaú 341, Santander 033), cobrindo cobrança, pagamento a fornecedores, folha e tributos.
  Pesquisa specs CNAB direto da fonte oficial dos bancos, cacheia como YAML
  reproduzível, e aplica mapeamentos curados para expressões ADVPL. Use quando o
  usuário pedir para gerar arquivo de configuração Protheus para CNAB 240, montar
  .2PE/.2PR, configurar SIGACFG, integrar novo banco no Protheus, ou mencionar
  TOTVS Protheus + CNAB.
version: 1.0.0-a
tags: [cnab, protheus, totvs, sigacfg, banking, brazil]
---

# CNAB-Protheus Skill

Gera arquivos de configuração SIGACFG (`.2PE` remessa, `.2PR` retorno) que o ERP Protheus utiliza para montar/parsear CNABs 240 dos principais bancos brasileiros.

A skill NÃO gera CNAB 240 raw — o Protheus, configurado com os arquivos produzidos pela skill, é quem gera o CNAB ao executar rotinas como FINA150/FINA200/FINA420/FINA430.

## Versão atual (v1.0-a)

Cobertura: **BB (001) — pagamento — remessa (.2PE)**. Validado byte-a-byte contra a fixture `001PG.2PE`.

Próximas versões adicionam Bradesco, Itaú, Santander, e operações cobrança/folha/tributos.

## Quando usar

- "Gere o .2PE para BB pagamento"
- "Crie a configuração SIGACFG do Protheus para CNAB 240 do Banco do Brasil"
- "Integre um novo banco CNAB no Protheus"
- "Atualize a spec CNAB do banco X"

## Fluxo

1. Confirma com o usuário: banco (BB/Bradesco/Itaú/Santander) + operação (pagamento/cobrança/folha/tributos) + direção (remessa/retorno).
2. Verifica se já existe `references/specs/{bank}/{operacao}.yaml` cacheado.
   - Se NÃO existe: dispara agente de pesquisa (`docs-lookup` ou subagente custom) para buscar o manual oficial do banco, extrair layout (segmentos, campos, posições), e salvar como YAML.
3. Invoca `scripts/gen_protheus_config.py --spec <yaml> --patterns references/mappings/field-patterns.yaml --output <bank>{op}.2PE`.
4. Roda validação em 3 camadas:
   - Sintática local (`validators.py`): tamanho de linha, posições não-sobrepostas, expressões ADVPL bem-formadas.
   - Byte-diff (`byte_diff.py`): contra fixture (apenas BB pagamento em v1.0-a).
   - Code review (`agents/cnab-config-reviewer.md`): subagente LLM com contexto do manual.
5. Apresenta arquivo gerado + relatório de validação.

## Comandos comuns

Gerar .2PE BB pagamento (assumindo spec já cacheado):

```bash
python scripts/gen_protheus_config.py \
  --spec references/specs/bb/pagamento.yaml \
  --patterns references/mappings/field-patterns.yaml \
  --output build/001PG.2PE
```

Forçar re-pesquisa (refresh) do spec:

```
# No prompt para Claude:
"Atualize a spec do BB pagamento — força re-pesquisa do manual oficial"
```

## Estrutura

- `references/format/` — documentação curada do formato SIGACFG, ADVPL, tabelas Protheus
- `references/mappings/` — patterns CNAB-field → ADVPL e mapeamentos Protheus
- `references/specs/{bank}/{op}.yaml` — YAML cacheado por (banco, operação)
- `references/fixtures/` — arquivos `.2PE`/`.2PR` de referência (ground truth)
- `scripts/` — gerador Python e validadores
- `agents/cnab-config-reviewer.md` — agent semântico de review

## Confiança por combo

Por ora apenas BB pagamento tem byte-fixture. Demais combinações (a serem implementadas em v1.0-b/c/d/e) terão **confiança reduzida** — sintática + review LLM, sem ground truth byte-a-byte. Cada arquivo gerado terá um header indicando o nível de confiança.

## Limites conhecidos

- Sem CNAB 400 (apenas 240).
- Sem cooperativas (Sicoob, Sicredi) em v1.0.
- Sem round-trip Protheus em CI — QA manual recomendada antes de uso em produção.
- Encoding fixo CP-1252. Caracteres fora do CP-1252 são substituídos por `?` (com warning).
