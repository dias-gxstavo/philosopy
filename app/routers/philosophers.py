from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud.crud_philosophers import get, get_all, get_philosopher_and_quotes
from app.database import get_session
from app.models.philosopher import (
    PhilosopherPublic,
    PhilosopherPublicWithQuotes,
)

router = APIRouter(prefix='/philosophers', tags=['philosophers'])


@router.get('/', response_model=List[PhilosopherPublic])
async def get_philosophers(
    skip: int = 0, limit: int = 20, db: Session = Depends(get_session)
):
    return await get_all(db, skip=skip, limit=limit)


@router.get('/{philosopher_id}', response_model=PhilosopherPublic)
async def get_philosopher(
    philosopher_id: int, db: Session = Depends(get_session)
):
    db_philosopher = await get(db, philosopher_id)
    if not db_philosopher:
        raise HTTPException(status_code=404, detail='Philosopher not found')
    return db_philosopher


@router.get(
    '/{philosopher_id}/quotes', response_model=PhilosopherPublicWithQuotes
)
async def get_philosophers_and_quotes(
    philosopher_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_session),
):
    return await get_philosopher_and_quotes(
        db, philosopher_id, skip=skip, limit=limit
    )
