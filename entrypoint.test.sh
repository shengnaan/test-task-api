#!/bin/bash
# entrypoint.test.sh

set -e

#echo "Applying database migrations..."
#alembic upgrade head

echo "Running tests..."
pytest -v
