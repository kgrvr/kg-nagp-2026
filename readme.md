# Kubernetes Assignment
 
## Repository
**GitHub:** https://github.com/kgrvr/kg-nagp-2026/
 
---
 
## Docker Hub
**Image URL:** https://hub.docker.com/r/kgrvr/kg-nagp-2026

**Tag**: latest

**Command**: `docker pull YOUR_DOCKERHUB_USERNAME/k8s-python-api:latest`
 
---
 
## Service API Endpoint
Run `minikube start` and then `minikube tunnel` to run locally.

**Base URL:** `http://127.0.0.1/`

**Swagger**: `http://127.0.0.1/docs`
- Describes API endpoints

**Employee Endpoint**: `GET http://127.0.0.1/employees`
- Returns all employee records from the database
 
**Response:**
```json
[
  {
    "id": 1,
    "name": "Alice Johnson",
    "role": "Engineer",
    "department": "Engineering",
    "salary": 95000
  },
  {
    "id": 2,
    "name": "Bob Smith",
    "role": "Manager",
    "department": "Operations",
    "salary": 105000
  },
  {
    "id": 3,
    "name": "Carol White",
    "role": "Designer",
    "department": "Product",
    "salary": 88000
  },
  {
    "id": 4,
    "name": "David Brown",
    "role": "Analyst",
    "department": "Finance",
    "salary": 82000
  },
  {
    "id": 5,
    "name": "Eva Green",
    "role": "DevOps",
    "department": "Engineering",
    "salary": 98000
  },
  {
    "id": 6,
    "name": "Frank Black",
    "role": "Scrum Master",
    "department": "Engineering",
    "salary": 91000
  },
  {
    "id": 7,
    "name": "Grace Lee",
    "role": "HR Specialist",
    "department": "HR",
    "salary": 75000
  },
  {
    "id": 8,
    "name": "Henry Wilson",
    "role": "Sales Lead",
    "department": "Sales",
    "salary": 87000
  },
  {
    "id": 9,
    "name": "Iris Moore",
    "role": "Data Scientist",
    "department": "Engineering",
    "salary": 102000
  },
  {
    "id": 10,
    "name": "Jake Taylor",
    "role": "QA Engineer",
    "department": "Engineering",
    "salary": 80000
  }
]
```

**Health Check**: `GET http://127.0.0.1/health`
- Returns API health status
 
**Response:**
```json
{
  "status": "ok"
}
```

---
 
## Tech Stack
 
| Component | Technology |
|---|---|
| Language | Python |
| Framework | Fast API |
| Database | PostgreSQL |
| Container Runtime | Docker |
| Orchestration | Kubernetes on Minikube |
| Ingress | NGINX Ingress Controller |
 
---
 
## Project Structure
 
```
nagp-k8s/
├── app/
│   ├── __init__.py           # Making a module
│   ├── main.py               # Fast API application
├── k8s/
│   ├── namespace.yaml        # Namespace definition
│   ├── configmap.yaml        # Non-sensitive config
│   ├── secret.yaml           # Sensitive config like database credentials
│   ├── postgres-pvc.yaml     # Persistent Storage Claim for PG database
│   ├── postgres-deployment.yaml  # PostgreSQL pod definition
│   ├── postgres-service.yaml     # Internal ClusterIP service for DB
│   ├── api-deployment.yaml   # Flask API pod definition
│   ├── api-service.yaml      # Internal ClusterIP service for API
│   ├── api-hpa.yaml          # Horizontal Pod Autoscaler
│   └── ingress.yaml          # NGINX Ingress for external access
├── README.md
├── requirements.txt      # Python dependencies
└── Dockerfile            # Container image definition
```
 
---
 
## How to Run Locally
 
### Prerequisites
- Docker Engine
- Minikube
- kubectl
 
### Steps
 
```bash
# 1. Start Minikube:
minikube start
minikube addons enable ingress
minikube addons enable metrics-server
 
# 2. Deploy all resources:
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/api-service.yaml
kubectl apply -f k8s/api-hpa.yaml
kubectl apply -f k8s/ingress.yaml
 
# 3. Wait for all pods to be Running:
kubectl get pods -n nagp-k8s --watch
 
# 4. Start tunnel:
minikube tunnel
 
# 5. Open browser and navigate to Swagger:
URL: http://127.0.0.1/docs
```