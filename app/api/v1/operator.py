from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.operator import Operator
from app.schemas.operator import OperatorCreate, OperatorUpdate, OperatorOut

router = APIRouter()

@router.get("/", response_model=List[OperatorOut])
def get_operators(db: Session = Depends(get_db)):
    """Get all operators"""
    return db.query(Operator).all()

@router.post("/", response_model=OperatorOut)
def create_operator(operator: OperatorCreate, db: Session = Depends(get_db)):
    """Create a new operator"""
    existing_operator = db.query(Operator).filter(Operator.operator_code == operator.operator_code).first()
    if existing_operator:
        raise HTTPException(status_code=400, detail="Operator code already exists")
    db_operator = Operator(**operator.model_dump())
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator

@router.get("/{operator_id}", response_model=OperatorOut)
def get_operator(operator_id: int, db: Session = Depends(get_db)):
    """Get an operator by ID"""
    db_operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if not db_operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return db_operator

@router.get("/code/{operator_code}", response_model=OperatorOut)
def get_operator_by_code(operator_code: str, db: Session = Depends(get_db)):
    """Get an operator by code"""
    db_operator = db.query(Operator).filter(Operator.operator_code == operator_code).first()
    if not db_operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return db_operator

@router.put("/{operator_id}", response_model=OperatorOut)
def update_operator(operator_id: int, operator: OperatorUpdate, db: Session = Depends(get_db)):
    """Update an operator"""
    db_operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if not db_operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    db_operator.operator_code = operator.operator_code
    db_operator.code = operator.code
    db_operator.operator_name = operator.operator_name
