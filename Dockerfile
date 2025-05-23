FROM python:3.11-slim as builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl build-essential && \
    rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.7.1
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock* /app/

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false

RUN poetry install --no-root --only main

FROM python:3.11-slim

RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app

COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY . /app

WORKDIR /app

USER appuser

ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["python", "run.py"]
