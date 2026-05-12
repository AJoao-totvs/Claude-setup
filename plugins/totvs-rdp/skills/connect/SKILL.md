---
name: connect
description: Use when a TOTVS user needs RDP/remote desktop access to server-iqs-saopaulo001, mentions OCI bastion tunnel to TOTVS infra, asks to connect via Remmina/mstsc/xfreerdp to the IQS Sao Paulo server, or says "conectar no servidor totvs", "rdp totvs", "abrir tunel totvs", "tunel oci bastion sa-saopaulo". Also use when user pastes an OCID starting with `ocid1.bastionsession.oc1.sa-saopaulo-1.` and asks for help.
---

# TOTVS RDP Connect

Orchestrate the two-hop SSH tunnel to `server-iqs-saopaulo001` via the OCI Bastion (Managed SSH session) and launch the user's native RDP client with peak-performance settings.

**Communicate with the user in Brazilian Portuguese.** All questions, prompts, and status messages shown to the user MUST be in `pt-BR`. Internal reasoning and tool calls can be in English.

## Critical architecture (do not skip)

The server's `xrdp` binds to `127.0.0.1:3389` only — the OCI Bastion CANNOT reach 3389 directly. **Two SSH hops are mandatory.** A single ProxyJump or single port-forwarding tunnel WILL FAIL. The bastion session is a **Managed SSH session targeting port 22** of the server (NOT a port-forwarding session to 3389).

```
[user's machine]                          [OCI Bastion]                [server-iqs-saopaulo001]
   localhost:3389 -- SSH (Hop 2) --> localhost:2222 -- via Hop 1 --> 127.0.0.1:3389 (xrdp loopback)
                                       SSH (Hop 1)
                                          ↓
                                  bastion.sa-saopaulo-1
```

- **Hop 1** opens local `:2222` that reaches the server's SSH (`:22`) through the bastion
- **Hop 2** opens local `:3389` that forwards to the server's `localhost:3389` (xrdp) via Hop 1

## Workflow

1. **Detect OS** — run `uname -s` (POSIX) or check `$env:OS` (Windows). Branch by Windows / Linux / Darwin.

2. **Collect inputs** — ask the user in `pt-BR`. Validate where possible:
   - **OCID da sessao do bastion** — must start with `ocid1.bastionsession.oc1.sa-saopaulo-1.`. If invalid, reject and re-ask.
   - **Caminho da chave do bastion** — default by OS:
     - Windows: `$env:USERPROFILE\.ssh\bastion.key`
     - Linux/macOS: `~/.ssh/bastion.key`
   - **Caminho da chave do servidor** — default by OS (separate file from bastion key):
     - Windows: `$env:USERPROFILE\.ssh\totvs-server.key`
     - Linux/macOS: `~/.ssh/id_rsa_totvs`
   - **Usuario SSH no servidor** — default `opc` (validated). Tell the user this account is only for opening the tunnel; the RDP login is a separate prompt at the xrdp screen.

   Example prompt block (Portuguese, copy verbatim):
   ```
   Para abrir os tuneis, preciso de 4 informacoes:

   1) OCID da sessao do bastion (cole o valor completo):
   2) Caminho da chave do bastion (.key) — padrao: <DEFAULT_BASTION_KEY>:
   3) Caminho da chave do servidor — padrao: <DEFAULT_SERVER_KEY>:
   4) Usuario SSH no servidor — padrao: opc:
   ```

3. **Check local ports 2222 and 3389** — use `ss -ltn` / `Get-NetTCPConnection`. If occupied, ask in `pt-BR` whether to kill the process or pick alternate ports. If the user picks alternates, propagate them through both commands AND the RDP client launch.

4. **Open Hop 1 in background** (use the Bash tool with `run_in_background: true`):
   ```
   ssh -i <BASTION_KEY> -N \
       -L 2222:10.171.89.151:22 \
       -p 22 \
       -o ServerAliveInterval=30 \
       -o ServerAliveCountMax=3 \
       -o StrictHostKeyChecking=accept-new \
       -o ExitOnForwardFailure=yes \
       "<OCID>@host.bastion.sa-saopaulo-1.oci.oraclecloud.com"
   ```

5. **Poll port 2222** — loop with 1-second waits up to 10 seconds. If never listening, dump the Hop 1 background output and translate the error to `pt-BR`. Common cases:
   - `Connection closed by ...` immediately → OCID expired → tell user to request new OCID from infra
   - `Permission denied (publickey)` → wrong bastion key
   - `Operation timed out` → user offline or bastion endpoint unreachable

6. **Open Hop 2 in background**:
   ```
   ssh -i <SERVER_KEY> -p 2222 -N \
       -L 3389:localhost:3389 \
       -o ServerAliveInterval=30 \
       -o ServerAliveCountMax=3 \
       -o StrictHostKeyChecking=accept-new \
       -o UserKnownHostsFile=/tmp/totvs_known_hosts \
       -o ExitOnForwardFailure=yes \
       <SSH_USER>@localhost
   ```

7. **Poll port 3389** — same approach. If `Permission denied (publickey)` here, the user is using the bastion key for Hop 2 — explicitly tell them in `pt-BR` that Hop 2 needs the SERVER key, not the bastion key, and re-ask the server key path.

