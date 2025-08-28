from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base import Base
from sqlalchemy.orm import relationship

# Enum definitions

class Vendor(Base):
    __tablename__ = "vendor"

    id = Column(Integer, primary_key=True, index=True)
    vendor_code = Column(String(50), unique=True, nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=True, index=True)
    vendor_name = Column(String(50), nullable=True, index=True)
    date_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_modified_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    products = relationship("Product", back_populates="vendor")

    def __repr__(self):
        return f"<Vendor(id={self.id}, vendor_code='{self.vendor_code}', code='{self.code}', vendor_name='{self.vendor_name}')>"