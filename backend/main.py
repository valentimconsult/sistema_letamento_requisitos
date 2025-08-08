from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
import os
import logging
from typing import List

from app.core.config import settings
from app.core.database import engine, Base
from app.core.security import get_current_user
from app.api.v1.api import api_router
from app.core.logging import setup_logging

# Configurar logging
setup_logging()

# Criar tabelas do banco de dados
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    logging.info("Aplicacao iniciada com sucesso")
    yield
    # Shutdown
    logging.info("Aplicacao finalizada")

# Criar instancia do FastAPI
app = FastAPI(
    title="Sistema BI - API de Requisitos",
    description="API para gerenciamento de requisitos em projetos de Business Intelligence",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar middleware de hosts confiaveis
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Em producao, especificar hosts permitidos
)

# Incluir rotas da API
app.include_router(api_router, prefix="/api/v1")

# Rota de health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "sistema-bi-api"
    }

# Rota raiz
@app.get("/")
async def root():
    return {
        "message": "Sistema BI - API de Requisitos",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
