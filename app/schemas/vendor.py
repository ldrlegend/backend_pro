from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class VendorBase(BaseModel):
    vendor_code: str
    code: Optional[str] = None
    vendor_name: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class VendorUpdate(BaseModel):
    vendor_code: Optional[str] = None
    code: Optional[str] = None
    vendor_name: Optional[str] = None

class VendorOut(VendorBase):
    id: int
    date_created: datetime
    last_modified_date: datetime

    model_config = ConfigDict(from_attributes=True)
