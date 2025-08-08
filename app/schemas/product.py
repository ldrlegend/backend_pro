from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.product import ProductStatus, SimType, OperatorCode, VendorCode, PurchaseType, SkuType, DataType

# Base Product Schema
class ProductBase(BaseModel):
    product_code: str
    status: ProductStatus = ProductStatus.ACTIVE
    type_of_sim: SimType
    operator_code: OperatorCode
    vendor_code: VendorCode
    purchase_type: PurchaseType
    sku_type: SkuType
    data_type: DataType
    hotspot: bool = False

# Create Product Schema
class ProductCreate(ProductBase):
    pass

# Update Product Schema
class ProductUpdate(BaseModel):
    product_code: Optional[str] = None
    status: Optional[ProductStatus] = None
    type_of_sim: Optional[SimType] = None
    operator_code: Optional[OperatorCode] = None
    vendor_code: Optional[VendorCode] = None
    purchase_type: Optional[PurchaseType] = None
    sku_type: Optional[SkuType] = None
    data_type: Optional[DataType] = None
    hotspot: Optional[bool] = None

# Product Response Schema
class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Product List Response Schema
class ProductList(BaseModel):
    products: list[ProductOut]
    total: int
    page: int
    size: int

    model_config = ConfigDict(from_attributes=True)
