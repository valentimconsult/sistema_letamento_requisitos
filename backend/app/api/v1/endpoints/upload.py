from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
import uuid
from datetime import datetime
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.user import User
from app.core.config import settings

router = APIRouter()

logger = logging.getLogger(__name__)

# Tipos de arquivo permitidos para logo
ALLOWED_LOGO_TYPES = {
    "image/jpeg",
    "image/jpg", 
    "image/png",
    "image/gif",
    "image/svg+xml"
}

# Tamanho maximo para logo (5MB)
MAX_LOGO_SIZE = 5 * 1024 * 1024

@router.post("/logo")
async def upload_logo(
    file: UploadFile = File(...),
    current_user: User = Depends(require_permissions(["upload:logo"])),
    db: Session = Depends(get_db)
):
    """
    Faz upload de uma logo para o sistema
    """
    try:
        # Validar tipo de arquivo
        if file.content_type not in ALLOWED_LOGO_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de arquivo nao permitido. Use apenas: JPEG, JPG, PNG, GIF ou SVG"
            )
        
        # Validar tamanho do arquivo
        if file.size and file.size > MAX_LOGO_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Arquivo muito grande. Tamanho maximo permitido: {MAX_LOGO_SIZE // (1024*1024)}MB"
            )
        
        # Criar nome unico para o arquivo
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ".png"
        unique_filename = f"logo_{uuid.uuid4().hex}{file_extension}"
        
        # Criar diretorio para logos se nao existir
        logo_dir = os.path.join(settings.UPLOAD_DIR, "logos")
        os.makedirs(logo_dir, exist_ok=True)
        
        # Caminho completo do arquivo
        file_path = os.path.join(logo_dir, unique_filename)
        
        # Salvar arquivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # URL para acessar o arquivo
        file_url = f"/api/v1/upload/logo/{unique_filename}"
        
        logger.info(f"Logo enviada com sucesso por {current_user.username}: {unique_filename}")
        
        return {
            "message": "Logo enviada com sucesso",
            "filename": unique_filename,
            "original_name": file.filename,
            "size": file.size,
            "url": file_url,
            "uploaded_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao fazer upload da logo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao fazer upload"
        )

@router.get("/logo/{filename}")
async def get_logo(
    filename: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retorna uma logo especifica
    """
    try:
        logo_dir = os.path.join(settings.UPLOAD_DIR, "logos")
        file_path = os.path.join(logo_dir, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Logo nao encontrada"
            )
        
        return FileResponse(file_path)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar logo {filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.delete("/logo/{filename}")
async def delete_logo(
    filename: str,
    current_user: User = Depends(require_permissions(["upload:logo"])),
    db: Session = Depends(get_db)
):
    """
    Remove uma logo especifica
    """
    try:
        logo_dir = os.path.join(settings.UPLOAD_DIR, "logos")
        file_path = os.path.join(logo_dir, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Logo nao encontrada"
            )
        
        # Remover arquivo
        os.remove(file_path)
        
        logger.info(f"Logo removida com sucesso por {current_user.username}: {filename}")
        
        return {
            "message": "Logo removida com sucesso",
            "filename": filename
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao remover logo {filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/logo")
async def list_logos(
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista todas as logos disponiveis
    """
    try:
        logo_dir = os.path.join(settings.UPLOAD_DIR, "logos")
        
        if not os.path.exists(logo_dir):
            return {"logos": []}
        
        logos = []
        for filename in os.listdir(logo_dir):
            if filename.startswith("logo_"):
                file_path = os.path.join(logo_dir, filename)
                file_stat = os.stat(file_path)
                
                logos.append({
                    "filename": filename,
                    "url": f"/api/v1/upload/logo/{filename}",
                    "size": file_stat.st_size,
                    "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat()
                })
        
        return {"logos": logos}
        
    except Exception as e:
        logger.error(f"Erro ao listar logos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
