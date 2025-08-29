from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.utils.enums.status import Status as ProductStatus
from app.utils.enums.type_of_sim import TypeOfSim as SimType
from app.utils.enums.purchase_type import PurchaseType
from app.utils.enums.sku_type import SkuType
from app.utils.enums.data_type import DataType
from app.utils.enums.import_type import ImportType
from app.models.product import DataPlanType
from app.models.product import YesNo

# Base Product Schema
class ProductBase(BaseModel):
    id: Optional[int] = None
    product_code: str
    status: ProductStatus
    type_of_sim: SimType
    operator_code: str
    vendor_code: str
    purchase_type: PurchaseType
    sku_type: SkuType
    data_type: DataType
    base_sim_sku_code: Optional[str] = None
    import_type: ImportType
    supported_countries: str
    daily_reset_time: Optional[str] = None
    network_type: str
    APN: Optional[str] = None
    hotspot: YesNo
    onsite_carrier: Optional[str] = None
    local_phone_number: YesNo
    local_number_country: Optional[str] = None
    kyc_needed: YesNo
    top_up_options: YesNo
    activation: Optional[str] = None
    unsupported_apps: Optional[str] = None
    telco_perks: Optional[str] = None
    data_plan_type: Optional[DataPlanType] = None
    note: Optional[str] = None

# Create Product Schema
class ProductCreate(ProductBase):
    pass

# Update Product Schema
class ProductUpdate(BaseModel):
    id: Optional[int] = None
    product_code: Optional[str] = None
    status: Optional[ProductStatus] = None
    type_of_sim: Optional[SimType] = None
    operator_code: Optional[str] = None
    vendor_code: Optional[str] = None
    purchase_type: Optional[PurchaseType] = None
    sku_type: Optional[SkuType] = None
    data_type: Optional[DataType] = None
    onsite_carrier: Optional[str] = None
    local_phone_number: Optional[YesNo] = None
    local_number_country: Optional[str] = None
    kyc_needed: Optional[YesNo] = None
    top_up_options: Optional[YesNo] = None
    activation: Optional[str] = None
    unsupported_apps: Optional[str] = None
    telco_perks: Optional[str] = None
    data_plan_type: Optional[DataPlanType] = None
    note: Optional[str] = None
    base_sim_sku_code: Optional[str] = None
    import_type: Optional[ImportType] = None
    supported_countries: Optional[str] = None
    daily_reset_time: Optional[str] = None
    network_type: Optional[str] = None
    APN: Optional[str] = None
    hotspot: Optional[YesNo] = None

# Product Response Schema
class ProductOut(ProductBase):
    date_created: datetime
    last_modified_date: datetime

    model_config = ConfigDict(from_attributes=True)

# Product List Response Schema
class ProductList(BaseModel):
    products: list[ProductOut]
    total: int
    page: int
    size: int

    model_config = ConfigDict(from_attributes=True)
