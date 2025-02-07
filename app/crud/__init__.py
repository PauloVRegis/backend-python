from .user import create_user, get_user
from .professor import create_professor, get_professor
from .training import create_training

# Exporta as funções CRUD para facilitar a importação
__all__ = [
    "create_user", "get_user",
    "create_professor", "get_professor",
    "create_training"
]