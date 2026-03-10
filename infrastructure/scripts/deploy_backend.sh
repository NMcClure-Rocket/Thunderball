#!/bin/bash

# Deploy backend application

echo "Deploying Thunderball Backend..."

# Set variables
ENVIRONMENT=${1:-dev}
BACKEND_DIR="../../backend"

echo "Deployment environment: $ENVIRONMENT"

# Load environment-specific variables
if [ -f "../env/${ENVIRONMENT}.env" ]; then
    export $(cat "../env/${ENVIRONMENT}.env" | grep -v '^#' | xargs)
fi

# Install Python dependencies
echo "Installing Python dependencies..."
cd "$BACKEND_DIR"
pip install -r requirements.txt

# Run database migrations if needed
echo "Running database migrations..."
# Add migration commands here

# Build COBOL programs
echo "Building COBOL programs..."
bash ../infrastructure/scripts/build_cobol.sh

# Start the application (adjust based on deployment target)
echo "Starting application..."
# For production, use gunicorn or similar
# gunicorn api.main:app --workers 4 --bind 0.0.0.0:8000

echo "Deployment complete!"
