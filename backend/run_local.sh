#!/bin/bash

# Run the backend API locally for development

echo "Starting Thunderball Backend API..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Load environment variables
if [ -f "../infrastructure/env/dev.env" ]; then
    export $(cat ../infrastructure/env/dev.env | grep -v '^#' | xargs)
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Run the FastAPI application with hot reload
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
