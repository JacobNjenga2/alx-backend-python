#!/bin/bash

# setup-ingress.sh - Install Nginx Ingress Controller and Set Up Ingress
# This script installs the Nginx Ingress controller and configures routing

set -e

echo "🌐 Starting Kubernetes Ingress Setup Process..."

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

# Function to install Nginx Ingress Controller
install_ingress_controller() {
    echo "📥 Installing Nginx Ingress Controller..."
    
    # Check if ingress-nginx namespace exists
    if kubectl get namespace ingress-nginx &> /dev/null; then
        echo "✅ Ingress namespace already exists"
    else
        echo "📦 Creating ingress-nginx namespace..."
        kubectl create namespace ingress-nginx
    fi
    
    # Install Nginx Ingress Controller using Helm (if available) or kubectl
    if command -v helm &> /dev/null; then
        echo "🚀 Installing with Helm..."
        helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
        helm repo update
        helm install nginx-ingress ingress-nginx/ingress-nginx \
            --namespace ingress-nginx \
            --set controller.service.type=LoadBalancer \
            --set controller.ingressClassResource.name=nginx \
            --set controller.ingressClassResource.default=true
    else
        echo "📦 Installing with kubectl apply..."
        kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
    fi
    
    echo "⏳ Waiting for Ingress Controller to be ready..."
    kubectl wait --namespace ingress-nginx \
        --for=condition=ready pod \
        --selector=app.kubernetes.io/component=controller \
        --timeout=300s
    
    echo "✅ Ingress Controller installed successfully!"
}

# Function to verify Ingress Controller installation
verify_ingress_controller() {
    echo "🔍 Verifying Ingress Controller installation..."
    
    echo "📊 Pods in ingress-nginx namespace:"
    kubectl get pods -n ingress-nginx
    
    echo ""
    echo "🌐 Services in ingress-nginx namespace:"
    kubectl get services -n ingress-nginx
    
    echo ""
    echo "📋 Ingress Classes:"
    kubectl get ingressclass
}

# Function to apply Ingress configuration
apply_ingress_config() {
    echo "📝 Applying Ingress configuration..."
    
    # Apply the ingress configuration
    kubectl apply -f k8s-ingress.yaml
    
    echo "⏳ Waiting for Ingress to be ready..."
    kubectl wait --for=condition=ready ingress django-messaging-ingress --timeout=300s
    
    echo "✅ Ingress configuration applied successfully!"
}

# Function to verify Ingress configuration
verify_ingress_config() {
    echo "🔍 Verifying Ingress configuration..."
    
    echo "📊 Ingress resources:"
    kubectl get ingress
    
    echo ""
    echo "📋 Ingress details:"
    kubectl describe ingress django-messaging-ingress
    
    echo ""
    echo "🔗 Service endpoints:"
    kubectl get endpoints django-messaging-service
}

# Function to test Ingress routing
test_ingress_routing() {
    echo "🧪 Testing Ingress routing..."
    
    # Get the Ingress Controller external IP
    echo "🔍 Getting Ingress Controller external IP..."
    
    # For Minikube, we need to use port-forwarding
    echo "📡 Setting up port forwarding for testing..."
    
    # Start port forwarding to the Ingress Controller
    kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8080:80 &
    PF_PID=$!
    
    # Wait for port forwarding to be ready
    sleep 5
    
    echo "🚀 Testing different paths..."
    
    # Test root path
    echo "Testing / path:"
    curl -s -H "Host: messaging.local" http://localhost:8080/ | head -5
    
    # Test health endpoint
    echo "Testing /health/ path:"
    curl -s -H "Host: messaging.local" http://localhost:8080/health/ || echo "Health endpoint not responding"
    
    # Test API path
    echo "Testing /api/ path:"
    curl -s -H "Host: messaging.local" http://localhost:8080/api/ | head -5
    
    echo "✅ Ingress routing test complete!"
    
    # Stop port forwarding
    kill $PF_PID 2>/dev/null || true
}

# Function to show Ingress logs
show_ingress_logs() {
    echo ""
    echo "📝 Ingress Controller Logs:"
    
    # Get Ingress Controller pod name
    INGRESS_POD=$(kubectl get pods -n ingress-nginx -l app.kubernetes.io/component=controller -o jsonpath='{.items[0].metadata.name}')
    
    if [ -n "$INGRESS_POD" ]; then
        echo "📋 Logs from $INGRESS_POD:"
        echo "----------------------------------------"
        kubectl logs -n ingress-nginx $INGRESS_POD --tail=10 || echo "No logs available"
        echo "----------------------------------------"
    else
        echo "❌ No Ingress Controller pod found"
    fi
}

# Function to add host entry for local testing
add_host_entry() {
    echo ""
    echo "🌐 Adding host entry for local testing..."
    
    # Get Minikube IP
    MINIKUBE_IP=$(minikube ip)
    
    if [ -n "$MINIKUBE_IP" ]; then
        echo "🎯 Minikube IP: $MINIKUBE_IP"
        echo "📝 Add this line to your /etc/hosts file (or C:\Windows\System32\drivers\etc\hosts on Windows):"
        echo "   $MINIKUBE_IP messaging.local"
        echo ""
        echo "💡 After adding the host entry, you can access your app at:"
        echo "   http://messaging.local"
    else
        echo "❌ Could not get Minikube IP"
    fi
}

# Main execution
main() {
    check_kubectl
    check_cluster
    
    echo "🎯 Current cluster status:"
    kubectl get nodes
    
    install_ingress_controller
    verify_ingress_controller
    apply_ingress_config
    verify_ingress_config
    test_ingress_routing
    show_ingress_logs
    add_host_entry
    
    echo ""
    echo "🎉 Ingress setup complete!"
    echo ""
    echo "📋 Useful commands for Ingress management:"
    echo "  - View Ingress: kubectl get ingress"
    echo "  - Check Ingress Controller: kubectl get pods -n ingress-nginx"
    echo "  - View Ingress logs: kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller"
    echo "  - Test routing: curl -H 'Host: messaging.local' http://localhost:8080/"
    echo ""
    echo "🚀 Ready for Task 4: Blue-Green Deployment Strategy!"
}

# Run main function
main "$@"
