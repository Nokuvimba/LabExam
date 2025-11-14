from typing import Annotated, Optional, List
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict
from annotated_types import  Ge,Le

CustomerStr = Annotated[Str, StringConstraints(pattern=r"^s\d{7}$")]
NameStr     = Annotated[Str, StringConstraints(min_length=1, max_length=100)]
YearInt = Annotated[int, Ge(2000), Le(2100)]

OrderInt = Annotated[int, Ge(3), Le(20)]
CentsInt = Annotated[int, Ge(1), Le(1 000 000)]

class CustomerCreate(BaseModel):
    name : NameStr
    customer_id : CustomerStr
    email: EmailStr
    customer_since: YearInt

class CustomerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name : NameStr
    customer_id : CustomerStr
    email: EmailStr
    customer_since: YearInt

class CustomerUpdatePUT(BaseModel):
    name : NameStr
    customer_id : CustomerStr
    email: EmailStr
    customer_since: YearInt

class CustomerUpdatePATCH(BaseModel):
    name : Optional[NameStr]=None
    customer_id : Optional[CustomerStr]=None
    email: Optional[EmailStr]=None
    customer_since: Optional[YearInt]=None

class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_number: OrderInt
    total_cents: CentsInt

class OrderCreate(BaseModel):
    order_number: OrderInt
    total_cents: CentsInt

class CustomerReadWithOrders(CustomerRead):
    orders: List[OrderRead] = []

class OrderReadWithCustomer(OrderRead):
    customer: Option["CustomerRead"]=None
