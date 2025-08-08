from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
from datetime import datetime
from typing import Dict, Any

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="em_andamento")
    priority = Column(String(20), nullable=False, default="media")
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget = Column(String(100), nullable=True)
    client_name = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    logo_url = Column(String(500), nullable=True)  # Novo campo para logo
    
    # Relacionamentos
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_by_user = relationship("User", back_populates="projects")
    requirements = relationship("Requirement", back_populates="project", cascade="all, delete-orphan")
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Project {self.name}>"
    
    @property
    def requirements_count(self) -> int:
        """Retorna o numero de requisitos do projeto"""
        return len(self.requirements) if self.requirements else 0
    
    @property
    def completed_requirements_count(self) -> int:
        """Retorna o numero de requisitos concluidos"""
        if not self.requirements:
            return 0
        return len([req for req in self.requirements if req.status == "concluido"])
    
    @property
    def progress_percentage(self) -> float:
        """Retorna a porcentagem de progresso do projeto"""
        if self.requirements_count == 0:
            return 0.0
        return (self.completed_requirements_count / self.requirements_count) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o projeto para dicionario"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "budget": self.budget,
            "client_name": self.client_name,
            "is_active": self.is_active,
            "logo_url": self.logo_url,  # Novo campo
            "created_by": self.created_by,
            "created_by_user": self.created_by_user.to_dict_safe() if self.created_by_user else None,
            "requirements_count": self.requirements_count,
            "completed_requirements_count": self.completed_requirements_count,
            "progress_percentage": round(self.progress_percentage, 2),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_summary(self) -> Dict[str, Any]:
        """Converte o projeto para dicionario resumido"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "client_name": self.client_name,
            "logo_url": self.logo_url,  # Novo campo
            "requirements_count": self.requirements_count,
            "progress_percentage": round(self.progress_percentage, 2),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
