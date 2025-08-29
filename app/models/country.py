from sqlalchemy import Column, Integer, String, Enum, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base import Base
from sqlalchemy.orm import relationship
import enum

# Enum definitions
class CountryType(enum.Enum):
    SINGLE_COUNTRY = "SINGLE_COUNTRY"
    MULTI_COUNTRY = "MULTI_COUNTRY"

class IsPopular(enum.Enum):
    YES = "YES"
    NO = "NO"

class Country(Base):
    __tablename__ = "country"   

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(Text, unique=True, nullable=False, index=True)
    country_name_vn = Column(Text, nullable=False)
    country_name_en = Column(Text, nullable=False)
    type_country = Column(Enum(CountryType), nullable=False, default=CountryType.SINGLE_COUNTRY, index=True)
    # parent_code= Column(Text, nullable=True)
    seo_url_key = Column(Text, nullable=False)
    is_popular = Column(Enum(IsPopular), nullable=False, default=IsPopular.NO, index=True)
    # sort_order = Column(Integer, nullable=False)
    type_bidv= Column(Enum(CountryType), nullable=False, default=CountryType.SINGLE_COUNTRY)
    date_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_modified_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    operators = relationship("Operator", back_populates="country")
    products = relationship("Product", foreign_keys="[Product.supported_countries]", back_populates="supported_country")

    @property
    def country_name(self):
        return self.country_name_en if self.country_name_en else self.country_name_vn

    def __repr__(self):
        return f"<Country(id={self.id}, country_code='{self.country_code}', country_name_vn='{self.country_name_vn}', country_name_en='{self.country_name_en}', type_country='{self.type_country}')>"