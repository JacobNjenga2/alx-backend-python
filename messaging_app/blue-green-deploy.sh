#!/bin/bash

# blue-green-deploy.sh - Blue-Green Deployment Strategy Implementation
# This script implements blue-green deployment for zero-downtime updates

set -e

echo "🔄 Starting Blue-Green Deployment Strategy..."

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

# Function to build and tag Docker images
build_images() {
    echo "🏗️  Building Docker images for blue-green deployment..."
    
    # Build v1.0 (blue) image
    echo "🔵 Building blue image (v1.0)..."
    docker build -t django-messaging:v1.0 .
    
    # Build v1.1 (green) image with some modifications
    echo "🟢 Building green image (v1.1)..."
    # For demonstration, we'll use the same image but tag it differently
    docker build -t django-messaging:v1.1 .
    
    echo "✅ Images built successfully!"
}

# Function to deploy blue-green configuration
deploy_blue_green() {
    echo "📦 Deploying blue-green configuration..."
    
    # Apply the blue-green configuration
    kubectl apply -f k8s-blue-green.yaml
    
    echo "⏳ Waiting for blue deployment to be ready..."
    kubectl wait --for=condition=ready deployment django-messaging-blue --timeout=300s
    
    echo "✅ Blue-green deployment ready!"
}

# Function to show deployment status
show_status() {
    echo ""
    echo "📊 Current Deployment Status:"
    echo "----------------------------------------"
    
    echo "🔵 Blue Deployment (v1.0):"
    kubectl get deployment django-messaging-blue -o wide
    
    echo ""
    echo "🟢 Green Deployment (v1.1):"
    kubectl get deployment django-messaging-green -o wide
    
    echo ""
    echo "📦 Pods:"
    kubectl get pods -l app=django-messaging -o wide
    
    echo ""
    echo "🌐 Services:"
    kubectl get services -l app=django-messaging
}

# Function to test blue deployment
test_blue() {
    echo ""
    echo "🧪 Testing Blue Deployment (v1.0)..."
    
    # Test blue service directly
    kubectl port-forward service/django-messaging-blue-service 8081:80 &
    BLUE_PF_PID=$!
    
    sleep 5
    
    echo "Testing blue service at localhost:8081..."
    curl -s http://localhost:8081/health/ || echo "Health check failed"
    
    # Stop port forwarding
    kill $BLUE_PF_PID 2>/dev/null || true
    
    echo "✅ Blue deployment test complete!"
}

# Function to test green deployment
test_green() {
    echo ""
    echo "🧪 Testing Green Deployment (v1.1)..."
    
    # Test green service directly
    kubectl port-forward service/django-messaging-green-service 8082:80 &
    GREEN_PF_PID=$!
    
    sleep 5
    
    echo "Testing green service at localhost:8082..."
    curl -s http://localhost:8082/health/ || echo "Health check failed"
    
    # Stop port forwarding
    kill $GREEN_PF_PID 2>/dev/null || true
    
    echo "✅ Green deployment test complete!"
}

# Function to switch traffic to green
switch_to_green() {
    echo ""
    echo "🔄 Switching traffic from Blue to Green..."
    
    # Scale up green deployment
    echo "📈 Scaling up green deployment..."
    kubectl scale deployment django-messaging-green --replicas=2
    
    # Wait for green pods to be ready
    echo "⏳ Waiting for green pods to be ready..."
    kubectl wait --for=condition=ready deployment django-messaging-green --timeout=300s
    
    # Update main service to point to green
    echo "🔄 Updating main service to route to green..."
    kubectl patch service django-messaging-service -p '{"spec":{"selector":{"color":"green"}}}'
    
    echo "✅ Traffic switched to Green deployment!"
}

# Function to switch traffic back to blue
switch_to_blue() {
    echo ""
    echo "🔄 Switching traffic back to Blue..."
    
    # Update main service to point back to blue
    echo "🔄 Updating main service to route to blue..."
    kubectl patch service django-messaging-service -p '{"spec":{"selector":{"color":"blue"}}}'
    
    # Scale down green deployment
    echo "📉 Scaling down green deployment..."
    kubectl scale deployment django-messaging-green --replicas=0
    
    echo "✅ Traffic switched back to Blue deployment!"
}

