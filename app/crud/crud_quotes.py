from typing import List, Optional

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.quote import Quote


async def get(session: Session, quote_id: int) -> Optional[Quote]:
    return session.get(Quote, quote_id)


async def get_all(
    session: Session,
    skip: int = 0,
    limit: int = 20
) -> List[Quote]:
    statement = select(Quote).offset(skip).limit(limit)
    result = session.exec(statement)
    return result.all()


async def get_quotes_randomized(
    session: Session,
    limit: int = 20,
) -> List[Quote]:
    statement = select(Quote).order_by(func.random()).limit(limit)
    result = session.exec(statement)
    return result.all()
