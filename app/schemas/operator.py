from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.country import CountryOut

class OperatorBase(BaseModel):
    operator_code: str
    operator_name: Optional[str] = None
    country: Optional[CountryOut] = None

class OperatorCreate(OperatorBase):
    pass

class OperatorUpdate(BaseModel):
    operator_code: Optional[str] = None
    operator_name: Optional[str] = None
    country: Optional[CountryOut] = None

class OperatorOut(OperatorBase):
    id: int
    date_created: datetime
    last_modified_date: datetime

    model_config = ConfigDict(from_attributes=True)
