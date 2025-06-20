#!/bin/bash

# ============================================================================
# QClickIn Production Deployment Script
# ============================================================================

set -e  # Exit on any error

echo "🚀 QClickIn Production Deployment Script"
echo "========================================"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if required files exist
check_requirements() {
    print_info "Checking deployment requirements..."
    
    if [ ! -f ".env" ]; then
        print_error "Environment file (.env) not found!"
        echo "Create .env file with production settings first."
        exit 1
    fi
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found!"
        exit 1
    fi
    
    if [ ! -f "Dockerfile" ]; then
        print_error "Dockerfile not found!"
        exit 1
    fi
    
    print_status "All required files found"
}

# Run tests before deployment
run_tests() {
    print_info "Running tests..."
    
    if command -v pytest &> /dev/null; then
        python -m pytest tests/ -v --tb=short
        print_status "Tests passed"
    else
        print_warning "pytest not found, skipping tests"
    fi
}

# Build Docker image
build_image() {
    print_info "Building Docker image..."
    
    docker build -t qclickin-api:latest .
    print_status "Docker image built successfully"
}

# Deploy based on platform choice
deploy() {
    echo ""
    echo "Choose deployment platform:"
    echo "1) Railway (Recommended)"
    echo "2) Docker + Manual"
    echo "3) Heroku"
    echo "4) Local Docker Compose"
    
    read -p "Enter choice (1-4): " choice
    
    case $choice in
        1)
            deploy_railway
            ;;
        2)
            deploy_docker
            ;;
        3)
            deploy_heroku
            ;;
        4)
            deploy_local
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
}

# Railway deployment
deploy_railway() {
    print_info "Deploying to Railway..."
    
    if ! command -v railway &> /dev/null; then
        print_error "Railway CLI not installed!"
        echo "Install with: npm install -g @railway/cli"
        exit 1
    fi
    
    railway login
    railway init --name qclickin-api
    railway up
    
    print_status "Deployed to Railway successfully!"
    railway status
}

# Docker deployment
deploy_docker() {
    print_info "Preparing Docker deployment..."
    
    echo "Docker image 'qclickin-api:latest' is ready"
    echo ""
    echo "To run manually:"
    echo "docker run -p 8000:8000 --env-file .env qclickin-api:latest"
    echo ""
    echo "To push to registry:"
    echo "docker tag qclickin-api:latest your-registry/qclickin-api:latest"
    echo "docker push your-registry/qclickin-api:latest"
    
    print_status "Docker deployment prepared"
}

# Heroku deployment
deploy_heroku() {
    print_info "Deploying to Heroku..."
    
    if ! command -v heroku &> /dev/null; then
        print_error "Heroku CLI not installed!"
        echo "Install from: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    heroku login
    heroku create qclickin-api --region us
    heroku addons:create heroku-postgresql:mini
    
    # Set environment variables
    print_info "Setting environment variables..."
    heroku config:set SECRET_KEY="$(openssl rand -hex 32)"
    heroku config:set ENVIRONMENT="production"
    
    git push heroku main
    
    print_status "Deployed to Heroku successfully!"
    heroku open
}

# Local deployment
deploy_local() {
    print_info "Starting local deployment with Docker Compose..."
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose not installed!"
        exit 1
    fi
    
    docker-compose up -d
    
    print_status "Local deployment started!"
    echo ""
    echo "Services running:"
    echo "- API: http://localhost:8000"
    echo "- Docs: http://localhost:8000/docs"
    echo "- Database: localhost:5432"
    echo "- Redis: localhost:6379"
    
    print_info "To stop: docker-compose down"
}

# Post-deployment verification
verify_deployment() {
    print_info "Verifying deployment..."
    
    echo ""
    echo "Manual verification checklist:"
    echo "1. Check health endpoint: /health"
    echo "2. Test authentication: /auth/login"
    echo "3. Verify API docs: /docs"
    echo "4. Test database connection"
    echo "5. Check logs for errors"
    
    print_status "Deployment script completed!"
}

# Main execution
main() {
    check_requirements
    run_tests
    build_image
    deploy
    verify_deployment
    
    echo ""
    print_status "🎉 QClickIn API deployment completed successfully!"
    echo ""
    echo "Next steps:"
    echo "- Set up monitoring and alerts"
    echo "- Configure custom domain"
    echo "- Set up SSL certificates"
    echo "- Implement CI/CD pipeline"
    echo ""
    echo "For detailed instructions, see DEPLOYMENT.md"
}

# Run main function
main "$@" 