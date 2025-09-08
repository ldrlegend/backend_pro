from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.attribute_group import AttributeGroupName

class AttributeGroupBase(BaseModel):
    group_name: Optional[AttributeGroupName] = None

class AttributeGroupCreate(AttributeGroupBase):
    pass

class AttributeGroupUpdate(AttributeGroupBase):
    group_name: Optional[AttributeGroupName] = None

class AttributeGroupOut(AttributeGroupBase):
    id: int
    group_name: Optional[AttributeGroupName] = None
    date_created: datetime
    last_modified_date: datetime

    model_config = ConfigDict(from_attributes=True)