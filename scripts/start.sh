#!/bin/bash
echo "Waiting for database to be ready..."
sleep 5  # Give postgres a few seconds to initialize

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8005