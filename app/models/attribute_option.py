from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base import Base
import enum
from app.models.attribute import Attribute
from sqlalchemy.orm import relationship

# Enum definitions

class AttributeOption(Base):
    __tablename__ = "attribute_option"

    id = Column(Integer, primary_key=True, index=True)
    attribute_code = Column(Text, ForeignKey("attribute.attribute_code"), nullable=False, index=True)
    attribute_option_vn = Column(Text, nullable=False)
    attribute_option_en = Column(Text, nullable=False)
    date_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_modified_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    attribute = relationship("Attribute", foreign_keys=[attribute_code], back_populates="attribute_options")
    product_attribute_value_index = relationship("ProductAttributeValueIndex", back_populates="attribute_option")
    # attribute_by_code = relationship("Attribute", foreign_keys=[attribute_code], back_populates="attribute_options")
    # item_attribute_value_index = relationship("ItemAttributeValueIndex", back_populates="attribute_option")
    @property
    def attribute_option_name(self):
        return self.attribute_option_en if self.attribute_option_en else self.attribute_option_vn

    def __repr__(self):
        return f"<AttributeOption(id={self.id}, attribute_code='{self.attribute_code}', attribute_option_vn='{self.attribute_option_vn}', attribute_option_en='{self.attribute_option_en}')>"