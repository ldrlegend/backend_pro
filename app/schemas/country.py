from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CountryBase(BaseModel):
    country_code: str
    country_name_vn: Optional[str] = None
    country_name_en: Optional[str] = None
    type_country: Optional[str] = None
    # parent_code: Optional[str] = None
    seo_url_key: Optional[str] = None
    # sort_order: Optional[int] = None
    is_popular: Optional[str] = None
    type_bidv: Optional[str] = None

class CountryCreate(CountryBase):
    pass

class CountryUpdate(BaseModel):
    country_code: Optional[str] = None
    country_name_vn: Optional[str] = None
    country_name_en: Optional[str] = None
    type_country: Optional[str] = None
    # parent_code: Optional[str] = None
    seo_url_key: Optional[str] = None
    # sort_order: Optional[int] = None
    is_popular: Optional[str] = None
    type_bidv: Optional[str] = None

class CountryOut(CountryBase):
    id: int
    date_created: datetime
    last_modified_date: datetime

    model_config = ConfigDict(from_attributes=True)
