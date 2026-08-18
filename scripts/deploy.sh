#!/bin/bash
set -e

echo "============================================="
echo "Starting deployment of Checkout API Service..."
echo "Deployment Version: v2.4"
echo "============================================="

# Ensure namespace exists
echo "Checking namespace..."
kubectl get namespace checkout-system || kubectl create namespace checkout-system

# Apply manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

echo "============================================="
echo "Deployment candidate v2.4 applied."
echo "Verify status using: kubectl get pods -n checkout-system"
echo "============================================="
