from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.country import Country
from app.schemas.country import CountryCreate, CountryUpdate, CountryOut

router = APIRouter()

@router.get("/", response_model=List[CountryOut])
def get_countries(db: Session = Depends(get_db)):
    """Get all countries"""
    return db.query(Country).all()

@router.post("/", response_model=CountryOut)
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    """Create a new country"""
    existing_country = db.query(Country).filter(Country.country_code == country.country_code).first()
    if existing_country:
        raise HTTPException(status_code=400, detail="Country code already exists")
    db_country = Country(**country.model_dump())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

@router.get("/{country_id}", response_model=CountryOut)
def get_country(country_id: int, db: Session = Depends(get_db)):
    """Get a country by ID"""
    db_country = db.query(Country).filter(Country.id == country_id).first()
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country

@router.get("/code/{country_code}", response_model=CountryOut)
def get_country_by_code(country_code: str, db: Session = Depends(get_db)):
    """Get a country by code"""
    db_country = db.query(Country).filter(Country.country_code == country_code).first()
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country

@router.put("/{country_id}", response_model=CountryOut)
def update_country(country_id: int, country: CountryUpdate, db: Session = Depends(get_db)):
    """Update a country"""
    db_country = db.query(Country).filter(Country.id == country_id).first()
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    db_country.country_code = country.country_code
    db_country.code = country.code
    db_country.country_name = country.country_name
