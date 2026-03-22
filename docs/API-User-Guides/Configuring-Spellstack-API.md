---
description: Configuring Spellstack API for local development and testing, including prerequisites, setup instructions, and troubleshooting tips.
---

# Configuring Spellstack API

Configure and run the Spellstack API locally for development and testing. Spellstack API is built with FastAPI and serves as the backend for the Spellstack commerce platform.

## Prerequisites

Before you begin, install the following tools:

- Python 3.11 or newer
- FastAPI and Uvicorn which can be installed from `backend/requirements.txt`
- IBM Db2 client and Db2 Connect license

## Local service overview

- Backend API: `http://localhost:8000`
- Frontend dev server: `http://localhost:3000`

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
