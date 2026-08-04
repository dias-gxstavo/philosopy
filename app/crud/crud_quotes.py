from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.philosopher import Philosopher
from app.models.quote import Quote, QuotePublicWithPhilosopherName


async def get(session: AsyncSession, quote_id: int) -> Optional[Quote]:
    return await session.get(Quote, quote_id)


async def get_all(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 20,
) -> List[Quote]:
    statement = select(Quote).offset(skip).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def get_quotes_randomized(
    session: AsyncSession,
    limit: int = 20,
) -> List[QuotePublicWithPhilosopherName]:
    statement = (
        select(Quote, Philosopher.name)
        .join(
            Philosopher,
            Quote.philosopher_id == Philosopher.philosopher_id,
        )
        .order_by(func.random())
        .limit(limit)
    )
    result = await session.exec(statement)
    return [
        QuotePublicWithPhilosopherName(
            quote_id=quote.quote_id,
            text=quote.text,
            philosopher_name=philosopher_name,
        )
        for quote, philosopher_name in result.all()
    ]
