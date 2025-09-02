#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Skipping collectstatic."

echo "Creating superuser if not exists..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = "manohar99"
email = "lakshmimanohart@gmail.com"
password = "reddy2005"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser created successfully.")
else:
    print("Superuser already exists.")
EOF

echo "Starting Gunicorn server..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers=4 --threads=2 --timeout=120