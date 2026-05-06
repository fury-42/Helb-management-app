# HELB Management App Backend

A production-grade FastAPI backend designed to help students manage their HELB (Higher Education Loans Board) funds through structured budgeting, expense tracking, and financial planning.

## 🏗 Architecture & Design Patterns

This project follows a strict **Layered Feature-Based Architecture**. Each feature is self-contained within the `app/apps/` directory, adhering to the following flow:

**Route → Service → Repository → Database**

### Layers:
1.  **Routes (`routes.py`)**: Handles HTTP requests/responses. Validates input using Pydantic schemas. **No business logic here.**
2.  **Service (`service.py`)**: Contains business rules and application workflows. Coordinates between repositories and handles notifications/background tasks.
3.  **Repository (`repository.py`)**: Encapsulates all SQLAlchemy queries. **No business rules here.**
4.  **Models (`models.py`)**: Defines the SQLAlchemy database schema.
5.  **Schemas (`schemas.py`)**: Pydantic models for request validation and response formatting.
6.  **Providers (`providers.py`)**: Handles dependency injection for services and repositories.

---

## 📂 Directory Structure

### Root Directory
- `.env`: Environment variables (Database URL, Secret Keys).
- `alembic/`: Database migration scripts and configuration.
- `app/`: Main application source code.
- `requirements.txt`: Project dependencies.
- `verify_fixes.py`: Utility script for verifying core functionality.

### `app/core/`
The system foundation.
- `database.py`: SQLAlchemy engine and session management.
- `settings.py`: Configuration management using `pydantic-settings`.
- `security.py`: JWT authentication and password hashing (Argon2).
- `logging_config.py`: Structured logging using `Loguru`.
- `rate_limiter.py`: API rate limiting using `SlowAPI`.

### `app/shared/`
Reusable utilities across modules.
- `exceptions.py`: Custom application exceptions and handlers.
- `idempotency.py`: Request idempotency logic to prevent duplicate processing.
- `notifications.py`: SMS notification service (Africa's Talking integration).

### `app/apps/` (Feature Modules)
- **`auth/`**: User authentication, login, and token generation.
- **`users/`**: User registration and profile management.
- **`semester/`**: Initialization of HELB funds and duration tracking.
- **`budget/`**: Allocation of funds into categories (Rent, Food, etc.).
- **`expenses/`**: Tracking of daily spending against the budget.
- **`emergency/`**: "Locked" contingency fund management.
- **`debts/`**: Peer-to-peer borrowing and repayment tracking.
- **`payments/`**: M-Pesa STK Push and Bank transfer integrations.
- **`loans/`**: Loan application and approval workflows.

---

## 🚀 Setup & Execution

### 1. Environment Configuration
Create a `.env` file in the root directory:
```env
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
SECRET_KEY="your-super-secret-key"
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Database Migrations
Apply the latest migrations to set up the database schema:
```bash
alembic upgrade head
```

### 4. Running the Application
Start the server using Uvicorn:
```bash
uvicorn app.main:app --reload
```

---

## 🛠 File-by-File Description (Key Files)

| File | Purpose |
| :--- | :--- |
| `app/main.py` | Entry point. Initializes FastAPI, registers routers, and sets up middleware. |
| `app/core/settings.py` | Loads `.env` and defines app-wide configurations. |
| `app/apps/users/models.py` | Defines the `User` table (email, phone, hashed password, role). |
| `app/apps/semester/service.py` | Logic for calculating weeks remaining and formatting semester status. |
| `app/apps/budget/repository.py` | Encapsulates DB logic for allocations and spent amount updates. |
| `app/shared/idempotency.py` | Prevents double-charging or duplicate submissions using `X-Idempotency-Key` header. |
| `app/shared/notifications.py` | Handles background SMS tasks to keep the API responsive. |

---

## 🔒 Security & Performance
- **Rate Limiting**: Protected endpoints limit attempts to prevent brute-force attacks.
- **Idempotency**: Critical operations (like payments) require a unique key.
- **Eager Loading**: Uses `joinedload` in repositories to prevent N+1 query performance issues.
- **Logging**: All requests and exceptions are logged with structured context.
