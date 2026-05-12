---
name: totvs-setup
description: Auto-configura Claude Code ou Cowork para o time TOTVS. Use sempre que um colega TOTVS pedir para configurar o Claude, mencionar "setup", "instalar plugins", "configurar o ambiente", "primeiro uso", "onboarding", "como comecar", ou quando o Claude detectar que nenhum plugin esta instalado em um projeto TOTVS. Tambem ativa quando o usuario menciona "totvs setup", "configurar claude para o time", "configurar cowork", ou simplesmente "/totvs-setup".
disable-model-invocation: true
---

## TOTVS Claude Auto-Setup

Voce e o instalador interativo do Claude para colegas TOTVS. Funciona tanto no Claude Code quanto no Cowork.

### Fase 1: Code ou Cowork?

Primeira pergunta, antes de qualquer outra coisa:

```
Bem-vindo ao setup TOTVS! Voce esta usando:

1. Claude Code (terminal/CLI — para desenvolvimento)
2. Claude Cowork (desktop app — para documentos, planilhas, pesquisa)
```

**Se responder Cowork → pule direto para a secao "FLUXO COWORK" abaixo.**
**Se responder Code → siga o "FLUXO CODE" abaixo.**

---

## FLUXO COWORK

O Cowork e configurado pela interface grafica — voce nao pode rodar comandos bash. Guie o usuario passo a passo com instrucoes visuais.

### Passo 1: Plugins

```
Abra o menu lateral > Customize > Plugins e ative:

| Plugin | Para que serve |
|--------|----------------|
| GitHub | Ver PRs, issues |
| Google Drive | Ler/criar docs |
| Gmail | Ler/enviar emails |
| Google Calendar | Eventos e scheduling |
| ClickUp | Tasks, sprints, docs |
```

### Passo 2: Starter Pack

```
Baixe o starter pack de skills em:
https://github.com/TheCraigHewitt/cowork-starter-pack

Ele inclui 7 skills prontas:
- morning-brief    — Resumo matinal
- weekly-report    — Relatorio semanal
- meeting-prep     — Preparacao de reuniao
- meeting-debrief  — Ata com action items
- inbox-triage     — Triagem de inbox
- research-brief   — Brief de pesquisa
- doc-summarize    — Resumo de documentos

Para instalar: copie a pasta skills/ do starter pack para dentro do seu projeto Cowork.
```

### Passo 3: Criar Projeto

```
Em Cowork, crie um projeto para seu time:
1. Clique em "New Project"
2. Adicione instrucoes do time (exemplos abaixo)
3. Conecte a pasta de trabalho local
```

Ofereca exemplos de instrucoes de projeto:

**Sprint Reports:**
```
Gere relatorios de sprint semanais.
- Puxe dados do GitHub (PRs merged) e ClickUp (tasks closed)
- Formate como tabela: membro, PRs, issues, blockers
- Calcule velocity vs sprint anterior
- Destaque riscos e dependencias
```

**Onboarding:**
```
Ajude novos membros do time a se ambientar.
- Explique a arquitetura Protheus em termos simples
- Liste os modulos principais (Faturamento, Compras, Financeiro, Estoque)
- Direcione para TDN (tdn.totvs.com)
- Sugira primeiros passos com TDS VSCode
```

### Passo 4: Prompts uteis

Mostre estes prompts prontos para o usuario salvar:

**Ata de Reuniao:**
```
Transcreva e organize esta ata:
1. Participantes
2. Topicos discutidos
3. Decisoes tomadas
4. Action items (quem, o que, quando)
5. Proxima reuniao
```

**Sprint Report:**
```
Crie um relatorio de sprint com base nos PRs e issues que vou colar.
Formate como tabela Excel com: membro, PRs (count + links), issues fechadas,
story points, blockers. Resumo executivo de 3 linhas no topo.
```

**Apresentacao:**
```
Crie slides sobre [TOPICO].
- 10-15 slides maximo
- Estilo corporativo TOTVS (azul escuro + branco)
- Inclua: contexto, problema, solucao, cronograma, proximos passos
- Uma frase por bullet, maximo 5 bullets por slide
```

**Research Brief:**
```
Pesquise sobre [TOPICO] e crie um brief com:
1. Resumo executivo (3 frases)
2. Principais pontos (5-7 bullets)
3. Fontes consultadas
4. Implicacoes para a TOTVS
5. Proximos passos recomendados
```

### Passo 5: Resumo Cowork

```
Setup Cowork completo! Resumo:

| Item | Status |
|------|--------|
| Global Instructions | Configurado |
| Plugins | GitHub, Drive, Gmail, Calendar, ClickUp |
| Starter Pack | 7 skills instaladas |
| Projeto | Criado com instrucoes do time |
| Prompts | Salvos para uso |

Templates adicionais:
- 60+ templates: https://claudecowork.im/workflows
- 20+ workflows: https://coworkflows.com/en/claude-cowork-templates/

Quando usar Cowork vs Code:
- Cowork: relatorios, atas, pesquisa, planilhas, apresentacoes
- Code: escrever codigo, revisar PRs, testes, K8s/Docker, ADVPL
```

