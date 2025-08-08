from pydantic import BaseModel, validator
from typing import Optional, Dict, Any
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "em_andamento"
    priority: str = "media"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[str] = None
    client_name: Optional[str] = None
    is_active: bool = True
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ["em_andamento", "concluido", "cancelado", "pausado"]
        if v not in valid_statuses:
            raise ValueError(f'Status deve ser um dos seguintes: {", ".join(valid_statuses)}')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        valid_priorities = ["baixa", "media", "alta", "critica"]
        if v not in valid_priorities:
            raise ValueError(f'Prioridade deve ser uma das seguintes: {", ".join(valid_priorities)}')
        return v

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[str] = None
    client_name: Optional[str] = None
    is_active: Optional[bool] = None
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ["em_andamento", "concluido", "cancelado", "pausado"]
            if v not in valid_statuses:
                raise ValueError(f'Status deve ser um dos seguintes: {", ".join(valid_statuses)}')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        if v is not None:
            valid_priorities = ["baixa", "media", "alta", "critica"]
            if v not in valid_priorities:
                raise ValueError(f'Prioridade deve ser uma das seguintes: {", ".join(valid_priorities)}')
        return v

class ProjectResponse(ProjectBase):
    id: str
    created_by: str
    created_by_user: Optional[Dict[str, Any]] = None
    requirements_count: int
    completed_requirements_count: int
    progress_percentage: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProjectResponseSummary(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    status: str
    priority: str
    client_name: Optional[str] = None
    requirements_count: int
    progress_percentage: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProjectFilter(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    client_name: Optional[str] = None
    created_by: Optional[str] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None
