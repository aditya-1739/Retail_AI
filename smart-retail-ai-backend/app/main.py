import logging
import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.db import models
from app.db.session import engine, SessionLocal
from app.routers import (
    product,
    sentiment,
    chatbot,
    face,
    auth
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("app")

# Lifespan for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database Tables
    logger.info("Initializing database tables...")
    try:
        models.Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database tables: {str(e)}", exc_info=True)
    yield
    # Shutdown
    logger.info("Shutting down SmartRetailAI API...")

app = FastAPI(
    title="SmartRetailAI API",
    version="1.0",
    lifespan=lifespan
)

# Custom Middleware for request logging and database auditing
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception as exc:
            logger.error(f"Exception during request: {request.method} {request.url.path} - {str(exc)}", exc_info=True)
            raise exc
        finally:
            duration = time.time() - start_time
            logger.info(
                f"Client: {request.client.host if request.client else 'unknown'} | "
                f"Request: {request.method} {request.url.path} | "
                f"Status: {status_code} | Duration: {duration:.4f}s"
            )
            # Log metadata in RequestHistory table
            db = SessionLocal()
            try:
                db_history = models.RequestHistory(
                    ip_address=request.client.host if request.client else "unknown",
                    method=request.method,
                    path=request.url.path,
                    status_code=status_code
                )
                db.add(db_history)
                db.commit()
            except Exception as e:
                logger.error(f"Failed to save request history to DB: {str(e)}")
            finally:
                db.close()

# Register middleware
app.add_middleware(RequestLoggingMiddleware)

# Configure CORS origins
allowed_origins = settings.ALLOWED_ORIGINS
if isinstance(allowed_origins, str):
    allowed_origins = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(sentiment.router)
app.include_router(chatbot.router)
app.include_router(face.router)

@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Welcome to SmartRetailAI API"
    }

@app.get("/health", tags=["Health"], summary="API Health Check")
def health():
    return {
        "status": "healthy",
        "timestamp": time.time()
    }