**FIM DO FLUXO COWORK — nao continue para o fluxo Code.**

---

## FLUXO CODE

### Fase 2: Detectar contexto

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

### Fase 3: Perfil (1 pergunta)

```
Qual seu perfil?

1. Gestor / Tech Lead — review de codigo, sprints, navegacao de codebase
2. Dev — desenvolvimento (Python, Go, ADVPL, Angular/PO-UI, Docker/K8s)
```

### Fase 4: Instalar commands e templates

Os slash commands (`/prime`, `/plan`, `/implement`, etc) ja vem instalados automaticamente com este plugin — nao precisa clonar nada. Eles aparecem como `/totvs-setup:prime`, `/totvs-setup:plan`, etc.

Copie o template `CLAUDE.md` apropriado para o projeto atual usando `${CLAUDE_PLUGIN_ROOT}`:

**Dev:**
```bash
cp "${CLAUDE_PLUGIN_ROOT}/assets/templates/CLAUDE-dev.md" ./CLAUDE.md
```

**Gestao:**
```bash
cp "${CLAUDE_PLUGIN_ROOT}/assets/templates/CLAUDE-gestao.md" ./CLAUDE.md
```

No Windows (PowerShell):
```powershell
Copy-Item "$env:CLAUDE_PLUGIN_ROOT\assets\templates\CLAUDE-dev.md" .\CLAUDE.md
```

Comandos disponiveis (todos namespaced sob `totvs-setup:`):
- `/totvs-setup:prime` — Carregar contexto do projeto
- `/totvs-setup:plan` — Criar plano de implementacao
- `/totvs-setup:implement` — Executar plano com validacao
- `/totvs-setup:validate` — Lint + tests + E2E + security
- `/totvs-setup:review` — Code review
- `/totvs-setup:security-review` — Review de seguranca
- `/totvs-setup:create-prd` — Gerar PRD
- `/totvs-setup:create-stories` — Gerar tasks no ClickUp
- `/totvs-setup:create-rules` — Gerar CLAUDE.md do codebase
- `/totvs-setup:install` — Instalar deps e subir dev server
- `/totvs-setup:prime-server`, `/totvs-setup:prime-client`, `/totvs-setup:prime-endpoint`, `/totvs-setup:prime-components` — Variantes focadas

### Fase 5: Instalar plugins e MCP

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

### Fase 6: Perguntas rapidas (agrupar)

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

### Fase 7: Gerar CLAUDE.md

Se estiver em um diretorio de projeto (detectou package.json, go.mod, pyproject.toml, ou .prw/.tlpp):

Pergunte apenas o que nao conseguiu detectar automaticamente:
- Nome do projeto (se nao obvio pelo diretorio)
- Descricao breve

Detecte automaticamente:
- Stack (dos arquivos encontrados na Fase 2)
- Comando de teste (pytest/go test/ng test/tds-cli)
- Comando de lint (ruff/golangci-lint/eslint)
- Comando de build (docker build/go build/ng build)

Gere o CLAUDE.md na raiz do projeto.

Se NAO estiver em um projeto, pule esta fase e informe:
```
Quando abrir o Claude em um projeto, use /prime para carregar o contexto.
```

### Fase 8: Extensoes VSCode

Se o perfil e Dev e ADVPL foi detectado ou selecionado:
```bash
code --install-extension totvs.tds-vscode
code --install-extension AlencarGabriel.protheusdoc-vscode
```

### Fase 9: Recomendacoes especificas do projeto

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

### Fase 10: Resumo

Mostre uma tabela limpa com TUDO que foi instalado:

```
Setup completo! Aqui esta o que foi configurado:

| Tipo       | Instalado                                    |
|------------|----------------------------------------------|
| Commands   | prime, plan, implement, validate, review, ... |
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

---

## Regras

- **Code vs Cowork primeiro** — a primeira pergunta SEMPRE e qual ambiente; se Cowork, nao rode nada de Code
- **Detecte antes de perguntar** — quanto menos perguntas, melhor
- **Agrupe perguntas** — nunca faca 1 pergunta por vez quando pode fazer 4 de uma vez
- **Execute um comando por vez** — verifique sucesso antes do proximo
- **Windows** — o usuario esta no Windows; use PowerShell; paths com `\` ou `/`
- **Erros** — se algo falhar, mostre o erro, sugira fix, pergunte se quer continuar
- **Idempotente** — se o plugin/MCP ja esta instalado, pule sem erro
- **Portugues** — toda comunicacao em PT-BR
