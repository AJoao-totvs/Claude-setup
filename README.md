# TOTVS Claude Setup — Marketplace

Marketplace interno do time MIT-IA para o **Claude Code**. Instale skills e plugins proprietarios da TOTVS direto via CLI, sem copiar pastas manualmente.

## Plugins disponiveis

| Plugin | O que faz | Comando para invocar |
|---|---|---|
| `totvs-setup` | Onboarding interativo do Claude Code para devs e gestores (instala superpowers, context7, code-review, github, ADVPL specialist, MCPs e gera CLAUDE.md) | `/totvs-setup:totvs-setup` |
| `totvs-rdp` | Conexao RDP automatizada ao `server-iqs-saopaulo001` via OCI Bastion (two-hop SSH + cliente RDP nativo com configuracao de pico) | `/totvs-rdp:connect` ou pedir "conectar no servidor TOTVS" |

## Instalacao (uma vez por dev)

### 1. Adicione o marketplace

```bash
claude plugin marketplace add AJoao-totvs/Claude-setup
```

Isso pede confirmacao da fonte na primeira vez. Depois, todas as atualizacoes vem automaticas.

### 2. Instale os plugins que precisar

```bash
# Onboarding completo (gestor ou dev)
claude plugin install totvs-setup@totvs-claude-setup

# Conexao RDP ao server-iqs-saopaulo001
claude plugin install totvs-rdp@totvs-claude-setup
```

Use `--scope user` (default) para deixar disponivel em todas as sessoes ou `--scope project` para limitar ao projeto atual.

### 3. Use

- **`totvs-setup`**: rode `/totvs-setup:totvs-setup` em uma nova sessao do Claude Code. Ele faz onboarding interativo (gestor ou dev), instala os plugins recomendados, gera `CLAUDE.md`.
- **`totvs-rdp`**: rode `/totvs-rdp:connect` ou simplesmente peca "conectar no servidor TOTVS" em qualquer sessao. A skill pergunta OCID, chaves SSH, e orquestra os dois tuneis + lanca o cliente RDP nativo.

## Pre-requisitos

### Para `totvs-setup`
- Claude Code instalado
- Acesso ao GitHub (para `claude plugin add ...`)
- `pnpm` (para os comandos `ccpi` que ele invoca)

### Para `totvs-rdp`
- Cliente SSH no PATH (`ssh`)
- Cliente RDP nativo:
  - **Windows**: `mstsc` (built-in)
  - **Linux**: `xfreerdp3` (preferencial) ou `xfreerdp` ou `remmina`
  - **macOS**: Microsoft Remote Desktop (App Store)
- Chave do bastion (`.key`) e chave do servidor (arquivos diferentes — solicite a infra)
- OCID da sessao do bastion (TTL ~3h, solicite a infra a cada conexao)

## Atualizar

```bash
claude plugin marketplace update totvs-claude-setup
claude plugin upgrade totvs-setup@totvs-claude-setup
claude plugin upgrade totvs-rdp@totvs-claude-setup
```

## Desinstalar

```bash
claude plugin uninstall totvs-setup
claude plugin uninstall totvs-rdp
claude plugin marketplace remove totvs-claude-setup
```

## Estrutura do repo

```
Claude-setup/
├── .claude-plugin/
│   └── marketplace.json        # manifesto do marketplace
├── plugins/
│   ├── totvs-setup/            # plugin de onboarding
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── skills/
│   │   │   └── totvs-setup/
│   │   │       └── SKILL.md
│   │   ├── commands/           # /totvs-setup:prime, /plan, /implement, etc
│   │   └── assets/             # profiles, templates, mcp-configs, setup-prompts
│   └── totvs-rdp/              # plugin de conexao RDP
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── connect/
│               ├── SKILL.md
│               ├── scripts/    # open-tunnels.sh, open-tunnels.ps1
│               └── templates/  # totvs.rdp.template
├── SKILLS-CATALOG.md           # catalogo de plugins externos recomendados
└── CHANGELOG.md
```

## Catalogo de plugins externos

Ver [`SKILLS-CATALOG.md`](./SKILLS-CATALOG.md) para a lista curada de plugins publicos (Anthropic + community + TonsOfSkills) que o time recomenda.

## Contribuir

1. Clone: `git clone git@github.com:AJoao-totvs/Claude-setup.git`
2. Crie uma branch: `git checkout -b feat/<seu-plugin>`
3. Adicione o plugin sob `plugins/<seu-plugin>/` seguindo a estrutura existente
4. Registre o plugin em `.claude-plugin/marketplace.json`
5. Teste localmente: `claude plugin marketplace add ~/path/para/Claude-setup`
6. Abra um PR descrevendo o uso e o teste end-to-end

## Suporte

Time MIT-IA — Augusto Zanini (`augusto.zanini@totvs.com.br`).
