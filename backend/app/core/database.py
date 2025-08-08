from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

# Criar engine do banco de dados
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False  # Set to True for SQL debugging
)

# Criar sessao do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Dependency para obter sessao do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logging.error(f"Erro na sessao do banco: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Funcao para verificar conexao com banco
def check_database_connection():
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        logging.info("Conexao com banco de dados estabelecida com sucesso")
        return True
    except Exception as e:
        logging.error(f"Erro ao conectar com banco de dados: {e}")
        return False
