from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

class Requirement(Base):
    __tablename__ = "requirements"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    type = Column(String(50), nullable=False, default="funcional")  # funcional, nao_funcional, regra_negocio
    priority = Column(String(20), nullable=False, default="media")  # baixa, media, alta, critica
    status = Column(String(50), nullable=False, default="pendente")  # pendente, em_analise, aprovado, em_desenvolvimento, concluido, cancelado
    complexity = Column(String(20), nullable=True)  # baixa, media, alta
    estimated_hours = Column(String(50), nullable=True)
    actual_hours = Column(String(50), nullable=True)
    due_date = Column(DateTime, nullable=True)
    completion_date = Column(DateTime, nullable=True)
    
    # Campos dinamicos (JSON)
    dynamic_fields = Column(JSON, default=dict)
    
    # Relacionamentos
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="requirements")
    
    assigned_to = Column(String(36), ForeignKey("users.id"), nullable=True)
    assigned_user = relationship("User", back_populates="assigned_requirements", foreign_keys=[assigned_to])
    
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_by_user = relationship("User", back_populates="created_requirements", foreign_keys=[created_by])
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Requirement {self.title}>"
    
    @property
    def is_overdue(self) -> bool:
        """Verifica se o requisito esta atrasado"""
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and self.status not in ["concluido", "cancelado"]
    
    @property
    def days_until_due(self) -> Optional[int]:
        """Retorna o numero de dias ate o vencimento"""
        if not self.due_date:
            return None
        delta = self.due_date - datetime.utcnow()
        return delta.days
    
    @property
    def progress_percentage(self) -> float:
        """Retorna a porcentagem de progresso baseada no status"""
        status_progress = {
            "pendente": 0,
            "em_analise": 25,
            "aprovado": 50,
            "em_desenvolvimento": 75,
            "concluido": 100,
            "cancelado": 0
        }
        return status_progress.get(self.status, 0)
    
    def get_dynamic_field(self, field_name: str) -> Any:
        """Obtem o valor de um campo dinamico"""
        return self.dynamic_fields.get(field_name)
    
    def set_dynamic_field(self, field_name: str, value: Any) -> None:
        """Define o valor de um campo dinamico"""
        if not self.dynamic_fields:
            self.dynamic_fields = {}
        self.dynamic_fields[field_name] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o requisito para dicionario"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "priority": self.priority,
            "status": self.status,
            "complexity": self.complexity,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completion_date": self.completion_date.isoformat() if self.completion_date else None,
            "dynamic_fields": self.dynamic_fields,
            "project_id": self.project_id,
            "project": self.project.to_dict_summary() if self.project else None,
            "assigned_to": self.assigned_to,
            "assigned_user": self.assigned_user.to_dict_safe() if self.assigned_user else None,
            "created_by": self.created_by,
            "created_by_user": self.created_by_user.to_dict_safe() if self.created_by_user else None,
            "is_overdue": self.is_overdue,
            "days_until_due": self.days_until_due,
            "progress_percentage": self.progress_percentage,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_summary(self) -> Dict[str, Any]:
        """Converte o requisito para dicionario resumido"""
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "priority": self.priority,
            "status": self.status,
            "complexity": self.complexity,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "is_overdue": self.is_overdue,
            "progress_percentage": self.progress_percentage,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
