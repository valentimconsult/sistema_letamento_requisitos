from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.user import User
from app.models.dynamic_field import DynamicFieldDefinition
from app.schemas.dynamic_field import DynamicFieldCreate, DynamicFieldUpdate, DynamicFieldResponse

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/", response_model=List[DynamicFieldResponse])
async def get_dynamic_fields(
    applies_to: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(require_permissions(["dynamic_field:read"])),
    db: Session = Depends(get_db)
):
    """Lista todos os campos dinamicos com filtros"""
    try:
        query = db.query(DynamicFieldDefinition)
        
        # Aplicar filtros
        if applies_to:
            query = query.filter(DynamicFieldDefinition.applies_to == applies_to)
        
        if is_active is not None:
            query = query.filter(DynamicFieldDefinition.is_active == is_active)
        
        # Ordenar por nome do campo
        query = query.order_by(DynamicFieldDefinition.field_name)
        
        fields = query.all()
        
        return fields
        
    except Exception as e:
        logger.error(f"Erro ao listar campos dinamicos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/{field_id}", response_model=DynamicFieldResponse)
async def get_dynamic_field(
    field_id: str,
    current_user: User = Depends(require_permissions(["dynamic_field:read"])),
    db: Session = Depends(get_db)
):
    """Obtem um campo dinamico especifico"""
    try:
        field = db.query(DynamicFieldDefinition).filter(DynamicFieldDefinition.id == field_id).first()
        
        if not field:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campo dinamico nao encontrado"
            )
        
        return field
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter campo dinamico: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/", response_model=DynamicFieldResponse, status_code=status.HTTP_201_CREATED)
async def create_dynamic_field(
    field_data: DynamicFieldCreate,
    current_user: User = Depends(require_permissions(["dynamic_field:create"])),
    db: Session = Depends(get_db)
):
    """Cria um novo campo dinamico"""
    try:
        # Verificar se o campo ja existe
        existing_field = db.query(DynamicFieldDefinition).filter(
            DynamicFieldDefinition.field_name == field_data.field_name,
            DynamicFieldDefinition.applies_to == field_data.applies_to
        ).first()
        
        if existing_field:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campo dinamico ja existe"
            )
        
        # Criar novo campo dinamico
        field = DynamicFieldDefinition(
            field_name=field_data.field_name,
            field_type=field_data.field_type,
            field_label=field_data.field_label,
            field_description=field_data.field_description,
            options=field_data.options,
            is_required=field_data.is_required,
            is_active=field_data.is_active,
            applies_to=field_data.applies_to,
            order_index=field_data.order_index,
            validation_rules=field_data.validation_rules
        )
        
        db.add(field)
        db.commit()
        db.refresh(field)
        
        logger.info(f"Campo dinamico criado por {current_user.username}: {field.field_name}")
        return field
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar campo dinamico: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.put("/{field_id}", response_model=DynamicFieldResponse)
async def update_dynamic_field(
    field_id: str,
    field_data: DynamicFieldUpdate,
    current_user: User = Depends(require_permissions(["dynamic_field:update"])),
    db: Session = Depends(get_db)
):
    """Atualiza um campo dinamico"""
    try:
        field = db.query(DynamicFieldDefinition).filter(DynamicFieldDefinition.id == field_id).first()
        
        if not field:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campo dinamico nao encontrado"
            )
        
        # Verificar se o novo nome ja existe
        if field_data.field_name and field_data.field_name != field.field_name:
            existing_field = db.query(DynamicFieldDefinition).filter(
                DynamicFieldDefinition.field_name == field_data.field_name,
                DynamicFieldDefinition.applies_to == field.applies_to,
                DynamicFieldDefinition.id != field_id
            ).first()
            
            if existing_field:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Campo dinamico ja existe"
                )
        
        # Atualizar campos
        update_data = field_data.dict(exclude_unset=True)
        
        for field_name, value in update_data.items():
            setattr(field, field_name, value)
        
        db.commit()
        db.refresh(field)
        
        logger.info(f"Campo dinamico atualizado por {current_user.username}: {field.field_name}")
        return field
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar campo dinamico: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.delete("/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dynamic_field(
    field_id: str,
    current_user: User = Depends(require_permissions(["dynamic_field:delete"])),
    db: Session = Depends(get_db)
):
    """Deleta um campo dinamico"""
    try:
        field = db.query(DynamicFieldDefinition).filter(DynamicFieldDefinition.id == field_id).first()
        
        if not field:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campo dinamico nao encontrado"
            )
        
        db.delete(field)
        db.commit()
        
        logger.info(f"Campo dinamico deletado por {current_user.username}: {field.field_name}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar campo dinamico: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/{field_id}/activate")
async def activate_dynamic_field(
    field_id: str,
    current_user: User = Depends(require_permissions(["dynamic_field:update"])),
    db: Session = Depends(get_db)
):
    """Ativa um campo dinamico"""
    try:
        field = db.query(DynamicFieldDefinition).filter(DynamicFieldDefinition.id == field_id).first()
        
        if not field:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campo dinamico nao encontrado"
            )
        
        field.is_active = True
        db.commit()
        
        logger.info(f"Campo dinamico ativado por {current_user.username}: {field.field_name}")
        return {"message": "Campo dinamico ativado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao ativar campo dinamico: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/{field_id}/deactivate")
async def deactivate_dynamic_field(
    field_id: str,
    current_user: User = Depends(require_permissions(["dynamic_field:update"])),
    db: Session = Depends(get_db)
):
    """Desativa um campo dinamico"""
    try:
        field = db.query(DynamicFieldDefinition).filter(DynamicFieldDefinition.id == field_id).first()
        
        if not field:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campo dinamico nao encontrado"
            )
        
        field.is_active = False
        db.commit()
        
        logger.info(f"Campo dinamico desativado por {current_user.username}: {field.field_name}")
        return {"message": "Campo dinamico desativado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao desativar campo dinamico: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/initialize-defaults")
async def initialize_default_fields(
    current_user: User = Depends(require_permissions(["dynamic_field:create"])),
    db: Session = Depends(get_db)
):
    """Inicializa os campos dinamicos padrao"""
    try:
        # Verificar se ja existem campos
        existing_count = db.query(DynamicFieldDefinition).count()
        
        if existing_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campos dinamicos ja foram inicializados"
            )
        
        # Criar campos padrao
        default_fields = DynamicFieldDefinition.get_default_fields()
        
        for field_data in default_fields:
            field = DynamicFieldDefinition(
                field_name=field_data["field_name"],
                field_type=field_data["field_type"],
                field_label=field_data["field_label"],
                field_description=field_data["field_description"],
                is_required=field_data["is_required"],
                applies_to=field_data["applies_to"]
            )
            
            if "options" in field_data:
                field.set_options(field_data["options"])
            
            db.add(field)
        
        db.commit()
        
        logger.info(f"Campos dinamicos padrao inicializados por {current_user.username}")
        return {"message": "Campos dinamicos padrao inicializados com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao inicializar campos dinamicos: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
