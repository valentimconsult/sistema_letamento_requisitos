from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional, Dict, Any
import logging
import pandas as pd
from datetime import datetime, timedelta
import os
import tempfile

from app.core.database import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.user import User
from app.models.project import Project
from app.models.requirement import Requirement
from app.core.config import settings

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/dashboard")
async def get_dashboard_data(
    current_user: User = Depends(require_permissions(["report:read"])),
    db: Session = Depends(get_db)
):
    """Obtem dados do dashboard"""
    try:
        # Estatisticas gerais
        total_projects = db.query(Project).count()
        active_projects = db.query(Project).filter(Project.is_active == True).count()
        total_requirements = db.query(Requirement).count()
        completed_requirements = db.query(Requirement).filter(Requirement.status == "concluido").count()
        
        # Projetos por status
        projects_by_status = db.query(
            Project.status,
            func.count(Project.id).label('count')
        ).group_by(Project.status).all()
        
        # Requisitos por status
        requirements_by_status = db.query(
            Requirement.status,
            func.count(Requirement.id).label('count')
        ).group_by(Requirement.status).all()
        
        # Requisitos por tipo
        requirements_by_type = db.query(
            Requirement.type,
            func.count(Requirement.id).label('count')
        ).group_by(Requirement.type).all()
        
        # Requisitos por prioridade
        requirements_by_priority = db.query(
            Requirement.priority,
            func.count(Requirement.id).label('count')
        ).group_by(Requirement.priority).all()
        
        # Requisitos atrasados
        overdue_requirements = db.query(Requirement).filter(
            and_(
                Requirement.due_date < datetime.utcnow(),
                Requirement.status.notin_(["concluido", "cancelado"])
            )
        ).count()
        
        # Projetos recentes (ultimos 30 dias)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_projects = db.query(Project).filter(
            Project.created_at >= thirty_days_ago
        ).count()
        
        # Requisitos recentes (ultimos 30 dias)
        recent_requirements = db.query(Requirement).filter(
            Requirement.created_at >= thirty_days_ago
        ).count()
        
        return {
            "summary": {
                "total_projects": total_projects,
                "active_projects": active_projects,
                "total_requirements": total_requirements,
                "completed_requirements": completed_requirements,
                "overdue_requirements": overdue_requirements,
                "recent_projects": recent_projects,
                "recent_requirements": recent_requirements
            },
            "projects_by_status": [
                {"status": status, "count": count} 
                for status, count in projects_by_status
            ],
            "requirements_by_status": [
                {"status": status, "count": count} 
                for status, count in requirements_by_status
            ],
            "requirements_by_type": [
                {"type": type, "count": count} 
                for type, count in requirements_by_type
            ],
            "requirements_by_priority": [
                {"priority": priority, "count": count} 
                for priority, count in requirements_by_priority
            ]
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter dados do dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/projects/export")
async def export_projects_report(
    format: str = Query("csv", regex="^(csv|excel|pdf)$"),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(require_permissions(["report:export"])),
    db: Session = Depends(get_db)
):
    """Exporta relatorio de projetos"""
    try:
        query = db.query(Project)
        
        # Aplicar filtros
        if status:
            query = query.filter(Project.status == status)
        
        if priority:
            query = query.filter(Project.priority == priority)
        
        if start_date:
            query = query.filter(Project.created_at >= start_date)
        
        if end_date:
            query = query.filter(Project.created_at <= end_date)
        
        projects = query.all()
        
        # Converter para DataFrame
        data = []
        for project in projects:
            data.append({
                "ID": project.id,
                "Nome": project.name,
                "Descricao": project.description,
                "Status": project.status,
                "Prioridade": project.priority,
                "Cliente": project.client_name,
                "Orcamento": project.budget,
                "Data Inicio": project.start_date,
                "Data Fim": project.end_date,
                "Requisitos": project.requirements_count,
                "Progresso (%)": project.progress_percentage,
                "Criado Por": project.created_by_user.full_name if project.created_by_user else "",
                "Data Criacao": project.created_at,
                "Data Atualizacao": project.updated_at
            })
        
        df = pd.DataFrame(data)
        
        # Criar arquivo temporario
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as tmp_file:
            if format == "csv":
                df.to_csv(tmp_file.name, index=False, encoding='utf-8-sig')
            elif format == "excel":
                df.to_excel(tmp_file.name, index=False, engine='openpyxl')
            elif format == "pdf":
                # Implementar geracao de PDF
                pass
            
            return FileResponse(
                tmp_file.name,
                media_type=f"application/{format}",
                filename=f"relatorio_projetos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            )
        
    except Exception as e:
        logger.error(f"Erro ao exportar relatorio de projetos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/requirements/export")
async def export_requirements_report(
    format: str = Query("csv", regex="^(csv|excel|pdf)$"),
    project_id: Optional[str] = None,
    type: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(require_permissions(["report:export"])),
    db: Session = Depends(get_db)
):
    """Exporta relatorio de requisitos"""
    try:
        query = db.query(Requirement)
        
        # Aplicar filtros
        if project_id:
            query = query.filter(Requirement.project_id == project_id)
        
        if type:
            query = query.filter(Requirement.type == type)
        
        if priority:
            query = query.filter(Requirement.priority == priority)
        
        if status:
            query = query.filter(Requirement.status == status)
        
        if start_date:
            query = query.filter(Requirement.created_at >= start_date)
        
        if end_date:
            query = query.filter(Requirement.created_at <= end_date)
        
        requirements = query.all()
        
        # Converter para DataFrame
        data = []
        for req in requirements:
            data.append({
                "ID": req.id,
                "Titulo": req.title,
                "Descricao": req.description,
                "Tipo": req.type,
                "Prioridade": req.priority,
                "Status": req.status,
                "Complexidade": req.complexity,
                "Horas Estimadas": req.estimated_hours,
                "Horas Reais": req.actual_hours,
                "Data Vencimento": req.due_date,
                "Data Conclusao": req.completion_date,
                "Projeto": req.project.name if req.project else "",
                "Atribuido Para": req.assigned_user.full_name if req.assigned_user else "",
                "Criado Por": req.created_by_user.full_name if req.created_by_user else "",
                "Atrasado": req.is_overdue,
                "Progresso (%)": req.progress_percentage,
                "Data Criacao": req.created_at,
                "Data Atualizacao": req.updated_at
            })
        
        df = pd.DataFrame(data)
        
        # Criar arquivo temporario
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}") as tmp_file:
            if format == "csv":
                df.to_csv(tmp_file.name, index=False, encoding='utf-8-sig')
            elif format == "excel":
                df.to_excel(tmp_file.name, index=False, engine='openpyxl')
            elif format == "pdf":
                # Implementar geracao de PDF
                pass
            
            return FileResponse(
                tmp_file.name,
                media_type=f"application/{format}",
                filename=f"relatorio_requisitos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            )
        
    except Exception as e:
        logger.error(f"Erro ao exportar relatorio de requisitos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/project/{project_id}/summary")
async def get_project_summary(
    project_id: str,
    current_user: User = Depends(require_permissions(["report:read"])),
    db: Session = Depends(get_db)
):
    """Obtem resumo de um projeto especifico"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto nao encontrado"
            )
        
        # Estatisticas do projeto
        requirements = project.requirements
        total_requirements = len(requirements)
        completed_requirements = len([r for r in requirements if r.status == "concluido"])
        overdue_requirements = len([r for r in requirements if r.is_overdue])
        
        # Requisitos por status
        requirements_by_status = {}
        for req in requirements:
            status = req.status
            requirements_by_status[status] = requirements_by_status.get(status, 0) + 1
        
        # Requisitos por tipo
        requirements_by_type = {}
        for req in requirements:
            type = req.type
            requirements_by_type[type] = requirements_by_type.get(type, 0) + 1
        
        # Requisitos por prioridade
        requirements_by_priority = {}
        for req in requirements:
            priority = req.priority
            requirements_by_priority[priority] = requirements_by_priority.get(priority, 0) + 1
        
        return {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "status": project.status,
                "priority": project.priority,
                "client_name": project.client_name,
                "progress_percentage": project.progress_percentage
            },
            "statistics": {
                "total_requirements": total_requirements,
                "completed_requirements": completed_requirements,
                "overdue_requirements": overdue_requirements,
                "completion_rate": (completed_requirements / total_requirements * 100) if total_requirements > 0 else 0
            },
            "requirements_by_status": [
                {"status": status, "count": count} 
                for status, count in requirements_by_status.items()
            ],
            "requirements_by_type": [
                {"type": type, "count": count} 
                for type, count in requirements_by_type.items()
            ],
            "requirements_by_priority": [
                {"priority": priority, "count": count} 
                for priority, count in requirements_by_priority.items()
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter resumo do projeto: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
