import structlog
import logging
import sys
from typing import Any, Dict
from config import get_settings

settings = get_settings()

def setup_logging():
    """Setup structured logging with different configurations for dev/prod"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.environment == "production" 
            else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )

    # Set specific loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.DEBUG if settings.debug else logging.WARNING
    )

def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)

class RequestLogger:
    """Middleware logger for HTTP requests"""
    
    def __init__(self):
        self.logger = get_logger("http")
    
    def log_request(self, request_id: str, method: str, url: str, 
                   status_code: int, duration: float, user_id: str = None):
        """Log HTTP request details"""
        self.logger.info(
            "HTTP Request",
            request_id=request_id,
            method=method,
            url=url,
            status_code=status_code,
            duration=duration,
            user_id=user_id
        )
    
    def log_error(self, request_id: str, error: Exception, 
                  method: str, url: str, user_id: str = None):
        """Log HTTP errors"""
        self.logger.error(
            "HTTP Error",
            request_id=request_id,
            error=str(error),
            error_type=type(error).__name__,
            method=method,
            url=url,
            user_id=user_id
        )

# Initialize logging
setup_logging() 