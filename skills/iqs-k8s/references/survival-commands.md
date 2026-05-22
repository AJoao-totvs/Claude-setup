# Comandos de Sobrevivência — Cluster IQS

Operações do dia a dia. Tudo que **muta** o cluster deve ser confirmado antes.

## Atualizar a aplicação (novo código)
1. Bump da versão e rebuild: `docker build -t docker.totvs.io/iqs/<app>:vX.Y.Z .`
2. Teste local: `docker run --rm -p <ext>:<int> docker.totvs.io/iqs/<app>:vX.Y.Z`
3. Push: `docker push docker.totvs.io/iqs/<app>:vX.Y.Z`
4. Atualizar `image:` no `k8s/deployment.yaml` para `vX.Y.Z`
5. Aplicar: `kubectl apply -f ./k8s`  → rollout sem downtime

## Operação
```bash
kubectl logs deploy/<app> -n iqs --tail=100     # logs
kubectl rollout restart deploy/<app> -n iqs      # reiniciar
kubectl rollout undo deploy/<app> -n iqs         # rollback p/ versão anterior
kubectl scale deploy/<app> -n iqs --replicas=2   # escalar
kubectl get svc -n iqs                            # ver EXTERNAL-IP
kubectl delete -f ./k8s                           # tirar do ar (CUIDADO)
```

## Criar o harbor-pull-secret (1x por namespace, se faltar)
Usa a credencial AD do próprio dev (digitada na hora; nunca versionada):
```bash
kubectl create secret docker-registry harbor-pull-secret \
  --docker-server=docker.totvs.io \
  --docker-username=SEU_USUARIO_AD \
  --docker-password=SUA_SENHA_AD \
  --docker-email=seu-email@totvs.com.br \
  -n iqs
```
