from fastapi import APIRouter

router = APIRouter(prefix="/promotions", tags=["Promotions"])


@router.get("/")
async def list_promotions():
    return []
