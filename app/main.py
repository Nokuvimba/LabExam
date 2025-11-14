# app/main.py
from typing import Optional

from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine, SessionLocal
from app.models import Base
#from app.schemas import 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (dev/exam). Prefer Alembic in production.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


# ---- Health ----
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/customers",response_model=CustomerRead,status_code=status.HTTP_201_CREATED)
def create_customer(payload:CustomerCreate, db:Session = Depends(get_db)):
    customer = CustomerCreate(**payload.model_dump())
    db.add(customer)
    commit_or_rollback(db, "Customer already exists")
    db.refresh(customer)
    return customer

@app.get("/api/customers",response_model=list[CustomerRead])
def list_customers(db:Session = Depends(get_db)):
    stmt = select(CustomerDB).order_by(CustomerDB.id)
    result = db.execute(stmt)
    users =result.scalars().all()
    return customers

@app.get("/api/customers/{customer_id}",response_model=list[CustomerRead])
def get_customer_byId(customer_id: int,db:Session = Depends(get_db)):
      stmt = select(CustomerDB).order_by(CustomerDB.id)
    result = db.execute(stmt)
    users =result.scalars().all()
    return customers  

@app.put("/api/customers/{customer_id}",response_model=CustomerRead)
def put_customer(customer_id: int,payload: CustomerUpdatePUT,db:Session = Depends(get_db)):
    customer=db.get(CustomerDB, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.name = payload.name
    customer.email = payload.email
    customer.customer_since = payload.customer_since
    customer.customer_id =payload.customer_id

    commit_or_rollback(db, "Customer already exists")
    db.refresh(customer)
    return customer

@app.patch("/api/customers/{customer_id}",response_model=CustomerRead)
def patch_customer(customer_id: int,payload: CustomerUpdatePATCH,db:Session = Depends(get_db)):
    customer=db.get(CustomerDB, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        data.payload.model_dump(exclude_unset=True)
        for k, v in data.items():
            setattr(customer,k,v)

    commit_or_rollback(db, "Customer already exists")
    db.refresh(customer)
    return customer

@app.delete("/api/customers/{customer_id}", status_code=204)
def delete_customer(customer_id: int,db:Session = Depends(get_db)) ->Response:
    customer=db.get(CustomerDB, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return Response(status_code=status.HTTP_202_NO_CONTENT)

@app.post("/api/orders",response_model=OrderRead,status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate,db:Session = Depends(get_db)):
    customer =db.get(CustomerDB, order.customer_id)
     if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    order = OrderDB(
        id=order.id, 
        order_number=order.order_number,
        totalCents=order.total_cents,
    )
    db.add(order)
        commit_or_rollback(db, "order already exists")
    db.refresh(customer)
    return order
   
@app.get("/api/oders", response_model=list[OrderRead])
def list_orders(db:Session = Depends(get_db)):
    stmt=select(OrderDB).order_by(OrderDB.id)
    return db.execute(stmt).scalars().all()

@app.get("/api/orders", response_model=list[OrderReadWithCustomer])
def get_orders_with_customer(order_id: int,db:Session = Depends(get_db)):
    stmt=select(OrderDB).whre(OrderDB.id==order_id).options(selectinload OrderDB.customer)
    order=db.execute(stmt).scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="order not found")

