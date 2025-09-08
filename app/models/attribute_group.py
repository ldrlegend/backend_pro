from sqlalchemy import Column, Integer, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base import Base
import enum
# from app.models.attribute import Attribute
from sqlalchemy.orm import relationship

# Enum definitions
class AttributeGroupName(str, enum.Enum):
    product = "product"
    sku = "sku"
    listing = "listing"
    item = "item"
    country = "country"


class AttributeGroup(Base):
    __tablename__ = "attribute_group"

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(Enum(AttributeGroupName), nullable=False, default=AttributeGroupName.product)
    date_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_modified_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    attribute_group_links = relationship("AttributeGroupLink", back_populates="attribute_group")
    # attributes = relationship("Attribute", foreign_keys="[Attribute.attribute_group_id]", back_populates="attribute_group")

    @property
    def __repr__(self):
        return f"<AttributeGroup(id={self.id}, group_name='{self.group_name}')>"