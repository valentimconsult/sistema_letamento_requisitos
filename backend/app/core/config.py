from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Configuracoes do banco de dados
    DATABASE_URL: str = "postgresql://admin:admin123@postgres:5432/sistema_bi"
    
    # Configuracoes de seguranca
    SECRET_KEY: str = "sua_chave_secreta_muito_segura_aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuracoes de CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:4000", 
        "http://localhost:80", 
        "http://localhost:3000",
        "http://127.0.0.1:4000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:80"
    ]
    
    # Configuracoes de email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Configuracoes de log
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Configuracoes de seguranca adicional
    RATE_LIMIT_PER_MINUTE: int = 60
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15
    
    # Configuracoes de upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Criar instancia das configuracoes
settings = Settings()

# Garantir que o diretorio de uploads existe
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)
