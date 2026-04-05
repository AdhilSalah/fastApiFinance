from fastapi import Depends
from typing import List, Optional
from datetime import date
from library.access.router import AccessRouter, Access
from library.access.permissions import Resource, Action
from library.auth.dependencies import get_current_user
from library.db.users.models import User
from library.db.finance.models import Finance, FinanceType
from finance.schemas import FinanceCreate, FinanceUpdate, FinanceResponse, SummaryResponse
import finance.service as service

router = AccessRouter()


@router.get("/", response_model=List[FinanceResponse])
@Access(Resource.Finance, Action.Read)
async def list_finances(
    from_date: date = None,
    to_date: date = None,
    limit: int = 100,
    offset: int = 0,
    search: Optional[str] = None,
    type: Optional[FinanceType] = None,
):
    return service.get_all_finances(
        from_date=from_date,
        to_date=to_date,
        limit=limit,
        offset=offset,
        search=search,
        type=type,
    )


@router.get("/dashboard", response_model=SummaryResponse)
@Access(Resource.Dashboard, Action.Read)
async def get_summary(from_date: date = None, to_date: date = None):
    return service.get_summary(from_date=from_date, to_date=to_date)


@router.get("/{finance_id}", response_model=FinanceResponse)
@Access(Resource.Finance, Action.Read)
async def get_finance(finance_id: int):
    return service.get_finance(finance_id)


@router.post("/", response_model=FinanceResponse, status_code=201)
@Access(Resource.Finance, Action.Create)
async def create_finance(data: FinanceCreate):
    return service.create_finance(data)


@router.put("/{finance_id}", response_model=FinanceResponse)
@Access(Resource.Finance, Action.Update)
async def update_finance(finance_id: int, data: FinanceUpdate):
    return service.update_finance(finance_id, data)


@router.delete("/{finance_id}", status_code=204)
@Access(Resource.Finance, Action.Delete)
async def delete_finance(finance_id: int):
    service.delete_finance(finance_id)
