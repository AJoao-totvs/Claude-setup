# Troubleshooting — Cluster IQS

Árvore sintoma → causa provável → ação. Sempre investigar com read-only antes de mutar.

| Sintoma | Causa provável | Ação |
|---|---|---|
| `ImagePullBackOff` / `ErrImagePull` | secret/credencial AD ou tag de imagem errada | `kubectl get secret harbor-pull-secret -n iqs`; conferir tag no deployment; refazer `docker login docker.totvs.io` e recriar o secret |
| `CrashLoopBackOff` | app quebra no boot | `kubectl logs deploy/<app> -n iqs --previous`; `kubectl describe pod <pod> -n iqs` → entrypoint/config/dependência |
| `OOMKilled` (em describe) | limite de memória baixo | subir `resources.limits.memory` no deployment e reaplicar |
| `Pending` | sem recurso no node / PVC não liga / quota | `kubectl describe pod <pod> -n iqs` → ler **Events** no fim |
| `Running` mas `0/1 Ready` | readiness probe falhando ou porta errada | conferir `readinessProbe.tcpSocket.port` == `containerPort` == porta real da app |
| Service não responde | `endpoints` vazio (selector ≠ labels) ou `targetPort` errado | `kubectl get endpoints <app>-svc -n iqs`; conferir `selector.app` == label do pod e `targetPort` |
| `EXTERNAL-IP <pending>` | LoadBalancer Oracle ainda provisionando | aguardar 2-5 min e `kubectl get svc -n iqs` de novo |

## Comandos de investigação (read-only, seguros)

```bash
kubectl get pods,deploy,svc -n iqs
kubectl describe pod <pod> -n iqs        # ler a seção Events
kubectl logs deploy/<app> -n iqs --tail=100
kubectl logs deploy/<app> -n iqs --previous   # container que crashou
kubectl get endpoints -n iqs
kubectl top pod -n iqs                    # uso CPU/mem (se metrics-server)
kubectl rollout history deploy/<app> -n iqs
```

> Shell interativo: rode você mesmo `! kubectl exec -it <pod> -n iqs -- sh` (o assistente roda bash não-interativo e usa `kubectl exec <pod> -n iqs -- <cmd>` para comandos pontuais).
