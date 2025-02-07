from .session import SessionLocal, engine, Base, get_db

# Exporta as configurações do banco de dados para facilitar a importação
__all__ = ["SessionLocal", "engine", "Base", "get_db"]