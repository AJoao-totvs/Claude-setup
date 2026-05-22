---
name: iqs-k8s
description: Gerencia, faz deploy e debuga aplicacoes no cluster Kubernetes IQS da TOTVS (namespace iqs) usando o Harbor privado docker.totvs.io. Use sempre que um colega pedir para fazer deploy, subir ou atualizar uma aplicacao no cluster, dockerizar um app, publicar imagem no Harbor, configurar kubectl/kubeconfig, ou quando algo que ja esta no ar estiver com problema (pod em CrashLoopBackOff, ImagePullBackOff, pod nao sobe, ver logs, reiniciar, rollback, IP pendente). Tambem ativa em "deploy iqs", "subir no kubernetes", "debugar pod", "kubectl", ou "/iqs-k8s".
---

## iqs-k8s — Deploy e Debug no Cluster IQS

Você ajuda colegas TOTVS a (1) subir/atualizar aplicações no cluster Kubernetes IQS (namespace `iqs`, Harbor `docker.totvs.io`) e (2) debugar workloads que já estão no ar. Conteúdo em PT-BR.

### Regras de segurança (sempre)
- **Nunca** escreva o token do cluster, senha AD ou qualquer secret em arquivo versionado. O token vai só para `~/.kube/config` do dev, em runtime.
- O `assets/kubeconfig.template` tem só dados não-secretos (server + CA). O token é colado pelo dev.
- **Confirme antes** de qualquer ação que muta registry ou cluster: `docker push`, `kubectl apply`, criar secret, `delete`, `rollout restart`, `rollout undo`, `scale`. Read-only (`get`/`describe`/`logs`/`top`) é livre.
- Você roda **bash não-interativo**: use `kubectl exec <pod> -n iqs -- <cmd>` para comandos pontuais; para shell interativo, oriente o dev a rodar `! kubectl exec -it ...`. Evite `-f`/`-w` (use `--tail`/`--since` ou background).

### Fase 0 — Roteamento
Pergunte (ou infira) o que o usuário quer:
- **A) Subir/atualizar um app** → siga **FLUXO DEPLOY**.
- **B) Algo no ar está com problema** → siga **FLUXO DEBUG**.
- **C) Só operar/inspecionar** → use `references/survival-commands.md`.

Antes de A ou B, garanta acesso: se `~/.kube/config` não existir ou `kubectl get pods -n iqs` falhar com erro de auth, faça o **SETUP DE ACESSO** primeiro.

### SETUP DE ACESSO (1ª vez)
1. Pré-reqs (time é Windows-first): Docker Desktop rodando (ícone verde, WSL2) e `kubectl` instalado (`winget install -e --id Kubernetes.kubectl`).
2. Monte o kubeconfig: copie `assets/kubeconfig.template` para `~/.kube/config` e substitua `<COLE_SEU_TOKEN_AQUI>` pelo token do cluster (o dev obtém da fonte segura/guia). **Não** escreva o token em nenhum outro lugar.
3. Valide: `kubectl get pods -n iqs`. Sucesso = lista de pods ou `No resources found`.

### FLUXO DEPLOY
1. **Dockerizar:** detecte o stack pelo arquivo-âncora e copie o template certo de `assets/` para `Dockerfile` na raiz do projeto, ajustando porta/CMD:
   - `package.json` → `Dockerfile.node` · `requirements.txt`/`pyproject.toml` → `Dockerfile.python` · `go.mod` → `Dockerfile.go` · `angular.json` → `Dockerfile.angular` · senão pergunte porta/comando/base.
2. **Build:** `docker build -t docker.totvs.io/iqs/<app>:vX.Y.Z .` (semver; nunca `:latest`).
3. **Teste local (opcional):** `docker run --rm -p <ext>:<int> docker.totvs.io/iqs/<app>:vX.Y.Z`.
4. **Login + push** (confirma): `docker login docker.totvs.io` (credencial AD do dev) → `docker push docker.totvs.io/iqs/<app>:vX.Y.Z`.
5. **Manifests:** crie `k8s/deployment.yaml` e `k8s/service.yaml` a partir de `assets/*.template`, substituindo `__APP_NAME__`, `__IMAGE__`, `__CONTAINER_PORT__`.
6. **Pull secret** (1x): se `kubectl get secret harbor-pull-secret -n iqs` falhar, crie-o (ver `references/survival-commands.md`).
7. **Deploy** (confirma): `kubectl apply -f ./k8s` → acompanhe `kubectl get pods -n iqs` (sem `-w`; rode de novo) até `1/1 Running` → `kubectl get svc -n iqs` para o `EXTERNAL-IP`.
8. **Update futuro:** bump de versão, rebuild, push, atualize `image:` no deployment, `kubectl apply` de novo.

### FLUXO DEBUG (dirigido por hipótese)
1. **Mapear:** `kubectl get pods,deploy,svc -n iqs` → olhe STATUS, RESTARTS, AGE.
2. **Focar:** `kubectl describe pod <pod> -n iqs` e leia a seção **Events**.
3. **Logs:** `kubectl logs deploy/<app> -n iqs --tail=100`; se crashou, `--previous`.
4. **Classificar:** cruze o sintoma com a tabela em `references/troubleshooting.md` → forme uma hipótese.
5. **Aprofundar** (conforme hipótese): `kubectl exec <pod> -n iqs -- env`, `kubectl get endpoints -n iqs`, `kubectl top pod -n iqs`, `kubectl rollout history deploy/<app> -n iqs`. Para testar sem expor: `kubectl port-forward deploy/<app> -n iqs <local>:<port>` (rode em background).
6. **Corrigir** (confirma antes): `kubectl rollout undo`, `rollout restart`, `scale`, corrigir secret, ou ajustar manifest + `apply`.
7. **Verificar:** `kubectl rollout status deploy/<app> -n iqs`, readiness `1/1`, e teste o endpoint.

### Referências
- `references/troubleshooting.md` — árvore de diagnóstico.
- `references/survival-commands.md` — operação do dia a dia.
- `assets/` — templates de kubeconfig, manifests e Dockerfiles.
