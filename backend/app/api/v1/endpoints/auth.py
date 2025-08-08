from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token, UserResponseSafe, UserPasswordChange

router = APIRouter()
security = HTTPBearer()

logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserResponseSafe, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuario"""
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
        
        logger.info(f"Novo usuario registrado: {user.username}")
        return user
        
    except Exception as e:
        logger.error(f"Erro ao registrar usuario: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Autentica um usuario e retorna token JWT"""
    try:
        # Buscar usuario
        user = db.query(User).filter(User.username == user_credentials.username).first()
        
        if not user:
            logger.warning(f"Tentativa de login falhou para usuario inexistente: {user_credentials.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais invalidas"
            )
        
        # Verificar senha
        if not verify_password(user_credentials.password, user.password_hash):
            logger.warning(f"Tentativa de login falhou para usuario: {user_credentials.username} - senha incorreta")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais invalidas"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inativo"
            )
        
        # Atualizar ultimo login
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Criar token de acesso
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id, "username": user.username},
            expires_delta=access_token_expires
        )
        
        logger.info(f"Login realizado com sucesso para usuario: {user.username}")
        
        # Retornar dados do usuario sem relacionamentos para evitar problemas
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_active": user.is_active,
            "last_login": user.last_login,
            "created_at": user.created_at
        }
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": user_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no login: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/logout")
async def logout(credentials: HTTPBearer = Depends(security)):
    """Logout do usuario (invalida o token no frontend)"""
    # Em uma implementacao mais robusta, adicionaria o token a uma blacklist
    logger.info("Logout realizado")
    return {"message": "Logout realizado com sucesso"}

@router.post("/change-password")
async def change_password(
    password_data: UserPasswordChange,
    current_user: User = Depends(security),
    db: Session = Depends(get_db)
):
    """Altera a senha do usuario atual"""
    try:
        # Verificar senha atual
        if not verify_password(password_data.current_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha atual incorreta"
            )
        
        # Atualizar senha
        current_user.password_hash = get_password_hash(password_data.new_password)
        db.commit()
        
        logger.info(f"Senha alterada para usuario: {current_user.username}")
        return {"message": "Senha alterada com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao alterar senha: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/me", response_model=UserResponseSafe)
async def get_current_user_info(current_user: User = Depends(security)):
    """Retorna informacoes do usuario atual"""
    return current_user

@router.post("/refresh-token", response_model=Token)
async def refresh_token(current_user: User = Depends(security)):
    """Renova o token de acesso"""
    try:
        # Criar novo token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": current_user.id, "username": current_user.username},
            expires_delta=access_token_expires
        )
        
        logger.info(f"Token renovado para usuario: {current_user.username}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": current_user
        }
        
    except Exception as e:
        logger.error(f"Erro ao renovar token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
