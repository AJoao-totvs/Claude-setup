# TOTVS Claude Code Jumpstart Bundle

Kit de onboarding do Claude Code para o time TOTVS.

## Como usar

1. Copie a pasta `skills/totvs-setup/` para `~/.claude/skills/` (ou `.claude/skills/` do projeto)
2. Abra o Claude Code e digite:
   ```
   /totvs-setup
   ```
3. O Claude pergunta seu perfil (gestor ou dev) e instala tudo automaticamente

Nao precisa de scripts, terminal, ou copiar comandos. O Claude faz tudo.

## O que o `/totvs-setup` instala

### Base (todos)
- Superpowers (PIV Loop, TDD, brainstorm)
- Context7 (docs atualizados)
- Code Review (review automatico)
- GitHub (PRs, issues)

### Gestor (adicional)
- Claude MD Management
- MCP: GitHub, Kubernetes
- CCPI: Project Planning, Sprint Management, PRD Generator

### Dev (adicional)
- Frontend Design, TypeScript LSP, Playwright
- ADVPL Specialist (Protheus: /generate, /migrate, /diagnose, /docs)
- MCP: GitHub, Kubernetes, Docker, Playwright
- CCPI: DevOps Pack, K8s Ops, FastAPI, Unit Tests, Security Scanner
- Banco de dados (pergunta qual)
- Gera CLAUDE.md do projeto automaticamente

## Arquivos do bundle

```
totvs-claude-bundle/
├── README.md                  ← Voce esta aqui
├── SKILLS-CATALOG.md          ← Catalogo completo de skills para download
├── skills/
│   └── totvs-setup/
│       └── SKILL.md           ← Skill de auto-setup (copiar para .claude/skills/)
├── profiles/
│   ├── gerencia.md            ← Guia detalhado: Gestores
│   └── dev.md                 ← Guia detalhado: Devs
├── templates/
│   ├── CLAUDE-gestao.md       ← Template CLAUDE.md para gestores
│   └── CLAUDE-dev.md          ← Template CLAUDE.md para devs
├── setup-prompts/
│   └── SETUP-COWORK.md        ← Setup do Claude Cowork (desktop)
└── mcp-configs/
    ├── gerencia.json          ← .mcp.json referencia
    └── dev.json               ← .mcp.json referencia
```

## Claude Cowork

Para quem usa Cowork (knowledge work, nao dev), veja `setup-prompts/SETUP-COWORK.md`.

## Catalogo de Skills

Veja `SKILLS-CATALOG.md` para a lista completa de 400+ plugins e skills disponiveis para download.

## Duvidas

Time MIT-IA (Augusto).
