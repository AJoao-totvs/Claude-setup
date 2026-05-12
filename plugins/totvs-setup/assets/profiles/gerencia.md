# Perfil: Gerencia

Setup para tech leads, gestores e coordenadores. Foco em navegar codebases, revisar PRs, acompanhar sprints e comunicar progresso.

## Plugins

| Plugin | Comando | Para que serve |
|--------|---------|----------------|
| superpowers | `claude plugin add superpowers@claude-plugins-official` | Workflow estruturado (brainstorm, plan, review) |
| context7 | `claude plugin add context7@claude-plugins-official` | Docs atualizados de qualquer lib/framework |
| code-review | `claude plugin add code-review@claude-plugins-official` | Review automatico (Critical/High/Medium/Nit) |
| github | `claude plugin add github@claude-plugins-official` | PRs, issues, code search |
| claude-md-management | `claude plugin add claude-md-management@claude-plugins-official` | Gerar e manter CLAUDE.md do projeto |

## MCP Servers

### GitHub (obrigatorio)
```bash
claude mcp add github-mcp -- npx -y @modelcontextprotocol/server-github
```
Requer: `GITHUB_PERSONAL_ACCESS_TOKEN` no env.

### Kubernetes (visibilidade de infra)
```bash
claude mcp add k8s -- npx -y mcp-server-kubernetes
```
Usa kubeconfig local. Permite ver pods, logs, status de deploys sem abrir terminal.

### ClickUp
```bash
claude mcp add clickup https://mcp.clickup.com/mcp
```
Autenticacao via OAuth automatico — sem env var necessaria.

### Notion (se usado para docs)
```bash
claude mcp add notion -- npx -y @notionhq/mcp-server
```
Requer: `NOTION_API_KEY` no env.

### Context7
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```

## Skills Customizadas

### /sprint-report
Crie em `.claude/skills/sprint-report/SKILL.md`:
```yaml
---
name: sprint-report
description: Gera relatorio de sprint com PRs merged, issues closed, e metricas
disable-model-invocation: true
---
```
```markdown
## Sprint Report

1. Query GitHub MCP: PRs merged this sprint
2. Query ClickUp MCP: issues completed
3. Summarize by team member and area
4. Output markdown table:
   - PRs merged (count + links)
   - Issues resolved
   - Blockers identified
   - Velocity vs previous sprint
```

### /pr-standards
Crie em `.claude/skills/pr-standards/SKILL.md`:
```yaml
---
name: pr-standards
description: Checklist padrao TOTVS para review de PRs
disable-model-invocation: true
---
```
```markdown
## PR Review Checklist

- [ ] Testes adicionados/atualizados
- [ ] Sem secrets hardcoded
- [ ] Error handling cobre edge cases
- [ ] Breaking changes documentados
- [ ] CLAUDE.md atualizado se arquitetura mudou
- [ ] Performance de queries SQL avaliada
- [ ] Go: `go vet` e `golangci-lint` passam
- [ ] Python: `ruff check` e `mypy` passam
- [ ] ADVPL: markers SQL corretos, MVC se rotina nova
```

### /create-prd (inspirado no Cole Medin)
Crie em `.claude/skills/create-prd/SKILL.md`:
```yaml
---
name: create-prd
description: Cria Product Requirements Document a partir de descricao informal
disable-model-invocation: true
---
```
```markdown
## PRD Generator

Transform informal feature description into structured PRD:

1. **Problem Statement**: What problem does this solve?
2. **User Stories**: As a [role], I want [action], so that [benefit]
3. **Requirements**: Functional + Non-functional
4. **Technical Constraints**: Stack, integrations, performance
5. **Success Metrics**: How do we measure success?
6. **Out of Scope**: What this does NOT include
7. **Acceptance Criteria**: Testable conditions for done

Output as markdown. Ask clarifying questions before generating.
```

## Workflow

```
1. Entender codebase      → Plan Mode (Shift+Tab) — read-only, sem risco
2. Criar PRD              → /create-prd
3. Gerar stories          → claude "break this PRD into ClickUp tasks"
4. Revisar PR             → /review ou claude review
5. Sprint report          → /sprint-report
6. Documentar decisao     → claude "create an ADR for [decision]"
7. Explorar modulo        → claude "trace data flow from API to DB for [feature]"
```

## Dicas

- **Plan Mode** (`Shift+Tab`): Explora sem editar — seguro para navegar codigo desconhecido
- **Agent Teams**: Spawne subagentes para review paralelo de multiplos PRs
- **CLAUDE.md como contrato de time**: Defina module boundaries, commands de verificacao, padroes de qualidade
- **REVIEW.md**: Crie na raiz do projeto com criterios de review do time
- **Git log is memory**: Commits descritivos servem de memoria pro Claude entre sessoes
