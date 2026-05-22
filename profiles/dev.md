# Perfil: Dev

Setup completo para desenvolvedores. Unifica Python, Go, ADVPL/TLPP, frontend, Docker/Kubernetes, e todas as ferramentas de produtividade.

## Filosofia: PIV Loop

Todo ciclo de desenvolvimento segue **Plan → Implement → Validate**:

```
PLAN
  ├── /prime (carregar contexto do projeto)
  ├── /create-prd (definir requisitos)
  ├── /plan (decompor em tarefas)
  └── /create-stories (opcional: push para ClickUp)

IMPLEMENT
  ├── contexto limpo (nova sessao ou /compact)
  ├── executar tarefas do plano
  ├── TDD: teste primeiro, implementar depois
  ├── agent-browser: validar E2E durante implementacao
  └── commits frequentes e descritivos

VALIDATE
  ├── lint + type check
  ├── testes unitarios
  ├── E2E via agent-browser
  ├── /review (code review automatico)
  └── /security-review (se toca auth/input/APIs)
```

## 5 Golden Rules

1. **Commandify**: Transforme padroes repetidos em commands/skills reutilizaveis
2. **Reduce Assumptions**: Claude deve perguntar antes de assumir
3. **Context is King**: Resete contexto entre tarefas; use /prime para carregar sob demanda
4. **Git Log is Memory**: Commits descritivos sao a memoria entre sessoes
5. **System Evolution**: Todo erro do agente vira melhoria no CLAUDE.md

## Plugins

| Plugin | Comando | Para que serve |
|--------|---------|----------------|
| superpowers | `claude plugin add superpowers@claude-plugins-official` | PIV loop, TDD, debugging, brainstorm |
| context7 | `claude plugin add context7@claude-plugins-official` | Docs atualizados de qualquer lib |
| code-review | `claude plugin add code-review@claude-plugins-official` | Review automatico |
| github | `claude plugin add github@claude-plugins-official` | PRs, issues, code search |
| frontend-design | `claude plugin add frontend-design@claude-plugins-official` | UI production-grade |
| advpl-specialist | `claude plugin marketplace add thalysjuvenal/advpl-specialist` | Agentes ADVPL/Protheus |

## Skills internas do bundle

| Skill | Para que serve |
|-------|----------------|
| iqs-k8s | Deploy e debug no cluster Kubernetes IQS (ns iqs) + Harbor docker.totvs.io |

## MCP Servers

### Obrigatorios

```bash
# Docs de qualquer lib (evita training data desatualizada)
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest

# GitHub (PRs, issues, code search)
claude mcp add github-mcp -- npx -y @modelcontextprotocol/server-github
# Requer: GITHUB_PERSONAL_ACCESS_TOKEN

# Kubernetes (gestao de containers — uso intenso TOTVS)
claude mcp add k8s -- npx -y mcp-server-kubernetes
# Usa: ~/.kube/config

# Docker (build, run, compose)
claude mcp add docker -- npx -y mcp-server-docker
```

### Browser: Agent Browser (preferido) vs Playwright

O Claude Code tem `agent-browser` como skill nativa para E2E validation durante implementacao — compartilha sessao e contexto. Use como primeira opcao.

Playwright MCP como alternativa para testes E2E mais estruturados:
```bash
claude mcp add playwright -- npx -y @anthropic/mcp-playwright
```

### Banco de Dados (configure conforme seu projeto)

```bash
# PostgreSQL
claude mcp add postgres -- npx -y @anthropic/mcp-postgres
# Requer: POSTGRES_CONNECTION_STRING

# SQL Server (MSSQL)
claude mcp add mssql -- npx -y @anthropic/mcp-mssql
# Requer: MSSQL_CONNECTION_STRING

# Oracle
claude mcp add oracle -- npx -y mcp-server-oracle
# Requer: ORACLE_CONNECTION_STRING
```

### Angular + PO-UI

```bash
# Angular CLI MCP (Angular 20.2+, built-in)
ng mcp

# PO-UI docs via Context7 (ja instalado na base)
# Use: /docs @po-ui/ng-components
```

