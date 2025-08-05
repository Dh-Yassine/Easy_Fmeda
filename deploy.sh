#!/bin/bash

# FMEDA Web Application Deployment Script
# This script helps deploy both frontend and backend

echo "🚀 FMEDA Web Application Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."
    
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        print_error "Node.js/npm is not installed. Please install Node.js first."
        exit 1
    fi
    
    print_status "All requirements are met!"
}

# Deploy backend
deploy_backend() {
    print_status "Deploying backend..."
    
    cd fmeda_backend
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        print_warning "Heroku CLI not found. Please install it first:"
        echo "npm install -g heroku"
        echo "heroku login"
        return 1
    fi
    
    # Check if app exists
    if ! heroku apps:info &> /dev/null; then
        print_status "Creating new Heroku app..."
        heroku create
    fi
    
    # Set environment variables
    print_status "Setting environment variables..."
    heroku config:set SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')"
    heroku config:set DEBUG="False"
    heroku config:set ALLOWED_HOSTS="$(heroku info -s | grep web_url | cut -d= -f2 | sed 's/https:\/\///')"
    
    # Deploy
    print_status "Deploying to Heroku..."
    git add .
    git commit -m "Deploy backend to Heroku"
    git push heroku main
    
    # Run migrations
    print_status "Running database migrations..."
    heroku run python manage.py migrate
    
    # Get the app URL
    BACKEND_URL=$(heroku info -s | grep web_url | cut -d= -f2)
    print_status "Backend deployed at: $BACKEND_URL"
    
    cd ..
    return 0
}

# Deploy frontend
deploy_frontend() {
    print_status "Deploying frontend..."
    
    cd fmeda-frontend
    
    # Install dependencies
    print_status "Installing dependencies..."
    npm install
    
    # Build the application
    print_status "Building application..."
    npm run build
    
    print_status "Frontend built successfully!"
    print_warning "Please deploy the 'build' folder to Vercel or Netlify manually."
    print_warning "Don't forget to set REACT_APP_API_BASE_URL environment variable."
    
    cd ..
}

# Main deployment function
main() {
    echo ""
    print_status "Starting deployment process..."
    
    # Check requirements
    check_requirements
    
    # Ask user what to deploy
    echo ""
    echo "What would you like to deploy?"
    echo "1. Backend only"
    echo "2. Frontend only"
    echo "3. Both (recommended)"
    echo "4. Exit"
    
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            deploy_backend
            ;;
        2)
            deploy_frontend
            ;;
        3)
            deploy_backend
            if [ $? -eq 0 ]; then
                deploy_frontend
            fi
            ;;
        4)
            print_status "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid choice. Please run the script again."
            exit 1
            ;;
    esac
    
    echo ""
    print_status "Deployment completed!"
    print_warning "Remember to:"
    print_warning "1. Update CORS settings in Django with your frontend domain"
    print_warning "2. Set REACT_APP_API_BASE_URL in your frontend deployment"
    print_warning "3. Test the full application flow"
}

# Run the script
main 