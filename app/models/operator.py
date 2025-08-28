from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base import Base
from sqlalchemy.orm import relationship

# Enum definitions

class Operator(Base):
    __tablename__ = "operator"

    id = Column(Integer, primary_key=True, index=True)
    operator_code = Column(String(50), unique=True, nullable=False, index=True)
    operator_name = Column(String(50), nullable=False, index=True)
    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)
    country = relationship("Country", back_populates="operators")
    date_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_modified_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    products = relationship("Product", back_populates="operator")

    def __repr__(self):
        return f"<Operator(id={self.id}, operator_code='{self.operator_code}', operator_name='{self.operator_name}')>"