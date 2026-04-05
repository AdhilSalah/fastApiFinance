from typing import List, Optional
from datetime import date
from fastapi import HTTPException, status
from library.db.finance import repository as repo
from library.db.finance.models import Finance, FinanceType
from finance.schemas import FinanceCreate, FinanceUpdate, SummaryResponse


def get_all_finances(
    from_date: date = None,
    to_date: date = None,
    limit: int = 100,
    offset: int = 0,
    search: Optional[str] = None,
    type: Optional[FinanceType] = None,
) -> List[Finance]:
    return repo.get_all(
        from_date=from_date,
        to_date=to_date,
        limit=limit,
        offset=offset,
        search=search,
        type=type,
    )


def get_finance(finance_id: int) -> Finance:
    entry = repo.get_by_id(finance_id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finance entry not found")
    return entry


def create_finance(data: FinanceCreate) -> Finance:
    return repo.create(
        amount=data.amount,
        type=data.type,
        category=data.category,
        date=data.date,
        notes=data.notes,
    )


def update_finance(finance_id: int, data: FinanceUpdate) -> Finance:
    entry = repo.update(finance_id, **data.model_dump(exclude_none=True))
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finance entry not found")
    return entry


def delete_finance(finance_id: int) -> None:
    if not repo.soft_delete(finance_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finance entry not found")


def get_summary(from_date: date = None, to_date: date = None) -> SummaryResponse:
    # Ensure get_summary uses all records in the date range, not just the first 100
    return SummaryResponse(**repo.get_summary(from_date=from_date, to_date=to_date))
