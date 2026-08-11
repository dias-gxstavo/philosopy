from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud.crud_quotes import get, get_all, get_quotes_randomized
from app.database import get_session
from app.models.quote import QuotePublic, QuotePublicWithPhilosopherName

router = APIRouter(prefix='/quotes', tags=['quotes'])


@router.get('/', response_model=List[QuotePublic])
async def get_quotes(
    skip: int = 0, limit: int = 20, db: Session = Depends(get_session)
):
    return await get_all(db, skip=skip, limit=limit)


@router.get('/random', response_model=List[QuotePublicWithPhilosopherName])
async def get_random_quotes(
    limit: int = 20,
    db: Session = Depends(get_session),
):
    return await get_quotes_randomized(db, limit=limit)


@router.get('/{quote_id}', response_model=QuotePublic)
async def get_quote(quote_id: int, db: Session = Depends(get_session)):
    db_quote = await get(db, quote_id)
    if not db_quote:
        raise HTTPException(status_code=404, detail='Quote not found')
    return db_quote
