# Thunderball Documentation

Welcome to the Thunderball project documentation.

## Project Overview

Thunderball is a full-stack application that integrates:
- **Frontend**: React + TypeScript (Vite)
- **Backend**: Python (FastAPI) with COBOL module integration
- **Database**: IBM Db2
- **DevOps**: CI/CD pipelines, automated testing

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │─────▶│   FastAPI    │─────▶│   COBOL     │
│  Frontend   │      │   Backend    │      │  Modules    │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │    Db2      │
                     │  Database   │
                     └─────────────┘
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- IBM Db2 database
- COBOL compiler (GnuCOBOL or IBM COBOL)

### Development Setup

1. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   python -m uvicorn api.main:app --reload
   ```

3. **Database Setup**
   ```bash
   cd infrastructure/scripts
   bash db2_migrate.sh dev
   ```

## Directory Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed directory structure and component descriptions.

## Development Workflow

See [DEVELOPMENT.md](DEVELOPMENT.md) for development guidelines and best practices.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions.

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
