# STAGE 1: Build React Frontend
FROM node:alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# STAGE 2: Build FastAPI Backend
FROM python:3.11-slim AS backend-builder
WORKDIR /app/backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/backend/wheels -r requirements.txt

# STAGE 3: Final Production Image
FROM python:3.11-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend \
    PORT=8080

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

COPY --from=backend-builder /app/backend/wheels /wheels
COPY --from=backend-builder /app/backend/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY backend /app/backend

COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

WORKDIR /app/backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
