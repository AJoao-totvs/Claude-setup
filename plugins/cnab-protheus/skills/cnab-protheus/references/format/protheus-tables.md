# Protheus Tables Referenced in `.2PE` Expressions

Tables and fields used by ADVPL expressions in CNAB SIGACFG configs. Only fields observed in `001PG.2PE` or commonly used in pagamento layouts are listed. Validator's allow-list mirrors this.

## SM0 — Empresa (Cabeçalho)

Single-row table with company data.

| Field | Description |
|-------|-------------|
| `M0_CGC` | CNPJ da empresa (14 dig, sem formatação) |
| `M0_NOME` | Razão social longa |
| `M0_NOMECOM` | Nome comercial/fantasia |
| `M0_INSC` | Inscrição estadual |
| `M0_ENDCOB` | Endereço de cobrança |
| `M0_ENDENT` | Endereço de entrega |
| `M0_CIDCOB` | Cidade de cobrança |
| `M0_CIDENT` | Cidade de entrega |
| `M0_CEPCOB` | CEP cobrança |
| `M0_CEPENT` | CEP entrega |
| `M0_ESTCOB` | Estado cobrança |
| `M0_ESTENT` | Estado entrega |
| `M0_COMPENT` | Complemento endereço entrega |
| `M0_TPINSC` | Tipo de inscrição (1=CPF, 2=CNPJ, 3=outro) |

## SEE — Parâmetros Banco/Convênio CNAB

Configuração por banco/agência/conta para CNAB.

| Field | Description |
|-------|-------------|
| `EE_CODIGO` | Código do banco (001, 237, ...) |
| `EE_CODEMP` | Código da empresa/convênio fornecido pelo banco |
| `EE_AGENCIA` | Agência |
| `EE_DVAGE` | DV da agência |
| `EE_CONTA` | Conta corrente |
| `EE_DVCTA` | DV da conta |
| `EE_ULTDSK` | NSA — último número sequencial do arquivo enviado |

## SA6 — Banco (Cadastro)

Cadastro de bancos da empresa.

| Field | Description |
|-------|-------------|
| `A6_COD` | Código do banco |
| `A6_AGENCIA` | Agência |
| `A6_DIGAGE` | DV agência |
| `A6_NUMCON` | Número da conta |
| `A6_DIGCONT` | DV conta |

## SEA — Cadastro CNAB / Modelos

Modelos e parâmetros operacionais de cobrança/pagamento.

| Field | Description |
|-------|-------------|
| `EA_BANCO` | Código do banco |
| `EA_MODELO` | Modelo operacional ("01", "03", "05", "17", "18", "30", "31", "41", "43", ...) — usado em condições IIF para escolher segmento |
| `EA_TIPOPAG` | Tipo do serviço de pagamento (ex: "20" para folha) |

## SE2 — Contas a Pagar

Títulos a pagar (fornecedores, tributos, etc.).

| Field | Description |
|-------|-------------|
| `E2_VENCTO` | Data de vencimento original |
| `E2_VENCREA` | Data de vencimento real (após adiamentos) |
| `E2_EMISSAO` | Data de emissão |
| `E2_VALOR` | Valor nominal |
| `E2_SALDO` | Saldo a pagar |
| `E2_JUROS` | Juros |
| `E2_MULTA` | Multa |
| `E2_DECRESC` | Decréscimo / desconto |
| `E2_ACRESC` | Acréscimo |
| `E2_VALJUR` | Valor de juros (alternativo) |
| `E2_VLCRUZ` | Valor cruzado / total |
| `E2_IDCNAB` | ID interno para conciliação CNAB |
| `E2_CODRET` | Código de retenção / receita (DARF/GPS) |
| `E2_CODBAR` | Código de barras (boleto / concessionária / tributo c/ código) |
| `E2_FORBCO` | Banco do fornecedor |
| `E2_FORAGE` | Agência do fornecedor |
| `E2_FORCTA` | Conta do fornecedor |
| `E2_FAGEDV` | DV agência fornecedor |
| `E2_FCTADV` | DV conta fornecedor |
| `E2_NOMFOR` | Nome do fornecedor |
| `E2_XNRREFE` | Nº referência customizado (ex: para tributos com identificador específico) |
| `E2_XCOMPET` | Competência (ex: tributo GPS) |
| `E2_XVLINSS` | Valor INSS |
| `E2_XVLENTI` | Valor de entidade |

## SA2 — Fornecedores

| Field | Description |
|-------|-------------|
| `A2_TIPO` | Tipo de pessoa ("F" / "J") |
| `A2_CGC` | CPF/CNPJ |
| `A2_NOME` | Nome / Razão social |
| `A2_END` | Endereço |
| `A2_COMPLEM` | Complemento |
| `A2_BAIRRO` | Bairro |
| `A2_MUN` | Município |
| `A2_EST` | Estado |
| `A2_CEP` | CEP |

## Other Globals

| Name | Description |
|------|-------------|
| `DDATABASE` | Data corrente do sistema |
| `NSEQ` | Variável de sequência do arquivo |
| `NLOTCNAB2`, `NSOMAVLLOTE`, `NTOTCNAB2` | Variáveis de controle do gerador CNAB Modelo 2 |
