#!/bin/bash

# rolling-update.sh - Rolling Update Strategy Implementation
# This script implements rolling updates for zero-downtime deployments

set -e

echo "🔄 Starting Rolling Update Strategy Implementation..."

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

# Function to build v2.0 Docker image
build_v2_image() {
    echo "🏗️  Building Django v2.0 Docker image..."
    
    # Build the new v2.0 image
    docker build -t django-messaging:v2.0 .
    
    echo "✅ v2.0 image built successfully!"
}

# Function to deploy rolling update configuration
deploy_rolling_update() {
    echo "📦 Deploying rolling update configuration..."
    
    # Apply the rolling update configuration
    kubectl apply -f k8s-rolling-update.yaml
    
    echo "⏳ Waiting for rolling update deployment to be ready..."
    kubectl wait --for=condition=ready deployment django-messaging-rolling --timeout=300s
    
    echo "✅ Rolling update deployment ready!"
}

# Function to show deployment status
show_status() {
    echo ""
    echo "📊 Current Rolling Update Status:"
    echo "----------------------------------------"
    
    echo "🔄 Rolling Update Deployment:"
    kubectl get deployment django-messaging-rolling -o wide
    
    echo ""
    echo "📦 Pods:"
    kubectl get pods -l app=django-messaging -o wide
    
    echo ""
    echo "🌐 Service:"
    kubectl get service django-messaging-rolling-service
    
    echo ""
    echo "📈 HPA Status:"
    kubectl get hpa django-messaging-hpa
}

# Function to trigger rolling update
trigger_rolling_update() {
    echo ""
    echo "🚀 Triggering Rolling Update to v2.0..."
    
    # Update the image in the deployment
    kubectl set image deployment/django-messaging-rolling django-app=django-messaging:v2.0
    
    echo "✅ Rolling update triggered!"
    echo "⏳ Monitoring rollout status..."
    
    # Watch the rollout
    kubectl rollout status deployment/django-messaging-rolling --timeout=300s
    
    if [ $? -eq 0 ]; then
        echo "✅ Rolling update completed successfully!"
    else
        echo "❌ Rolling update failed or timed out!"
        return 1
    fi
}

# Function to monitor rollout progress
monitor_rollout() {
    echo ""
    echo "📊 Monitoring Rollout Progress..."
    
    # Show rollout status
    echo "🔄 Rollout Status:"
    kubectl rollout status deployment/django-messaging-rolling
    
    echo ""
    echo "📦 Pod Status:"
    kubectl get pods -l app=django-messaging -o wide
    
    echo ""
    echo "📈 Rollout History:"
    kubectl rollout history deployment/django-messaging-rolling
    
    echo ""
    echo "📋 Recent Events:"
    kubectl get events --field-selector involvedObject.name=django-messaging-rolling --sort-by=.metadata.creationTimestamp | tail -10
}

# Function to test application during update
test_during_update() {
    echo ""
    echo "🧪 Testing Application During Update..."
    
    # Set up port forwarding
    kubectl port-forward service/django-messaging-rolling-service 8080:80 &
    PF_PID=$!
    
    sleep 5
    
    echo "🚀 Running continuous health checks during update..."
    
    # Run health checks every 2 seconds for 30 seconds
    for i in {1..15}; do
        echo "Health check $i:"
        if curl -s http://localhost:8080/health/ > /dev/null; then
            echo "✅ Health check passed"
        else
            echo "❌ Health check failed"
        fi
        
        if [ $i -lt 15 ]; then
            sleep 2
        fi
    done
    
    # Stop port forwarding
    kill $PF_PID 2>/dev/null || true
    
    echo "✅ Testing during update complete!"
}

# Function to test for downtime
test_downtime() {
    echo ""
    echo "⏱️  Testing for Downtime During Update..."
    
    # Set up port forwarding
    kubectl port-forward service/django-messaging-rolling-service 8080:80 &
    PF_PID=$!
    
    sleep 5
    
    echo "🚀 Running intensive load test to check for downtime..."
    
    # Run multiple concurrent requests to simulate load
    for i in {1..50}; do
        (
            if curl -s -w "Request $i: %{http_code} %{time_total}s\n" \
                     -o /dev/null \
                     http://localhost:8080/health/; then
                echo "✅ Request $i successful"
            else
                echo "❌ Request $i failed"
            fi
        ) &
    done
    
    # Wait for all requests to complete
    wait
    
    echo "✅ Downtime testing complete!"
    
    # Stop port forwarding
    kill $PF_PID 2>/dev/null || true
}

# Function to rollback deployment
rollback_deployment() {
    echo ""
    echo "🔄 Rolling back deployment..."
    
    # Check rollout history
    echo "📚 Rollout History:"
    kubectl rollout history deployment/django-messaging-rolling
    
    # Rollback to previous revision
    kubectl rollout undo deployment/django-messaging-rolling
    
    echo "⏳ Waiting for rollback to complete..."
    kubectl rollout status deployment/django-messaging-rolling --timeout=300s
    
    if [ $? -eq 0 ]; then
        echo "✅ Rollback completed successfully!"
    else
        echo "❌ Rollback failed or timed out!"
        return 1
    fi
}

