from pydantic import BaseModel
from typing import Optional
from datetime import date
from library.db.finance.models import FinanceType
from typing import List, Dict

class FinanceCreate(BaseModel):
    amount: float
    type: FinanceType
    category: str
    date: date
    notes: Optional[str] = None


class FinanceUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[FinanceType] = None
    category: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None


class FinanceResponse(BaseModel):
    id: int
    amount: float
    type: FinanceType
    category: str
    date: date
    notes: Optional[str] = None

    class Config:
        from_attributes = True





class SummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    category_totals: Dict[str, float]
    recent_activity: List[FinanceResponse]
    trends: Dict[str, float]
