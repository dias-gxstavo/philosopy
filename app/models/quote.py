from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

import app.models.philosopher


class QuoteBase(SQLModel):
    text: str
    philosopher_id: int = Field(foreign_key="philosopher.philosopher_id")


class Quote(QuoteBase, table=True):
    quote_id: Optional[int] = Field(default=None, primary_key=True)
    philosopher: Optional["Philosopher"] = Relationship(
        back_populates="quotes"
    )


class QuotePublic(QuoteBase):
    quote_id: int


class QuotePublicNested(SQLModel):
    text: str
    quote_id: int


class QuotePublicWithPhilosopher(QuotePublic):
    philosopher: "PhilosopherPublic"
