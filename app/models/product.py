from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base import Base
import enum

# Enum definitions
class ProductStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"

class SimType(enum.Enum):
    SIM = "SIM"
    E_SIM = "eSIM"

class OperatorCode(enum.Enum):
    DTAC = "DTAC"
    AIS = "ais"
    JY = "JOYTEL"

class VendorCode(enum.Enum):
    DTAC = "DTAC"
    FRAGRANT = "FRAGRANT"
    COMMBITZ = "COMMBITZ"
    KANGO = "KANGO"

class PurchaseType(enum.Enum):
    API_PURCHASE = "API Purchase"
    MANUAL_PURCHASE = "Manual Purchase"
    ONLY_STOCK = "Only Stock"

class SkuType(enum.Enum):
    BASE = "Base"
    DATAPACK = "Datapack"
    BASE_DATAPACK = "Base + Datapack"

class DataType(enum.Enum):
    FIXED_DATA = "Fixed Data"
    DAILY_DATA = "Daily Data"

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(Enum(ProductStatus, values_callable=lambda obj: [e.value for e in obj]), nullable=False, default=ProductStatus.ACTIVE)
    type_of_sim = Column(Enum(SimType, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    operator_code = Column(Enum(OperatorCode, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    vendor_code = Column(Enum(VendorCode, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    purchase_type = Column(Enum(PurchaseType, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    sku_type = Column(Enum(SkuType, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    data_type = Column(Enum(DataType, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    hotspot = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Product(id={self.id}, product_code='{self.product_code}', status='{self.status.value}')>"
