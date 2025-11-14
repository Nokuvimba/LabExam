from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint

class Base(DeclarativeBase):
    pass

class CustomerDB(Base):
    _tablename_ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(100), nullable=False)
    customer_id : Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(Integer, nullable=False)
    customer_since: Mapped[int] = mapped_column(Integer, nullable=False)

    orders: Mapped[List["OrderDB"]]=relationship(back_populates="customer", cascade="all, delete-orphan")

class OrderDB(Base):
    _tablename_ ="orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[int] = mapped_column(Integer, nullable=False)
    total_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    customer_id: Mapped[int] =mapped_column(ForeignKey("customers.id", on delete="CASCADE"), nullable=False)
    customer: Mapped["CustomerDB"]= relationship(back_populates="projects")