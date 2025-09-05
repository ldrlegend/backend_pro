from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.attribute import Attribute
from app.schemas.attribute import AttributeCreate, AttributeUpdate, AttributeOut

router = APIRouter()

@router.get("/", response_model=List[AttributeOut])
def get_attributes(db: Session = Depends(get_db)):
    """Get all attributes"""
    return db.query(Attribute).all()

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
    return db_attribute

@router.get("/{attribute_id}", response_model=AttributeOut)
def get_attribute(attribute_id: int, db: Session = Depends(get_db)):
    """Get a attribute by ID"""
    db_attribute = db.query(Attribute).filter(Attribute.id == attribute_id).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="attribute not found")
    return db_attribute

@router.get("/code/{attribute_code}", response_model=AttributeOut)
def get_attribute_by_code(attribute_code: str, db: Session = Depends(get_db)):
    """Get a attribute by code"""
    db_attribute = db.query(Attribute).filter(Attribute.attribute_code == attribute_code).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="attribute not found")
    return db_attribute

@router.put("/{attribute_id}", response_model=AttributeOut)
def update_attribute(attribute_id: int, attribute: AttributeUpdate, db: Session = Depends(get_db)):
    """Update a attribute"""
    db_attribute = db.query(Attribute).filter(Attribute.id == attribute_id).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="attribute not found")
    db_attribute.attribute_code = attribute.attribute_code
    db_attribute.attribute_name_vn = attribute.attribute_name_vn
    db_attribute.attribute_name_en = attribute.attribute_name_en
    db_attribute.type_attribute = attribute.type_attribute
    db_attribute.attribute_group = attribute.attribute_group
    db.commit()
    db.refresh(db_attribute)
    return db_attribute
