from typing import List, Optional
from datetime import date
from sqlalchemy import func
from library.db.database import db_session
from library.db.finance.models import Finance, FinanceType
from collections import defaultdict
from datetime import timedelta, date as date_type

def get_all(
    from_date: Optional[date_type] = None,
    to_date: Optional[date_type] = None,
    limit: int = 100,
    offset: int = 0,
    search: Optional[str] = None,
    type: Optional[FinanceType] = None,
) -> List[Finance]:
    with db_session() as db:
        query = db.query(Finance).filter(Finance.deleted_at == None)
        
        if from_date:
            query = query.filter(Finance.date >= from_date)
        if to_date:
            query = query.filter(Finance.date <= to_date)
            
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Finance.category.ilike(search_filter)) | (Finance.notes.ilike(search_filter))
            )
            
        if type:
            query = query.filter(Finance.type == type)
            
        if limit is not None:
            query = query.offset(offset).limit(limit)
            
        return query.all()


def get_by_id(finance_id: int) -> Optional[Finance]:
    with db_session() as db:
        return db.query(Finance).filter(Finance.id == finance_id, Finance.deleted_at == None).first()


def create(
    amount: float,
    type: FinanceType,
    category: str,
    date: date,
    notes: Optional[str] = None,
) -> Finance:
    with db_session() as db:
        entry = Finance(
            amount=amount,
            type=type,
            category=category,
            date=date,
            notes=notes,
        )
        db.add(entry)
        db.flush()
        db.refresh(entry)
        return entry


def update(finance_id: int, **kwargs) -> Optional[Finance]:
    with db_session() as db:
        entry = db.query(Finance).filter(Finance.id == finance_id, Finance.deleted_at == None).first()
        if not entry:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(entry, key, value)
        db.flush()
        db.refresh(entry)
        return entry


def delete(finance_id: int) -> bool:
    with db_session() as db:
        entry = db.query(Finance).filter(Finance.id == finance_id, Finance.deleted_at == None).first()
        if not entry:
            return False
        db.delete(entry)
        return True


def soft_delete(finance_id: int) -> bool:
    with db_session() as db:
        entry = db.query(Finance).filter(Finance.id == finance_id, Finance.deleted_at == None).first()
        if not entry:
            return False
        entry.deleted_at = func.now()
        return True





def get_summary(from_date: Optional[date_type] = None, to_date: Optional[date_type] = None) -> dict:
    all_entries = get_all(from_date=from_date, to_date=to_date)
    
    total_income = sum(e.amount for e in all_entries if e.type == FinanceType.income)
    total_expenses = sum(e.amount for e in all_entries if e.type == FinanceType.expense)
    
    category_totals = defaultdict(float)
    for e in all_entries:
        category_totals[e.category] += e.amount
        
    recent_activity = sorted(all_entries, key=lambda x: x.date, reverse=True)[:5]
    
    # Trends: last 7 days
    today = date_type.today()
    last_7_days = [today - timedelta(days=i) for i in range(7)]
    trends = {d.isoformat(): 0.0 for d in last_7_days}
    
    for e in all_entries:
        date_str = e.date.isoformat()
        if date_str in trends:
            trends[date_str] += e.amount if e.type == FinanceType.income else -e.amount
            
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": total_income - total_expenses,
        "category_totals": dict(category_totals),
        "recent_activity": recent_activity,
        "trends": trends
    }
