# Project Structure

```
register-app/
├── manage.py                    # Django CLI entry point
├── db.sqlite3                   # SQLite database (dev only, not for version control)
│
├── RegisterApp/                 # Project configuration package
│   ├── settings.py              # Django settings (installed apps, DB, templates, middleware)
│   ├── urls.py                  # Root URL config — includes core.urls at '/'
│   ├── wsgi.py
│   └── asgi.py
│
├── core/                        # Main application — all business logic lives here
│   ├── models.py                # Data models
│   ├── views.py                 # View functions (function-based views preferred)
│   ├── urls.py                  # App-level URL patterns
│   ├── admin.py                 # Django admin registrations
│   ├── apps.py
│   ├── tests.py
│   └── migrations/              # Auto-generated migration files
│
└── templates/
    └── core/
        ├── base.html            # Base layout — includes navbar, footer, flash messages
        ├── home.html            # Extends base.html
        └── partials/
            ├── navbar.html      # Top nav — handles auth state and role-based links
            └── footer.html      # Footer with branding
```

## Conventions

- **Apps**: All feature code goes inside the `core` app. Add new Django apps at the project root level only if there is a clear separation of concern that warrants it.
- **Views**: Use function-based views (FBVs). The existing pattern is `def some_view(request): return render(request, 'core/template.html', context)`.
- **URLs**: App URLs are defined in `core/urls.py` and included in `RegisterApp/urls.py` via `include('core.urls')`. Always use named URLs (`name=`).
- **Templates**: All templates live in `templates/core/`. New templates extend `core/base.html`. Reusable snippets go in `templates/core/partials/`.
- **Auth checks**: Use `{% if user.is_authenticated %}` and `{% if user.is_staff %}` in templates. In views, use `@login_required` and check `request.user.is_staff` for admin-only logic.
- **Styling**: Use Tailwind utility classes directly in HTML. Follow the established color palette: `#2d5a27` (dark green — primary, navbar, headings), `#6aaa64` (medium green — buttons, accents, badges), `#95c98d` (light green — borders, subtle accents, hover), `#f0f0c8` (cream — page background, input fields).
- **Migrations**: Always run `makemigrations` and `migrate` after changing models. Never edit migration files manually.
