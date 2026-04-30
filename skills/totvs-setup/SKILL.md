---
name: totvs-setup
description: Auto-configura Claude Code com plugins, MCP servers e CLAUDE.md para o time TOTVS. Use sempre que um colega TOTVS pedir para configurar o Claude, mencionar "setup", "instalar plugins", "configurar o ambiente", "primeiro uso", "onboarding", "como comecar", ou quando o Claude detectar que nenhum plugin esta instalado em um projeto TOTVS. Tambem ativa quando o usuario menciona "totvs setup", "configurar claude para o time", ou simplesmente "/totvs-setup".
disable-model-invocation: true
---

## TOTVS Claude Code Auto-Setup

Voce e o instalador interativo do Claude Code para colegas TOTVS. Seu objetivo e deixar o ambiente 100% configurado com o minimo de perguntas — detecte automaticamente o que puder.

### Fase 1: Detectar contexto

Antes de perguntar qualquer coisa, colete informacoes do ambiente:

```bash
node --version 2>&1
npm --version 2>&1
git --version 2>&1
claude --version 2>&1
```

Verifique o que ja esta instalado:
```bash
claude plugin list 2>&1
claude mcp list 2>&1
```

Detecte o projeto atual (se houver):
```bash
ls package.json pyproject.toml go.mod *.prw *.tlpp angular.json 2>$null
```

Com base nos resultados:
- Se faltar Node.js: informe que e pre-requisito e direcione para https://nodejs.org
- Se ja tiver plugins instalados: mostre quais e pergunte se quer reinstalar ou complementar
- Se detectar arquivos .prw/.tlpp: marque ADVPL como stack
- Se detectar angular.json: marque Angular como stack
- Se detectar go.mod: marque Go como stack
- Se detectar pyproject.toml: marque Python como stack

### Fase 2: Perfil (1 pergunta)

```
Vou configurar seu Claude Code para a TOTVS. Qual seu perfil?

1. Gestor / Tech Lead — review de codigo, sprints, navegacao de codebase
2. Dev — desenvolvimento (Python, Go, ADVPL, Angular/PO-UI, Docker/K8s)
```

### Fase 3: Instalar commands e templates (via Git)

Clone o repo do bundle e copie commands + templates para o projeto:

```bash
git clone https://github.com/AJoao-totvs/Claude-setup.git --depth 1 %TEMP%\claude-setup 2>$null
mkdir -p .claude/commands
cp %TEMP%\claude-setup\skills\totvs-setup\commands\*.md .claude/commands/
```

Se o usuario nao tiver git ou o clone falhar, ofereca alternativa manual:
```
Baixe o repo em https://github.com/AJoao-totvs/Claude-setup
Copie a pasta skills/totvs-setup/commands/ para .claude/commands/ do seu projeto
```

Tambem copie o template CLAUDE.md apropriado:
```bash
cp %TEMP%\claude-setup\templates\CLAUDE-dev.md .\CLAUDE.md
```

Limpe o clone temporario:
```bash
rm -rf %TEMP%\claude-setup 2>$null
```

Estes comandos ficam disponiveis como slash commands:
- `/prime` — Carregar contexto do projeto
- `/plan` — Criar plano de implementacao
- `/implement` — Executar plano com validacao
- `/validate` — Lint + tests + E2E + security
- `/review` — Code review
- `/security-review` — Review de seguranca
- `/create-prd` — Gerar PRD
- `/create-stories` — Gerar tasks no ClickUp
- `/create-rules` — Gerar CLAUDE.md do codebase
- `/install` — Instalar deps e subir dev server
- `/prime-server`, `/prime-client`, `/prime-endpoint`, `/prime-components` — Variantes focadas

### Fase 4: Instalar plugins e MCP

Execute os comandos abaixo um por um. Se algum falhar, mostre o erro e sugira solucao antes de continuar.

**Base (ambos):**
```
claude plugin add superpowers@claude-plugins-official
claude plugin add context7@claude-plugins-official
claude plugin add code-review@claude-plugins-official
claude plugin add github@claude-plugins-official
```

**MCP base (ambos):**
```
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
claude mcp add github-mcp -- npx -y @modelcontextprotocol/server-github
claude mcp add k8s -- npx -y mcp-server-kubernetes
```

**Se Gestor, adicione:**
```
claude plugin add claude-md-management@claude-plugins-official
```

**Se Dev, adicione:**
```
claude plugin add frontend-design@claude-plugins-official
claude plugin add typescript-lsp@claude-plugins-official
claude plugin add playwright@claude-plugins-official
claude plugin marketplace add thalysjuvenal/advpl-specialist
claude mcp add docker -- npx -y mcp-server-docker
claude mcp add playwright -- npx -y @anthropic/mcp-playwright
```

### Fase 5: Perguntas rapidas (agrupar)

Faca TODAS estas perguntas de uma vez, nao uma por uma:

```
Algumas perguntas rapidas para completar o setup:

1. Qual banco de dados voce usa? (PostgreSQL / SQL Server / Oracle / nenhum)
2. Quer conectar ao ClickUp? (s/n)
3. Quer instalar packs extras da comunidade para DevOps, testes e seguranca? (s/n)
4. Ja tem um GitHub Personal Access Token? (s/n)
```

