#!/bin/bash
set -e

echo "============================================="
echo "Starting deployment of Checkout API Service..."
echo "Deployment Version: v2.4"
echo "============================================="

# Ensure namespace exists
echo "Checking namespace..."
kubectl get namespace checkout-system || kubectl create namespace checkout-system

# Secrets are provisioned by the operations team; never commit their values.
echo "Checking required dependency Secret and keys..."
kubectl get secret checkout-api-dependencies -n checkout-system >/dev/null
for key in DATABASE_URL REDIS_URL; do
  value="$(kubectl get secret checkout-api-dependencies -n checkout-system -o "jsonpath={.data.$key}")"
  if [ -z "$value" ]; then
    echo "Missing required key $key in checkout-api-dependencies" >&2
    exit 1
  fi
done

# Apply manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

echo "============================================="
echo "Deployment candidate v2.4 applied."
echo "Verify status using: kubectl get pods -n checkout-system"
echo "============================================="
