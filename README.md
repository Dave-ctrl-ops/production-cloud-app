Production-cloud-app
A production-oriented FastAPI application deployed on Microsoft Azure with PostgreSQL, Docker, and GitHub Actions.

Overview:
This project is a task management REST API built with FastAPI and PostgreSQL.
It was developed to learn and implement a production-style cloud workflow, including containerization, automated testing, CI/CD, database migrations, and Azure deployment.

Tech Stack:
Python
FastAPI
PostgreSQL
Docker & Docker Compose
GitHub Actions
Azure App Service
Azure Container Registry
Azure Database for PostgreSQL
Pydantic
pytest

Features:
CRUD task API
API input validation
PostgreSQL database
Database migrations
Automated testing
Dockerized development
GitHub Actions CI/CD
Azure cloud deployment
Production health check

Architecture:

GitHub
   ↓
GitHub Actions
   ↓
Docker
   ↓
Azure Container Registry
   ↓
Azure App Service
   ↓
FastAPI
   ↓
Azure PostgreSQL

API:

GET     /tasks
POST    /tasks
PUT     /tasks/{task_id}
DELETE  /tasks/{task_id}
GET     /health

Author:
Dev K K
