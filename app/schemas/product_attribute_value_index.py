from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ProductAttributeValueIndexBase(BaseModel):
    product_id: int
    attribute_id: int
    attribute_option_id: int

class ProductAttributeValueIndexCreate(ProductAttributeValueIndexBase):
    pass

class ProductAttributeValueIndexUpdate(BaseModel):
    product_id: Optional[int] = None
    attribute_id: Optional[int] = None
    attribute_option_id: Optional[int] = None

class ProductAttributeValueIndexOut(ProductAttributeValueIndexBase):
    id: int
    date_created: datetime
    last_modified_date: datetime
    attribute_value: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
