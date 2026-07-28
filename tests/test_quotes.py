from http import HTTPStatus

import pytest

from app.models.philosopher import Philosopher
from app.models.quote import Quote

TEXT_QUOTE = "Life is only meaningful when we are striving for a goal."


@pytest.fixture(name="philosopher_with_quote")
async def philosopher_with_quote_fixture(session):
    philosopher = Philosopher(
        name="Aristotle",
        birth_year=-384,
        death_year=-322,
        bio="Ancient Greek philosopher and polymath",
    )
    session.add(philosopher)
    await session.commit()
    await session.refresh(philosopher)

    quote = Quote(
        text=TEXT_QUOTE,
        philosopher_id=philosopher.philosopher_id,
    )
    session.add(quote)
    await session.commit()

    return philosopher, quote


async def test_list_quotes_returns_seeded_quote(
    client,
    philosopher_with_quote
    ):

    response = await client.get("/quotes/")

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["text"] == TEXT_QUOTE
    assert data[0]["philosopher_id"] == 1


async def test_list_quotes_empty_when_no_data(client):
    response = await client.get("/quotes/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []
