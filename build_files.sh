#!/usr/bin/env bash
# Vercel build script — runs during deployment

set -e  # stop on any error

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Build complete."
