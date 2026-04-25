# STAGE 1: Build React Frontend
FROM node:alpine AS frontend-builder
WORKDIR /app/client

COPY client/package.json client/package-lock.json* ./
RUN npm install

COPY client/ ./
RUN npm run build

# STAGE 2: Build FastAPI Backend
FROM python:3.11-slim AS backend-builder
WORKDIR /app/api

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/api/wheels -r requirements.txt

# STAGE 3: Final Production Image
FROM python:3.11-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/api \
    PORT=8000

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

COPY --from=backend-builder /app/api/wheels /wheels
COPY --from=backend-builder /app/api/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY api /app/api

COPY --from=frontend-builder /app/client/dist /app/client/dist

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

WORKDIR /app/api
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
