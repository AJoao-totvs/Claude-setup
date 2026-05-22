#!/usr/bin/env bash
# Dev-time validator for the iqs-k8s skill. Doubles as a no-secret guard.
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp="$(mktemp -d)"
fail=0
trap 'rm -rf "$tmp"' EXIT

# 1. Required files exist
for f in SKILL.md \
         assets/kubeconfig.template \
         assets/deployment.yaml.template assets/service.yaml.template \
         assets/Dockerfile.node assets/Dockerfile.python \
         assets/Dockerfile.go assets/Dockerfile.angular \
         references/troubleshooting.md references/survival-commands.md; do
  [ -f "$DIR/$f" ] || { echo "MISSING: $f"; fail=1; }
done

# 2. Frontmatter has name + description
if [ -f "$DIR/SKILL.md" ]; then
  awk '/^---$/{c++; next} c==1{print}' "$DIR/SKILL.md" > "$tmp/fm.yaml"
  grep -q '^name:' "$tmp/fm.yaml"        || { echo "FRONTMATTER: no name"; fail=1; }
  grep -q '^description:' "$tmp/fm.yaml" || { echo "FRONTMATTER: no description"; fail=1; }
  # Body must be filled (not the Task-7 placeholder) and contain both flows
  grep -q 'corpo preenchido na Task 7' "$DIR/SKILL.md" && { echo "BODY: still placeholder"; fail=1; }
  grep -q 'FLUXO DEPLOY' "$DIR/SKILL.md" || { echo "BODY: missing FLUXO DEPLOY"; fail=1; }
  grep -q 'FLUXO DEBUG'  "$DIR/SKILL.md" || { echo "BODY: missing FLUXO DEBUG"; fail=1; }
fi

# 3. SECRET SCAN (the critical guard). Exclude this script itself.
if grep -rEn --exclude='validate-skill.sh' 'eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.' "$DIR"; then
  echo "LEAK: JWT-shaped token found"; fail=1
fi
if grep -rEn --exclude='validate-skill.sh' 'BEGIN [A-Z ]*PRIVATE KEY' "$DIR"; then
  echo "LEAK: private key found"; fail=1
fi

# 4. kubeconfig keeps the token as a placeholder
if [ -f "$DIR/assets/kubeconfig.template" ]; then
  grep -q '<COLE_SEU_TOKEN_AQUI>' "$DIR/assets/kubeconfig.template" \
    || { echo "kubeconfig: token placeholder missing"; fail=1; }
fi

# 5. Manifests render to valid k8s (client-side dry-run if kubectl present)
if [ -f "$DIR/assets/deployment.yaml.template" ]; then
  mkdir -p "$tmp/manifests"
  for f in deployment service; do
    sed -e 's/__APP_NAME__/sample-app/g' \
        -e 's#__IMAGE__#docker.totvs.io/iqs/sample-app:v0.0.1#g' \
        -e 's/__CONTAINER_PORT__/3000/g' \
        "$DIR/assets/$f.yaml.template" > "$tmp/manifests/$f.yaml"
  done
  if command -v kubectl >/dev/null 2>&1; then
    kubectl apply --dry-run=client -f "$tmp/manifests" >/dev/null \
      && echo "manifests: dry-run OK" || { echo "manifests: dry-run FAILED"; fail=1; }
  else
    echo "manifests: kubectl absent, skipped dry-run (render OK)"
  fi
fi

[ "$fail" = 0 ] && echo "ALL CHECKS PASS" || { echo "CHECKS FAILED"; exit 1; }
