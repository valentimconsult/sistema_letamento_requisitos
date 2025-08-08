from pydantic import BaseModel, validator
from typing import Optional, Dict, Any
from datetime import datetime

class RequirementBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: str = "funcional"
    priority: str = "media"
    status: str = "pendente"
    complexity: Optional[str] = None
    estimated_hours: Optional[str] = None
    actual_hours: Optional[str] = None
    due_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    dynamic_fields: Dict[str, Any] = {}
    
    @validator('type')
    def validate_type(cls, v):
        valid_types = ["funcional", "nao_funcional", "regra_negocio"]
        if v not in valid_types:
            raise ValueError(f'Tipo deve ser um dos seguintes: {", ".join(valid_types)}')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        valid_priorities = ["baixa", "media", "alta", "critica"]
        if v not in valid_priorities:
            raise ValueError(f'Prioridade deve ser uma das seguintes: {", ".join(valid_priorities)}')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ["pendente", "em_analise", "aprovado", "em_desenvolvimento", "concluido", "cancelado"]
        if v not in valid_statuses:
            raise ValueError(f'Status deve ser um dos seguintes: {", ".join(valid_statuses)}')
        return v
    
    @validator('complexity')
    def validate_complexity(cls, v):
        if v is not None:
            valid_complexities = ["baixa", "media", "alta"]
            if v not in valid_complexities:
                raise ValueError(f'Complexidade deve ser uma das seguintes: {", ".join(valid_complexities)}')
        return v

class RequirementCreate(RequirementBase):
    project_id: str
    assigned_to: Optional[str] = None

class RequirementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    complexity: Optional[str] = None
    estimated_hours: Optional[str] = None
    actual_hours: Optional[str] = None
    due_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    dynamic_fields: Optional[Dict[str, Any]] = None
    
    @validator('type')
    def validate_type(cls, v):
        if v is not None:
            valid_types = ["funcional", "nao_funcional", "regra_negocio"]
            if v not in valid_types:
                raise ValueError(f'Tipo deve ser um dos seguintes: {", ".join(valid_types)}')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        if v is not None:
            valid_priorities = ["baixa", "media", "alta", "critica"]
            if v not in valid_priorities:
                raise ValueError(f'Prioridade deve ser uma das seguintes: {", ".join(valid_priorities)}')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ["pendente", "em_analise", "aprovado", "em_desenvolvimento", "concluido", "cancelado"]
            if v not in valid_statuses:
                raise ValueError(f'Status deve ser um dos seguintes: {", ".join(valid_statuses)}')
        return v
    
    @validator('complexity')
    def validate_complexity(cls, v):
        if v is not None:
            valid_complexities = ["baixa", "media", "alta"]
            if v not in valid_complexities:
                raise ValueError(f'Complexidade deve ser uma das seguintes: {", ".join(valid_complexities)}')
        return v

class RequirementResponse(RequirementBase):
    id: str
    project_id: str
    project: Optional[Dict[str, Any]] = None
    assigned_to: Optional[str] = None
    assigned_user: Optional[Dict[str, Any]] = None
    created_by: str
    created_by_user: Optional[Dict[str, Any]] = None
    is_overdue: bool
    days_until_due: Optional[int] = None
    progress_percentage: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class RequirementResponseSummary(BaseModel):
    id: str
    title: str
    type: str
    priority: str
    status: str
    complexity: Optional[str] = None
    due_date: Optional[datetime] = None
    is_overdue: bool
    progress_percentage: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class RequirementFilter(BaseModel):
    project_id: Optional[str] = None
    type: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    complexity: Optional[str] = None
    assigned_to: Optional[str] = None
    created_by: Optional[str] = None
    is_overdue: Optional[bool] = None
    search: Optional[str] = None