### Frontend adicional (se aplicavel)

```bash
# Figma design-to-code
claude mcp add figma -- npx -y @anthropic/mcp-figma
# Requer: FIGMA_PERSONAL_ACCESS_TOKEN
```

### Observabilidade (opcional)

```bash
# Sentry
claude mcp add sentry -- npx -y @sentry/mcp-server
# Requer: SENTRY_AUTH_TOKEN, SENTRY_ORG

# AWS
claude mcp add aws -- npx -y @awslabs/mcp-server-aws
```

### ClickUp

```bash
claude mcp add clickup https://mcp.clickup.com/mcp
# OAuth automatico — sem env var
```

## Hooks (`.claude/settings.json`)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo $CLAUDE_FILE_PATH | grep -qE '\\.(py)$'; then ruff format $CLAUDE_FILE_PATH 2>/dev/null && ruff check --fix $CLAUDE_FILE_PATH 2>/dev/null; fi || true"
          }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo $CLAUDE_FILE_PATH | grep -qE '\\.(go)$'; then gofmt -w $CLAUDE_FILE_PATH 2>/dev/null; fi || true"
          }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo $CLAUDE_FILE_PATH | grep -qE '\\.(ts|tsx|js|jsx)$'; then npx prettier --write $CLAUDE_FILE_PATH 2>/dev/null && npx eslint --fix $CLAUDE_FILE_PATH 2>/dev/null; fi || true"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo $CLAUDE_FILE_PATH | grep -qE '\\.(env|env\\.|credentials|secret|key)$'; then echo 'BLOCKED: nao editar secrets via AI' && exit 1; fi"
          }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo $CLAUDE_FILE_PATH | grep -qE '(package-lock|yarn\\.lock|pnpm-lock|Pipfile\\.lock|poetry\\.lock|go\\.sum)'; then echo 'BLOCKED: nao editar lock files' && exit 1; fi"
          }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo $CLAUDE_FILE_PATH | grep -qE '\\.(ini|cfg|appserver)$'; then echo 'BLOCKED: nao editar config de servidor via AI' && exit 1; fi"
          }
        ]
      }
    ]
  }
}
```

## Subagentes

| Subagente | Linguagem/Area | Quando usar |
|-----------|---------------|-------------|
| `python-reviewer` | Python | Apos modificar .py |
| `go-reviewer` | Go | Apos modificar .go |
| `typescript-reviewer` | TS/JS | Apos modificar .ts/.tsx |
| `go-build-resolver` | Go | Build Go falhou |
| `database-reviewer` | SQL | Queries, migrations, schema |
| `security-reviewer` | Todas | Auth, input, secrets, APIs |
| `code-reviewer` | Todas | Sempre, apos qualquer mudanca |
| `tdd-guide` | Todas | Antes de implementar feature/fix |
| `e2e-runner` | Frontend | Testes E2E Playwright |

## Skills ADVPL (via advpl-specialist)

| Comando | Funcao |
|---------|--------|
| `/generate` | Gerar codigo ADVPL/TLPP (MVC, REST, SOAP) |
| `/migrate` | Migrar ADVPL → TLPP |
| `/diagnose` | Diagnosticar erro Protheus |
| `/docs` | Consultar funcoes nativas TDN |

## Skills Angular + PO-UI

#### /po-crud
Crie em `.claude/skills/po-crud/SKILL.md`:
```yaml
---
name: po-crud
description: Scaffold CRUD completo Angular + PO-UI com dynamic pages e servico REST
disable-model-invocation: true
---
```
```markdown
## PO-UI CRUD Scaffold

Generate a complete CRUD module using PO-UI dynamic components.

### What is generated:
1. **Feature module** (lazy-loaded) with routing
2. **List page** using `po-page-dynamic-table`
   - Automatic columns from metadata
   - Search, pagination, filters
   - Actions: new, edit, view, delete
3. **Edit page** using `po-page-dynamic-edit`
   - Form fields from metadata
   - Create and update modes
