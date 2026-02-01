import aiohttp
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.transactional import transactional
from app.core.db import db
from app.models.promotions import Promotion
from app.database import AsyncSessionLocal
from sqlalchemy import delete

import uuid

DEFAULT_THUMB = "https://en.wikipedia.org/wiki/File:Hatton_National_Bank_New_Logo.jpg"


API_URL = "https://venus.hnb.lk/api/get_all_web_card_promos?page={page}&cardType=Credit"


def get_hnb_thumb_url(thumb_path: str | None) -> str:
    if not thumb_path:
        return DEFAULT_THUMB
    return f"https://assets.hnb.lk/atdi/{thumb_path}"


async def fetch_hnb_page(session: aiohttp.ClientSession, page: int):
    async with session.get(API_URL.format(page=page)) as resp:
        return await resp.json()


async def fetch_all_hnb_promos():
    async with aiohttp.ClientSession() as session:
        data = await fetch_hnb_page(session, 1)
        total_pages = data.get("totalPages", 1)
        all_offers = data["data"]

        tasks = [fetch_hnb_page(session, p) for p in range(2, total_pages + 1)]
        results = await asyncio.gather(*tasks)
        for page_data in results:
            all_offers.extend(page_data["data"])

        return all_offers


async def save_hnb_promos_to_db():
    offers = await fetch_all_hnb_promos()
    async with AsyncSessionLocal() as session:
        for offer in offers:
            result = await session.execute(
                select(Promotion).where((Promotion.title == offer["title"]) & (Promotion.merchant == offer["merchant"]))
            )
            promo_exists = result.scalars().first()
            if promo_exists:
                continue

            promo = Promotion(
                title=offer["title"],
                merchant=offer["merchant"],
                thumb=get_hnb_thumb_url(offer.get("thumb")),
                card_type=offer["cardType"],
                valid_to=offer["to"],
            )
            session.add(promo)
        await session.commit()


@transactional
@db
async def refresh_hnb_promotions(db):
    """
    FULL ATOMIC REFRESH
    - delete all
    - insert all
    - rollback on ANY failure
    """
    offers = await fetch_all_hnb_promos()

    await db.execute(delete(Promotion))

    for offer in offers:
        db.add(
            Promotion(
                title=offer["title"],
                merchant=offer["merchant"],
                thumb=get_hnb_thumb_url(offer.get("thumb")),
                card_type=offer["cardType"],
                valid_to=offer["to"],
            )
        )
