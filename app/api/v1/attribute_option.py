from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.attribute_option import AttributeOption
from app.schemas.attribute_option import AttributeOptionCreate, AttributeOptionUpdate, AttributeOptionOut

router = APIRouter()

@router.get("/", response_model=List[AttributeOptionOut])
def get_attribute_options(db: Session = Depends(get_db)):
    """Get all attribute_options"""
    return db.query(AttributeOption).all()

@router.post("/", response_model=AttributeOptionOut)
def create_attribute_option(attribute_option: AttributeOptionCreate, db: Session = Depends(get_db)):
    """Create a new attribute option"""
    existing_attribute_option = db.query(AttributeOption).filter(AttributeOption.attribute_code == attribute_option.attribute_code).first()
    if existing_attribute_option:
        raise HTTPException(status_code=400, detail="Attribute option already exists")
    db_attribute_option = AttributeOption(**attribute_option.model_dump())
    db.add(db_attribute_option)
    db.commit()
    db.refresh(db_attribute_option)
    return db_attribute_option

@router.get("/{attribute_id}", response_model=AttributeOptionOut)
def get_attribute_option(attribute_id: int, db: Session = Depends(get_db)):    
    """Get a attribute_option by ID"""
    db_attribute_option = db.query(AttributeOption).filter(AttributeOption.id == attribute_id).first()
    if not db_attribute_option:
        raise HTTPException(status_code=404, detail="attribute_option not found")
    return db_attribute_option

@router.get("/code/{attribute_code}", response_model=AttributeOptionOut)
def get_attribute_option_by_code(attribute_code: str, db: Session = Depends(get_db)):
    """Get a attribute_option by code"""
    db_attribute_option = db.query(AttributeOption).filter(AttributeOption.attribute_code == attribute_code).first()
    if not db_attribute_option:
        raise HTTPException(status_code=404, detail="attribute_option not found")
    return db_attribute_option

@router.put("/{attribute_id}", response_model=AttributeOptionOut)
def update_attribute_option(attribute_id: int, attribute_option: AttributeOptionUpdate, db: Session = Depends(get_db)):
    """Update a attribute_option"""
    db_attribute_option = db.query(AttributeOption).filter(AttributeOption.id == attribute_id).first()
    if not db_attribute_option:
        raise HTTPException(status_code=404, detail="attribute_option not found")
    db_attribute_option.attribute_code = attribute_option.attribute_code
    db_attribute_option.attribute_option_vn = attribute_option.attribute_option_vn
    db_attribute_option.attribute_option_en = attribute_option.attribute_option_en
    db.commit()
    db.refresh(db_attribute_option)
    return db_attribute_option
