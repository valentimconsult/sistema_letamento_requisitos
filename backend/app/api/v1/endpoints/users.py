from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user, require_permissions, get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserResponseSafe

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/", response_model=List[UserResponseSafe])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(require_permissions(["user:read", "user:admin"])),
    db: Session = Depends(get_db)
):
    """Lista todos os usuarios com filtros"""
    try:
        query = db.query(User)
        
        # Aplicar filtros
        if search:
            query = query.filter(
                User.username.contains(search) |
                User.email.contains(search) |
                User.first_name.contains(search) |
                User.last_name.contains(search)
            )
        
        if role:
            query = query.filter(User.role == role)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        # Ordenar por nome de usuario
        query = query.order_by(User.username)
        
        # Paginacao
        users = query.offset(skip).limit(limit).all()
        
        return users
        
    except Exception as e:
        logger.error(f"Erro ao listar usuarios: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(require_permissions(["user:read", "user:admin"])),
    db: Session = Depends(get_db)
):
    """Obtem um usuario especifico"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario nao encontrado"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter usuario: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(require_permissions(["user:create", "user:admin"])),
    db: Session = Depends(get_db)
):
    """Cria um novo usuario"""
    try:
        # Verificar se o usuario ja existe
        existing_user = db.query(User).filter(
            (User.username == user_data.username) | (User.email == user_data.email)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario ou email ja existe"
            )
        
        # Criar novo usuario
        user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=user_data.role,
            permissions=user_data.permissions,
            is_active=user_data.is_active
        )
        user.password_hash = get_password_hash(user_data.password)
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Usuario criado por {current_user.username}: {user.username}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar usuario: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: User = Depends(require_permissions(["user:update", "user:admin"])),
    db: Session = Depends(get_db)
):
    """Atualiza um usuario"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario nao encontrado"
            )
        
        # Verificar se nao esta tentando alterar um superuser sem ser admin
        if user.is_superuser and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nao e possivel alterar um superusuario"
            )
        
        # Atualizar campos
        update_data = user_data.dict(exclude_unset=True)
        
        # Verificar se username ou email ja existe
        if "username" in update_data or "email" in update_data:
            existing_user = db.query(User).filter(
                User.id != user_id,
                (User.username == update_data.get("username", user.username)) |
                (User.email == update_data.get("email", user.email))
            ).first()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Usuario ou email ja existe"
                )
        
        # Atualizar senha se fornecida
        if "password" in update_data:
            user.password_hash = get_password_hash(update_data["password"])
            del update_data["password"]
        
        # Atualizar outros campos
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        logger.info(f"Usuario atualizado por {current_user.username}: {user.username}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar usuario: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_permissions(["user:delete", "user:admin"])),
    db: Session = Depends(get_db)
):
    """Deleta um usuario"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario nao encontrado"
            )
        
        # Nao permitir deletar o proprio usuario
        if user.id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nao e possivel deletar o proprio usuario"
            )
        
        # Nao permitir deletar superusuarios
        if user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nao e possivel deletar um superusuario"
            )
        
        db.delete(user)
        db.commit()
        
        logger.info(f"Usuario deletado por {current_user.username}: {user.username}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar usuario: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/{user_id}/activate")
async def activate_user(
    user_id: str,
    current_user: User = Depends(require_permissions(["user:update", "user:admin"])),
    db: Session = Depends(get_db)
):
    """Ativa um usuario"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario nao encontrado"
            )
        
        user.is_active = True
        db.commit()
        
        logger.info(f"Usuario ativado por {current_user.username}: {user.username}")
        return {"message": "Usuario ativado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao ativar usuario: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/{user_id}/deactivate")
async def deactivate_user(
    user_id: str,
    current_user: User = Depends(require_permissions(["user:update", "user:admin"])),
    db: Session = Depends(get_db)
):
    """Desativa um usuario"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario nao encontrado"
            )
        
        # Nao permitir desativar o proprio usuario
        if user.id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nao e possivel desativar o proprio usuario"
            )
        
        user.is_active = False
        db.commit()
        
        logger.info(f"Usuario desativado por {current_user.username}: {user.username}")
        return {"message": "Usuario desativado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao desativar usuario: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
