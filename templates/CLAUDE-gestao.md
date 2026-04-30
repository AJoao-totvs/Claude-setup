# Project: [NOME DO PROJETO]

## Overview
[Descricao breve — 2-3 frases]

## Tech Stack
- **Backend**: Python 3.12+, Go 1.22+, ADVPL/TLPP
- **Frontend**: Angular 21+ com PO-UI
- **ERP**: TOTVS Protheus 12.1.2410+
- **Database**: [PostgreSQL / SQL Server]
- **Infrastructure**: Docker, Kubernetes
- **CI/CD**: [GitHub Actions / GitLab CI / Jenkins]
- **Issue Tracking**: ClickUp

## Architecture
[Descreva a arquitetura: monolito, microservicos, modulos Protheus, etc]

### Module Boundaries
| Module | Owner | Path | Stack |
|--------|-------|------|-------|
| [modulo-1] | [time/pessoa] | `src/modulo-1/` | [Python/Go/ADVPL/Angular] |
| [modulo-2] | [time/pessoa] | `src/modulo-2/` | [Python/Go/ADVPL/Angular] |

## Key Directories
```
src/              → Source principal
  backend/        → Python/Go services
  frontend/       → Angular + PO-UI
  protheus/       → Rotinas ADVPL/TLPP
tests/            → Testes (pytest, go test, Karma, advpl-unit-test)
deploy/           → Dockerfiles, k8s manifests, Helm charts
docs/             → Documentacao tecnica, ADRs
```

## Verification Commands
```bash
# Python
pytest --cov -x
ruff check . && ruff format --check .

# Go
go test ./... -cover -race
golangci-lint run

# Angular / PO-UI
ng test --watch=false
ng build --configuration=production

# ADVPL
tds-cli compile --server=[server] --env=[env] --program=[source.prw]

# Docker / K8s
docker build -t [service] .
kubectl apply --dry-run=client -f deploy/
```

## Review Standards
- Tests obrigatorios para toda feature/bugfix
- Security review para auth, input handling, APIs
- Performance review para queries SQL e endpoints
- No hardcoded secrets — env vars ou k8s secrets
- ADVPL: MVC obrigatorio para rotinas novas
- Angular: PO-UI components preferidos sobre custom HTML
- Go: `go vet` e `golangci-lint` passam
- Python: `ruff check` e `mypy` passam

## Contacts
- **Tech Lead**: [nome]
- **DevOps**: [nome]
- **Ticket Prefix**: [PROJ-]
