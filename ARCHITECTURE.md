# FastAPI Backend Architecture Guide (From Zero Production-Ready → Structure)

## 1. Objective

This guide teaches you how to:
- Start a backend project from an empty folder
- Structure it properly from day one
- Build features in a consistent, scalable way

*"Discipline in structure early prevents chaos later."*

## 2. Start From an Empty Folder

Assume you have a new project directory: `backend/`

## 3. Step 1: Create the Base Structure

Create the following folders and files:

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── settings.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── apps/
│   │
│   ├── shared/
│   │   ├── utils.py
│   │   └── exceptions.py
│
└── tests/
```

## 4. Step 2: Core Layer (System Foundation)

The core folder contains system-wide logic used everywhere.

### 4.1 database.py (Database Setup)

```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://user:password@localhost:5432/dbname"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**What is happening here:**
- `engine` connects your app to the database
- `SessionLocal` creates sessions (conversations with the DB)
- `Base` is the parent class for all models
- `get_db()` creates a new DB session per request and safely closes it

Without this file, your app cannot talk to the database correctly.

### 4.2 settings.py (Configuration)

```python
# app/core/settings.py
class Settings:
    APP_NAME = "My Backend"
    DEBUG = True
    DATABASE_URL = "postgresql://user:password@localhost:5432/dbname"


settings = Settings()
```

**What is happening here:**
- Central place for configuration
- Prevents hardcoding values across files
- Later, you can load environment variables here

### 4.3 security.py (Optional Early Setup)

```python
# app/core/security.py
def hash_password(password: str):
    return password  # replace with real hashing later
```

**What is happening here:**
- This will contain authentication logic
- Keeps security separate from business logic

## 5. Step 3: main.py (Application Entry Point)

```python
# app/main.py
from fastapi import FastAPI

app = FastAPI(title="My Backend")

@app.get("/")
def root():
    return {"message": "API is running"}
```

**What is happening here:**
- Creates the FastAPI application
- This is the starting point of your system
- Every request enters through this file

## 6. Step 4: Create Your First Feature (Users App)

`app/apps/users/`

Inside it:

```text
users/
├── models.py
├── schemas.py
├── repository.py
├── service.py
├── routes.py
└── providers.py
```

**What is happening here:**
You are creating a self-contained feature module. Each feature:
- owns its data
- owns its logic
- owns its API

## 7. Build Flow for Every Feature

Always follow this order:

### 7.1 models.py (Define Database Structure First)

```python
# app/apps/users/models.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
```

**What is happening here:**
- Defines the database table
- This is the foundation of your feature
- Everything else depends on this structure

### 7.2 schemas.py (Define Input/Output)

```python
# app/apps/users/schemas.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True
```

**What is happening here:**
- Validates incoming data
- Controls outgoing data
- Protects your system from invalid input

### 7.3 repository.py (Database Access Only)

```python
# app/apps/users/repository.py
from .models import User

class UserRepository:
    def create(self, db, data):
        user = User(**data.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_by_email(self, db, email):
        return db.query(User).filter(User.email == email).first()
```

**What is happening here:**
- Executes database operations
- Translates Python objects to database records
- Does NOT make decisions

### 7.4 service.py (Business Logic)

```python
# app/apps/users/service.py
class UserService:
    def __init__(self, repo):
        self.repo = repo

    def create_user(self, db, data):
        existing = self.repo.get_by_email(db, data.email)
        if existing:
            raise Exception("User already exists")
        return self.repo.create(db, data)
```

**What is happening here:**
- Applies rules (no duplicate users)
- Controls system behavior
- Decides what should happen

### 7.5 providers.py (Dependency Injection)

```python
# app/apps/users/providers.py
from .service import UserService
from .repository import UserRepository

def get_user_service():
    return UserService(UserRepository())
```

**What is happening here:**
- Creates objects (services)
- Supplies them to routes automatically
- Keeps object creation consistent

### 7.6 routes.py (API Layer)

```python
# app/apps/users/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import UserCreate, UserResponse
from .providers import get_user_service
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    service = Depends(get_user_service)
):
    return service.create_user(db, data)
```

