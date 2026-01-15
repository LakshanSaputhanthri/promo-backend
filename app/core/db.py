import contextvars
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession

# SINGLE shared ContextVar
db_session_context = contextvars.ContextVar("db_session", default=None)


def db(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session: AsyncSession = db_session_context.get()
        if session is None:
            raise RuntimeError("DB session not initialized. Use @transactional.")
        return await func(*args, **kwargs, db=session)

    return wrapper