4. **Detail page** using `po-page-dynamic-detail`
   - Read-only view
5. **Service** with HttpClient calls to REST API
6. **Metadata definition** (PoDynamicFormField[])

### PO-UI Dynamic Page Pattern:
```typescript
// list.component.ts
@Component({
  template: `
    <po-page-dynamic-table
      [p-service-api]="serviceApi"
      [p-title]="title"
      [p-actions]="actions">
    </po-page-dynamic-table>
  `
})
export class ListComponent {
  serviceApi = '/api/v1/[resource]';
  title = '[Resource Name]';
  actions: PoPageDynamicTableActions = {
    new: '/[resource]/new',
    edit: '/[resource]/edit/:id',
    detail: '/[resource]/detail/:id',
    remove: true
  };
}

// edit.component.ts
@Component({
  template: `
    <po-page-dynamic-edit
      [p-service-api]="serviceApi"
      [p-title]="title">
    </po-page-dynamic-edit>
  `
})
export class EditComponent {
  serviceApi = '/api/v1/[resource]';
  title = '[Resource Name]';
}
```

### REST API contract (TOTVS standard):
- GET /api/v1/[resource] → `{"hasNext": bool, "items": [], "remainingRecords": int}`
- GET /api/v1/[resource]/:id → single item
- POST /api/v1/[resource] → create
- PUT /api/v1/[resource]/:id → update
- DELETE /api/v1/[resource]/:id → delete
- GET /api/v1/[resource]/metadata → field definitions for dynamic rendering

Ask user for: resource name, fields (name/type/required), API base URL, master-detail (Y/N).
```

#### /po-form
Crie em `.claude/skills/po-form/SKILL.md`:
```yaml
---
name: po-form
description: Gerar formulario PO-UI com po-dynamic-form a partir de descricao de campos
disable-model-invocation: true
---
```
```markdown
## PO-UI Dynamic Form Generator

Generate a po-dynamic-form component from field descriptions.

### Field types supported:
- text, email, url, password
- number, currency, decimal
- date, dateTime, time
- select, multiSelect, combo (searchable)
- checkbox, radio, switch
- textarea, richText
- upload

### Output:
```typescript
const fields: Array<PoDynamicFormField> = [
  { property: 'name', label: 'Nome', required: true, gridColumns: 6, order: 1 },
  { property: 'email', label: 'E-mail', type: 'email', gridColumns: 6, order: 2 },
  { property: 'department', label: 'Departamento', type: 'select',
    options: [
      { label: 'TI', value: 'TI' },
      { label: 'RH', value: 'RH' }
    ],
    gridColumns: 4, order: 3 },
  { property: 'active', label: 'Ativo', type: 'boolean', booleanTrue: 'Sim', booleanFalse: 'Não' }
];
```

### Validation rules via metadata:
- required, minLength, maxLength
- min, max (numbers)
- pattern (regex)
- mask (input mask)
- Custom validation via `validate` property

Ask user for: field names, types, validations, grid layout (columns).
```

#### /po-table
Crie em `.claude/skills/po-table/SKILL.md`:
```yaml
---
name: po-table
description: Configurar po-table com colunas, acoes, filtros e paginacao
disable-model-invocation: true
---
```
```markdown
## PO-UI Table Configuration

Generate a po-table component with columns, actions, and service integration.

### Features to configure:
1. **Columns** (PoTableColumn[]) — label, property, type, width, sortable, visible
2. **Actions** (PoTableAction[]) — row actions (edit, delete, custom)
3. **Service API** — REST endpoint for data loading
4. **Pagination** — server-side with TOTVS standard (hasNext, items, remainingRecords)
5. **Filters** — disclaimer filters, advanced search
6. **Selection** — single, multi, none
7. **Height** — fixed or auto
8. **Literals** — custom labels (noData, loadMore, etc)

### Column types:
- string, number, currency, date, dateTime, time
- boolean, subtitle, label, link, icon, color, cellTemplate