# Function to pause and resume rollout
pause_resume_rollout() {
    echo ""
    echo "⏸️  Pausing and Resuming Rollout..."
    
    # Pause the rollout
    echo "⏸️  Pausing rollout..."
    kubectl rollout pause deployment/django-messaging-rolling
    
    echo "⏳ Rollout paused. Checking status..."
    kubectl rollout status deployment/django-messaging-rolling
    
    echo "Press Enter to resume rollout..."
    read
    
    # Resume the rollout
    echo "▶️  Resuming rollout..."
    kubectl rollout resume deployment/django-messaging-rolling
    
    echo "⏳ Waiting for rollout to complete..."
    kubectl rollout status deployment/django-messaging-rolling --timeout=300s
    
    echo "✅ Rollout resumed and completed!"
}

# Function to show resource usage
show_resource_usage() {
    echo ""
    echo "💾 Resource Usage During Update..."
    
    echo "📊 Pod Resource Usage:"
    kubectl top pods -l app=django-messaging
    
    echo ""
    echo "🖥️  Node Resource Usage:"
    kubectl top nodes
    
    echo ""
    echo "📈 Resource Requests and Limits:"
    kubectl get pods -l app=django-messaging -o custom-columns="NAME:.metadata.name,CPU_REQUEST:.spec.containers[0].resources.requests.cpu,CPU_LIMIT:.spec.containers[0].resources.limits.cpu,MEMORY_REQUEST:.spec.containers[0].resources.requests.memory,MEMORY_LIMIT:.spec.containers[0].resources.limits.memory"
}

# Function to show logs
show_logs() {
    echo ""
    echo "📝 Application Logs During Update..."
    
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

# Function to cleanup
cleanup() {
    echo ""
    echo "🧹 Cleaning up rolling update deployment..."
    
    # Delete rolling update resources
    kubectl delete -f k8s-rolling-update.yaml --ignore-not-found=true
    
    echo "✅ Cleanup complete!"
}

# Function to show update strategy details
show_strategy() {
    echo ""
    echo "📋 Rolling Update Strategy Details:"
    echo "----------------------------------------"
    
    echo "🔄 Update Strategy:"
    kubectl get deployment django-messaging-rolling -o jsonpath='{.spec.strategy}' | jq '.' 2>/dev/null || echo "Strategy: RollingUpdate with maxSurge=1, maxUnavailable=0"
    
    echo ""
    echo "📊 Current Replicas:"
    kubectl get deployment django-messaging-rolling -o jsonpath='{.spec.replicas}'
    
    echo ""
    echo "🎯 HPA Configuration:"
    kubectl get hpa django-messaging-hpa -o yaml | grep -A 10 "spec:"
}

# Main menu function
show_menu() {
    echo ""
    echo "🔄 Rolling Update Menu:"
    echo "1. Deploy Rolling Update Configuration"
    echo "2. Build v2.0 Image"
    echo "3. Trigger Rolling Update"
    echo "4. Monitor Rollout Progress"
    echo "5. Test During Update"
    echo "6. Test for Downtime"
    echo "7. Show Status"
    echo "8. Show Strategy Details"
    echo "9. Pause/Resume Rollout"
    echo "10. Rollback Deployment"
    echo "11. Show Resource Usage"
    echo "12. Show Logs"
    echo "13. Cleanup"
    echo "0. Exit"
    echo ""
}

# Main execution
main() {
    check_kubectl
    check_cluster
    
    while true; do
        show_menu
        read -p "Select an option (0-13): " choice
        
        case $choice in
            1)
                deploy_rolling_update
                ;;
            2)
                build_v2_image
                ;;
            3)
                trigger_rolling_update
                ;;
            4)
                monitor_rollout
                ;;
            5)
                test_during_update
                ;;
            6)
                test_downtime
                ;;
            7)
                show_status
                ;;
            8)
                show_strategy
                ;;
            9)
                pause_resume_rollout
                ;;
            10)
                rollback_deployment
                ;;
            11)
                show_resource_usage
                ;;
            12)
                show_logs
                ;;
            13)
                cleanup
                ;;
            0)
                echo "👋 Exiting Rolling Update Strategy..."
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
            deploy_rolling_update
            ;;
        "update")
            build_v2_image
            trigger_rolling_update
            ;;
        "monitor")
            monitor_rollout
            ;;
        "test")
            test_during_update
            test_downtime
            ;;
        "rollback")
            rollback_deployment
            ;;
        "status")
            show_status
            ;;
        "cleanup")
            cleanup
            ;;
        *)
            echo "Usage: $0 [deploy|update|monitor|test|rollback|status|cleanup]"
            exit 1
            ;;
    esac
fi
