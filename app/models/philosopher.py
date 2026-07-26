from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.quote import Quote, QuotePublic


class PhilosopherBase(SQLModel):
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    bio: Optional[str] = None


class Philosopher(PhilosopherBase, table=True):
    philosopher_id: Optional[int] = Field(default=None, primary_key=True)
    quotes: list["Quote"] = Relationship(
        back_populates="philosopher"
    )


class PhilosopherPublic(PhilosopherBase):
    philosopher_id: int


class PhilosopherPublicWithQuotes(PhilosopherPublic):
    quotes: list["QuotePublic"] = []
