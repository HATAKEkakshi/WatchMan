# WatchMan Kubernetes Deployment with ArgoCD

## 🚀 ArgoCD Deployment

### 1. Apply ArgoCD Application
```bash
kubectl apply -f argocd/application.yaml
```

### 2. Access Application
- **Frontend**: http://watchman.local
- **Add to /etc/hosts**: `127.0.0.1 watchman.local`

## 📦 Components

- **Frontend**: 2 replicas with ingress
- **Backend**: 2 replicas with internal service
- **MongoDB**: 1 replica with persistent storage (5Gi)
- **Redis**: 1 replica for caching
- **Qdrant**: 1 replica with persistent storage (2Gi)

## 🔧 Configuration

- **Namespace**: `watchman`
- **Ingress**: NGINX controller required
- **Secrets**: GROQ API key stored securely
- **Auto-sync**: Enabled with self-healing

## 📋 Commands

```bash
# Check application status
kubectl get applications -n argocd

# View pods
kubectl get pods -n watchman

# Check services
kubectl get svc -n watchman

# View ingress
kubectl get ingress -n watchman
```