# Tech Stack

## Backend
- **Python / Django 5.2.4** — primary framework
- **SQLite** — default database (`db.sqlite3`), file lives at project root
- Django's built-in auth system (`django.contrib.auth`) for user management and role checks (`user.is_staff`, `user.is_authenticated`)

## Frontend
- **Tailwind CSS v4** — loaded via CDN (`@tailwindcss/browser@4`), utility-first styling
- **Alpine.js** — loaded via CDN (`unpkg.com/alpinejs`), used for lightweight interactivity (`x-cloak` is already configured)
- **Google Fonts / Poppins** — global typeface, applied via `* { font-family: 'Poppins', sans-serif; }`
- Django template engine — server-side rendering with `{% block %}`, `{% include %}`, `{% url %}` tags

## Common Commands

```bash
# Run development server
python manage.py runserver

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser (admin)
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Run tests
python manage.py test
```

## Notes
- No `requirements.txt` or `pyproject.toml` detected — add one when introducing new dependencies
- No static file pipeline (webpack, vite, etc.) — all CSS/JS is CDN-based
- `DEBUG = True` and `ALLOWED_HOSTS = []` — development config only, not production-ready
