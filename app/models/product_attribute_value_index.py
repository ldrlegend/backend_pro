from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.db.base import Base
from sqlalchemy.orm import relationship


class ProductAttributeValueIndex(Base):
    __tablename__ = "product_attribute_value_index"   

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False, index=True)
    attribute_id = Column(Integer, ForeignKey("attribute.id"), nullable=False, index=True)
    attribute_option_id = Column(Integer, ForeignKey("attribute_option.id"), nullable=False, index=True)
    date_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_modified_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Ensure one attribute per product (prevent duplicates)
    __table_args__ = (UniqueConstraint('product_id', 'attribute_id', name='uq_product_attribute'),)

    # Relationships
    product = relationship("Product", foreign_keys=[product_id], back_populates="product_attribute_value_index")
    attribute = relationship("Attribute", foreign_keys=[attribute_id], back_populates="product_attribute_value_index")
    attribute_option = relationship("AttributeOption", foreign_keys=[attribute_option_id], back_populates="product_attribute_value_index")


    @property
    def attribute_value(self):
        return self.attribute_option.attribute_option_en

    def __repr__(self):
        return f"<ProductAttributeValueIndex(id={self.id}, product_id='{self.product_id}', attribute_id='{self.attribute_id}', attribute_option_id='{self.attribute_option_id}')>"