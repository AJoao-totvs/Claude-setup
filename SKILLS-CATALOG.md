# Catalogo de Skills & Plugins — TOTVS Claude Bundle

Lista curada de skills prontas para download, organizadas por categoria.
Funciona no **Claude Code** (CLI) e indicacoes para **Claude Cowork** (desktop).

---

## Como instalar

```bash
# Plugins oficiais Anthropic
claude plugin add NOME@claude-plugins-official

# Plugins community marketplace (GitHub)
claude plugin marketplace add USUARIO/REPO

# CCPI — gerenciador de plugins TonsOfSkills (2800+ skills)
pnpm add -g @intentsolutionsio/ccpi
ccpi install NOME-DO-PLUGIN
ccpi search TERMO
```

---

## 1. BASE OBRIGATORIA (todos os perfis)

| Plugin | Comando | O que faz |
|--------|---------|-----------|
| **Superpowers** | `claude plugin add superpowers@claude-plugins-official` | PIV Loop, TDD, brainstorm, debugging sistematico, 14 skills de workflow |
| **Context7** | `claude plugin add context7@claude-plugins-official` | Docs atualizados de qualquer lib via MCP |
| **Code Review** | `claude plugin add code-review@claude-plugins-official` | Review automatico multi-agente |
| **GitHub** | `claude plugin add github@claude-plugins-official` | PRs, issues, code search |

---

## 2. ANGULAR / FRONTEND

| Plugin | Comando | O que faz |
|--------|---------|-----------|
| **Frontend Design** | `claude plugin add frontend-design@claude-plugins-official` | UI production-grade, design system patterns |
| **Playwright** | `claude plugin add playwright@claude-plugins-official` | Browser automation, E2E testing |
| **TypeScript LSP** | `claude plugin add typescript-lsp@claude-plugins-official` | Type checking, refactoring, code navigation em tempo real |
| **Figma** | `claude plugin add figma@claude-plugins-official` | Design-to-code via Figma MCP |
| **UI Design Toolkit** | `ccpi install ui-design-toolkit` | Component design & responsive UI |

---

## 3. PYTHON

| Plugin | Comando | O que faz |
|--------|---------|-----------|
| **FastAPI Pack** | `ccpi install fastapi-pack` | 30 skills para FastAPI (endpoints, auth, DI, async) |
| **Django Expert** | `ccpi install django-expert-pack` | Django ORM, DRF, models, serializers |
| **SQLAlchemy Toolkit** | `ccpi install sqlalchemy-toolkit` | SQLAlchemy 2.0 patterns |

Nativo (ja vem com Claude Code): `python-reviewer`, `tdd-guide`

---

## 4. GO

| Plugin | Comando | O que faz |
|--------|---------|-----------|
| **Golang Pack** | `ccpi install golang-pack` | Go backend patterns |

Nativo: `go-reviewer`, `go-build-resolver`

---

## 5. ADVPL / PROTHEUS

| Plugin | Comando | O que faz |
|--------|---------|-----------|
| **ADVPL Specialist** | `claude plugin marketplace add thalysjuvenal/advpl-specialist` | 4 agentes (code-gen, migrator, debugger, docs) + 4 comandos (/generate, /migrate, /diagnose, /docs) |

GitHub: https://github.com/thalysjuvenal/advpl-specialist

---

## 6. DEVOPS / KUBERNETES / DOCKER

| Plugin | Comando | O que faz |
|--------|---------|-----------|
| **DevOps Automation Pack** | `ccpi install devops-automation-pack` | K8s, Docker, CI/CD, monitoring |
| **Kubernetes Operations** | `ccpi install kubernetes-operations` | K8s deployment skills |
| **Docker Compose Generator** | `ccpi install docker-compose-generator` | Multi-container Docker configs |
| **Helm Chart Generator** | `ccpi install helm-chart-generator` | Gerar Helm charts |
| **CI/CD Pipeline Builder** | `ccpi install ci-cd-pipeline-builder` | GitHub Actions, GitLab CI, Jenkins |
| **GitOps Workflow** | `ccpi install gitops-workflow-builder` | ArgoCD & Flux workflows |
| **Terraform IaC** | `ccpi install terraform-iac-generator` | Terraform config generation |
| **Monitoring Stack** | `ccpi install monitoring-stack-deployer` | Prometheus, Grafana, Datadog |

---

## 7. SEGURANCA

| Plugin | Comando | O que faz |
|--------|---------|-----------|
| **Container Security Scanner** | `ccpi install container-security-scanner` | Trivy, Snyk — scan vulnerabilidades |
| **Vulnerability Scanner** | `ccpi install vulnerability-scanner` | OWASP Top 10, SQL injection, XSS |
| **API Security Testing** | `ccpi install api-security-testing` | Audit de seguranca de APIs |
| **Encryption Toolkit** | `ccpi install encryption-toolkit` | Criptografia best practices |

Nativo: `security-reviewer` (agent)

---

## 8. TESTES

| Plugin | Comando | O que faz |
|--------|---------|-----------|
| **Unit Test Generator** | `ccpi install unit-test-generator` | pytest, jest, vitest, go test |
| **Integration Test Runner** | `ccpi install integration-test-runner` | Testes de integracao |
| **E2E Test Builder** | `ccpi install e2e-test-builder` | Scaffold testes E2E |
| **Load Test Generator** | `ccpi install load-test-generator` | Performance & load testing |

Nativo: `tdd-guide`, `e2e-runner`, `test-coverage`

---

## 9. PLANEJAMENTO & GESTAO

