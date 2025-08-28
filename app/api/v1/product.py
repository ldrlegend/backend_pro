from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.product import Product
from app.utils.enums.status import Status
from app.utils.enums.type_of_sim import TypeOfSim as SimType
from app.utils.enums.purchase_type import PurchaseType
from app.utils.enums.sku_type import SkuType
from app.utils.enums.data_type import DataType
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut, ProductList

router = APIRouter()

@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    # Check if product_code already exists
    existing_product = db.query(Product).filter(Product.product_code == product.product_code).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product code already exists")
    
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductOut])
def get_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    status: Optional[Status] = Query(None, description="Filter by status"),
    # operator_code: Optional[OperatorCode] = Query(None, description="Filter by operator"),
    # vendor_code: Optional[VendorCode] = Query(None, description="Filter by vendor"),
    purchase_type: Optional[PurchaseType] = Query(None, description="Filter by purchase type"),
    db: Session = Depends(get_db)
):
    """Get all products with optional filtering"""
    query = db.query(Product)
    
    # Apply filters
    if status:
        query = query.filter(Product.status == status)
    # if operator_code:
    #     query = query.filter(Product.operator_code == operator_code)
    # if vendor_code:
    #     query = query.filter(Product.vendor_code == vendor_code)
    if purchase_type:
        query = query.filter(Product.purchase_type == purchase_type)
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/code/{product_code}", response_model=ProductOut)
def get_product_by_code(product_code: str, db: Session = Depends(get_db)):
    """Get a specific product by product code"""
    product = db.query(Product).filter(Product.product_code == product_code).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    """Update a product"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if new product_code already exists (if being updated)
    if product_update.product_code and product_update.product_code != db_product.product_code:
        existing_product = db.query(Product).filter(Product.product_code == product_update.product_code).first()
        if existing_product:
            raise HTTPException(status_code=400, detail="Product code already exists")
    
    # Update only provided fields
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product (soft delete by setting status to deleted)"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.status = Status.DELETED
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/enums/status", response_model=List[str])
def get_status_options():
    """Get all available status options"""
    return [status.value for status in Status]

@router.get("/enums/sim-types", response_model=List[str])
def get_sim_type_options():
    """Get all available SIM type options"""
    return [sim_type.value for sim_type in SimType]

# @router.get("/enums/operators", response_model=List[str])
# def get_operator_options():
#     """Get all available operator options"""
#     return [operator.value for operator in OperatorCode]

# @router.get("/enums/vendors", response_model=List[str])
# def get_vendor_options():
#     """Get all available vendor options"""
#     return [vendor.value for vendor in VendorCode]

@router.get("/enums/purchase-types", response_model=List[str])
def get_purchase_type_options():
    """Get all available purchase type options"""
    return [purchase_type.value for purchase_type in PurchaseType]

@router.get("/enums/sku-types", response_model=List[str])
def get_sku_type_options():
    """Get all available SKU type options"""
    return [sku_type.value for sku_type in SkuType]

@router.get("/enums/data-types", response_model=List[str])
def get_data_type_options():
    """Get all available data type options"""
    return [data_type.value for data_type in DataType]
