# Finance FastAPI Application

A robust, modular FastAPI application for managing personal finances, featuring advanced access control, audit logging, and efficient data retrieval.

## Features

- **Modular Architecture**: Clean separation of concerns with `users`, `finance`, and `library` modules.
- **Decorator-based Access Control**: Granular Role-Based Access Control (RBAC) using a custom `AccessRouter` and `@Access(Resource, Action)` decorators.
- **Audit Fields & Soft Delete**: All models include `created_at`, `updated_at`, and `deleted_at` fields for tracking and safe data recovery.
- **Pagination, Filtering, and Search**: List endpoints support `limit`, `offset`, and full-text `search` across relevant fields.
- **Environment-based Seeding**: Automatically seeds initial users and financial data based on `.env` configuration.

## Project Structure

```text
├── finance/             # Finance management module (routers, services, schemas)
├── users/               # User management module (routers, services, schemas)
├── library/             # Shared logic and cross-cutting concerns
│   ├── access/          # Permissions, roles, and custom AccessRouter
│   ├── auth/            # JWT authentication and dependencies
│   ├── db/              # Database models, repositories, and session management
│   └── seeder.py        # Automatic data seeding logic
├── .env                 # Environment configuration
├── main.py              # Application entry point and startup logic
└── requirements.txt     # Python dependencies
```

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- Virtual environment (recommended)

### 2. Installation
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory (one is provided by default) and configure your database and seed user credentials:

```env
# Database
DB_URL=sqlite:///./finance_app.db

# Admin User
ADMIN_NAME=Admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123

# Analyst User
ANALYST_NAME=Analyst
ANALYST_EMAIL=analyst@example.com
ANALYST_PASSWORD=analyst123

# Regular User
USER_NAME=User
USER_EMAIL=user@example.com
USER_PASSWORD=user123
```

### 4. Running the Application
The application will automatically create the database and seed the initial data on startup.

```bash
uvicorn main:app --reload
```

### 5. API Documentation
Once the server is running, you can access the interactive API documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Default Credentials (Seeded)

| Role     | Email                | Password   |
|----------|----------------------|------------|
| Admin    | admin@example.com    | admin123   |
| Analyst  | analyst@example.com  | analyst123 |
| Viewer   | user@example.com     | user123    |

## Core Concepts

### @Access Decorator
Used to protect routes with granular permissions. Example:
```python
@router.get("/", response_model=List[FinanceResponse])
@Access(Resource.Finance, Action.Read)
async def list_finances(...):
    ...
```

### Soft Deletion
When a record is deleted, it is not removed from the database. Instead, `deleted_at` is set to the current timestamp. Repository methods automatically filter out these records during standard queries.
# fastApiFinance
