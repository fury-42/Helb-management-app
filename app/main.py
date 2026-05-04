from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.settings import settings
from app.shared.exceptions import AppException, app_exception_handler
from app.core.logging_config import setup_logging
from app.core.rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
import time

# Initialize logging
logger = setup_logging()

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

    # Register rate limiter
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Register global exception handlers
    app.add_exception_handler(AppException, app_exception_handler)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        
        logger.info(
            f"Method: {request.method} Path: {request.url.path} "
            f"Status: {response.status_code} Duration: {process_time:.2f}ms"
        )
        return response

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled exception occurred: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    @app.get("/")
    def root():
        return {"message": f"{settings.APP_NAME} API is running"}

    # Register routers
    from app.apps.users.routes import router as users_router
    from app.apps.auth.routes import router as auth_router
    from app.apps.semester.routes import router as semester_router
    from app.apps.budget.routes import router as budget_router
    from app.apps.expenses.routes import router as expenses_router
    from app.apps.emergency.routes import router as emergency_router
    from app.apps.debts.routes import router as debts_router
    from app.apps.payments.routes import router as payments_router
    
    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(semester_router)
    app.include_router(budget_router)
    app.include_router(expenses_router)
    app.include_router(emergency_router)
    app.include_router(debts_router)
    app.include_router(payments_router)
    
    return app

app = create_app()
