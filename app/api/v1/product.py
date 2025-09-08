from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional, Any
from app.db.session import get_db
from app.models.product import Product
from app.models.attribute import Attribute
from app.models.attribute_group import AttributeGroup, AttributeGroupName
from app.models.attribute_option import AttributeOption
from app.models.product_attribute_value_index import ProductAttributeValueIndex
from app.models.attribute_group_link import AttributeGroupLink
from app.utils.enums.status import Status
from app.schemas.product import (
    ProductOut, ProductList, AvailableAttribute, AvailableAttributesResponse,
    create_dynamic_product_create_schema, create_dynamic_product_update_schema,
    create_dynamic_product_out_schema, format_product_for_dynamic_schema,
    extract_attributes_from_request
)

router = APIRouter()

def get_product_attributes(db: Session) -> list[AvailableAttribute]:
    """Get all available attributes for the 'product' group"""
    # Temporarily get all attributes until database is updated with attribute_group_id column
    attributes = db.query(Attribute).join(AttributeGroupLink).join(AttributeGroup).filter(
        AttributeGroup.group_name == AttributeGroupName.product
    ).options(
        joinedload(Attribute.attribute_group_links).joinedload(AttributeGroupLink.attribute_group),
        joinedload(Attribute.attribute_options)
    ).all()
    
    available_attributes = []
    for attr in attributes:
        options = [
            {
                "id": opt.id,
                "attribute_option_en": opt.attribute_option_en,
                "attribute_option_vn": opt.attribute_option_vn
            }
            for opt in attr.attribute_options
        ]
        
        # Temporarily set group name as "Product" until database is updated with attribute_group_id column
        group_name = "Product"
        
        available_attributes.append(AvailableAttribute(
            attribute_code=attr.attribute_code,
            attribute_name_en=attr.attribute_name_en,
            attribute_name_vn=attr.attribute_name_vn,
            type_attribute=attr.type_attribute.value,
            attribute_group=group_name,
            options=options
        ))
    
    return available_attributes

@router.get("/available-attributes", response_model=AvailableAttributesResponse)
def get_available_attributes(db: Session = Depends(get_db)):
    """Get all available attributes for the 'product' group"""
    attributes = get_product_attributes(db)
    return AvailableAttributesResponse(attributes=attributes)


@router.post("/")
def create_product(request_data: dict, db: Session = Depends(get_db)):
    """Create a new product with dynamic attributes"""
    
    # Get available attributes to validate against
    attributes = get_product_attributes(db)
    
    # Create dynamic schema and validate request
    ProductCreateSchema = create_dynamic_product_create_schema(attributes)
    
    try:
        validated_data = ProductCreateSchema(**request_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    
    # Check if product_code already exists
    existing_product = db.query(Product).filter(Product.product_code == validated_data.product_code).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product code already exists")
    
    # Create base product (exclude attribute from model_dump)
    base_product_data = {
        'product_code': validated_data.product_code,
        'status': validated_data.status,
        'vendor_code': validated_data.vendor_code,
        'operator_code': validated_data.operator_code,
        'supported_countries': validated_data.supported_countries,
        'note': validated_data.note,
    }
    
    db_product = Product(**base_product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Extract and handle dynamic attributes
    attribute_values = extract_attributes_from_request(request_data, attributes)
    
    for attribute_code, option_value in attribute_values.items():
        if option_value:  # Only process non-empty values
            # Find the attribute
            attribute = db.query(Attribute).filter(
                Attribute.attribute_code == attribute_code
            ).first()
            if not attribute:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Attribute '{attribute_code}' not found in product group"
                )
            
            # Find the attribute option
            attribute_option = None
            if option_value.isdigit():
                # Try to find by ID first
                attribute_option = db.query(AttributeOption).filter(
                    AttributeOption.id == int(option_value),
                    AttributeOption.attribute_code == attribute_code
                ).first()
            
            if not attribute_option:
                # Try to find by text (English or Vietnamese)
                attribute_option = db.query(AttributeOption).filter(
                    AttributeOption.attribute_code == attribute_code,
                    (AttributeOption.attribute_option_en == option_value) |
                    (AttributeOption.attribute_option_vn == option_value)
                ).first()
            
            if not attribute_option:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Attribute option '{option_value}' not found for attribute '{attribute_code}'"
                )
            
            # Create the mapping
            pavi = ProductAttributeValueIndex(
                product_id=db_product.id,
                attribute_id=attribute.id,
                attribute_option_id=attribute_option.id
            )
            db.add(pavi)
    
    db.commit()
    db.refresh(db_product)
    
    # Format response using dynamic schema
    ProductOutSchema = create_dynamic_product_out_schema(attributes)
    response_data = format_product_for_dynamic_schema(db_product, attributes)
    
    return ProductOutSchema(**response_data)

