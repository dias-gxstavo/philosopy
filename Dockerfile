FROM python:3.14-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache --no-dev

CMD ["/app/.venv/bin/fastapi", "run", "app/main.py"]