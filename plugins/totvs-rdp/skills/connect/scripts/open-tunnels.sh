#!/usr/bin/env bash
# TOTVS RDP — two-hop SSH tunnel opener (POSIX).
# Usage:
#   open-tunnels.sh --ocid OCID --bastion-key PATH --server-key PATH [--user opc] [--local-rdp 3389] [--local-jump 2222]
#
# Exits 0 once both tunnels are listening locally. Prints two background PIDs to stdout.

set -euo pipefail

OCID=""
BASTION_KEY=""
SERVER_KEY=""
SSH_USER="opc"
LOCAL_RDP="3389"
LOCAL_JUMP="2222"
SERVER_IP="10.171.89.151"
BASTION_HOST="host.bastion.sa-saopaulo-1.oci.oraclecloud.com"
KNOWN_HOSTS_FILE="${TMPDIR:-/tmp}/totvs_known_hosts"

err() { printf 'erro: %s\n' "$*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ocid)         OCID="$2"; shift 2 ;;
    --bastion-key)  BASTION_KEY="$2"; shift 2 ;;
    --server-key)   SERVER_KEY="$2"; shift 2 ;;
    --user)         SSH_USER="$2"; shift 2 ;;
    --local-rdp)    LOCAL_RDP="$2"; shift 2 ;;
    --local-jump)   LOCAL_JUMP="$2"; shift 2 ;;
    *) err "argumento desconhecido: $1" ;;
  esac
done

[[ -z "$OCID" ]] && err "--ocid e obrigatorio"
[[ -z "$BASTION_KEY" ]] && err "--bastion-key e obrigatorio"
[[ -z "$SERVER_KEY" ]] && err "--server-key e obrigatorio"
[[ ! -r "$BASTION_KEY" ]] && err "chave do bastion nao legivel: $BASTION_KEY"
[[ ! -r "$SERVER_KEY" ]] && err "chave do servidor nao legivel: $SERVER_KEY"

if [[ ! "$OCID" =~ ^ocid1\.bastionsession\.oc1\.sa-saopaulo-1\. ]]; then
  err "OCID nao tem o prefixo esperado (ocid1.bastionsession.oc1.sa-saopaulo-1.)"
fi

# Ensure proper key perms (ssh refuses world-readable keys)
chmod 600 "$BASTION_KEY" "$SERVER_KEY" 2>/dev/null || true

is_listening() {
  ss -ltn "sport = :$1" 2>/dev/null | grep -q LISTEN
}

wait_port() {
  local port="$1" attempts="${2:-10}" i=0
  while (( i < attempts )); do
    is_listening "$port" && return 0
    sleep 1
    i=$((i + 1))
  done
  return 1
}

# Hop 1
hop1_log=$(mktemp)
ssh -i "$BASTION_KEY" -N \
  -L "${LOCAL_JUMP}:${SERVER_IP}:22" \
  -p 22 \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -o StrictHostKeyChecking=accept-new \
  -o ExitOnForwardFailure=yes \
  -E "$hop1_log" \
  "${OCID}@${BASTION_HOST}" &
HOP1_PID=$!

if ! wait_port "$LOCAL_JUMP" 10; then
  kill "$HOP1_PID" 2>/dev/null || true
  printf 'erro: hop 1 nao subiu. log:\n' >&2
  tail -20 "$hop1_log" >&2
  rm -f "$hop1_log"
  exit 2
fi

# Hop 2
hop2_log=$(mktemp)
ssh -i "$SERVER_KEY" -p "$LOCAL_JUMP" -N \
  -L "${LOCAL_RDP}:localhost:3389" \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -o StrictHostKeyChecking=accept-new \
  -o UserKnownHostsFile="$KNOWN_HOSTS_FILE" \
  -o ExitOnForwardFailure=yes \
  -E "$hop2_log" \
  "${SSH_USER}@localhost" &
HOP2_PID=$!

if ! wait_port "$LOCAL_RDP" 10; then
  kill "$HOP2_PID" "$HOP1_PID" 2>/dev/null || true
  printf 'erro: hop 2 nao subiu. log:\n' >&2
  tail -20 "$hop2_log" >&2
  rm -f "$hop1_log" "$hop2_log"
  exit 3
fi

printf '%s %s\n' "$HOP1_PID" "$HOP2_PID"
printf 'tuneis ativos. porta RDP local: %s\n' "$LOCAL_RDP" >&2