**What is happening here:**
- Receives HTTP request
- Validates input
- Calls service layer
- Returns response
This is the entry point into your system.

## 8. Step 5: Register Feature in main.py

```python
from fastapi import FastAPI
from app.apps.users.routes import router as user_router

app = FastAPI()
app.include_router(user_router)
```

**What is happening here:**
- Connects your feature to the main app
- Makes endpoints accessible
Without this, your routes won't work.

## 9. Step 6: Create Database Tables

```python
from app.core.database import Base, engine
from app.apps.users.models import User

Base.metadata.create_all(bind=engine)
```

**What is happening here:**
- Reads models
- Creates tables in the database

**Where Alembic Fits:**
- Tracks database changes over time
- Replaces `create_all` in production
- Prevents data loss

**Connection:** `models.py` → `Base` → `Alembic` → `Database`

## 10. Full Request Flow (Understand This Deeply)

**Request:** `POST /users`

**Flow:**
1. Route receives request
2. Schema validates data
3. Route calls service
4. Service applies logic
5. Service calls repository
6. Repository talks to database
7. Response returns back

**Key Idea:** Each layer does one job only.

## 11. Rules (Must Follow Always)

**Rule 1: Routes are thin**
- **Explanation:** Routes should only: accept requests, call services, return responses.
- **Why:** Keeps endpoints simple and reusable.

**Rule 2: Services contain logic**
- **Explanation:** All decisions belong here: validation rules, workflows.
- **Why:** Centralizes logic and avoids duplication.

**Rule 3: Repository handles database**
- **Explanation:** Only database queries happen here.
- **Why:** Separates data access from logic.

**Rule 4: Models define structure**
- **Explanation:** Models only describe tables.
- **Why:** Prevents tight coupling.

**Rule 5: Schemas validate data**
- **Explanation:** Schemas filter input/output.
- **Why:** Protects system integrity.

## 12. How to Build Any Feature

**What is happening here:**
This is your repeatable system.

**Steps:**
1. Create app folder
2. Define models
3. Define schemas
4. Write repository
5. Write service
6. Write routes
7. Register in `main`

## 13. Final Mental Model

**Routes → Service → Repository → Database**

**What this means:**
- Each layer passes responsibility forward
- Each layer reduces complexity

---

## FastAPI Backend Folder Structure Example

```text
backend/
│
├── app/                          # Main application folder
│   ├── main.py                   # Starts the FastAPI app, registers all routes, middleware, and startup tasks
│   │
│   ├── core/                     # System-wide files used by the whole project
│   │   ├── settings.py           # App settings like project name, environment, database URL, secret keys
│   │   ├── database.py           # Database connection, session creation, Base model, get_db dependency
│   │   └── security.py           # Password hashing, token logic, authentication helpers
│   │
│   ├── apps/                     # Each feature of the system lives here as its own app
│   │   ├── users/                # Users feature
│   │   │   ├── models.py          # Database table structure for users
│   │   │   ├── schemas.py         # Request and response validation for users
│   │   │   ├── repository.py      # Database queries for users only
│   │   │   ├── service.py        # Business rules and logic for users only
│   │   │   ├── routes.py         # HTTP endpoints for users
│   │   │   └── providers.py      # Functions that create and provide services, repos, or other shared objects
│   │   │
│   │   ├── payments/              # Payments feature
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── repository.py
│   │   │   ├── service.py
│   │   │   ├── routes.py
│   │   │   └── providers.py
│   │   │
│   │   └── bookings/              # Another feature, same pattern
│   │       ├── models.py
│   │       ├── schemas.py
│   │       ├── repository.py
│   │       ├── service.py
│   │       ├── routes.py
│   │       └── providers.py
│   │
│   ├── shared/                   # Reusable code used across multiple apps
│   │   ├── utils.py              # Helper functions used in many places
│   │   ├── exceptions.py         # Custom errors and error handlers
│   │   └── middleware.py         # Middleware for logging, timing, auth, etc.
│   │
│   └── __init__.py               # Makes app a Python package
│
├── tests/                        # Tests for the whole project
│   ├── test_users.py
│   ├── test_payments.py
│   └── test_bookings.py
│
├── alembic/                      # Database migration files
├── alembic.ini                   # Alembic configuration
├── requirements.txt              # Project dependencies
├── .env                          # Environment variables
└── README.md                     # Project notes and setup instructions
```

