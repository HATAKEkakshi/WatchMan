#!/bin/bash

echo "🚀 Deploying WatchMan to Kubernetes..."

# Apply manifests in order
kubectl apply -f namespace.yaml
kubectl apply -f secrets.yaml
kubectl apply -f mongodb.yaml
kubectl apply -f redis.yaml
kubectl apply -f qdrant.yaml
kubectl apply -f backend.yaml
kubectl apply -f frontend.yaml
kubectl apply -f ingress.yaml

echo "✅ Deployment complete!"
echo "📋 Check status with: kubectl get pods -n watchman"
echo "🌐 Access app at: http://watchman.local"
echo "📊 Add to /etc/hosts: 127.0.0.1 watchman.local"