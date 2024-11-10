#!/bin/bash
set -e

# Debugging: Print out environment variables related to the database
echo "DATABASE_URL is: $DATABASE_URL"
echo "DB_NAME is: $DB_NAME"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Execute the command passed to the container
exec "$@"
