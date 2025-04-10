#!/bin/bash
# entrypoint.sh

echo "Applying database migrations..."
alembic upgrade head

echo "Starting the server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