@router.get("/")
def get_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    status: Optional[Status] = Query(None, description="Filter by status"),
    dynamic_schema: bool = Query(True, description="Use dynamic schema with attribute fields"),
    db: Session = Depends(get_db)
):
    """Get all products with their dynamic attributes"""
    query = db.query(Product)
    
    # Apply filters
    if status:
        query = query.filter(Product.status == status)
    
    # if dynamic_schema:
    #     # Temporarily get all products with attributes until database is updated
    #     query = query.join(ProductAttributeValueIndex).join(Attribute).join(AttributeGroupLink).join(AttributeGroup).filter(
    #         AttributeGroup.group_name == AttributeGroupName.product
    #     ).distinct()
    #     # Load relationships for dynamic schema
    #     query = query.options(
    #         joinedload(Product.product_attribute_value_index)
    #         .joinedload(ProductAttributeValueIndex.attribute)
    #         .joinedload(Attribute.attribute_group_links)
    #         .joinedload(AttributeGroupLink.attribute_group),
    #         joinedload(Product.product_attribute_value_index)
    #         .joinedload(ProductAttributeValueIndex.attribute_option)
    # )
    
    products = query.offset(skip).limit(limit).all()
    
    if dynamic_schema:
        # Return with dynamic schema
        attributes = get_product_attributes(db)
        print(attributes)
        ProductOutSchema = create_dynamic_product_out_schema(attributes)
        return [ProductOutSchema(**format_product_for_dynamic_schema(product, attributes)) for product in products]
    else:
        # Return with static schema
        return [ProductOut.model_validate(product) for product in products]


@router.get("/{product_id}")
def get_product(
    product_id: int, 
    dynamic_schema: bool = Query(True, description="Use dynamic schema with attribute fields"),
    db: Session = Depends(get_db)
):
    """Get a specific product by ID with its dynamic attributes"""
    product = db.query(Product).options(
        joinedload(Product.product_attribute_value_index)
        .joinedload(ProductAttributeValueIndex.attribute),
        joinedload(Product.product_attribute_value_index)
        .joinedload(ProductAttributeValueIndex.attribute_option)
    ).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if dynamic_schema:
        # Return with dynamic schema showing attribute.* fields
        attributes = get_product_attributes(db)
        ProductOutSchema = create_dynamic_product_out_schema(attributes)
        response_data = format_product_for_dynamic_schema(product, attributes)
        
        return ProductOutSchema(**response_data)
    else:
        # Return with static schema
        return ProductOut.model_validate(product)

@router.get("/code/{product_code}")
def get_product_by_code(
    product_code: str,
    dynamic_schema: bool = Query(True, description="Use dynamic schema with attribute fields"),
    db: Session = Depends(get_db)
):
    """Get a specific product by product code with its dynamic attributes"""
    product = db.query(Product).filter(Product.product_code == product_code).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if dynamic_schema:
        # Return with dynamic schema showing attribute.* fields
        attributes = get_product_attributes(db)
        ProductOutSchema = create_dynamic_product_out_schema(attributes)
        response_data = format_product_for_dynamic_schema(product, attributes)
        return ProductOutSchema(**response_data)
    else:
        # Return with static schema
        return ProductOut.model_validate(product)

@router.put("/{product_id}")
def update_product(product_id: int, request_data: dict, db: Session = Depends(get_db)):
    """Update a product and its dynamic attributes"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get available attributes to validate against
    attributes = get_product_attributes(db)
    
    # Create dynamic schema and validate request
    ProductUpdateSchema = create_dynamic_product_update_schema(attributes)
    
    try:
        validated_data = ProductUpdateSchema(**request_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    
    # Check if new product_code already exists (if being updated)
    if validated_data.product_code and validated_data.product_code != db_product.product_code:
        existing_product = db.query(Product).filter(Product.product_code == validated_data.product_code).first()
        if existing_product:
            raise HTTPException(status_code=400, detail="Product code already exists")
    
    # Update base product fields
    base_fields = ['product_code', 'status', 'vendor_code', 'operator_code', 'supported_countries', 'note']
    for field in base_fields:
        value = getattr(validated_data, field, None)
        if value is not None:
            setattr(db_product, field, value)
    
    # Extract and handle attribute updates
    attribute_values = extract_attributes_from_request(request_data, attributes)
    
    if attribute_values:
        # Remove existing attributes that are being updated
        for attribute_code in attribute_values.keys():
            attribute = db.query(Attribute).filter(Attribute.attribute_code == attribute_code).first()
            if attribute:
                db.query(ProductAttributeValueIndex).filter(
                    ProductAttributeValueIndex.product_id == product_id,
                    ProductAttributeValueIndex.attribute_id == attribute.id
                ).delete()
        
        # Add new attribute values
        for attribute_code, option_value in attribute_values.items():
            if option_value:  # Only process non-empty values
                # Find the attribute
                attribute = db.query(Attribute).filter(
                    Attribute.attribute_code == attribute_code
                ).first()
                if not attribute:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Attribute '{attribute_code}' not found in product group"
                    )
                
                # Find the attribute option
                attribute_option = None
                if option_value.isdigit():
                    attribute_option = db.query(AttributeOption).filter(
                        AttributeOption.id == int(option_value),
                        AttributeOption.attribute_code == attribute_code
                    ).first()
                
                if not attribute_option:
                    attribute_option = db.query(AttributeOption).filter(
                        AttributeOption.attribute_code == attribute_code,
                        (AttributeOption.attribute_option_en == option_value) |
                        (AttributeOption.attribute_option_vn == option_value)
                    ).first()
                
                if not attribute_option:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Attribute option '{option_value}' not found for attribute '{attribute_code}'"
                    )
                
                # Create the mapping
                pavi = ProductAttributeValueIndex(
                    product_id=db_product.id,
                    attribute_id=attribute.id,
                    attribute_option_id=attribute_option.id
                )
                db.add(pavi)
    
    db.commit()
    db.refresh(db_product)
    
    # Format response using dynamic schema
    ProductOutSchema = create_dynamic_product_out_schema(attributes)
    response_data = format_product_for_dynamic_schema(db_product, attributes)
    
    return ProductOutSchema(**response_data)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product (soft delete by setting status to deleted)"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.status = Status.DELETED
    db.commit()
    return {"message": "Product deleted successfully"}