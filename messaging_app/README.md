# Kubernetes Container Orchestration Project
## Django Messaging App

**Project Duration**: August 10-17, 2025  
**Objective**: Transform a Django messaging app from simple Docker containers to a fully orchestrated, scalable Kubernetes deployment.

---

## 🚀 Project Overview

This project demonstrates fundamental Kubernetes concepts through practical implementation with a Django messaging application. You'll learn container orchestration principles including scalability, fault tolerance, and CI/CD integration.

---

## 📋 Task Breakdown

### Task 0: Install Kubernetes and Set Up Local Cluster
**Objective**: Learn how to set up and use Kubernetes locally using Minikube.

**Files**:
- `kurbeScript` - Automated setup script for Minikube and kubectl

**Learning Goals**:
- Kubernetes cluster architecture
- Basic kubectl commands
- Cluster health verification

**Implementation**:
```bash
# Make script executable and run
chmod +x kurbeScript
./kurbeScript
```

**Key Commands**:
- `minikube start` - Start local cluster
- `kubectl cluster-info` - Verify cluster status
- `kubectl get pods --all-namespaces` - List all pods

---

### Task 1: Deploy the Django Messaging App
**Objective**: Define Docker image, create Deployment and ClusterIP Service.

**Files**:
- `k8s-deployment.yaml` - Django app deployment with health checks
- `k8s-service.yaml` - Services and MySQL deployment

**Learning Goals**:
- Kubernetes Deployment concepts
- Service types and networking
- Health checks and resource limits

**Implementation**:
```bash
# Build Docker image
docker build -t django-messaging:latest .

# Apply Kubernetes manifests
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml

# Verify deployment
kubectl get pods
kubectl get services
```

**Best Practices Implemented**:
- Resource requests and limits
- Liveness and readiness probes
- ConfigMaps for configuration
- Health check endpoints

---

### Task 2: Scale the Django App
**Objective**: Scale replicas to 3, monitor pods, perform load testing, monitor resource usage.

**Files**:
- `scale-app.sh` - Scaling and monitoring script

**Learning Goals**:
- Horizontal scaling
- Resource monitoring
- Load testing
- Performance analysis

**Implementation**:
```bash
# Make script executable and run
chmod +x scale-app.sh
./scale-app.sh
```

**Key Features**:
- Automatic scaling to 3 replicas
- Resource usage monitoring
- Load testing with curl
- Pod and service monitoring

---

### Task 3: Set Up Kubernetes Ingress
**Objective**: Install Nginx Ingress controller, create Ingress resource, route traffic via paths.

**Files**:
- `k8s-ingress.yaml` - Ingress configuration with path-based routing
- `setup-ingress.sh` - Ingress controller installation script

**Learning Goals**:
- Ingress controller concepts
- Path-based routing
- External access configuration
- Security headers

**Implementation**:
```bash
# Make script executable and run
chmod +x setup-ingress.sh
./setup-ingress.sh
```

**Routing Paths**:
- `/` - Main application
- `/api/` - API endpoints
- `/admin/` - Django admin
- `/health/` - Health checks
- `/blue/` - Blue deployment (Task 4)
- `/green/` - Green deployment (Task 4)

---

### Task 4: Blue-Green Deployment Strategy
**Objective**: Deploy two versions, switch traffic gradually, monitor logs.

**Files**:
- `k8s-blue-green.yaml` - Blue-green deployment configuration
- `blue-green-deploy.sh` - Deployment management script

**Learning Goals**:
- Zero-downtime deployments
- Traffic switching strategies
- Deployment rollback
- Canary testing

**Implementation**:
```bash
# Make script executable and run
chmod +x blue-green-deploy.sh
./blue-green-deploy.sh
```

**Deployment Strategy**:
- Blue: Current stable version (v1.0)
- Green: New version (v1.1)
- Gradual traffic switching
- Easy rollback capability

---

### Task 5: Apply Rolling Updates
**Objective**: Update Docker image to v2.0, trigger rolling update, monitor rollout, test for downtime.

**Files**:
- `k8s-rolling-update.yaml` - Rolling update deployment configuration
- `rolling-update.sh` - Rolling update management script

