from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from typing import List
from datetime import date

from app.models.promotions import Promotion
from app.database import AsyncSessionLocal
from app.schemas.promotion import PromotionOut

router = APIRouter(prefix="/promotions", tags=["Promotions"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/", response_model=List[PromotionOut])
async def get_promotions(
    merchant: str | None = Query(None, description="Filter by merchant name"),
    valid_before: date | None = Query(None, description="Filter promotions valid before this date"),
    db: AsyncSession = Depends(get_db),
):
    query = select(Promotion)

    filters = []
    if merchant:
        filters.append(Promotion.merchant == merchant)
    if valid_before:
        filters.append(Promotion.valid_to >= valid_before)

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)
    promotions = result.scalars().all()
    return promotions
