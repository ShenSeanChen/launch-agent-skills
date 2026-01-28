# Directory: launch-agent-skills/skills/fastapi-setup/skill.md
---
name: FastAPI Project Setup
description: Scaffold a production-ready FastAPI project with best practices from launch-rag patterns
triggers:
  - fastapi
  - api setup
  - project structure
  - python api
  - backend setup
---

# FastAPI Project Setup Skill

## Purpose

Scaffold a production-ready FastAPI project following proven patterns from [launch-rag](https://github.com/ShenSeanChen/launch-rag) including:
- Clean folder structure (core, services, models, schemas)
- Environment configuration
- Health checks and API documentation
- Docker support
- Type hints and validation

## Project Structure

```
project-name/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Environment & settings
│   │   └── database.py        # Database client & operations
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py        # API request schemas (Pydantic)
│   │   └── responses.py       # API response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   └── [feature].py       # Business logic
│   └── routers/
│       ├── __init__.py
│       └── [feature].py       # API route handlers
├── sql/
│   └── init.sql               # Database initialization
├── static/                    # Static files if needed
├── tests/
│   ├── __init__.py
│   └── test_[feature].py
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── main.py                    # FastAPI app entry point
├── requirements.txt
└── README.md
```

## Instructions

### Step 1: Create Core Files

**main.py** - Application entry point:

```python
# Directory: project-name/main.py
"""
FastAPI application entry point.
Run with: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="API Description",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.APP_NAME}


# Import and include routers
# from app.routers import feature
# app.include_router(feature.router, prefix="/api/v1", tags=["feature"])
```

**app/core/config.py** - Configuration:

```python
# Directory: project-name/app/core/config.py
"""
Application configuration using Pydantic settings.
Loads from environment variables with .env file support.
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # App
    APP_NAME: str = "FastAPI Service"
    DEBUG: bool = False
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Database (Supabase)
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    
    # AI Provider (optional)
    OPENAI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
```

### Step 2: Create Request/Response Models

**app/models/requests.py**:

```python
# Directory: project-name/app/models/requests.py
"""
API request schemas using Pydantic for validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class ExampleRequest(BaseModel):
    """Example request schema."""
    
    query: str = Field(..., description="User query", min_length=1)
    limit: int = Field(default=10, ge=1, le=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "example query",
                "limit": 10
            }
        }
```

**app/models/responses.py**:

```python
# Directory: project-name/app/models/responses.py
"""
API response schemas using Pydantic.
"""

from pydantic import BaseModel
from typing import Optional, List, Any


class ExampleResponse(BaseModel):
    """Example response schema."""
    
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"result": "example"},
                "error": None
            }
        }
```

### Step 3: Create Environment Template

**.env.example**:

```bash
# Application
APP_NAME=FastAPI Service
DEBUG=true

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# AI (optional)
OPENAI_API_KEY=sk-your_key
```

### Step 4: Create Requirements

**requirements.txt**:

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-dotenv>=1.0.0
httpx>=0.26.0
supabase>=2.3.0
```

### Step 5: Create Dockerfile

**Dockerfile**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8080

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## Checklist

When setting up a new FastAPI project:

- [ ] Create folder structure
- [ ] Set up `app/core/config.py` with settings
- [ ] Create `.env.example` with all required variables
- [ ] Add health check endpoint `/healthz`
- [ ] Configure CORS for frontend
- [ ] Create request/response Pydantic models
- [ ] Add Dockerfile for deployment
- [ ] Set up `.gitignore` and `.dockerignore`
- [ ] Write initial README with setup instructions

## Related Skills

- `supabase-setup` - Configure Supabase database integration
