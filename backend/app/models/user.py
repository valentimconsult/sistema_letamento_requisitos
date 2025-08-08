from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
from datetime import datetime
from typing import Dict, Any

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    role = Column(String(50), nullable=False, default="analista")
    permissions = Column(JSON, default=list)  # Lista de permissoes
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    projects = relationship("Project", back_populates="created_by_user", foreign_keys="Project.created_by")
    assigned_requirements = relationship("Requirement", back_populates="assigned_user", foreign_keys="Requirement.assigned_to")
    created_requirements = relationship("Requirement", back_populates="created_by_user", foreign_keys="Requirement.created_by")
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    @property
    def full_name(self) -> str:
        """Retorna o nome completo do usuario"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def has_permission(self, permission: str) -> bool:
        """Verifica se o usuario tem uma permissao especifica"""
        if self.is_superuser:
            return True
        return permission in self.permissions
    
    def has_role(self, role: str) -> bool:
        """Verifica se o usuario tem um role especifico"""
        return self.role == role
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o usuario para dicionario"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "role": self.role,
            "permissions": self.permissions,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_safe(self) -> Dict[str, Any]:
        """Converte o usuario para dicionario sem informacoes sensiveis"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "role": self.role,
            "is_active": self.is_active,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
