from sqlmodel import Session, SQLModel, create_engine

from app.settings import settings

engine = create_engine(
    str(settings.DATABASE_URL),
    echo=settings.DEBUG_SQL,
    pool_pre_ping=True,
)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)