### Example:
```typescript
columns: PoTableColumn[] = [
  { property: 'code', label: 'Codigo', width: '100px' },
  { property: 'name', label: 'Nome', sortable: true },
  { property: 'status', label: 'Status', type: 'label', labels: [
    { value: 'active', label: 'Ativo', color: 'color-10' },
    { value: 'inactive', label: 'Inativo', color: 'color-07' }
  ]},
  { property: 'value', label: 'Valor', type: 'currency', format: 'BRL' }
];
```

Ask user for: columns (name/type), row actions, API endpoint, filters needed.
```

#### /po-theme
Crie em `.claude/skills/po-theme/SKILL.md`:
```yaml
---
name: po-theme
description: Configurar tema customizado PO-UI (cores, fontes, branding)
disable-model-invocation: true
---
```
```markdown
## PO-UI Theme Customization

Create or modify a PO-UI custom theme.

### Theme files:
- Base: `node_modules/@po-ui/style/css/po-theme-default.min.css`
- Custom: `src/assets/css/themes/po-theme-[name].css`
- Activation: angular.json styles array or `--theme` flag

### Available base themes:
- po-theme-default (PO-UI padrao)
- po-theme-totvs (TOTVS branding)
- po-theme-fluig (Fluig standards)

### Customization approach:
1. Copy base theme
2. Override CSS custom properties (--color-primary, --color-action, etc)
3. Update angular.json to reference custom theme
4. Test with `ng serve --theme [name]`

### Key CSS variables:
- --color-primary, --color-primary-dark, --color-primary-light
- --color-action, --color-action-hover
- --font-family, --font-size-default
- --color-neutral-dark, --color-neutral-mid, --color-neutral-light

Ask user for: brand colors (primary, secondary), font preference, base theme to extend.
```

### Skills customizadas adicionais

#### /mvc-scaffold
Crie em `.claude/skills/mvc-scaffold/SKILL.md`:
```yaml
---
name: mvc-scaffold
description: Scaffold rotina MVC Protheus (ModelDef, ViewDef, MenuDef)
disable-model-invocation: true
---
```
```markdown
## MVC Scaffold

Generate Protheus MVC routine:
1. MenuDef — operations (Incluir, Alterar, Excluir, Visualizar)
2. ModelDef — SX3 fields, SetRelation, validation blocks
3. ViewDef — FWFormStruct (header) + FWFormGridStruct (items if master-detail)

Ask for: table alias, master-detail (Y/N), fields to include.
```

#### /rest-api
Crie em `.claude/skills/rest-api/SKILL.md`:
```yaml
---
name: rest-api
description: Criar endpoint REST ADVPL/TLPP padrao TOTVS API
disable-model-invocation: true
---
```
```markdown
## REST API Generator (TOTVS Standard)

Generate WSRESTFUL endpoints following api.totvs.com.br patterns.
Methods: GET (list + by ID), POST, PUT, DELETE.
Response: {"hasNext": bool, "items": [], "remainingRecords": int}

Ask for: resource name, table alias, fields, auth required.
```

#### /esql-check
Crie em `.claude/skills/esql-check/SKILL.md`:
```yaml
---
name: esql-check
description: Valida Embedded SQL em codigo ADVPL
---
```
```markdown
## Embedded SQL Validator

Check for:
- Correct BeginSQL/EndSQL syntax
- Proper markers: %Table:%, %XFilial:%, %Exp:%, %NotDel%
- No SELECT * — list columns explicitly
- No string concatenation (SQL injection risk)
- Index usage and pagination
```

#### /prime (inspirado Cole Medin)
Crie em `.claude/skills/prime/SKILL.md`:
```yaml
---
name: prime
description: Carrega contexto do projeto antes de comecar trabalho
---
```
```markdown
## Prime Context

Load project context efficiently:
1. Read CLAUDE.md for project conventions
2. Read recent git log (last 20 commits)
3. Identify key directories and their purposes
4. Note tech stack and verification commands
5. Summarize current state in 5 bullet points

Use this at the START of every session or after /compact.
```

#### /validate (inspirado Cole Medin)
Crie em `.claude/skills/validate/SKILL.md`:
```yaml
---
name: validate
description: Valida implementacao com piramide de 5 camadas
disable-model-invocation: true
---
```
```markdown
## Validation Pyramid

