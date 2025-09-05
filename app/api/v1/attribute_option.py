from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.attribute_option import AttributeOption
from app.schemas.attribute_option import AttributeOptionCreate, AttributeOptionUpdate, AttributeOptionOut

router = APIRouter()

@router.get("/", response_model=List[AttributeOptionOut])
def get_attributes(db: Session = Depends(get_db)):
    """Get all attributes"""
    return db.query(AttributeOption).all()

@router.post("/", response_model=AttributeOptionOut)
def create_attribute_option(attribute: AttributeOptionCreate, db: Session = Depends(get_db)):
    """Create a new attribute option"""
    db_attribute = AttributeOption(**attribute.model_dump())
    db.add(db_attribute)
    db.commit()
    db.refresh(db_attribute)
    return db_attribute

@router.get("/{attribute_id}", response_model=AttributeOptionOut)
def get_attribute_option(attribute_id: int, db: Session = Depends(get_db)):    
    """Get a attribute by ID"""
    db_attribute = db.query(AttributeOption).filter(AttributeOption.id == attribute_id).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="attribute not found")
    return db_attribute

@router.get("/code/{attribute_code}", response_model=AttributeOptionOut)
def get_attribute_option_by_code(attribute_code: str, db: Session = Depends(get_db)):
    """Get a attribute by code"""
    db_attribute = db.query(AttributeOption).filter(AttributeOption.attribute_code == attribute_code).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="attribute_option not found")
    return db_attribute

@router.put("/{attribute_id}", response_model=AttributeOptionOut)
def update_attribute_option(attribute_id: int, attribute: AttributeOptionUpdate, db: Session = Depends(get_db)):
    """Update a attribute_option"""
    db_attribute = db.query(AttributeOption).filter(AttributeOption.id == attribute_id).first()
    if not db_attribute:
        raise HTTPException(status_code=404, detail="attribute_option not found")
    db_attribute.attribute_code = attribute.attribute_code
    db_attribute.attribute_option_vn = attribute.attribute_option_vn
    db_attribute.attribute_option_en = attribute.attribute_option_en
    db.commit()
    db.refresh(db_attribute)
    return db_attribute
