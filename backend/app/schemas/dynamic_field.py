from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class DynamicFieldBase(BaseModel):
    field_name: str
    field_type: str
    field_label: Optional[str] = None
    field_description: Optional[str] = None
    options: Optional[List[str]] = None
    is_required: bool = False
    is_active: bool = True
    applies_to: str = "requirement"
    order_index: Optional[str] = None
    validation_rules: Optional[Dict[str, Any]] = None
    
    @validator('field_type')
    def validate_field_type(cls, v):
        valid_types = ["text", "number", "date", "select", "textarea", "boolean"]
        if v not in valid_types:
            raise ValueError(f'Tipo deve ser um dos seguintes: {", ".join(valid_types)}')
        return v
    
    @validator('applies_to')
    def validate_applies_to(cls, v):
        valid_applies = ["requirement", "project"]
        if v not in valid_applies:
            raise ValueError(f'Aplica-se deve ser um dos seguintes: {", ".join(valid_applies)}')
        return v

class DynamicFieldCreate(DynamicFieldBase):
    pass

class DynamicFieldUpdate(BaseModel):
    field_name: Optional[str] = None
    field_type: Optional[str] = None
    field_label: Optional[str] = None
    field_description: Optional[str] = None
    options: Optional[List[str]] = None
    is_required: Optional[bool] = None
    is_active: Optional[bool] = None
    applies_to: Optional[str] = None
    order_index: Optional[str] = None
    validation_rules: Optional[Dict[str, Any]] = None
    
    @validator('field_type')
    def validate_field_type(cls, v):
        if v is not None:
            valid_types = ["text", "number", "date", "select", "textarea", "boolean"]
            if v not in valid_types:
                raise ValueError(f'Tipo deve ser um dos seguintes: {", ".join(valid_types)}')
        return v
    
    @validator('applies_to')
    def validate_applies_to(cls, v):
        if v is not None:
            valid_applies = ["requirement", "project"]
            if v not in valid_applies:
                raise ValueError(f'Aplica-se deve ser um dos seguintes: {", ".join(valid_applies)}')
        return v

class DynamicFieldResponse(DynamicFieldBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
