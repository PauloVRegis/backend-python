from .session import SessionLocal, engine, Base

# Exporta as configurações do banco de dados para facilitar a importação
__all__ = ["SessionLocal", "engine", "Base"]