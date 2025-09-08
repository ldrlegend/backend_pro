import numbers
from sqlalchemy import Column, Integer, String, Enum, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base import Base
import enum
from sqlalchemy.orm import relationship

# Enum definitions
class AttributeType(str, enum.Enum):
    text = "Text"
    number = "Number"
    select = "Select"
    multi_select = "Multiselect"

# AttributeGroup enum moved to attribute_group.py to avoid conflicts

class AttributeStatus(str, enum.Enum):
    active = "Active"
    deleted = "Deleted"

class Attribute(Base):
    __tablename__ = "attribute"   

    id = Column(Integer, primary_key=True, index=True)
    attribute_code = Column(Text, unique=True, nullable=False, index=True)
    attribute_name_vn = Column(Text, nullable=False)
    attribute_name_en = Column(Text, nullable=False)
    type_attribute = Column(Enum(AttributeType), nullable=False, default=AttributeType.text, index=True)
    status = Column(Enum(AttributeStatus), nullable=False, default=AttributeStatus.active, index=True)
    # attribute_group = Column(Enum(AttributeGroup), nullable=False, default=AttributeGroup.product)
    # attribute_group_id = Column(Integer, ForeignKey("attribute_group.id"), nullable=False, index=True)
    date_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_modified_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    attribute_group_links = relationship("AttributeGroupLink", back_populates="attribute")
    attribute_options = relationship("AttributeOption", foreign_keys="[AttributeOption.attribute_code]", back_populates="attribute")
    product_attribute_value_index = relationship("ProductAttributeValueIndex", back_populates="attribute")
    # item_attribute_value_index = relationship("ItemAttributeValueIndex", back_populates="attribute")
    
    @property
    def attribute_name(self):
        return self.attribute_name_en if self.attribute_name_en else self.attribute_name_vn

    def __repr__(self):
        return f"<Attribute(id={self.id}, attribute_code='{self.attribute_code}', attribute_name_vn='{self.attribute_name_vn}', attribute_name_en='{self.attribute_name_en}', type_attribute='{self.type_attribute}', attribute_group_id='{self.attribute_group_id}')>"