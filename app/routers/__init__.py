from .auth import router as auth_router
from .users import router as users_router
from .professors import router as professors_router

# Exporta os roteadores para facilitar a importação
__all__ = ["auth_router", "users_router", "professors_router"]