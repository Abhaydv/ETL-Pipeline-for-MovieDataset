#!/bin/sh
set -e

# If DATABASE_URL is set, run migrations
if [ -n "$DATABASE_URL" ]; then
  echo "Running alembic migrations..."
  alembic upgrade head
else
  echo "DATABASE_URL not set, skipping alembic migrations"
fi

# Run the ETL pipeline
exec python etl_pipeline.py
