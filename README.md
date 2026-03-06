# Feathr
This project is a part of the Feathr Platform engineer interview process.

Overview
A microservices-based inventory system using Flask, MongoDB, and Elasticsearch running on Kubernetes.

Core Features
CRUD API: Manage products (ID, Name, Category, Price, Quantity).

Full-Text Search: Fast description searching via Elasticsearch.

Analytics: Real-time stats on average price and popular categories.

Setup & Deployment
1. Start Cluster
Bash
minikube start
eval $(minikube docker-env)
2. Build & Deploy
Bash
# Build the Flask app image
docker build -t inventory-app:latest .

# Deploy everything (Mongo, ES, and Flask)
kubectl apply -f kubernetes/
3. Verify
Wait until all pods show Running:

Bash
kubectl get pods
Testing the API
1. Connection
Run this command to open a "tunnel" to the API:

Bash
kubectl port-forward service/flask-service 5000:5000
2. Seed Data
Populate the system with sample products:

Bash
python app/seed.py
3. Key Endpoints
List Products: GET /products

Search: GET /products/search?query=laptop

Analytics: GET /products/analytics

File Structure
/app: Flask application logic and seed scripts.

/kubernetes: YAML manifests for deployments and services.

Dockerfile: Container configuration for the Flask app