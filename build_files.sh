#!/usr/bin/env bash
# Vercel build script — runs during deployment

set -e  # stop on any error

echo "==> Installing Python dependencies..."
pip install --break-system-packages -r requirements.txt


echo "==> Running database migrations..."
python manage.py maekemigrations --noinput
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Build complete."
