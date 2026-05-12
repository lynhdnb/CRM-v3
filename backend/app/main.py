"""
CRM Edu - Backend Entry Point
FastAPI application initialization
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.auth.api import router as auth_router
from app.modules.users.api import router as users_router
from app.modules.courses.api import router as courses_router
from app.modules.organizations.api import router as organizations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("🚀 Application startup")
    yield
    print("🛑 Application shutdown")


app = FastAPI(
    title="CRM Edu API",
    description="Educational CRM for music schools and training centers",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(courses_router, prefix="/api/v1")
print("🔍 DEBUG: organizations_router подключается")
app.include_router(organizations_router, prefix="/api/v1")  # ← эта строка подключает организации


@app.get("/api/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "ok", "service": "crm-edu-backend"}


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "CRM Edu API is running",
        "docs": "/api/docs",
        "version": "0.1.0",
    }