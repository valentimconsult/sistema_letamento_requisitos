from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, projects, requirements, dynamic_fields, reports, upload

api_router = APIRouter()

# Incluir rotas de autenticacao
api_router.include_router(auth.router, prefix="/auth", tags=["autenticacao"])

# Incluir rotas de usuarios
api_router.include_router(users.router, prefix="/users", tags=["usuarios"])

# Incluir rotas de projetos
api_router.include_router(projects.router, prefix="/projects", tags=["projetos"])

# Incluir rotas de requisitos
api_router.include_router(requirements.router, prefix="/requirements", tags=["requisitos"])

# Incluir rotas de campos dinamicos
api_router.include_router(dynamic_fields.router, prefix="/dynamic-fields", tags=["campos-dinamicos"])

# Incluir rotas de relatorios
api_router.include_router(reports.router, prefix="/reports", tags=["relatorios"])

# Incluir rotas de upload
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
