#!/bin/bash

echo "Waiting for database to be ready..."

until pg_isready -h db -p 5432; do
  echo "Waiting for database..."
  sleep 2
done

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8005
