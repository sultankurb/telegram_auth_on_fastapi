FROM python:3.14.4-alpine3.23

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT="/venv" \
    PATH="/venv/bin:$PATH"

WORKDIR /application

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml ./

RUN uv sync --no-dev

COPY ./application/ .

CMD uv run main.py