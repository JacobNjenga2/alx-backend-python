# GitHub Actions CI/CD Setup Guide

This document explains how to set up and configure the GitHub Actions workflows for the Django Messaging App.

## 📋 Overview

We have implemented two main workflows:

1. **`ci.yml`** - Continuous Integration (Testing, Linting, Security)
2. **`dep.yml`** - Docker Build and Deployment

## 🔧 Required GitHub Secrets

To use the Docker deployment workflow, you need to configure the following secrets in your GitHub repository:

### Setting up GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Add the following secrets:

#### Docker Hub Secrets

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `DOCKER_USERNAME` | Your Docker Hub username | `yourusername` |
| `DOCKER_PASSWORD` | Your Docker Hub password or access token | `dckr_pat_xxxxxxxxxxxxx` |

### Creating a Docker Hub Access Token (Recommended)

Instead of using your Docker Hub password, create an access token:

1. Log in to [Docker Hub](https://hub.docker.com/)
2. Go to **Account Settings** → **Security**
3. Click **"New Access Token"**
4. Name: `github-actions-messaging-app`
5. Permissions: **Read, Write, Delete**
6. Copy the generated token and use it as `DOCKER_PASSWORD`

## 🚀 Workflow Features

### CI Workflow (`ci.yml`)

#### ✅ **Testing**
- Runs tests on Python 3.9, 3.10, and 3.11
- Uses MySQL 8.0 service for database testing
- Generates code coverage reports
- Uploads coverage artifacts

#### 🔍 **Code Quality**
- **Flake8**: Python linting and style checking
- **Black**: Code formatting validation
- **isort**: Import sorting validation
- **mypy**: Type checking (optional)

#### 🔒 **Security**
- **Safety**: Checks for known security vulnerabilities in dependencies
- **Bandit**: Static security analysis for Python code
- Uploads security reports as artifacts

#### 📊 **Build Status**
- Aggregates results from all jobs
- Fails if any critical checks fail
- Provides clear status notifications

### Deployment Workflow (`dep.yml`)

#### 🐳 **Docker Build**
- Builds multi-platform Docker images (linux/amd64, linux/arm64)
- Uses BuildKit for optimized builds
- Implements layer caching for faster builds
- Runs security scanning with Trivy

#### 📦 **Image Management**
- Tags images based on branches and tags:
  - `main` branch → `latest` tag
  - `develop` branch → `develop` tag
  - Tags → semantic version tags (`v1.0.0`, `1.0`, `1`)
  - PRs → `pr-123` tags (build only, not pushed)

#### 🚀 **Deployment**
- **Staging**: Auto-deploys from `develop` branch
- **Production**: Auto-deploys from `main` branch
- Uses environment protection rules
- Supports rollback strategies

## 📁 File Structure

```
.github/
└── workflows/
    ├── ci.yml      # CI/CD pipeline for testing and quality
    └── dep.yml     # Docker build and deployment
.flake8             # Flake8 configuration
pyproject.toml      # Tool configurations (Black, isort, mypy, pytest, coverage)
requirements.txt    # Updated with testing and quality tools
```

## 🏃‍♂️ Running Locally

### Prerequisites
```bash
# Install development dependencies
pip install -r requirements.txt
```

### Code Quality Checks
```bash
# Linting
flake8 .

# Code formatting
black --check .
black .  # To format

# Import sorting
isort --check-only .
isort .  # To sort

# Type checking
mypy .

# Security checks
safety check
bandit -r .
```

### Testing
```bash
# Run tests with coverage
pytest --cov=. --cov-report=html

# Run specific test types
pytest -m unit
pytest -m integration
pytest -m "not slow"
```

## 🔄 Workflow Triggers

### CI Workflow Triggers
- **Push** to `main` or `develop` branches
- **Pull Requests** to `main` or `develop` branches

### Deployment Workflow Triggers
- **Push** to `main`, `develop` branches
- **Tags** matching `v*.*.*` pattern
- **Pull Requests** to `main` (build only, no push)

## 🎯 Best Practices

### Branch Strategy
- `main` - Production-ready code
- `develop` - Integration branch for features
- Feature branches - Individual features/fixes

### Commit Messages
Use conventional commits for automatic versioning:
```
feat: add user authentication
fix: resolve memory leak in message processing
docs: update API documentation
test: add integration tests for chat functionality
```

### Testing Strategy
- Write unit tests for individual functions/methods
- Write integration tests for API endpoints
- Use factories for test data generation
- Aim for >80% code coverage

### Security
- Regularly update dependencies
- Review security scan results
- Use secrets for sensitive configuration
- Follow Django security best practices

## 🚨 Troubleshooting

### Common Issues

#### Docker Build Fails
```bash
# Check Dockerfile syntax
docker build -t test-image .

# Verify secrets are set correctly
# Go to GitHub repository → Settings → Secrets
```

#### Tests Fail in CI but Pass Locally
```bash
# Check environment variables
# Ensure MySQL service is configured correctly
# Verify Python versions match
```

#### Linting Failures
```bash
# Fix formatting issues
black .
isort .

# Check specific flake8 errors
flake8 . --show-source
```

### Getting Help

1. Check workflow logs in GitHub Actions tab
2. Review configuration files for syntax errors
3. Ensure all required secrets are configured
4. Verify branch protection rules if deployments fail

## 📈 Monitoring and Metrics

The workflows provide several monitoring capabilities:

- **Build Status**: Overall pipeline health
- **Test Coverage**: Code quality metrics
- **Security Reports**: Vulnerability tracking
- **Deployment Status**: Release monitoring
- **Performance**: Build time tracking

All reports are stored as artifacts and can be downloaded from the GitHub Actions interface.

## 🔮 Future Enhancements

Consider implementing:

- Slack/email notifications for deployment status
- Automated rollback on deployment failures
- Performance testing in CI pipeline
- Database migration testing
- End-to-end testing with Playwright/Selenium
- Integration with monitoring tools (Datadog, New Relic)
- Automated dependency updates with Dependabot
