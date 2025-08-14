#!/bin/bash

# scale-app.sh - Scale Django App and Monitor Performance
# This script scales the Django app to 3 replicas and monitors performance

set -e

echo "🚀 Starting Django App Scaling Process..."

# Function to check if kubectl is available
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        echo "❌ kubectl not found. Please run kurbeScript first."
        exit 1
    fi
}

# Function to check if cluster is running
check_cluster() {
    echo "🔍 Checking cluster status..."
    if ! kubectl cluster-info &> /dev/null; then
        echo "❌ Cluster not accessible. Please start Minikube first."
        exit 1
    fi
    echo "✅ Cluster is accessible"
}

# Function to scale the deployment
scale_deployment() {
    echo "📈 Scaling Django app to 3 replicas..."
    kubectl scale deployment django-messaging-app --replicas=3
    
    echo "⏳ Waiting for all pods to be ready..."
    kubectl wait --for=condition=Ready pods -l app=django-messaging --timeout=300s
    
    echo "✅ Scaling complete!"
}

# Function to monitor pods
monitor_pods() {
    echo ""
    echo "📊 Pod Status:"
    kubectl get pods -l app=django-messaging -o wide
    
    echo ""
    echo "📈 Pod Details:"
    kubectl describe pods -l app=django-messaging
}

# Function to monitor resource usage
monitor_resources() {
    echo ""
    echo "💾 Resource Usage:"
    
    # Get resource usage for all pods
    echo "📊 Pod Resource Usage:"
    kubectl top pods -l app=django-messaging
    
    echo ""
    echo "🖥️  Node Resource Usage:"
    kubectl top nodes
    
    echo ""
    echo "📈 Resource Requests and Limits:"
    kubectl get pods -l app=django-messaging -o custom-columns="NAME:.metadata.name,CPU_REQUEST:.spec.containers[0].resources.requests.cpu,CPU_LIMIT:.spec.containers[0].resources.limits.cpu,MEMORY_REQUEST:.spec.containers[0].resources.requests.memory,MEMORY_LIMIT:.spec.containers[0].resources.limits.memory"
}

# Function to perform load testing
load_test() {
    echo ""
    echo "🔥 Starting Load Testing..."
    
    # Get the service IP
    SERVICE_IP=$(kubectl get service django-messaging-service -o jsonpath='{.spec.clusterIP}')
    
    if [ -z "$SERVICE_IP" ]; then
        echo "❌ Could not get service IP. Load testing skipped."
        return
    fi
    
    echo "🎯 Service IP: $SERVICE_IP"
    echo "📡 Port forwarding to access service..."
    
    # Start port forwarding in background
    kubectl port-forward service/django-messaging-service 8080:80 &
    PF_PID=$!
    
    # Wait for port forwarding to be ready
    sleep 5
    
    echo "🚀 Running load test with curl..."
    
    # Simple load test with multiple concurrent requests
    for i in {1..10}; do
        echo "Request $i:"
        curl -s -w "Status: %{http_code}, Time: %{time_total}s\n" \
             -o /dev/null \
             http://localhost:8080/health/ &
    done
    
    # Wait for all requests to complete
    wait
    
    echo "✅ Load testing complete!"
    
    # Stop port forwarding
    kill $PF_PID 2>/dev/null || true
}

# Function to show logs
show_logs() {
    echo ""
    echo "📝 Recent Logs from Django Pods:"
    
    # Get all pod names
    PODS=$(kubectl get pods -l app=django-messaging -o jsonpath='{.items[*].metadata.name}')
    
    for pod in $PODS; do
        echo ""
        echo "📋 Logs from $pod:"
        echo "----------------------------------------"
        kubectl logs $pod --tail=10 || echo "No logs available"
        echo "----------------------------------------"
    done
}

# Function to show service endpoints
show_endpoints() {
    echo ""
    echo "🔗 Service Endpoints:"
    kubectl get endpoints django-messaging-service
    
    echo ""
    echo "🌐 Service Details:"
    kubectl describe service django-messaging-service
}

# Main execution
main() {
    check_kubectl
    check_cluster
    
    echo "🎯 Current deployment status:"
    kubectl get deployment django-messaging-app
    
    scale_deployment
    monitor_pods
    monitor_resources
    load_test
    show_logs
    show_endpoints
    
    echo ""
    echo "🎉 Scaling and monitoring complete!"
    echo ""
    echo "📋 Useful commands for ongoing monitoring:"
    echo "  - Watch pods: kubectl get pods -l app=django-messaging -w"
    echo "  - View logs: kubectl logs -f <pod-name>"
    echo "  - Check events: kubectl get events --sort-by=.metadata.creationTimestamp"
    echo "  - Monitor resources: kubectl top pods -l app=django-messaging"
    echo ""
    echo "🚀 Ready for Task 3: Set Up Kubernetes Ingress!"
}

# Run main function
main "$@"
