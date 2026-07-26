
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlmodel import Session

from app.database import get_session
from app.routers import philosophers, quotes

app = FastAPI(
    title="a python api to get famous philosophers quotes"
)

app.include_router(philosophers.router)
app.include_router(quotes.router)


@app.get("/health", status_code=status.HTTP_200_OK, tags=["health"])
def health_check(db: Session = Depends(get_session)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )
