from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.philosopher import Philosopher, PhilosopherPublicWithQuotes
from app.models.quote import QuotePublic


async def get(session: AsyncSession, philosopher_id: int
) -> Optional[Philosopher]:
    return await session.get(Philosopher, philosopher_id)


async def get_all(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 20,
) -> List[Philosopher]:
    statement = select(Philosopher).offset(skip).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def get_philosopher_and_quotes(
    session: AsyncSession,
    philosopher_id: int,
    skip: int = 0,
    limit: int = 20,
) -> PhilosopherPublicWithQuotes:
    statement = (
        select(Philosopher)
        .where(Philosopher.philosopher_id == philosopher_id)
        .options(selectinload(Philosopher.quotes))
    )
    result = await session.exec(statement)
    philosopher = result.first()

    if not philosopher:
        raise HTTPException(status_code=404, detail="Philosopher not found")

    paginated_quotes = philosopher.quotes[skip : skip + limit]

    return PhilosopherPublicWithQuotes(
        **philosopher.model_dump(),
        quotes=[QuotePublic.model_validate(q) for q in paginated_quotes],
    )
