from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session, init_db
from app.routers import philosophers, quotes
from app.settings import settings

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    send_default_pii=True,
    enable_logs=True,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title='a python api to get famous philosophers quotes', lifespan=lifespan
)

app.include_router(philosophers.router)
app.include_router(quotes.router)


@app.get('/health', status_code=status.HTTP_200_OK, tags=['health'])
async def health_check(db: AsyncSession = Depends(get_session)):
    try:
        await db.execute(text('SELECT 1'))
        return {'status': 'healthy', 'database': 'connected'}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f'Database connection failed: {str(e)}',
        )