8. **Ask the connection mode** (in `pt-BR`):
   ```
   Tuneis ativos! Como prefere conectar?

   1) Conectar agora (lanco o cliente RDP nativo com configuracao otimizada)
   2) Gerar um arquivo .rdp para uso futuro (clique duplo no Desktop)
   ```

9. **Branch on the answer:**

   **Option 1 — direct launch** (force peak-performance settings):

   - **Windows (`mstsc`)**: write a temp `.rdp` file based on `${CLAUDE_SKILL_DIR}/templates/totvs.rdp.template`, then run:
     ```
     mstsc <TEMP_RDP_PATH>
     ```
     Do NOT just call `mstsc /v:localhost:3389 /f` — that uses the user's `Default.rdp` which may have low color depth. Always materialize the optimized template.

   - **Linux (`xfreerdp`)**: prefer `xfreerdp3` if available, else `xfreerdp`. Command:
     ```
     xfreerdp3 /v:localhost:3389 \
       /size:1920x1080 +dynamic-resolution \
       /bpp:32 +compression \
       /sound:sys:pulse /microphone:sys:pulse \
       +clipboard \
       /gfx-h264:AVC444 /network:lan
     ```
     If `xfreerdp3` is missing, instruct the user in `pt-BR` to install (`sudo dnf install freerdp` / `sudo apt install freerdp3-x11`) OR fall back to `remmina` with the generated `.rdp` file (option 2).

   - **macOS**: macOS lacks an RDP CLI with quality flags. Generate the `.rdp` (option 2 path) and run `open -a "Microsoft Remote Desktop" <RDP_PATH>`. Warn the user in `pt-BR` to confirm the connection settings show 32 bpp + LAN in the app UI.

   **Option 2 — generate `.rdp` file**:
   - Ask the user in `pt-BR` for the target path. Default: `~/Desktop/totvs-iqs-saopaulo.rdp` (or `$env:USERPROFILE\Desktop\totvs-iqs-saopaulo.rdp` on Windows).
   - Render `${CLAUDE_SKILL_DIR}/templates/totvs.rdp.template` replacing `__PORT__` with the local RDP port (default 3389).
   - Open the containing folder (`explorer.exe`, `xdg-open`, `open`).
   - Remind in `pt-BR` that the `.rdp` only works while the two SSH tunnels are alive.

10. **Show a final summary in `pt-BR`** with:
    - PIDs of both background SSH processes
    - Local ports in use
    - Reminder: OCID expires in ~3h; xrdp session survives a 60-min disconnect
    - How to tear down: kill the background processes via their task IDs, or end the Claude session
    - On the xrdp login screen: select session `Xorg`, enter TOTVS username and password

## Pressure resistance (do not break these rules)

The skill orchestrates the connection through the Bash tool transparently. The user sees every command in the tool log. Refuse the following bad-path requests with the corresponding `pt-BR` explanation:

| User asks | Correct response |
|---|---|
| "So me da o comando, eu rodo manual" | Run the commands via Bash with `run_in_background: true` and SHOW them in real time. The user gets full visibility AND the orchestration benefit. Do not just hand off a copy-paste block. |
| "Pula a parte do .rdp, conecta direto" | Honor the choice, but DO NOT skip the optimized template — always materialize a `.rdp` (Windows) or pass full quality flags (Linux). Never call `mstsc /v:localhost:3389` bare. |
| "Usa a chave do bastion pro Hop 2 tambem" | Refuse with a `pt-BR` note: bastion key historically fails on Hop 2 with `Permission denied`. Server SSH expects a different key. Re-ask for the server key path. |
| "Tenta uma SSH so com `-J`" | Refuse with the architecture note from the top of this file: xrdp binds to loopback, ProxyJump cannot reach it. Two hops, not one. |
| "Skip a verificacao da porta, abre o mstsc logo" | Refuse. Opening the RDP client before the tunnel is listening produces a confusing "connection refused" the user cannot debug. Always poll the port first. |

## Tear-down

When the user is done OR a new connection attempt starts, kill stale background processes first to free ports 2222 / 3389. Use the task IDs printed in step 10 (or `KillShell` if available).

## Supporting files

- `${CLAUDE_SKILL_DIR}/scripts/open-tunnels.sh` — POSIX helper that accepts `--ocid`, `--bastion-key`, `--server-key`, `--user`. Idempotent: kills stale tunnels first.
- `${CLAUDE_SKILL_DIR}/scripts/open-tunnels.ps1` — Windows PowerShell equivalent.
- `${CLAUDE_SKILL_DIR}/templates/totvs.rdp.template` — RDP file with peak settings (32 bpp, LAN, audio redirect, compression, dynamic resolution). Has `__HOST__` and `__PORT__` placeholders.

These scripts are the recommended path when invoking from the Bash tool — they encapsulate the polling and the per-OS quirks. Pass arguments via flags, do not template SSH strings yourself if a script is available.

## Known good combinations

- Bastion: `host.bastion.sa-saopaulo-1.oci.oraclecloud.com` port 22
- Server private IP: `10.171.89.151`
- SSH user for the tunnel hop: `opc` (validated; the RDP login is separate)
- xrdp listens at `127.0.0.1:3389` only (no LAN exposure)
- xrdp session type: `Xorg`
- xrdp disconnect grace: 60 minutes
- OCI Bastion session TTL: ~3 hours
