from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class AttributeOptionBase(BaseModel):
    attribute_code: str
    attribute_option_vn: Optional[str] = None
    attribute_option_en: Optional[str] = None

class AttributeOptionCreate(AttributeOptionBase):
    pass

class AttributeOptionCreate(AttributeOptionBase):
    attribute_code: Optional[str] = None
    attribute_option_vn: Optional[str] = None
    attribute_option_en: Optional[str] = None

class AttributeOptionUpdate(AttributeOptionBase):
    attribute_code: Optional[str] = None
    attribute_option_vn: Optional[str] = None
    attribute_option_en: Optional[str] = None

class AttributeOptionOut(AttributeOptionBase):
    id: int
    date_created: datetime
    last_modified_date: datetime

    model_config = ConfigDict(from_attributes=True)
