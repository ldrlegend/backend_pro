from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorOut

router = APIRouter()

@router.get("/", response_model=List[VendorOut])
def get_vendors(db: Session = Depends(get_db)):
    """Get all vendors"""
    return db.query(Vendor).all()

@router.post("/", response_model=VendorOut)
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    """Create a new vendor"""
    existing_vendor = db.query(Vendor).filter(Vendor.vendor_code == vendor.vendor_code).first()
    if existing_vendor:
        raise HTTPException(status_code=400, detail="Vendor code already exists")
    db_vendor = Vendor(**vendor.model_dump())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

@router.get("/{vendor_id}", response_model=VendorOut)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    """Get a vendor by ID"""
    db_vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@router.get("/code/{vendor_code}", response_model=VendorOut)
def get_vendor_by_code(vendor_code: str, db: Session = Depends(get_db)):
    """Get a vendor by code"""
    db_vendor = db.query(Vendor).filter(Vendor.vendor_code == vendor_code).first()
    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@router.put("/{vendor_id}", response_model=VendorOut)
def update_vendor(vendor_id: int, vendor: VendorUpdate, db: Session = Depends(get_db)):
    """Update a vendor"""
    db_vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    db_vendor.vendor_code = vendor.vendor_code
    db_vendor.code = vendor.code
    db_vendor.vendor_name = vendor.vendor_name
