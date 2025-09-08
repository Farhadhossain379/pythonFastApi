from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import Customer
from schemas import CustomerCreate, CustomerUpdate, CustomerOut
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.post("/addCustomer", response_model=CustomerOut)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)   # JWT protected
):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/getAllCustomers", response_model=List[CustomerOut])
def read_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Customer).offset(skip).limit(limit).all()

@router.get("/getCustomerById/{customer_id}", response_model=CustomerOut)
def read_customer(customer_id: int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    db_customer = db.query(Customer).filter(Customer.customerid == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/updateCustomerById/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    db_customer = db.query(Customer).filter(Customer.customerid == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/deleteCustomerById/{customer_id}", response_model=CustomerOut)
def delete_customer(customer_id: int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    db_customer = db.query(Customer).filter(Customer.customerid == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return db_customer
