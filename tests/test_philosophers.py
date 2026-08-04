from http import HTTPStatus

import pytest

from app.models.philosopher import Philosopher
from app.models.quote import Quote

PHILOSOPHER = "Aristotle"


@pytest.fixture(name="philosopher")
async def philosopher_fixture(session):
    philosopher = Philosopher(
        name="Aristotle",
        birth_year=-384,
        death_year=-322,
        bio="Ancient Greek philosopher and polymath",
    )
    session.add(philosopher)
    await session.commit()
    await session.refresh(philosopher)
    return philosopher


@pytest.fixture(name="philosopher_with_quotes")
async def philosopher_with_quotes_fixture(session, philosopher):
    quotes = [
        Quote(
            text="Life is only meaningful when we are striving for a goal.",
            philosopher_id=philosopher.philosopher_id
        ),

        Quote(
            text="95% of everything you do is the result of habit.",
            philosopher_id=philosopher.philosopher_id
        ),
    ]
    session.add_all(quotes)
    await session.commit()
    return philosopher, quotes


async def test_list_philosophers_returns_seeded_philosopher(
    client,
    philosopher
    ):

    response = await client.get("/philosophers/")

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data[0]["name"] == PHILOSOPHER


async def test_list_philosophers_empty_when_no_data(client):
    response = await client.get("/philosophers/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


async def test_get_philosopher_by_id(client, philosopher):
    response = await client.get(f"/philosophers/{philosopher.philosopher_id}")

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["philosopher_id"] == philosopher.philosopher_id
    assert data["name"] == PHILOSOPHER


async def test_get_philosopher_not_found(client):
    response = await client.get("/philosophers/9999")

    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_philosopher_quotes_endpoint_returns_related_quotes(
    client,
    philosopher_with_quotes
    ):

    philosopher, quotes = philosopher_with_quotes

    response = await client.get(
        f"/philosophers/{philosopher.philosopher_id}/quotes"
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    texts = {q["text"] for q in data["quotes"]}
    assert texts == {q.text for q in quotes}
    assert all("philosopher_id" not in quote for quote in data["quotes"])


async def test_philosopher_quotes_endpoint_empty_when_no_quotes(
    client,
    philosopher
    ):

    response = await client.get(
        f"/philosophers/{philosopher.philosopher_id}/quotes"
    )
    data = response.json()

    assert data['quotes'] == []
    assert response.status_code == HTTPStatus.OK
