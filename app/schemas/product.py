from pydantic import BaseModel, ConfigDict, Field, create_model
from typing import Optional, Dict, Any, Type
from datetime import datetime
from app.utils.enums.status import Status as ProductStatus

# Base Product Schema (only core fields)
class ProductBase(BaseModel):
    product_code: str
    status: ProductStatus = ProductStatus.ACTIVE
    vendor_code: str
    operator_code: str
    supported_countries: str
    note: Optional[str] = None

# Static Product Response Schema (without dynamic attributes)
class ProductOut(ProductBase):
    id: int
    date_created: datetime
    last_modified_date: datetime

    model_config = ConfigDict(from_attributes=True)

# Product List Response Schema
class ProductList(BaseModel):
    products: list[ProductOut]
    total: int
    page: int
    size: int

    model_config = ConfigDict(from_attributes=True)

# Schema for available attributes (to show what attributes can be used)
class AvailableAttribute(BaseModel):
    attribute_code: str
    attribute_name_en: str
    attribute_name_vn: str
    type_attribute: str
    attribute_group: str
    options: list[Dict[str, Any]] = []

    model_config = ConfigDict(from_attributes=True)

class AvailableAttributesResponse(BaseModel):
    attributes: list[AvailableAttribute]

# Dynamic schema creation functions
def create_dynamic_product_create_schema(attributes: list) -> Type[BaseModel]:
    """Create a dynamic ProductCreate schema with nested attribute object"""
    
    # Start with base fields
    fields = {
        'product_code': (str, ...),
        'status': (ProductStatus, ProductStatus.ACTIVE),
        'vendor_code': (str, ...),
        'operator_code': (str, ...),
        'supported_countries': (str, ...),
        'note': (Optional[str], None),
        'attribute': (Optional[Dict[str, str]], Field(default_factory=dict, description="Dynamic attributes"))
    }
    
    return create_model('ProductCreate', **fields, __base__=BaseModel)

def create_dynamic_product_update_schema(attributes: list) -> Type[BaseModel]:
    """Create a dynamic ProductUpdate schema with nested attribute object"""
    
    # Start with base fields (all optional for updates)
    fields = {
        'product_code': (Optional[str], None),
        'status': (Optional[ProductStatus], None),
        'vendor_code': (Optional[str], None),
        'operator_code': (Optional[str], None),
        'supported_countries': (Optional[str], None),
        'note': (Optional[str], None),
        'attribute': (Optional[Dict[str, str]], Field(default_factory=dict, description="Dynamic attributes"))
    }
    
    return create_model('ProductUpdate', **fields, __base__=BaseModel)

def create_dynamic_product_out_schema(attributes: list) -> Type[BaseModel]:
    """Create a dynamic ProductOut schema with nested attribute object"""
    
    # Start with base fields
    fields = {
        'id': (int, ...),
        'product_code': (str, ...),
        'status': (ProductStatus, ...),
        'vendor_code': (str, ...),
        'operator_code': (str, ...),
        'supported_countries': (str, ...),
        'note': (Optional[str], None),
        'date_created': (datetime, ...),
        'last_modified_date': (datetime, ...),
        'attribute': (Optional[Dict[str, str]], Field(default_factory=dict, description="Dynamic attributes"))
    }
    
    DynamicProductOut = create_model('DynamicProductOut', **fields, __base__=BaseModel)
    DynamicProductOut.model_config = ConfigDict(from_attributes=True)
    
    return DynamicProductOut

# Helper function to convert product data to match dynamic schema
def format_product_for_dynamic_schema(product, attributes: list) -> dict:
    """Format product data to match the dynamic schema with nested attribute object"""
    
    # Start with base product data
    result = {
        'id': product.id,
        'product_code': product.product_code,
        'status': product.status,
        'vendor_code': product.vendor_code,
        'operator_code': product.operator_code,
        'supported_countries': product.supported_countries,
        'note': product.note,
        'date_created': product.date_created,
        'last_modified_date': product.last_modified_date,
        'attribute': {}
    }
    
    # Add attributes to nested object
    for pavi in product.product_attribute_value_index:
        result['attribute'][pavi.attribute.attribute_code] = pavi.attribute_value
    
    return result

def extract_attributes_from_request(request_data: dict, attributes: list) -> dict:
    """Extract attribute values from request data with nested attribute object"""
    
    extracted_attributes = {}
    
    # Check if there's an 'attribute' object in the request
    if 'attribute' in request_data and isinstance(request_data['attribute'], dict):
        for attribute_code, value in request_data['attribute'].items():
            if value is not None:
                extracted_attributes[attribute_code] = value
    
    return extracted_attributes