# Function to perform gradual traffic switching
gradual_switch() {
    echo ""
    echo "🔄 Performing gradual traffic switch..."
    
    # First, scale up green to 1 replica
    echo "📈 Scaling green to 1 replica..."
    kubectl scale deployment django-messaging-green --replicas=1
    
    # Wait for green to be ready
    kubectl wait --for=condition=ready deployment django-messaging-green --timeout=300s
    
    # Test green deployment
    test_green
    
    # Ask user if they want to continue
    read -p "🔄 Green deployment is ready. Switch traffic to green? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        switch_to_green
        echo "✅ Traffic successfully switched to Green!"
    else
        echo "❌ Traffic switch cancelled. Rolling back..."
        kubectl scale deployment django-messaging-green --replicas=0
    fi
}

# Function to monitor deployment logs
monitor_logs() {
    echo ""
    echo "📝 Monitoring deployment logs..."
    
    echo "🔵 Blue deployment logs:"
    echo "----------------------------------------"
    kubectl logs -l app=django-messaging,color=blue --tail=5 || echo "No blue pods running"
    
    echo ""
    echo "🟢 Green deployment logs:"
    echo "----------------------------------------"
    kubectl logs -l app=django-messaging,color=green --tail=5 || echo "No green pods running"
}

# Function to rollback to blue
rollback_to_blue() {
    echo ""
    echo "🔄 Rolling back to Blue deployment..."
    
    # Switch traffic back to blue
    switch_to_blue
    
    # Scale down green completely
    kubectl scale deployment django-messaging-green --replicas=0
    
    echo "✅ Rollback to Blue deployment complete!"
}

# Function to show deployment history
show_history() {
    echo ""
    echo "📚 Deployment History:"
    echo "----------------------------------------"
    
    echo "🔵 Blue deployment events:"
    kubectl get events --field-selector involvedObject.name=django-messaging-blue --sort-by=.metadata.creationTimestamp | tail -5
    
    echo ""
    echo "🟢 Green deployment events:"
    kubectl get events --field-selector involvedObject.name=django-messaging-green --sort-by=.metadata.creationTimestamp | tail -5
}

# Function to cleanup
cleanup() {
    echo ""
    echo "🧹 Cleaning up blue-green deployment..."
    
    # Delete blue-green resources
    kubectl delete -f k8s-blue-green.yaml --ignore-not-found=true
    
    echo "✅ Cleanup complete!"
}

# Main menu function
show_menu() {
    echo ""
    echo "🔄 Blue-Green Deployment Menu:"
    echo "1. Deploy Blue-Green Configuration"
    echo "2. Show Status"
    echo "3. Test Blue Deployment"
    echo "4. Test Green Deployment"
    echo "5. Switch to Green"
    echo "6. Switch to Blue"
    echo "7. Gradual Switch"
    echo "8. Monitor Logs"
    echo "9. Rollback to Blue"
    echo "10. Show History"
    echo "11. Cleanup"
    echo "0. Exit"
    echo ""
}

# Main execution
main() {
    check_kubectl
    check_cluster
    
    while true; do
        show_menu
        read -p "Select an option (0-11): " choice
        
        case $choice in
            1)
                build_images
                deploy_blue_green
                ;;
            2)
                show_status
                ;;
            3)
                test_blue
                ;;
            4)
                test_green
                ;;
            5)
                switch_to_green
                ;;
            6)
                switch_to_blue
                ;;
            7)
                gradual_switch
                ;;
            8)
                monitor_logs
                ;;
            9)
                rollback_to_blue
                ;;
            10)
                show_history
                ;;
            11)
                cleanup
                ;;
            0)
                echo "👋 Exiting Blue-Green Deployment..."
                exit 0
                ;;
            *)
                echo "❌ Invalid option. Please try again."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Check if script is run with arguments
if [ $# -eq 0 ]; then
    main
else
    # Run specific function based on argument
    case $1 in
        "deploy")
            build_images
            deploy_blue_green
            ;;
        "status")
            show_status
            ;;
        "switch-green")
            switch_to_green
            ;;
        "switch-blue")
            switch_to_blue
            ;;
        "test")
            test_blue
            test_green
            ;;
        "cleanup")
            cleanup
            ;;
        *)
            echo "Usage: $0 [deploy|status|switch-green|switch-blue|test|cleanup]"
            exit 1
            ;;
    esac
fi
