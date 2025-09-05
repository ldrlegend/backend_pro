from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class AttributeBase(BaseModel):
    attribute_code: str
    attribute_name_vn: Optional[str] = None
    attribute_name_en: Optional[str] = None
    type_attribute: Optional[str] = None
    attribute_group: Optional[str] = None

class AttributeCreate(AttributeBase):
    pass

class AttributeUpdate(BaseModel):
    attribute_code: Optional[str] = None
    attribute_name_vn: Optional[str] = None
    attribute_name_en: Optional[str] = None
    type_attribute: Optional[str] = None
    attribute_group: Optional[str] = None

class AttributeOut(AttributeBase):
    id: int
    date_created: datetime
    last_modified_date: datetime

    model_config = ConfigDict(from_attributes=True)
