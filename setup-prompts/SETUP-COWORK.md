# Setup Claude Cowork — Time TOTVS

Cowork e o Claude para knowledge work (documentos, planilhas, pesquisa, comunicacao).
Para desenvolvimento de codigo, use Claude Code.

## 1. Ativar Cowork (Admin)

1. Abra claude.ai como Owner da organizacao
2. Organization settings > Capabilities
3. Ligue **Cowork** para todos os usuarios

## 2. Configurar Global Instructions

Settings > Cowork > Global Instructions. Cole:

```
Voce e um assistente de produtividade do time TOTVS.

Regras:
- Responda em portugues brasileiro
- Use tom profissional e direto
- Formate saidas como tabelas ou bullet points quando possivel
- Ao criar documentos, use o template padrao TOTVS
- Priorize clareza sobre formalidade

Contexto do time:
- Empresa: TOTVS (maior empresa de tecnologia do Brasil)
- Produto: Protheus ERP, plataformas cloud
- Stack tecnico: Python, Go, ADVPL/TLPP, Angular + PO-UI, Docker, Kubernetes
- Metodologia: Agile/Scrum
```

## 3. Conectar plugins Cowork

No menu lateral > Customize > Plugins:

| Plugin | Para que serve |
|--------|----------------|
| **GitHub** | Ver PRs, issues (read-only) |
| **Google Drive** | Ler/criar docs |
| **Gmail** | Ler/enviar emails |
| **Google Calendar** | Eventos e scheduling |
| **ClickUp** | Tasks, sprints, docs |

## 4. Instalar Starter Pack (skills prontas)

Baixe de: https://github.com/TheCraigHewitt/cowork-starter-pack

Skills incluidas:
- **morning-brief** — Resumo matinal do que precisa de atencao
- **weekly-report** — Relatorio semanal automatico
- **meeting-prep** — Preparacao de reuniao com agenda e contexto
- **meeting-debrief** — Ata de reuniao com action items
- **inbox-triage** — Triagem de inbox (prioridade, acao, delegar)
- **research-brief** — Brief de pesquisa estruturado
- **doc-summarize** — Resumo de documentos longos

## 5. Criar Projeto por Time/Area

1. Cowork > New Project
2. Adicione instrucoes especificas do time:

### Exemplo: Projeto "Sprint Reports"
```
Instrucoes: Gere relatorios de sprint semanais.
- Puxe dados do GitHub (PRs merged) e ClickUp (tasks closed)
- Formate como tabela com colunas: membro, PRs, issues, blockers
- Calcule velocity vs sprint anterior
- Destaque riscos e dependencias
- Salve como .xlsx na pasta do projeto
```

### Exemplo: Projeto "Onboarding"
```
Instrucoes: Ajude novos membros do time a se ambientar.
- Explique a arquitetura Protheus em termos simples
- Liste os modulos principais (Faturamento, Compras, Financeiro, Estoque)
- Direcione para TDN (tdn.totvs.com) para documentacao
- Sugira primeiros passos com o TDS VSCode
```

## 6. Prompts prontos para Cowork

### Gestao de Sprint
```
Crie um relatorio de sprint com base nos PRs e issues que vou colar.
Formate como tabela Excel com: membro, PRs (count + links), issues fechadas,
story points, blockers. Adicione um resumo executivo de 3 linhas no topo.
```

### Ata de Reuniao
```
Transcreva e organize esta ata de reuniao:
1. Participantes
2. Topicos discutidos (bullet points)
3. Decisoes tomadas
4. Action items (quem, o que, quando)
5. Proxima reuniao

[cole a transcricao aqui]
```

### Preparacao de Apresentacao
```
Crie slides para uma apresentacao sobre [TOPICO].
- 10-15 slides maximo
- Estilo corporativo TOTVS (azul escuro + branco)
- Inclua: contexto, problema, solucao, cronograma, proximos passos
- Uma frase por bullet, maximo 5 bullets por slide
```

### Analise de Metricas
```
Analise estes dados de [metricas/vendas/performance]:
1. Identifique tendencias
2. Compare com periodo anterior
3. Destaque anomalias
4. Sugira 3 acoes baseadas nos dados
Formate como relatorio com graficos se possivel.

[cole os dados aqui]
```

### Research Brief
```
Pesquise sobre [TOPICO] e crie um brief com:
1. Resumo executivo (3 frases)
2. Principais pontos (5-7 bullets)
3. Fontes consultadas
4. Implicacoes para a TOTVS
5. Proximos passos recomendados
```

## Templates adicionais

- 60+ templates oficiais: https://claudecowork.im/workflows
- 20+ workflow templates: https://coworkflows.com/en/claude-cowork-templates/

## Quando usar Cowork vs Code

| Tarefa | Ferramenta |
|--------|------------|
| Escrever codigo | **Code** |
| Revisar PR | **Code** |
| Rodar testes | **Code** |
| Gerenciar K8s/Docker | **Code** |
| Desenvolvimento ADVPL | **Code** |
| Relatorios e planilhas | **Cowork** |
| Atas de reuniao | **Cowork** |
| Pesquisa e briefs | **Cowork** |
| Triagem de email/inbox | **Cowork** |
| Preparar apresentacoes | **Cowork** |
| Organizar arquivos | **Cowork** |
