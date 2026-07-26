from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.philosopher import Philosopher, PhilosopherPublicWithQuotes
from app.models.quote import Quote


async def get(session: Session, philosopher_id: int
) -> Optional[Philosopher]:
    return session.get(Philosopher, philosopher_id)


async def get_all(
    session: Session,
    skip: int = 0,
    limit: int = 20
) -> List[Philosopher]:
    statement = select(Philosopher).offset(skip).limit(limit)
    result = session.exec(statement)
    return result.all()


async def get_philosopher_and_quotes(
    session: Session,
    philosopher_id: int,
    skip: int = 0,
    limit: int = 20,
) -> PhilosopherPublicWithQuotes:
    philosopher = session.get(Philosopher, philosopher_id)
    if not philosopher:
        raise HTTPException(status_code=404, detail="Philosopher not found")

    quotes_statement = (
        select(Quote)
        .where(Quote.philosopher_id == philosopher_id)
        .offset(skip)
        .limit(limit)
    )
    quotes = session.exec(quotes_statement).all()

    return PhilosopherPublicWithQuotes(
        **philosopher.model_dump(),
        quotes=quotes
    )