Run all layers in order. Stop on first failure.

1. **Lint + Type Check**
   - Python: `ruff check . && mypy app/`
   - Go: `golangci-lint run && go vet ./...`
   - Angular: `ng build --configuration=production && npx eslint src/`

2. **Unit Tests**
   - Python: `pytest --cov -x`
   - Go: `go test ./... -cover -race`
   - Angular: `ng test --watch=false --code-coverage`

3. **E2E Tests**
   - agent-browser validation of critical flows
   - Or: `npx playwright test`

4. **Code Review**
   - Run /review (automated)
   - Check diff against plan

5. **Security Review**
   - Run security-reviewer agent if touching auth/input/APIs
```

## Workflow Completo

```
NOVO FEATURE:
  /prime → /brainstorm → /plan → TDD → implement → /validate → /review → commit

BUG FIX:
  /prime → /diagnose → TDD (failing test) → fix → /validate → commit

ADVPL:
  /prime → /generate ou /mvc-scaffold → /esql-check → /validate → commit

ANGULAR + PO-UI:
  /prime → /po-crud (scaffold CRUD) → /po-form (ajustar campos) → ng test → /validate → commit

INFRA:
  kubectl get pods → diagnose → fix manifest → kubectl apply --dry-run → apply
```

## CLAUDE.md Templates

| Perfil | Template |
|--------|----------|
| Gestao | `templates/CLAUDE-gestao.md` |
| Dev | `templates/CLAUDE-dev.md` |

Copie o template do seu perfil para a raiz do projeto como `CLAUDE.md` e preencha os campos `[ENTRE COLCHETES]`.

## Referencias

### PO-UI / Angular
- PO-UI docs: https://po-ui.io
- PO-UI GitHub: https://github.com/po-ui/po-angular
- PO-UI npm: https://www.npmjs.com/org/po-ui
- PO-UI CRUD workshop: https://github.com/po-ui/crud-po-ui-workshop
- PO-UI sample app: https://github.com/po-ui/po-sample-conference
- Design system: https://adele.uxpin.com/totvs-portinari-ui

### Protheus / ADVPL
- TDN: https://tdn.totvs.com
- API TOTVS: https://api.totvs.com.br
- DevForum: https://devforum.totvs.com.br
- TLPP Samples: https://github.com/totvs/tlpp-samples

### IDE
- TDS VSCode: `code --install-extension totvs.tds-vscode`
- ProtheusDoc: `code --install-extension AlencarGabriel.protheusdoc-vscode`

### Metodologia
- AI Transformation Workshop (Cole Medin): https://github.com/coleam00/ai-transformation-workshop

## Dicas

- **Context7 sempre**: Consulte docs atualizados ANTES de implementar — training data pode estar stale
- **PO-UI dynamic pages**: Use po-page-dynamic-table/edit/detail para CRUDs — minimo de codigo, maximo de padronizacao
- **PO-UI > HTML custom**: Preferir componentes PO-UI em toda interface; so usar HTML custom quando PO-UI nao tem o componente
- **ng add @po-ui/ng-components**: Instala e configura PO-UI automaticamente (schematics)
- **TDD obrigatorio**: Superpowers enforça RED → GREEN → REFACTOR
- **Agent-browser > Playwright**: Para validacao E2E durante implementacao, agent-browser compartilha contexto
- **Block secrets via hook**: PreToolUse impede editar .env, credentials, lock files, configs de servidor
- **Git log is memory**: Commits descritivos servem de contexto entre sessoes
- **ADVPL → TLPP**: Rotinas novas em TLPP; migrar existentes quando houver manutencao
- **MVC obrigatorio**: Para rotinas Protheus novas, sempre usar ModelDef/ViewDef/MenuDef
- **K8s MCP**: Consulte pods, logs, descreva resources sem sair do Claude
- **Commandify erros**: Quando o Claude erra, transforme a correcao em regra no CLAUDE.md
