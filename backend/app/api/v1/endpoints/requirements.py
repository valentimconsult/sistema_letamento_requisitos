from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.user import User
from app.models.project import Project
from app.models.requirement import Requirement
from app.schemas.requirement import RequirementCreate, RequirementUpdate, RequirementResponse, RequirementResponseSummary, RequirementFilter

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/", response_model=List[RequirementResponseSummary])
async def get_requirements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    project_id: Optional[str] = None,
    type: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    complexity: Optional[str] = None,
    assigned_to: Optional[str] = None,
    created_by: Optional[str] = None,
    is_overdue: Optional[bool] = None,
    current_user: User = Depends(require_permissions(["requirement:read"])),
    db: Session = Depends(get_db)
):
    """Lista todos os requisitos com filtros"""
    try:
        query = db.query(Requirement)
        
        # Aplicar filtros
        if search:
            query = query.filter(
                Requirement.title.contains(search) |
                Requirement.description.contains(search)
            )
        
        if project_id:
            query = query.filter(Requirement.project_id == project_id)
        
        if type:
            query = query.filter(Requirement.type == type)
        
        if priority:
            query = query.filter(Requirement.priority == priority)
        
        if status:
            query = query.filter(Requirement.status == status)
        
        if complexity:
            query = query.filter(Requirement.complexity == complexity)
        
        if assigned_to:
            query = query.filter(Requirement.assigned_to == assigned_to)
        
        if created_by:
            query = query.filter(Requirement.created_by == created_by)
        
        if is_overdue is not None:
            if is_overdue:
                # Requisitos atrasados
                query = query.filter(
                    Requirement.due_date < datetime.utcnow(),
                    Requirement.status.notin_(["concluido", "cancelado"])
                )
            else:
                # Requisitos nao atrasados
                query = query.filter(
                    (Requirement.due_date >= datetime.utcnow()) |
                    (Requirement.due_date.is_(None)) |
                    (Requirement.status.in_(["concluido", "cancelado"]))
                )
        
        # Ordenar por data de criacao (mais recentes primeiro)
        query = query.order_by(Requirement.created_at.desc())
        
        # Paginacao
        requirements = query.offset(skip).limit(limit).all()
        
        return requirements
        
    except Exception as e:
        logger.error(f"Erro ao listar requisitos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/{requirement_id}", response_model=RequirementResponse)
async def get_requirement(
    requirement_id: str,
    current_user: User = Depends(require_permissions(["requirement:read"])),
    db: Session = Depends(get_db)
):
    """Obtem um requisito especifico"""
    try:
        requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
        
        if not requirement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requisito nao encontrado"
            )
        
        return requirement
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter requisito: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/", response_model=RequirementResponse, status_code=status.HTTP_201_CREATED)
async def create_requirement(
    requirement_data: RequirementCreate,
    current_user: User = Depends(require_permissions(["requirement:create"])),
    db: Session = Depends(get_db)
):
    """Cria um novo requisito"""
    try:
        # Verificar se o projeto existe
        project = db.query(Project).filter(Project.id == requirement_data.project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto nao encontrado"
            )
        
        # Verificar se o usuario atribuido existe
        if requirement_data.assigned_to:
            assigned_user = db.query(User).filter(User.id == requirement_data.assigned_to).first()
            if not assigned_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Usuario atribuido nao encontrado"
                )
        
        # Criar novo requisito
        requirement = Requirement(
            title=requirement_data.title,
            description=requirement_data.description,
            type=requirement_data.type,
            priority=requirement_data.priority,
            status=requirement_data.status,
            complexity=requirement_data.complexity,
            estimated_hours=requirement_data.estimated_hours,
            actual_hours=requirement_data.actual_hours,
            due_date=requirement_data.due_date,
            completion_date=requirement_data.completion_date,
            dynamic_fields=requirement_data.dynamic_fields,
            project_id=requirement_data.project_id,
            assigned_to=requirement_data.assigned_to,
            created_by=current_user.id
        )
        
        db.add(requirement)
        db.commit()
        db.refresh(requirement)
        
        logger.info(f"Requisito criado por {current_user.username}: {requirement.title}")
        return requirement
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar requisito: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.put("/{requirement_id}", response_model=RequirementResponse)
async def update_requirement(
    requirement_id: str,
    requirement_data: RequirementUpdate,
    current_user: User = Depends(require_permissions(["requirement:update"])),
    db: Session = Depends(get_db)
):
    """Atualiza um requisito"""
    try:
        requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
        
        if not requirement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requisito nao encontrado"
            )
        
        # Verificar permissoes (apenas criador, atribuido ou admin pode editar)
        can_edit = (
            requirement.created_by == current_user.id or
            requirement.assigned_to == current_user.id or
            current_user.has_permission("requirement:admin")
        )
        
        if not can_edit:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nao tem permissao para editar este requisito"
            )
        
        # Verificar se o usuario atribuido existe
        if requirement_data.assigned_to:
            assigned_user = db.query(User).filter(User.id == requirement_data.assigned_to).first()
            if not assigned_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Usuario atribuido nao encontrado"
                )
        
        # Atualizar campos
        update_data = requirement_data.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(requirement, field, value)
        
        db.commit()
        db.refresh(requirement)
        
        logger.info(f"Requisito atualizado por {current_user.username}: {requirement.title}")
        return requirement
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar requisito: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.delete("/{requirement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_requirement(
    requirement_id: str,
    current_user: User = Depends(require_permissions(["requirement:delete"])),
    db: Session = Depends(get_db)
):
    """Deleta um requisito"""
    try:
        requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
        
        if not requirement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requisito nao encontrado"
            )
        
        # Verificar permissoes (apenas criador ou admin pode deletar)
        if requirement.created_by != current_user.id and not current_user.has_permission("requirement:admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nao tem permissao para deletar este requisito"
            )
        
        db.delete(requirement)
        db.commit()
        
        logger.info(f"Requisito deletado por {current_user.username}: {requirement.title}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar requisito: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/{requirement_id}/assign/{user_id}")
async def assign_requirement(
    requirement_id: str,
    user_id: str,
    current_user: User = Depends(require_permissions(["requirement:update"])),
    db: Session = Depends(get_db)
):
    """Atribui um requisito a um usuario"""
    try:
        requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
        
        if not requirement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requisito nao encontrado"
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario nao encontrado"
            )
        
        requirement.assigned_to = user_id
        db.commit()
        
        logger.info(f"Requisito atribuido por {current_user.username}: {requirement.title} -> {user.username}")
        return {"message": "Requisito atribuido com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atribuir requisito: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/{requirement_id}/complete")
async def complete_requirement(
    requirement_id: str,
    current_user: User = Depends(require_permissions(["requirement:update"])),
    db: Session = Depends(get_db)
):
    """Marca um requisito como concluido"""
    try:
        requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
        
        if not requirement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requisito nao encontrado"
            )
        
        requirement.status = "concluido"
        requirement.completion_date = datetime.utcnow()
        db.commit()
        
        logger.info(f"Requisito concluido por {current_user.username}: {requirement.title}")
        return {"message": "Requisito marcado como concluido"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao concluir requisito: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
