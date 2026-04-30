# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Gestion Paroissiale** — A parish management REST API built with Django. Language of application and code comments is French. The system handles user authentication, roles (fidèle, prêtre, admin), email verification, and activity logging.

## Commands

```bash
# Activate virtualenv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver 0.0.0.0:8000

# Create a superuser
python manage.py createsuperuser

# Run all tests
python manage.py test

# Start Redis (via Docker)
docker-compose up -d

# Check Redis connectivity
python test_redis.py
```

## Environment Configuration

Requires a `.env` file at the project root. Key variables:

```json
SECRET_KEY='...'
DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,*
DB_NAME=gestion_paroissiale_db
DB_USER=root
DB_PASSWORD=...
DB_HOST=127.0.0.1
DB_PORT=3306
REDIS_URL=redis://127.0.0.1:6379/0
```

Email is sent via Gmail SMTP — `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` (app password) must also be set.

## Architecture

### Request flow

```flow
Request → gestion_p/urls.py → View (accounts/*/views.py) → Service class → Model → MySQL
                                                                          ↘ Redis (JWT blacklist, sessions, rate limiting)
```

### Layer responsibilities

- **Views** (`accounts/auth/views.py`, `accounts/profile/views.py`, etc.) — HTTP handling, request validation, call into services, return standardized responses via `accounts/core/response.py:standardized_response()`.
- **Services** (`accounts/auth/services.py`, `accounts/profile/services.py`, `accounts/verification/services.py`) — all business logic lives here, not in views.
- **`accounts/core/`** — shared utilities: `jwt_utils.py` (TokenManager over Redis), `base_view.py` (BaseAPIView), `response.py`, `exceptions.py`, `permissions.py`.
- **`core/`** — empty app reserved for future cross-cutting modules.

### Custom User model

`accounts.models.User` extends `AbstractBaseUser`. Key fields: `role` (fidele/etudiant | pretre | admin), `is_verified`, `sacrement`, `created_by` (self-FK). Always use `AUTH_USER_MODEL = 'accounts.User'` when referencing the user in new apps.

### JWT & Redis

`TokenManager` (`accounts/core/jwt_utils.py`) manages the full token lifecycle:

- Access token: 3 days; Refresh token: 14 days.
- Tokens are tracked in Redis by `jti`; logout and password-change blacklist tokens server-side.
- On password change, `blacklist_all_user_tokens()` invalidates every active token for the user.

### Authentication security

- 5 failed login attempts trigger a 15-minute account lockout (tracked in Redis).
- Email verification is required; unverified users cannot authenticate.
- Rate limiting is applied via DRF throttle classes.

### API response format

All endpoints return:

```json
{ "success": bool, "data": {}, "error": "...", "message": "..." }
```

Use `standardized_response()` from `accounts/core/response.py` for every new endpoint.

### API documentation

Swagger UI is at `/docs/` and ReDoc at `/redoc/` (powered by drf-spectacular/drf-yasg).

## Key files

| Purpose | Path |
| --- | --- |
| Settings | `gestion_p/settings.py` |
| Root URL router | `gestion_p/urls.py` |
| User model | `accounts/models.py` |
| Auth service | `accounts/auth/services.py` |
| Profile service | `accounts/profile/services.py` |
| Email verification | `accounts/verification/services.py` |
| JWT / Redis utils | `accounts/core/jwt_utils.py` |
| Email templates | `templates/emails/` |
| Docker setup | `docker-compose.yaml` |
