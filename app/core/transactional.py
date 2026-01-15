from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import db_session_context
from app.database import AsyncSessionLocal


def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        existing_session: AsyncSession = db_session_context.get()
        if existing_session:
            # Nested transactional call
            return await func(*args, **kwargs)

        async with AsyncSessionLocal() as session:
            token = db_session_context.set(session)
            try:
                async with session.begin():
                    result = await func(*args, **kwargs)
                return result
            except Exception:
                await session.rollback()
                raise
            finally:
                db_session_context.reset(token)

    return wrapper
