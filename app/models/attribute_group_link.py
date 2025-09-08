from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base import Base
import enum
from app.models.attribute import Attribute
from sqlalchemy.orm import relationship

# Enum definitions

class AttributeGroupLink(Base):
    __tablename__ = "attribute_group_link"

    id = Column(Integer, primary_key=True, index=True)
    attribute_id = Column(Integer, ForeignKey("attribute.id"), nullable=False, index=True)
    group_id = Column(Integer, ForeignKey("attribute_group.id"), nullable=False, index=True)
    date_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_modified_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    attribute = relationship("Attribute", foreign_keys=[attribute_id], back_populates="attribute_group_links")
    attribute_group = relationship("AttributeGroup", foreign_keys=[group_id], back_populates="attribute_group_links")

    @property
    def attribute_group_name(self):
        return self.attribute_group.group_name

    def __repr__(self):
        return f"<AttributeGroupLink(id={self.id}, attribute_id='{self.attribute_id}', group_id='{self.group_id}')>"