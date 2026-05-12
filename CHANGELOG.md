# Changelog

## [Unreleased] — feat: marketplace format + totvs-rdp plugin

### Adicionado
- **Formato de marketplace** (`.claude-plugin/marketplace.json`) — repo agora eh um marketplace Claude Code padrao, instalavel via `claude plugin marketplace add AJoao-totvs/Claude-setup`.
- **Plugin `totvs-rdp`** (`/totvs-rdp:connect`) — orquestra two-hop SSH via OCI Bastion + lanca cliente RDP nativo com configuracao de pico (32 bpp, LAN, H.264). Suporte Windows / Linux / macOS. Skill construida via TDD (RED/GREEN/REFACTOR) com cenarios de pressao validados.

### Mudado
- **`totvs-setup`** virou plugin formal (`plugins/totvs-setup/`) com `plugin.json`. Slash commands agora sao namespaced sob `totvs-setup:` (ex: `/totvs-setup:prime` em vez de `/prime`).
- **Templates, profiles, mcp-configs, setup-prompts** movidos para `plugins/totvs-setup/assets/`. SKILL.md atualizada para usar `${CLAUDE_PLUGIN_ROOT}/assets/...` em vez de `git clone` do repo.

### Removido
- Necessidade de copiar manualmente `skills/totvs-setup/` para `~/.claude/skills/`. Agora basta `claude plugin install totvs-setup@totvs-claude-setup`.

### Migracao para devs que ja usavam o bundle antigo

Quem ja tinha copiado a pasta `skills/totvs-setup/` manualmente:

```bash
# Remover instalacao antiga
rm -rf ~/.claude/skills/totvs-setup

# Instalar via marketplace
claude plugin marketplace add AJoao-totvs/Claude-setup
claude plugin install totvs-setup@totvs-claude-setup
```

Slash commands antigos (`/prime`, `/plan`, etc) agora viram `/totvs-setup:prime`, `/totvs-setup:plan` etc.

---

## [0.1.0] — bundle inicial

- Skill `totvs-setup` para onboarding manual
- Templates `CLAUDE-dev.md` / `CLAUDE-gestao.md`
- Profiles `gerencia.md` / `dev.md`
- Catalogo `SKILLS-CATALOG.md` com 400+ plugins externos
- Setup do Claude Cowork