**Learning Goals**:
- Rolling update strategies
- Zero-downtime deployments
- Rollout monitoring
- Automatic scaling with HPA

**Implementation**:
```bash
# Make script executable and run
chmod +x rolling-update.sh
./rolling-update.sh
```

**Update Strategy**:
- RollingUpdate with maxSurge=1, maxUnavailable=0
- Horizontal Pod Autoscaler (HPA)
- Startup probes for better health checking
- Graceful termination handling

---

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ingress       │    │   Services      │    │   Deployments   │
│   Controller    │    │                 │    │                 │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Path-based    │    │   Load          │    │   Django App    │
│   Routing       │    │   Balancing     │    │   Pods          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Docker installed and running
- Windows 10/11, macOS, or Linux
- At least 4GB RAM available

### Step 1: Setup Kubernetes
```bash
cd messaging_app
./kurbeScript
```

### Step 2: Deploy Application
```bash
# Build and deploy
docker build -t django-messaging:latest .
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
```

### Step 3: Scale and Monitor
```bash
./scale-app.sh
```

### Step 4: Setup Ingress
```bash
./setup-ingress.sh
```

### Step 5: Blue-Green Deployment
```bash
./blue-green-deploy.sh
```

### Step 6: Rolling Updates
```bash
./rolling-update.sh
```

---

## 🔧 Configuration

### Environment Variables
- `DEBUG`: Django debug mode
- `MYSQL_DB`: Database name
- `MYSQL_USER`: Database user
- `MYSQL_PASSWORD`: Database password
- `MYSQL_HOST`: Database host
- `MYSQL_PORT`: Database port

### Resource Limits
- **CPU**: 250m request, 500m limit
- **Memory**: 256Mi request, 512Mi limit

### Health Checks
- **Liveness Probe**: `/health/` endpoint, 30s initial delay
- **Readiness Probe**: `/health/` endpoint, 5s initial delay
- **Startup Probe**: `/health/` endpoint, 10s initial delay

---

## 📊 Monitoring and Debugging

### Useful Commands
```bash
# View all resources
kubectl get all

# Check pod status
kubectl get pods -o wide

# View logs
kubectl logs <pod-name>

# Describe resources
kubectl describe pod <pod-name>

# Port forwarding
kubectl port-forward service/<service-name> 8080:80

# Watch resources
kubectl get pods -w
```

### Dashboard Access
```bash
# Enable dashboard
minikube addons enable dashboard

# Access dashboard
minikube dashboard
```

---

## 🧪 Testing

### Health Check Endpoint
The Django app includes a `/health/` endpoint for Kubernetes health checks.

### Load Testing
Each script includes built-in load testing capabilities using curl.

### Downtime Testing
The rolling update script tests for zero-downtime during deployments.

---

## 🔒 Security Features

- Security headers via Ingress annotations
- Resource limits to prevent resource exhaustion
- Health checks to ensure application health
- Graceful termination handling

---

## 📈 Scaling Features

- Horizontal Pod Autoscaler (HPA)
- Configurable replica counts
- Resource-based scaling policies
- Stabilization windows for scaling

---

## 🚨 Troubleshooting

### Common Issues

1. **Minikube not starting**
   ```bash
   minikube delete
   minikube start --driver=docker
   ```

2. **Pods not ready**
   ```bash
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

3. **Service not accessible**
   ```bash
   kubectl get endpoints
   kubectl describe service <service-name>
   ```

4. **Image pull errors**
   ```bash
   # For local images in Minikube
   eval $(minikube docker-env)
   docker build -t django-messaging:latest .
   ```

---

## 📚 Learning Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)

---

## 🤝 Contributing

This project is designed for learning purposes. Feel free to:
- Modify configurations
- Add new features
- Improve scripts
- Report issues

---

## 📄 License

This project is for educational purposes as part of the ALX Backend Python curriculum.

---

## 🎯 Success Metrics

By completing this project, you will understand:
- ✅ Kubernetes cluster setup and management
- ✅ Application deployment and scaling
- ✅ Service networking and load balancing
- ✅ Ingress configuration and routing
- ✅ Zero-downtime deployment strategies
- ✅ Rolling update mechanisms
- ✅ Resource monitoring and optimization
- ✅ Container orchestration best practices

---

**Happy Learning! 🚀**