### What is happening in this structure

The project is split into layers so each part has one job. `main.py` starts the application and connects everything together.

`core/` stores the global foundation of the app:
- settings
- database connection
- security helpers

`apps/` stores the real features of the system. Each feature has its own folder and its own files. That means `users` code stays inside `users/`, `payments` code stays inside `payments/`, and so on.

Inside each app:
- `models.py` defines what data exists in the database.
- `schemas.py` defines what data is allowed to enter and leave through the API.
- `repository.py` handles database queries only.
- `service.py` handles logic and rules.
- `routes.py` handles HTTP requests and responses.
- `providers.py` creates and supplies objects like services and repositories.

`shared/` contains code reused by many apps so you do not repeat yourself.

`tests/` stores automated tests so you can check that features still work after changes.

`alembic/` and `alembic.ini` handle database migrations, so database changes can be tracked safely over time.

---

## How a senior engineer would start this from beginning to end

A senior engineer does not start by writing endpoints first. They start by defining the boundaries of the system.

### 1. Decide the feature boundaries

They first ask:
- What are the main business areas?
- What should be its own app?
- What should stay shared?

For example:
- users
- payments
- bookings

They do this first because clean boundaries prevent messy code later.

### 2. Create the base project skeleton

They create:
- `app/`
- `core/`
- `apps/`
- `shared/`
- `tests/`

This gives the project a predictable shape before any logic is added.

### 3. Set up core systems

They build:
- `settings.py`
- `database.py`
- `security.py`

This is the foundation. Without this, every app would solve setup differently, which creates chaos.

### 4. Build one feature at a time

They do not build everything at once. They choose one feature, for example `users`, and complete its full path:
- model
- schema
- repository
- service
- routes
- providers

Only after that feature is working do they move to the next one.

### 5. Keep routes thin

The senior engineer keeps routes simple. Routes should only:
- receive requests
- call services
- return responses

They do not put business rules inside routes.

### 6. Put all decisions in services

All rules live in the service layer. That is where they check:
- duplicates
- permissions
- calculations
- workflow logic

This keeps the app easy to test and easy to change.

### 7. Put database queries in repositories

The repository layer only talks to the database. No business rules. No HTTP logic. No validation logic. This gives the system clean separation.

### 8. Use providers for clean object creation

Instead of creating everything manually inside routes, they use providers to supply services and repositories in a clean and repeatable way.

### 9. Add migrations early

A senior engineer does not rely on manual table creation for long. They use Alembic from early on so database changes are recorded properly.

### 10. Add tests as features grow

They write tests for:
- services
- repositories
- routes

That way they can change code without fear of breaking things.

---

## Checklist a senior engineer would use

### Project setup
- [ ] Project folder created
- [ ] `app/` folder created
- [ ] `core/`, `apps/`, `shared/`, and `tests/` folders created
- [ ] `main.py` created
- [ ] environment variables set up
- [ ] database connection configured

### Core foundation
- [ ] `settings.py` created
- [ ] `database.py` created
- [ ] `security.py` created
- [ ] database session handling works correctly

### Feature structure
- [ ] feature folder created inside `apps/`
- [ ] `models.py` created
- [ ] `schemas.py` created
- [ ] `repository.py` created
- [ ] `service.py` created
- [ ] `routes.py` created
- [ ] `providers.py` created

### Architecture rules
- [ ] routes contain no business logic
- [ ] services contain all business rules
- [ ] repositories only handle database operations
- [ ] schemas validate input and output
- [ ] models only define database structure
- [ ] shared code is not duplicated across apps

### Application wiring
- [ ] routes registered in `main.py`
- [ ] app starts successfully
- [ ] endpoints respond correctly
- [ ] database tables are created through migrations

### Quality control
- [ ] code is readable
- [ ] names are consistent
- [ ] functions do one job only
- [ ] tests exist for key logic
- [ ] changes do not break old features
