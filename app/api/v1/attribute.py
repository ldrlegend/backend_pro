from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.db.session import get_db
from app.models.attribute import Attribute
from app.schemas.attribute import AttributeCreate, AttributeUpdate, AttributeOut

router = APIRouter()

@router.get("/", response_model=List[AttributeOut])
def get_attributes(db: Session = Depends(get_db)):
    """Get all attributes"""
    attributes = db.query(Attribute).options(joinedload(Attribute.attribute_group)).all()
    result = []
    for attr in attributes:
        attr_dict = {
            "id": attr.id,
            "attribute_code": attr.attribute_code,
            "attribute_name_vn": attr.attribute_name_vn,
            "attribute_name_en": attr.attribute_name_en,
            "type_attribute": attr.type_attribute.value if attr.type_attribute else None,
            "attribute_group_id": attr.attribute_group_id,
            "status": attr.status,
            "attribute_group_name": attr.attribute_group.group_name.value if attr.attribute_group else None,
            "date_created": attr.date_created,
            "last_modified_date": attr.last_modified_date
        }
        result.append(AttributeOut(**attr_dict))
    return result

@router.post("/", response_model=AttributeOut)
def create_attribute(attribute: AttributeCreate, db: Session = Depends(get_db)):
    """Create a new attribute"""
    existing_attribute = db.query(Attribute).filter(Attribute.attribute_code == attribute.attribute_code).first()
    if existing_attribute:
        raise HTTPException(status_code=400, detail="Attribute code already exists")
    db_attribute = Attribute(**attribute.model_dump())
    db.add(db_attribute)
    db.commit()
    db.refresh(db_attribute)
    
    # Reload with attribute group
    db_attribute = db.query(Attribute).options(joinedload(Attribute.attribute_group)).filter(Attribute.id == db_attribute.id).first()
    
    attr_dict = {
        "id": db_attribute.id,
        "attribute_code": db_attribute.attribute_code,
        "attribute_name_vn": db_attribute.attribute_name_vn,
        "attribute_name_en": db_attribute.attribute_name_en,
        "type_attribute": db_attribute.type_attribute.value if db_attribute.type_attribute else None,
        "attribute_group_id": db_attribute.attribute_group_id,
        "status": db_attribute.status,
        "attribute_group_name": db_attribute.attribute_group.group_name.value if db_attribute.attribute_group else None,
        "date_created": db_attribute.date_created,
        "last_modified_date": db_attribute.last_modified_date
    }
    return AttributeOut(**attr_dict)

@router.get("/{attribute_id}", response_model=AttributeOut)
def get_attribute(attribute_id: int, db: Session = Depends(get_db)):
    """Get a attribute by ID"""
    db_attribute = db.query(Attribute).options(joinedload(Attribute.attribute_group)).filter(Attribute.id == attribute_id).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="attribute not found")
    
    attr_dict = {
        "id": db_attribute.id,
        "attribute_code": db_attribute.attribute_code,
        "attribute_name_vn": db_attribute.attribute_name_vn,
        "attribute_name_en": db_attribute.attribute_name_en,
        "type_attribute": db_attribute.type_attribute.value if db_attribute.type_attribute else None,
        "attribute_group_id": db_attribute.attribute_group_id,
        "status": db_attribute.status,
        "attribute_group_name": db_attribute.attribute_group.group_name.value if db_attribute.attribute_group else None,
        "date_created": db_attribute.date_created,
        "last_modified_date": db_attribute.last_modified_date
    }
    return AttributeOut(**attr_dict)

@router.get("/code/{attribute_code}", response_model=AttributeOut)
def get_attribute_by_code(attribute_code: str, db: Session = Depends(get_db)):
    """Get a attribute by code"""
    db_attribute = db.query(Attribute).options(joinedload(Attribute.attribute_group)).filter(Attribute.attribute_code == attribute_code).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="attribute not found")
    
    attr_dict = {
        "id": db_attribute.id,
        "attribute_code": db_attribute.attribute_code,
        "attribute_name_vn": db_attribute.attribute_name_vn,
        "attribute_name_en": db_attribute.attribute_name_en,
        "type_attribute": db_attribute.type_attribute.value if db_attribute.type_attribute else None,
        "attribute_group_id": db_attribute.attribute_group_id,
        "status": db_attribute.status,
        "attribute_group_name": db_attribute.attribute_group.group_name.value if db_attribute.attribute_group else None,
        "date_created": db_attribute.date_created,
        "last_modified_date": db_attribute.last_modified_date
    }
    return AttributeOut(**attr_dict)

@router.put("/{attribute_id}", response_model=AttributeOut)
def update_attribute(attribute_id: int, attribute: AttributeUpdate, db: Session = Depends(get_db)):
    """Update a attribute"""
    db_attribute = db.query(Attribute).options(joinedload(Attribute.attribute_group)).filter(Attribute.id == attribute_id).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="attribute not found")
    
    if attribute.attribute_code is not None:
        db_attribute.attribute_code = attribute.attribute_code
    if attribute.attribute_name_vn is not None:
        db_attribute.attribute_name_vn = attribute.attribute_name_vn
    if attribute.attribute_name_en is not None:
        db_attribute.attribute_name_en = attribute.attribute_name_en
    if attribute.type_attribute is not None:
        db_attribute.type_attribute = attribute.type_attribute
    if attribute.attribute_group_id is not None:
        db_attribute.attribute_group_id = attribute.attribute_group_id
    if attribute.status is not None:
        db_attribute.status = attribute.status
    
    db.commit()
    db.refresh(db_attribute)
    
    attr_dict = {
        "id": db_attribute.id,
        "attribute_code": db_attribute.attribute_code,
        "attribute_name_vn": db_attribute.attribute_name_vn,
        "attribute_name_en": db_attribute.attribute_name_en,
        "type_attribute": db_attribute.type_attribute.value if db_attribute.type_attribute else None,
        "attribute_group_id": db_attribute.attribute_group_id,
        "status": db_attribute.status,
        "attribute_group_name": db_attribute.attribute_group.group_name.value if db_attribute.attribute_group else None,
        "date_created": db_attribute.date_created,
        "last_modified_date": db_attribute.last_modified_date
    }
    return AttributeOut(**attr_dict)
