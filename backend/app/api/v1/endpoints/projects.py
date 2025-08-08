from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.user import User
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectResponseSummary, ProjectFilter

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/", response_model=List[ProjectResponseSummary])
async def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    client_name: Optional[str] = None,
    created_by: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(require_permissions(["project:read"])),
    db: Session = Depends(get_db)
):
    """Lista todos os projetos com filtros"""
    try:
        query = db.query(Project)
        
        # Aplicar filtros
        if search:
            query = query.filter(
                Project.name.contains(search) |
                Project.description.contains(search) |
                Project.client_name.contains(search)
            )
        
        if status:
            query = query.filter(Project.status == status)
        
        if priority:
            query = query.filter(Project.priority == priority)
        
        if client_name:
            query = query.filter(Project.client_name.contains(client_name))
        
        if created_by:
            query = query.filter(Project.created_by == created_by)
        
        if is_active is not None:
            query = query.filter(Project.is_active == is_active)
        
        # Ordenar por data de criacao (mais recentes primeiro)
        query = query.order_by(Project.created_at.desc())
        
        # Paginacao
        projects = query.offset(skip).limit(limit).all()
        
        return projects
        
    except Exception as e:
        logger.error(f"Erro ao listar projetos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: User = Depends(require_permissions(["project:read"])),
    db: Session = Depends(get_db)
):
    """Obtem um projeto especifico"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto nao encontrado"
            )
        
        return project
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter projeto: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(require_permissions(["project:create"])),
    db: Session = Depends(get_db)
):
    """Cria um novo projeto"""
    try:
        # Criar novo projeto
        project = Project(
            name=project_data.name,
            description=project_data.description,
            status=project_data.status,
            priority=project_data.priority,
            start_date=project_data.start_date,
            end_date=project_data.end_date,
            budget=project_data.budget,
            client_name=project_data.client_name,
            is_active=project_data.is_active,
            created_by=current_user.id
        )
        
        db.add(project)
        db.commit()
        db.refresh(project)
        
        logger.info(f"Projeto criado por {current_user.username}: {project.name}")
        return project
        
    except Exception as e:
        logger.error(f"Erro ao criar projeto: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(require_permissions(["project:update"])),
    db: Session = Depends(get_db)
):
    """Atualiza um projeto"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto nao encontrado"
            )
        
        # Verificar permissoes (apenas criador ou admin pode editar)
        if project.created_by != current_user.id and not current_user.has_permission("project:admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nao tem permissao para editar este projeto"
            )
        
        # Atualizar campos
        update_data = project_data.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(project, field, value)
        
        db.commit()
        db.refresh(project)
        
        logger.info(f"Projeto atualizado por {current_user.username}: {project.name}")
        return project
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar projeto: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: User = Depends(require_permissions(["project:delete"])),
    db: Session = Depends(get_db)
):
    """Deleta um projeto"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto nao encontrado"
            )
        
        # Verificar permissoes (apenas criador ou admin pode deletar)
        if project.created_by != current_user.id and not current_user.has_permission("project:admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nao tem permissao para deletar este projeto"
            )
        
        db.delete(project)
        db.commit()
        
        logger.info(f"Projeto deletado por {current_user.username}: {project.name}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar projeto: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/{project_id}/requirements")
async def get_project_requirements(
    project_id: str,
    current_user: User = Depends(require_permissions(["requirement:read"])),
    db: Session = Depends(get_db)
):
    """Lista todos os requisitos de um projeto"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto nao encontrado"
            )
        
        return project.requirements
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao listar requisitos do projeto: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/{project_id}/activate")
async def activate_project(
    project_id: str,
    current_user: User = Depends(require_permissions(["project:update"])),
    db: Session = Depends(get_db)
):
    """Ativa um projeto"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto nao encontrado"
            )
        
        project.is_active = True
        db.commit()
        
        logger.info(f"Projeto ativado por {current_user.username}: {project.name}")
        return {"message": "Projeto ativado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao ativar projeto: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/{project_id}/deactivate")
async def deactivate_project(
    project_id: str,
    current_user: User = Depends(require_permissions(["project:update"])),
    db: Session = Depends(get_db)
):
    """Desativa um projeto"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto nao encontrado"
            )
        
        project.is_active = False
        db.commit()
        
        logger.info(f"Projeto desativado por {current_user.username}: {project.name}")
        return {"message": "Projeto desativado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao desativar projeto: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
