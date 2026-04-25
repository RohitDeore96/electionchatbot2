# Election Assistant - Smart Civic Engagement

## Overview
Welcome to the **Smart Election Assistant**, a state-of-the-art solution designed during the **Virtual PromptWar** by **Antigravity Studio**. This project provides an intelligent guide to the civic engagement process, built with **Google Cloud Run**, FastAPI, React, and **Vertex AI**. By embedding advanced **Prompt Engineering** and rigorous **DevSecOps** practices, we ensure scalable, secure, and neutral election assistance.

## Features
* Gemini chatbot for answering election-related queries with neutral, process-oriented guidance. Designed by **Antigravity Studio** leveraging advanced **Prompt Engineering**.
* Google Maps polling location integration to help users find where to vote securely.
* Strict Content Security Policy (CSP) and active **DevSecOps** hardening to ensure robust frontend security.

## Architecture Flow
The application features a decoupled architecture with a React frontend for the user interface and a Python FastAPI backend for handling logic and API requests. Google Secret Manager is utilized to securely store and access sensitive environment variables.

```mermaid
graph TD
    A[React UI] --> B[FastAPI Backend]
    B --> C[Vertex AI (Gemini 2.5 Flash)]
    B --> D[Google Maps API]
    B --> E[Firestore (Logs)]
```

## Local Setup
1. Install backend dependencies: `cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt` (or `venv\Scripts\activate` on Windows).
2. Install frontend dependencies: `cd frontend && npm install`.
3. Run the backend locally: `uvicorn app.main:app --reload`.
4. Run the frontend locally: `npm run dev`.
