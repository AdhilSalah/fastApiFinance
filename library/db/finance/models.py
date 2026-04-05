import enum
from datetime import date as date_type
from sqlalchemy import Column, Integer, Float, String, Enum, Date, DateTime, func
from library.db.database import Base


class FinanceType(str, enum.Enum):
    income = "income"
    expense = "expense"


class Finance(Base):
    __tablename__ = "finances"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(FinanceType), nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(String, nullable=True)

    # Audit fields
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
