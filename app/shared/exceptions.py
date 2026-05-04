from fastapi import FastAPI
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

from loguru import logger

def app_exception_handler(request, exc: AppException):
    logger.warning(f"AppException: {exc.message} (Status: {exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
