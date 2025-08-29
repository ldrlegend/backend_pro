from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.country import CountryOut

class OperatorBase(BaseModel):
    operator_code: str
    operator_name: Optional[str] = None
    country_code: str

class OperatorCreate(OperatorBase):
    pass

class OperatorUpdate(BaseModel):
    operator_code: Optional[str] = None
    operator_name: Optional[str] = None
    country_code: Optional[str] = None

class OperatorOut(OperatorBase):
    id: int
    date_created: datetime
    last_modified_date: datetime
    country: Optional[CountryOut] = None

    model_config = ConfigDict(from_attributes=True)
