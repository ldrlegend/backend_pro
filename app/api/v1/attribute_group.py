from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.attribute_group import AttributeGroup
from app.schemas.attribute_group import AttributeGroupCreate, AttributeGroupUpdate, AttributeGroupOut

router = APIRouter()

@router.get("/", response_model=List[AttributeGroupOut])
def get_attribute_groups(db: Session = Depends(get_db)):
    """Get all attribute_groups"""
    return db.query(AttributeGroup).all()

@router.post("/", response_model=AttributeGroupOut)
def create_attribute_group(attribute_group: AttributeGroupCreate, db: Session = Depends(get_db)):
    """Create a new attribute group"""
    db_attribute_group = AttributeGroup(**attribute_group.model_dump())
    db.add(db_attribute_group)
    db.commit()
    db.refresh(db_attribute_group)
    return db_attribute_group

@router.get("/{attribute_id}", response_model=AttributeGroupOut)
def get_attribute_group(attribute_id: int, db: Session = Depends(get_db)):    
    """Get a attribute_group by ID"""
    db_attribute_group = db.query(AttributeGroup).filter(AttributeGroup.id == attribute_id).first()
    if not db_attribute_group:
        raise HTTPException(status_code=404, detail="attribute_group not found")
    return db_attribute_group

@router.get("/code/{attribute_code}", response_model=AttributeGroupOut)
def get_attribute_group_by_code(attribute_code: str, db: Session = Depends(get_db)):
    """Get a attribute_group by code"""
    db_attribute_group = db.query(AttributeGroup).filter(AttributeGroup.group_name == attribute_code).first()
    if not db_attribute_group:
        raise HTTPException(status_code=404, detail="attribute_group not found")
    return db_attribute_group   

@router.put("/{attribute_id}", response_model=AttributeGroupOut)
def update_attribute_group(attribute_id: int, attribute_group: AttributeGroupUpdate, db: Session = Depends(get_db)):
    """Update a attribute_group"""
    db_attribute_group = db.query(AttributeGroup).filter(AttributeGroup.id == attribute_id).first()
    if not db_attribute_group:
        raise HTTPException(status_code=404, detail="attribute_group not found")
    db_attribute_group.group_name = attribute_group.group_name
    db.commit()
    db.refresh(db_attribute_group)
    return db_attribute_group