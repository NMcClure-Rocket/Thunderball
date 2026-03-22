---
description: Running Spellstack API for local development and testing, including prerequisites, setup instructions, and troubleshooting tips.
---

# Running Spellstack API

Configure and run the Spellstack API locally for development and testing. Spellstack API is built with FastAPI and serves as the backend for the Spellstack commerce platform.

## Prerequisites

Before you begin, install the following tools:

- Python 3.11 or newer
- FastAPI and Uvicorn
- IBM Db2 client and Db2 Connect license

!!! info "info"
    Fast API and Uvicorn can be installed through the `requirements.txt` file in the backend folder.

## Database configuration

The API connects to an IBM Db2 database for inventory and transaction data. Connection settings are defined in `backend/config/settings.yaml`. You will need to update the `db2` section of the configuration with your local database connection details, including host, port, database name, username, and password.

Database credentials are not stored in `settings.yaml` and must be provided through environment variables. Ensure your local Db2 instance is running and accessible before starting the backend.

## Local service overview

The Spellstack API runs on `http://localhost:8000` and provides RESTful endpoints for the frontend client to access the product catalog, inventory data, and purchase workflows. The frontend development server runs separately on `http://localhost:3000` and communicates with the API for all backend interactions.

## Project setup

1. Open a PowerShell terminal for the frontend and run:

    ```powershell
       cd frontend
       npm install
       npm run dev
    ```

1. Open a second PowerShell terminal for the backend and run:

    ```powershell
       cd backend
       python -m venv .venv
       .\venv\Scripts\Activate
       pip install -r requirements.txt
       py -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
    ```

1. Keep both terminals running while developing so the frontend and backend stay live.

## Verification

After both services are running, confirm the API is up:

1. Call the backend health endpoint:

    ```powershell
    curl http://localhost:8000/health
    ```

    Expected response:

    ```json
    {"status": "healthy"}
    ```

2. Open the interactive API docs in your browser at `http://localhost:8000/docs`. FastAPI automatically generates this page from the application routes and is useful for manual endpoint testing without a frontend.

3. Open the frontend at `http://localhost:3000` to confirm the client application is running and able to reach the backend.

## API response conventions

**Status codes**  

| Status | Meaning in this API |
| --- | --- |
| 200 OK | Request accepted and processed successfully |
| 400 Bad Request | Invalid request shape, field type, or missing required input |
| 401 Unauthorized | Credential failure for /logon |
| 404 Not Found | Resource not found |

## Troubleshooting

**Port already in use**  

- If port 8000 is already in use, stop the existing process or run uvicorn on a different port.
- If port 3000 is already in use, restart the frontend with a different dev port.

**Virtual environment activation fails on Windows**  

- If PowerShell blocks script execution, run PowerShell as administrator and update execution policy as needed.

**Dependency installation issues**  

- Upgrade pip before installing requirements.
- Recreate the virtual environment if package resolution fails.

**Locating log output**  

- The backend writes logs to `backend/logs/app.log`. If that file does not exist, the `logs/` directory may need to be created manually inside the `backend` folder before starting the server.
- Console output at INFO level is also printed to the terminal where uvicorn is running.
