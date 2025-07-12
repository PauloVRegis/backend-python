from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import structlog
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from config import get_settings
from app.database.session import init_db
from app.middleware.auth import auth_middleware, security_middleware, limiter, RateLimitExceeded
from app.utils.logger import get_logger
from app.utils.cache import cache_service

# Import routers
from .routers import users, professors, training, auth, exercises

settings = get_settings()
logger = get_logger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting SmartForce application")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down SmartForce application")

# Create FastAPI app with optimizations
app = FastAPI(
    title="SmartForce - Workout Training App",
    description="A comprehensive workout training application with user management and exercise tracking",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add rate limiting exception handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )

# Add global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Request tracking middleware
@app.middleware("http")
async def track_requests(request: Request, call_next):
    start_time = time.time()
    
    # Add request ID
    request.state.request_id = str(time.time())
    
    try:
        response = await call_next(request)
        
        # Record metrics
        duration = time.time() - start_time
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        REQUEST_LATENCY.observe(duration)
        
        # Add security headers
        response.headers["X-Request-ID"] = request.state.request_id
        response.headers["X-Response-Time"] = str(duration)
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Request failed: {e}", exc_info=True)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=500
        ).inc()
        REQUEST_LATENCY.observe(duration)
        raise

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

# Metrics endpoint for Prometheus
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Root endpoint
@app.get("/")
async def read_root():
    """Root endpoint with app information"""
    return {
        "message": "Welcome to SmartForce!",
        "version": "1.0.0",
        "docs": "/docs" if settings.debug else None,
        "health": "/health"
    }

# Include routers
app.include_router(
    auth.router,
    prefix="/api/v1",
    tags=["authentication"]
)

app.include_router(
    users.router,
    prefix="/api/v1",
    tags=["users"]
)

app.include_router(
    professors.router,
    prefix="/api/v1",
    tags=["professors"]
)

app.include_router(
    training.router,
    prefix="/api/v1",
    tags=["training"]
)

app.include_router(
    exercises.router,
    prefix="/api/v1",
    tags=["exercises"]
)

# Add rate limiter to app state
app.state.limiter = limiter