| Plugin | Comando | O que faz |
|--------|---------|-----------|
| **Project Planning Toolkit** | `ccpi install project-planning-toolkit` | Decomposicao de projetos |
| **Sprint Management** | `ccpi install sprint-management` | Agile sprint workflows |
| **PRD Generator** | `ccpi install prd-generator` | Gerar PRD a partir de requisitos |
| **Documentation Generator** | `ccpi install documentation-generator` | Docs automaticos do codigo |
| **Linear** | `claude plugin add linear@claude-plugins-official` | Issue tracking Linear |
| **Asana** | `claude plugin add asana@claude-plugins-official` | Task tracking Asana |
| **GitLab** | `claude plugin add gitlab@claude-plugins-official` | GitLab workflows |
| **Claude MD Management** | `claude plugin add claude-md-management@claude-plugins-official` | Gerar e manter CLAUDE.md |

---

## 10. BANCO DE DADOS

| Plugin | Comando | O que faz |
|--------|---------|-----------|
| **MSSQL** | `claude mcp add mssql -- npx -y @anthropic/mcp-mssql` | SQL Server integration |
| **Postgres Schema Designer** | `ccpi install postgres-schema-designer` | Design de schema PostgreSQL |
| **Oracle** | `claude mcp add oracle -- npx -y mcp-server-oracle` | Oracle DB integration |
| **Database Migration Tool** | `ccpi install database-migration-tool` | Migration management |

Nativo: `database-reviewer` (agent)

---

## 11. OBSERVABILIDADE

| Plugin | Comando | O que faz |
|--------|---------|-----------|
| **Sentry Pack** | `ccpi install sentry-pack` | Error tracking & monitoring |
| **Datadog Integration** | `ccpi install datadog-integration` | Metricas & monitoring |

---

## 12. REPOSITORIOS COM SKILLS PRONTAS (bulk download)

| Repo | Tamanho | Comando | URL |
|------|---------|---------|-----|
| **Antigravity Awesome Skills** | 1400+ skills | `git clone` + copiar para `.claude/skills/` | https://github.com/sickn33/antigravity-awesome-skills |
| **Awesome Agent Skills** | 1000+ skills | `git clone` + copiar | https://github.com/VoltAgent/awesome-agent-skills |
| **Awesome Claude Code Toolkit** | 135 agents, 400K+ skills | Curated list | https://github.com/rohitg00/awesome-claude-code-toolkit |
| **Awesome Claude Skills** | 232+ skills | Engineering, marketing, product | https://github.com/alirezarezvani/claude-skills |
| **TonsOfSkills** | 423 plugins, 2849 skills | Via `ccpi` | https://tonsofskills.com |

---

## CLAUDE COWORK — O que funciona

Cowork e para **knowledge work** (documentos, planilhas, pesquisa), nao dev. Skills de Code NAO rodam no Cowork.

### Setup Cowork para o time

1. **Admin**: Organization settings > Capabilities > Ligar Cowork
2. **Global instructions**: Settings > Cowork > Global instructions
3. **Projects**: Agrupar tarefas com instrucoes, memoria, pastas proprias

### Plugins que funcionam no Cowork

| Plugin | O que faz |
|--------|-----------|
| Gmail | Ler/enviar emails |
| Google Drive | Ler/criar docs |
| Google Calendar | Eventos e scheduling |
| GitHub | PRs e issues (leitura) |
| ClickUp | Tasks, sprints, docs |
| ClickUp | Tasks e docs (via ClickUp MCP oficial) |
| Context7 | Docs de libs |

### Starter Pack para Cowork

**Repo**: https://github.com/TheCraigHewitt/cowork-starter-pack

Inclui 7 skills prontas:
- `morning-brief` — resumo matinal
- `weekly-report` — relatorio semanal
- `meeting-prep` — preparacao de reuniao
- `meeting-debrief` — ata de reuniao
- `inbox-triage` — triagem de inbox
- `research-brief` — brief de pesquisa
- `doc-summarize` — resumo de documentos

**Instalar**: Copiar pasta `skills/` para dentro do projeto Cowork.

### Prompts prontos para Cowork

| Fonte | URL |
|-------|-----|
| Templates oficiais (60+) | https://claudecowork.im/workflows |
| Workflow templates (20+) | https://coworkflows.com/en/claude-cowork-templates/ |

---

## RECOMENDACAO POR PERFIL TOTVS

### Gestor / Tech Lead

**Code**:
```bash
claude plugin add superpowers@claude-plugins-official
claude plugin add context7@claude-plugins-official
claude plugin add code-review@claude-plugins-official
claude plugin add github@claude-plugins-official
claude plugin add claude-md-management@claude-plugins-official
ccpi install project-planning-toolkit
ccpi install sprint-management
ccpi install prd-generator
```

**Cowork**: Instalar starter-pack + plugins Gmail, ClickUp

### Dev (Python + Go + Angular/PO-UI + ADVPL + Docker/K8s)

**Code**:
```bash
# Base
claude plugin add superpowers@claude-plugins-official
claude plugin add context7@claude-plugins-official
claude plugin add code-review@claude-plugins-official
claude plugin add github@claude-plugins-official

# Frontend
claude plugin add frontend-design@claude-plugins-official
claude plugin add typescript-lsp@claude-plugins-official
claude plugin add playwright@claude-plugins-official

# ADVPL
claude plugin marketplace add thalysjuvenal/advpl-specialist

# DevOps
ccpi install devops-automation-pack
ccpi install kubernetes-operations
ccpi install docker-compose-generator

# Python
ccpi install fastapi-pack

# Testes
ccpi install unit-test-generator

# Seguranca
ccpi install container-security-scanner
ccpi install vulnerability-scanner
```

**Cowork**: Plugins GitHub + ClickUp + starter-pack para weekly reports
