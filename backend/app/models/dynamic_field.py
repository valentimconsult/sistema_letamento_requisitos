from sqlalchemy import Column, String, DateTime, Boolean, JSON, Text
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

class DynamicFieldDefinition(Base):
    __tablename__ = "dynamic_field_definitions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    field_name = Column(String(100), nullable=False, index=True)
    field_type = Column(String(50), nullable=False)  # text, number, date, select, textarea, boolean
    field_label = Column(String(200), nullable=True)
    field_description = Column(Text, nullable=True)
    options = Column(JSON, nullable=True)  # Para campos do tipo select
    is_required = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    applies_to = Column(String(50), nullable=False, default="requirement")  # requirement, project
    order_index = Column(String(10), nullable=True)  # Para ordenacao dos campos
    validation_rules = Column(JSON, nullable=True)  # Regras de validacao
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<DynamicFieldDefinition {self.field_name}>"
    
    def get_options_list(self) -> List[str]:
        """Retorna a lista de opcoes para campos do tipo select"""
        if self.field_type == "select" and self.options:
            return self.options if isinstance(self.options, list) else []
        return []
    
    def set_options(self, options: List[str]) -> None:
        """Define as opcoes para campos do tipo select"""
        self.options = options
    
    def add_option(self, option: str) -> None:
        """Adiciona uma opcao para campos do tipo select"""
        if not self.options:
            self.options = []
        if option not in self.options:
            self.options.append(option)
    
    def remove_option(self, option: str) -> None:
        """Remove uma opcao de campos do tipo select"""
        if self.options and option in self.options:
            self.options.remove(option)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a definicao de campo para dicionario"""
        return {
            "id": self.id,
            "field_name": self.field_name,
            "field_type": self.field_type,
            "field_label": self.field_label,
            "field_description": self.field_description,
            "options": self.get_options_list(),
            "is_required": self.is_required,
            "is_active": self.is_active,
            "applies_to": self.applies_to,
            "order_index": self.order_index,
            "validation_rules": self.validation_rules,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_default_fields(cls) -> List[Dict[str, Any]]:
        """Retorna os campos dinamicos padrao"""
        return [
            {
                "field_name": "fonte_dados",
                "field_type": "text",
                "field_label": "Fonte de Dados",
                "field_description": "Sistema ou fonte de dados principal",
                "is_required": False,
                "applies_to": "requirement"
            },
            {
                "field_name": "kpis_envolvidos",
                "field_type": "select",
                "field_label": "KPIs Envolvidos",
                "field_description": "Indicadores de performance relacionados",
                "options": ["Vendas", "Lucratividade", "Custo", "ROI", "Produtividade"],
                "is_required": False,
                "applies_to": "requirement"
            },
            {
                "field_name": "data_entrega_estimada",
                "field_type": "date",
                "field_label": "Data de Entrega Estimada",
                "field_description": "Data estimada para entrega",
                "is_required": False,
                "applies_to": "requirement"
            },
            {
                "field_name": "complexidade",
                "field_type": "select",
                "field_label": "Complexidade",
                "field_description": "Nivel de complexidade do requisito",
                "options": ["Baixa", "Media", "Alta"],
                "is_required": False,
                "applies_to": "requirement"
            },
            {
                "field_name": "observacoes",
                "field_type": "textarea",
                "field_label": "Observacoes",
                "field_description": "Observacoes adicionais",
                "is_required": False,
                "applies_to": "requirement"
            }
        ]
