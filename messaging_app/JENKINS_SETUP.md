# Jenkins CI/CD Pipeline Setup Guide

This guide explains how to set up and configure Jenkins for the Django Messaging App CI/CD pipeline.

## 📋 Overview

The Jenkins pipeline (`Jenkinsfile`) provides:

- ✅ **Code Checkout** from GitHub with credentials
- 🐍 **Python Environment** setup with virtual environment
- 📦 **Dependency Management** with pip
- 🗄️ **Database Setup** with MySQL for testing
- 🔍 **Code Quality Checks** (flake8, black, isort)
- 🔒 **Security Scanning** (safety, bandit)
- 🧪 **Comprehensive Testing** with pytest
- 📊 **Report Generation** (coverage, HTML reports)
- ⚙️ **Django System Checks**
- 📦 **Artifact Building** for deployment
- 📧 **Email Notifications**

## 🛠️ Jenkins Prerequisites

### Jenkins Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install openjdk-11-jdk
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Get initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### Required Jenkins Plugins

Install these plugins via **Manage Jenkins** → **Manage Plugins**:

#### Essential Plugins
- **Pipeline**: Pipeline as Code support
- **Git**: Git SCM integration
- **GitHub**: GitHub integration
- **Credentials**: Secure credential management
- **Workspace Cleanup**: Clean workspace after builds

#### Testing & Reporting Plugins
- **JUnit**: Test result publishing
- **HTML Publisher**: HTML report publishing
- **Cobertura**: Coverage report publishing
- **Warnings Next Generation**: Code quality warnings
- **Test Results Analyzer**: Test trend analysis

#### Notification Plugins
- **Email Extension**: Advanced email notifications
- **Slack Notification**: Slack integration (optional)
- **Build Timeout**: Timeout management

#### Quality & Security Plugins
- **SonarQube Scanner**: Code quality analysis (optional)
- **OWASP Dependency Check**: Security vulnerability scanning
- **Pipeline Stage View**: Visual pipeline representation

## 🔑 Required Credentials

### Setting up GitHub Credentials

1. **Go to Jenkins Dashboard** → **Manage Jenkins** → **Manage Credentials**
2. **Click** on **(global)** domain
3. **Click** "Add Credentials"
4. **Select** credential type:

#### Option 1: Username with Password
```
Kind: Username with password
Scope: Global
Username: your-github-username
Password: your-github-personal-access-token
ID: github-credentials
Description: GitHub Access Token for Messaging App
```

#### Option 2: SSH Username with Private Key (Recommended)
```
Kind: SSH Username with private key
Scope: Global
Username: git
Private Key: [Your SSH private key]
ID: github-ssh-credentials
Description: GitHub SSH Key for Messaging App
```

### Creating GitHub Personal Access Token

1. **Go to GitHub** → **Settings** → **Developer settings** → **Personal access tokens**
2. **Click** "Generate new token"
3. **Set expiration** and select scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
   - `read:org` (Read org and team membership)
4. **Copy the token** and use it as password in Jenkins credentials

## 🗄️ Database Setup

### MySQL Setup for Jenkins

```bash
# Install MySQL
sudo apt install mysql-server

# Secure installation
sudo mysql_secure_installation

# Create Jenkins database and user
sudo mysql -u root -p
```

```sql
-- Create database and user for Jenkins testing
CREATE DATABASE messaging_db_test;
CREATE USER 'jenkins_user'@'localhost' IDENTIFIED BY 'jenkins_password';
GRANT ALL PRIVILEGES ON messaging_db_test.* TO 'jenkins_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Environment Variables

Set these in Jenkins **Global Properties** (Manage Jenkins → Configure System):

```
MYSQL_ROOT_PASSWORD=your_root_password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🚀 Pipeline Setup

### Creating the Pipeline Job

1. **Go to Jenkins Dashboard** → **New Item**
2. **Enter name**: `django-messaging-app-pipeline`
3. **Select**: "Multibranch Pipeline"
4. **Click**: "OK"

### Configuring Branch Sources

1. **Add source**: "GitHub"
2. **Configure**:
   ```
   Owner: your-github-username
   Repository: alx-backend-python
   Credentials: github-credentials
   
   Behaviors:
   ✅ Discover branches
   ✅ Discover pull requests from origin
   ✅ Discover pull requests from forks
   
   Property strategy: All branches get the same properties
   ```

3. **Build Configuration**:
   ```
   Mode: by Jenkinsfile
   Script Path: messaging_app/Jenkinsfile
   ```

4. **Scan Multibranch Pipeline Triggers**:
   ```
   ✅ Periodically if not otherwise run
   Interval: 1 day
   ```

### Pipeline Environment Setup

The pipeline automatically:

1. **Checks out code** from your GitHub repository
2. **Sets up Python virtual environment**
3. **Installs dependencies** from `requirements.txt`
4. **Configures database** for testing
5. **Runs comprehensive tests** and quality checks
6. **Generates reports** and artifacts
7. **Sends notifications** on completion

## 📊 Reports and Artifacts

### Available Reports

The pipeline generates several reports accessible via build page:

#### Test Reports
- **JUnit Test Results**: `/testReport/`
- **Coverage Report**: `/Coverage_Report/`
- **Pytest HTML Report**: `/Pytest_Report/`

#### Code Quality Reports
- **Flake8 Linting**: `reports/flake8-report.txt`
- **Black Formatting**: `reports/black-report.txt`
- **Import Sorting**: `reports/isort-report.txt`

#### Security Reports
- **Safety Vulnerability Scan**: `reports/safety-report.json`
- **Bandit Security Analysis**: `reports/bandit-report.json`

