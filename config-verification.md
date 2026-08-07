# k8s/configmap.yaml

Developers forgot to include DATABASE_URL and REDIS_URL here which results in the application to default to volatile, in-memory SQLite and local cache.

# app/app.py

