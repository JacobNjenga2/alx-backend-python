#!/bin/bash

# Quick Kubernetes Installation Script for WSL
# This script installs Minikube and kubectl with timeout protection

set -e

echo "🚀 Quick Kubernetes Installation Starting..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to download with timeout
download_with_timeout() {
    local url=$1
    local output=$2
    local timeout=${3:-60}
    
    echo "📥 Downloading $output (timeout: ${timeout}s)..."
    
    if command_exists curl; then
        timeout $timeout curl -L -o "$output" "$url" || {
            echo "❌ Download failed or timed out. Trying alternative method..."
            return 1
        }
    elif command_exists wget; then
        timeout $timeout wget -O "$output" "$url" || {
            echo "❌ Download failed or timed out. Trying alternative method..."
            return 1
        }
    else
        echo "❌ Neither curl nor wget found. Please install one manually."
        return 1
    fi
    
    return 0
}

# Function to install Minikube
install_minikube() {
    echo "🔧 Installing Minikube..."
    
    # Try package manager first (fastest)
    if command_exists apt; then
        echo "📦 Trying apt installation..."
        sudo apt update -qq && sudo apt install -y minikube && return 0
    fi
    
    # Fallback to direct download
    echo "📥 Downloading Minikube binary..."
    if download_with_timeout \
        "https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64" \
        "minikube" 120; then
        
        chmod +x minikube
        sudo mv minikube /usr/local/bin/
        echo "✅ Minikube installed successfully!"
        return 0
    fi
    
    echo "❌ Minikube installation failed. Please install manually."
    return 1
}

# Function to install kubectl (if not already installed)
install_kubectl() {
    if command_exists kubectl; then
        echo "✅ kubectl already installed: $(kubectl version --client --short)"
        return 0
    fi
    
    echo "🔧 Installing kubectl..."
    
    # Try package manager first
    if command_exists apt; then
        echo "📦 Trying apt installation..."
        sudo apt update -qq && sudo apt install -y kubectl && return 0
    fi
    
    # Fallback to direct download
    echo "📥 Downloading kubectl binary..."
    if download_with_timeout \
        "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
        "kubectl" 120; then
        
        chmod +x kubectl
        sudo mv kubectl /usr/local/bin/
        echo "✅ kubectl installed successfully!"
        return 0
    fi
    
    echo "❌ kubectl installation failed. Please install manually."
    return 1
}

# Function to start Minikube cluster
start_cluster() {
    echo "🚀 Starting Minikube cluster..."
    
    # Check if Docker is available
    if ! command_exists docker; then
        echo "⚠️  Docker not found. Starting with none driver..."
        minikube start --driver=none --memory=4096 --cpus=2
    else
        echo "🐳 Starting with Docker driver..."
        minikube start --driver=docker --memory=4096 --cpus=2
    fi
    
    echo "⏳ Waiting for cluster to be ready..."
    kubectl wait --for=condition=Ready nodes --all --timeout=300s
    
    echo "✅ Cluster is ready!"
}

# Function to verify installation
verify_installation() {
    echo "🔍 Verifying installation..."
    
    echo "📊 Minikube version:"
    minikube version
    
    echo ""
    echo "📊 kubectl version:"
    kubectl version --client
    
    echo ""
    echo "📊 Cluster status:"
    minikube status
    
    echo ""
    echo "📦 Available pods:"
    kubectl get pods --all-namespaces
}

# Function to show manual installation steps
show_manual_steps() {
    echo ""
    echo "📋 Manual Installation Steps (if automated fails):"
    echo "----------------------------------------"
    echo "1. Install Minikube:"
    echo "   curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64"
    echo "   chmod +x minikube-linux-amd64"
    echo "   sudo mv minikube-linux-amd64 /usr/local/bin/minikube"
    echo ""
    echo "2. Install kubectl (if needed):"
    echo "   curl -LO \"https://dl.k8s.io/release/\$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl\""
    echo "   chmod +x kubectl"
    echo "   sudo mv kubectl /usr/local/bin/"
    echo ""
    echo "3. Start cluster:"
    echo "   minikube start --driver=docker --memory=4096 --cpus=2"
    echo ""
    echo "4. Verify:"
    echo "   kubectl cluster-info"
    echo "   minikube status"
}

# Main execution
main() {
    echo "🎯 Starting quick installation process..."
    
    # Install Minikube
    if install_minikube; then
        echo "✅ Minikube installation successful!"
    else
        echo "❌ Minikube installation failed. Showing manual steps..."
        show_manual_steps
        exit 1
    fi
    
    # Install kubectl (if needed)
    if install_kubectl; then
        echo "✅ kubectl installation successful!"
    else
        echo "❌ kubectl installation failed. Showing manual steps..."
        show_manual_steps
        exit 1
    fi
    
    # Start cluster
    start_cluster
    
    # Verify installation
    verify_installation
    
    echo ""
    echo "🎉 Installation complete! Ready for Task 1."
    echo ""
    echo "📋 Next steps:"
    echo "  - Build Docker image: docker build -t django-messaging:latest ."
    echo "  - Deploy to Kubernetes: kubectl apply -f k8s-deployment.yaml"
    echo "  - Check status: kubectl get pods"
}

# Run with error handling
if main; then
    echo "✅ All installations completed successfully!"
else
    echo "❌ Installation encountered errors. Check output above."
    show_manual_steps
    exit 1
fi