#### Build Artifacts
- **Deployment Package**: `messaging-app-{BUILD_NUMBER}.tar.gz`
- **Requirements Freeze**: `reports/requirements-freeze.txt`
- **Build Information**: `reports/build-info.json`

### Accessing Reports

1. **Go to build page**: `http://jenkins-url/job/django-messaging-app-pipeline/job/main/{BUILD_NUMBER}/`
2. **Click on report links** in the left sidebar
3. **Download artifacts** from the build artifacts section

## 🔧 Pipeline Configuration

### Customizing the Pipeline

The `Jenkinsfile` includes several configurable sections:

#### Environment Variables
```groovy
environment {
    PYTHON_VERSION = '3.11'        // Python version to use
    VENV_NAME = 'messaging_app_venv' // Virtual environment name
    MYSQL_DB = 'messaging_db_test'   // Test database name
    // ... other variables
}
```

#### Build Triggers
```groovy
triggers {
    pollSCM('H/5 * * * *')  // Poll every 5 minutes
    cron('H 2 * * *')       // Daily build at 2 AM
}
```

#### Test Configuration
```groovy
pytest \
    --cov-fail-under=70 \    // Minimum coverage threshold
    --maxfail=10 \           // Maximum test failures
    -n auto \               // Parallel test execution
    // ... other options
```

### Branch-Specific Behavior

- **Main Branch**: Full pipeline + deployment artifacts
- **Develop Branch**: Full pipeline + staging deployment
- **Feature Branches**: Testing and quality checks only
- **Pull Requests**: Testing without deployment

## 📧 Notification Setup

### Email Configuration

1. **Go to** Manage Jenkins → Configure System
2. **Find** "Extended E-mail Notification"
3. **Configure**:
   ```
   SMTP server: smtp.gmail.com
   SMTP port: 587
   Use SMTP Authentication: ✅
   Username: your-email@gmail.com
   Password: your-app-password
   Use SSL: ✅
   Default Content Type: HTML (text/html)
   ```

### Slack Integration (Optional)

1. **Install** Slack Notification plugin
2. **Create** Slack app and get webhook URL
3. **Add** webhook URL to Jenkins credentials
4. **Configure** in pipeline or global settings

## 🚨 Troubleshooting

### Common Issues

#### Permission Denied for Git
```bash
# Fix SSH key permissions on Jenkins server
sudo chown jenkins:jenkins /var/lib/jenkins/.ssh/id_rsa
sudo chmod 600 /var/lib/jenkins/.ssh/id_rsa
```

#### Python/Pip Issues
```bash
# Ensure Python and pip are available
sudo apt install python3 python3-pip python3-venv
sudo ln -s /usr/bin/python3 /usr/bin/python
```

#### MySQL Connection Issues
```bash
# Check MySQL service
sudo systemctl status mysql
sudo systemctl start mysql

# Verify user permissions
mysql -u jenkins_user -p -e "SHOW DATABASES;"
```

#### Virtual Environment Issues
```bash
# Install venv module
sudo apt install python3-venv

# Check Python version
python3 --version
which python3
```

### Debugging Pipeline

#### Enable Debug Logging
Add to Jenkinsfile:
```groovy
options {
    // Add debug logging
    buildDiscarder(logRotator(daysToKeepStr: '30', numToKeepStr: '10'))
    timestamps()
    ansiColor('xterm')
}
```

#### Manual Testing
```bash
# Test commands manually on Jenkins server
sudo su - jenkins
cd /var/lib/jenkins/workspace/django-messaging-app-pipeline/main/messaging_app
python3 -m venv test_venv
source test_venv/bin/activate
pip install -r requirements.txt
pytest --version
```

## 🔒 Security Best Practices

### Credential Management
- ✅ Use Jenkins Credentials Store
- ✅ Rotate credentials regularly
- ✅ Use least privilege principle
- ✅ Enable audit logging

### Pipeline Security
- ✅ Use specific plugin versions
- ✅ Validate input parameters
- ✅ Sanitize shell commands
- ✅ Use sandbox mode for untrusted scripts

### Server Security
- ✅ Keep Jenkins updated
- ✅ Use HTTPS/SSL
- ✅ Implement authentication
- ✅ Regular security scanning

## 📈 Performance Optimization

### Pipeline Performance
- 🚀 Use parallel stages
- 🚀 Implement build caching
- 🚀 Optimize Docker layers
- 🚀 Use build agents

### Resource Management
- 🚀 Set resource limits
- 🚀 Clean up workspaces
- 🚀 Archive only necessary artifacts
- 🚀 Implement retention policies

## 🔮 Advanced Features

### Blue-Green Deployment
```groovy
stage('Blue-Green Deploy') {
    when { branch 'main' }
    steps {
        script {
            // Implement blue-green deployment logic
            // Switch traffic between environments
        }
    }
}
```

### Integration Testing
```groovy
stage('Integration Tests') {
    steps {
        script {
            // Start services with docker-compose
            // Run integration tests
            // Tear down services
        }
    }
}
```

### Performance Testing
```groovy
stage('Performance Tests') {
    steps {
        script {
            // Run load tests with locust or k6
            // Generate performance reports
        }
    }
}
```

## 📚 Additional Resources

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Pipeline Syntax Reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Plugin Documentation](https://plugins.jenkins.io/)
- [Best Practices Guide](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)

## 🆘 Support

If you encounter issues:

1. **Check Jenkins logs**: `/var/log/jenkins/jenkins.log`
2. **Review build console output** in Jenkins UI
3. **Verify credentials** and permissions
4. **Test commands manually** on Jenkins server
5. **Check plugin compatibility** and versions

Remember to customize the pipeline according to your specific requirements and infrastructure setup!
