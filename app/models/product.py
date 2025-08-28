from sqlalchemy import Column, Integer, String, Enum, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base import Base
from app.utils.enums.status import Status
from app.utils.enums.type_of_sim import TypeOfSim
from app.utils.enums.purchase_type import PurchaseType
from app.utils.enums.sku_type import SkuType
from app.utils.enums.data_type import DataType
from app.utils.enums.import_type import ImportType
from app.utils.enums.kyc import KYC
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import enum

class YesNo(enum.Enum):
    YES = "YES"
    NO = "NO"

class DataPlanType(enum.Enum):
    Optional_Data_Plan = "Optional Data Plan"
    No_Data_Plan = "No Data Plan"

class Product(Base):
    __tablename__ = "product"   

    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(Text, unique=True, nullable=False, index=True)
    status = Column(Enum(Status), nullable=False, default=Status.ACTIVE)
    type_of_sim = Column(Enum(TypeOfSim), nullable=False)
    purchase_type = Column(Enum(PurchaseType), nullable=False)
    vendor_code = Column(Text, ForeignKey("vendor.vendor_code"), nullable=False)
    operator_code = Column(Text, ForeignKey("operator.operator_code"), nullable=False)
    sku_type = Column(Enum(SkuType), nullable=False)
    data_type = Column(Enum(DataType), nullable=False)
    base_sim_sku_code = Column(Text, nullable=True)
    import_type = Column(Enum(ImportType), nullable=False)
    supported_countries = Column(Text, ForeignKey("country.country_code"), nullable=False)
    daily_reset_time = Column(Text, nullable=True)
    network_type = Column(Text, nullable=False)
    APN = Column(Text, nullable=True)
    onsite_carrier = Column(Text, nullable=True)
    local_phone_number = Column(Enum(YesNo), default=YesNo.NO)
    local_number_country = Column(Text, ForeignKey("country.country_code"), nullable=True)
    hotspot = Column(Enum(YesNo), default=YesNo.NO)
    # kyc_code = Column(Integer, ForeignKey("kyc.kyc_code"), nullable=True)
    kyc_needed = Column(Enum(YesNo), default=YesNo.NO)
    kyc_link = Column(Enum(KYC), nullable=True)
    top_up_options = Column(Enum(YesNo), default=YesNo.NO)
    activation = Column(Text, nullable=True)
    unsupported_apps = Column(Text, nullable=True)
    telco_perks = Column(Text, nullable=True)
    data_plan_type = Column(Enum(DataPlanType), nullable=True)
    note = Column(Text, nullable=True)
    date_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_modified_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())



    #Relationships to kyc table
    # kyc = relationship("KYC", foreign_keys=[kyc_code], back_populates="products")
    supported_country = relationship("Country", foreign_keys=[supported_countries], back_populates="products")
    local_number_country_rel = relationship("Country", foreign_keys=[local_number_country])
    vendor = relationship("Vendor", foreign_keys=[vendor_code], back_populates="products")
    operator = relationship("Operator", foreign_keys=[operator_code], back_populates="products")

    #Properties
    @property
    def supported_country_name(self):
        return self.supported_country.country_name if self.supported_country else None

    # @property
    # def kyc_needed(self):
    #     return self.kyc.kyc_needed if self.kyc else None

    # @property
    # def kyc_link(self):
    #     return self.kyc.kyc_link if self.kyc else None
    
    def __repr__(self):
        return f"<Product(id={self.id}, product_code='{self.product_code}', status='{self.status.value}')>"
