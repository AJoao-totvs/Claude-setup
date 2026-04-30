# Project: [NOME DO PROJETO]

## Overview
[Descricao breve — 2-3 frases]

## Tech Stack
- **Backend**: Python 3.12+, Go 1.22+
- **Frontend**: Angular 21+ com PO-UI (@po-ui/ng-components, @po-ui/ng-templates)
- **ERP**: TOTVS Protheus 12.1.2410+, ADVPL/TLPP
- **Database**: [PostgreSQL / SQL Server]
- **Cache**: [Redis]
- **Infrastructure**: Docker, Kubernetes
- **CI/CD**: [GitHub Actions / GitLab CI]

## Key Directories
```
# Backend Python
app/
  api/              → Endpoints/routers (FastAPI/Django)
  models/           → Data models / ORM
  services/         → Business logic
  repositories/     → Data access layer

# Backend Go
cmd/                → Entrypoints (main.go)
internal/           → Packages privados
pkg/                → Packages publicos

# Frontend Angular + PO-UI
src/
  app/
    shared/         → PO-UI shared modules, services, interceptors
    features/       → Feature modules (lazy loaded)
      [feature]/
        [feature].component.ts
        [feature].module.ts
        [feature].service.ts
    core/           → Guards, interceptors, auth
  assets/           → Imagens, i18n
  environments/     → Environment configs

# Protheus
protheus/
  rotinas/          → Rotinas MVC e funcionais (.prw, .tlpp)
  pontos_entrada/   → Entry points (PE_*.prw)
  web_services/     → REST/SOAP endpoints
  includes/         → Headers (.ch)

# Infra
deploy/             → Dockerfiles, k8s manifests, Helm charts
migrations/         → Database migrations (Alembic / goose)
scripts/            → Automacao
tests/              → Testes
```

## Verification Commands
```bash
# Python
pytest --cov=app --cov-report=term-missing
ruff check . && ruff format --check .
mypy app/

# Go
go test ./... -cover -race
golangci-lint run
go vet ./...

# Angular + PO-UI
ng test --watch=false --code-coverage
ng build --configuration=production
npx eslint src/

# ADVPL
tds-cli compile --server=[server] --env=[env] --program=[source.prw]
tds-cli rpo-check --server=[server] --env=[env]

# Docker / Kubernetes
docker build -t [service-name] .
docker compose up -d
kubectl apply --dry-run=client -f deploy/
kubectl get pods -n [namespace]
```

---

## Python Conventions
- **Framework**: [FastAPI / Django]
- **ORM**: [SQLAlchemy / Django ORM]
- **Migrations**: [Alembic / Django migrations]
- **Formatting**: ruff format
- **Linting**: ruff check
- **Type checking**: mypy
- **Testing**: pytest + pytest-cov
- **Patterns**: Repository, Service Layer, Dependency Injection

## Go Conventions
- **Framework**: [Gin / Echo / net/http / gRPC]
- **ORM**: [GORM / sqlx / raw SQL]
- **Migrations**: [goose / migrate]
- **Formatting**: gofmt
- **Linting**: golangci-lint
- **Testing**: go test -race -cover
- **Patterns**: Clean Architecture, interfaces for DI

## Angular + PO-UI Conventions
- **PO-UI version**: 21.x (@po-ui/ng-components, @po-ui/ng-templates)
- **Angular version**: 21.x
- **Theme**: @po-ui/style (po-theme-totvs)
- **Components**: Preferir PO-UI sobre HTML custom em TODA interface
- **Dynamic Pages**: Usar po-page-dynamic-table, po-page-dynamic-edit, po-page-dynamic-detail para CRUDs
- **Forms**: po-dynamic-form com metadata para formularios padrao
- **Tables**: po-table com po-page-dynamic-table para listagens
- **Module structure**: Feature modules lazy-loaded
- **Services**: HttpClient para REST APIs, subscribe para handling
- **Testing**: Karma + Jasmine (default Angular)

### PO-UI Packages
```
@po-ui/ng-components    → Componentes core (po-table, po-input, po-combo, etc)
@po-ui/ng-templates     → Templates de pagina (po-page-dynamic-*)
@po-ui/ng-code-editor   → Editor de codigo
@po-ui/ng-storage       → Storage local (IndexedDB/LocalStorage)
@po-ui/ng-sync          → Sync local-servidor
@po-ui/ng-schematics    → Scaffolding via ng generate
@po-ui/style            → Tema e CSS
```

### PO-UI Dynamic Components
```typescript
// CRUD com metadata — minimo de codigo
// po-page-dynamic-table: listagem automatica
// po-page-dynamic-edit: formulario de criacao/edicao
// po-page-dynamic-detail: visualizacao read-only

// Exemplo: definir campos via metadata
const fields: Array<PoDynamicFormField> = [
  { property: 'name', label: 'Nome', required: true, gridColumns: 6 },
  { property: 'email', label: 'E-mail', type: 'email', gridColumns: 6 },
  { property: 'status', label: 'Status', type: 'select', options: [...] }
];
```

## ADVPL / TLPP Conventions
- **Nomenclatura**: prefixo `Z` para customizados (ex: ZFATA001.prw)
- **Entry points**: PE_[NomeRotina].prw
- **REST services**: ZAPI_[Recurso].prw
- **MVC obrigatorio** para rotinas novas (MenuDef, ModelDef, ViewDef)
- **TLPP preferido** para rotinas novas (strong typing, namespaces)
- **Embedded SQL**: SEMPRE usar %Table:%, %XFilial:%, %NotDel%
- **NUNCA** concatenar strings em queries SQL
- **API padrao TOTVS**: response `{"hasNext", "items", "remainingRecords"}`

### Protheus Tables Reference
| Alias | Descricao | Modulo |
|-------|-----------|--------|
| SA1 | Clientes | Faturamento |
| SA2 | Fornecedores | Compras |
| SC5 | Pedidos de Venda | Faturamento |
| SC6 | Itens de Pedido | Faturamento |
| SD1 | Itens NF Entrada | Compras |
| SD2 | Itens NF Saida | Faturamento |
| SE1 | Contas a Receber | Financeiro |
| SE2 | Contas a Pagar | Financeiro |
| SB1 | Produtos | Estoque |
| SB2 | Saldos Estoque | Estoque |

## Docker & Kubernetes
- Multi-stage builds para imagens menores
- Health checks: `/health` e `/ready`
- Resource limits definidos em manifests
- Secrets via Kubernetes Secrets ou external secret operator
- Namespaces por ambiente: dev, staging, prod

## Security
- Nunca hardcode secrets — env vars ou k8s secrets
- Validar todo input (Pydantic, Go validator, Angular reactive forms)
- Rate limiting em endpoints publicos
- Auth: [JWT / OAuth2 / API keys / Protheus Basic Auth]
- SQL injection: queries parametrizadas (Python/Go), markers (ADVPL)

## References
- PO-UI: https://po-ui.io
- PO-UI GitHub: https://github.com/po-ui/po-angular
- TDN: https://tdn.totvs.com
- API TOTVS: https://api.totvs.com.br
- DevForum: https://devforum.totvs.com.br
- TLPP Samples: https://github.com/totvs/tlpp-samples