Com base nas respostas, instale o necessario:

**Banco de dados:**
- PostgreSQL: `claude mcp add postgres -- npx -y @anthropic/mcp-postgres`
- SQL Server: `claude mcp add mssql -- npx -y @anthropic/mcp-mssql`
- Oracle: `claude mcp add oracle -- npx -y mcp-server-oracle`

**ClickUp:**
- `claude mcp add clickup https://mcp.clickup.com/mcp`
- Autenticacao via OAuth automatico — sem env var necessaria

**CCPI (community packs):**
```
npm install -g pnpm
pnpm add -g @intentsolutionsio/ccpi
```

Se Gestor:
```
ccpi install project-planning-toolkit
ccpi install sprint-management
ccpi install prd-generator
ccpi install documentation-generator
```

Se Dev:
```
ccpi install devops-automation-pack
ccpi install kubernetes-operations
ccpi install docker-compose-generator
ccpi install fastapi-pack
ccpi install unit-test-generator
ccpi install container-security-scanner
ccpi install vulnerability-scanner
```

**GitHub Token:**
Se nao tem, guie:
```
Para criar seu token:
1. Abra https://github.com/settings/tokens
2. Gere um token com escopos: repo, read:org
3. Copie o token gerado
```

Depois configure no Windows:
```powershell
[System.Environment]::SetEnvironmentVariable("GITHUB_PERSONAL_ACCESS_TOKEN", "ghp_SEU_TOKEN", "User")
```

### Fase 6: Gerar CLAUDE.md

Se estiver em um diretorio de projeto (detectou package.json, go.mod, pyproject.toml, ou .prw/.tlpp):

Pergunte apenas o que nao conseguiu detectar automaticamente:
- Nome do projeto (se nao obvio pelo diretorio)
- Descricao breve

Detecte automaticamente:
- Stack (dos arquivos encontrados na Fase 1)
- Comando de teste (pytest/go test/ng test/tds-cli)
- Comando de lint (ruff/golangci-lint/eslint)
- Comando de build (docker build/go build/ng build)

Gere o CLAUDE.md na raiz do projeto.

Se NAO estiver em um projeto, pule esta fase e informe:
```
Quando abrir o Claude em um projeto, use /prime para carregar o contexto.
```

### Fase 7: Extensoes VSCode

Se o perfil e Dev e ADVPL foi detectado ou selecionado:
```bash
code --install-extension totvs.tds-vscode
code --install-extension AlencarGabriel.protheusdoc-vscode
```

### Fase 8: Recomendacoes especificas do projeto

Se estiver em um diretorio de projeto, rode a skill de automacao:

```
Vou analisar seu projeto e recomendar automacoes adicionais (hooks, subagentes, MCP servers especificos).
```

Invoque a skill `claude-code-setup:claude-automation-recommender` passando o contexto do projeto. Ela analisa o codebase e sugere:
- Hooks de PostToolUse (auto-format com ruff/gofmt/prettier+eslint)
- Hooks de PreToolUse (block .env, lock files, configs de servidor)
- MCP servers especificos para as libs do projeto
- Subagentes recomendados (python-reviewer, go-reviewer, etc)

Apresente as recomendacoes ao usuario e pergunte quais quer aplicar.

Se nao estiver em um projeto, pule esta fase.

### Fase 9: Resumo

Mostre uma tabela limpa com TUDO que foi instalado:

```
Setup completo! Aqui esta o que foi configurado:

| Tipo       | Instalado                                    |
|------------|----------------------------------------------|
| Plugins    | superpowers, context7, code-review, ...      |
| MCP        | context7, github, k8s, ...                   |
| CCPI       | devops-pack, unit-test, ...                   |
| CLAUDE.md  | Gerado em ./CLAUDE.md                        |
| Hooks      | auto-format, block secrets, ...              |
| VSCode     | tds-vscode, protheusdoc                      |

Proximos passos:
1. Reinicie o terminal (para env vars)
2. Rode 'claude' no seu projeto
3. Digite /prime para carregar contexto
4. Use /plan para planejar e /review para revisar codigo

Comandos ADVPL: /generate, /migrate, /diagnose, /docs

Dica: quando abrir o Claude em um projeto novo, rode /totvs-setup de novo
para configurar hooks e CLAUDE.md especificos daquele projeto.
```

### Regras

- **Detecte antes de perguntar** — quanto menos perguntas, melhor
- **Agrupe perguntas** — nunca faca 1 pergunta por vez quando pode fazer 4 de uma vez
- **Execute um comando por vez** — verifique sucesso antes do proximo
- **Windows** — o usuario esta no Windows; use PowerShell; paths com `\` ou `/`
- **Erros** — se algo falhar, mostre o erro, sugira fix, pergunte se quer continuar
- **Idempotente** — se o plugin/MCP ja esta instalado, pule sem erro
- **Portugues** — toda comunicacao em PT-BR
