FROM python:3.11.4-buster as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.6.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache 

RUN pip install poetry==$POETRY_VERSION

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM builder as test-builder

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --with dev --no-root

FROM python:3.11-slim-buster as tests

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/

COPY --from=test-builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app
COPY . .

ENTRYPOINT ["pytest"]


FROM python:3.11-slim-buster as production

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app
COPY src src

ENTRYPOINT ["python", "src/main.py"]
