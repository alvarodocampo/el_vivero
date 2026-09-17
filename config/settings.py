import os
from pathlib import Path


# =========================================================
# RUTAS DEL PROYECTO
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SEGURIDAD
# =========================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-development-only-change-me-before-production",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost",
    ).split(",")
    if host.strip()
]


# =========================================================
# APLICACIONES
# =========================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Necesario para django-allauth
    "django.contrib.sites",

    # Django Allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    # Login con Google
    "allauth.socialaccount.providers.google",

    # Aplicaciones del proyecto
    "core.apps.CoreConfig",
]


# =========================================================
# DJANGO SITES
# =========================================================

SITE_ID = 1


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # Necesario para django-allauth
    "allauth.account.middleware.AccountMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URLS
# =========================================================

ROOT_URLCONF = "config.urls"


# =========================================================
# PLANTILLAS
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [BASE_DIR / 'templates',
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = "config.wsgi.application"


# =========================================================
# BASE DE DATOS
# =========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",

        "NAME": BASE_DIR / "db.sqlite3",
    }
}

if os.environ.get("DATABASE_URL"):
    import dj_database_url

    DATABASES["default"] = dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )


# =========================================================
# VALIDACIÓN DE CONTRASEÑAS
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =========================================================
# INTERNACIONALIZACIÓN
# =========================================================

LANGUAGE_CODE = "es-es"

TIME_ZONE = "Europe/Madrid"

USE_I18N = True

USE_TZ = True


# =========================================================
# ARCHIVOS ESTÁTICOS
# =========================================================

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Precio base configurable sin modificar el código.
DEFAULT_PRICE_PER_NIGHT = os.environ.get("DEFAULT_PRICE_PER_NIGHT", "100.00")


# =========================================================
# SEGURIDAD DE PRODUCCIÓN
# =========================================================

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# =========================================================
# AUTENTICACIÓN
# =========================================================

AUTHENTICATION_BACKENDS = [
    # Mantiene funcionando el login del admin de Django
    "django.contrib.auth.backends.ModelBackend",

    # Login mediante django-allauth
    "allauth.account.auth_backends.AuthenticationBackend",
]


# =========================================================
# DJANGO ALLAUTH
# =========================================================

# Queremos iniciar sesión mediante correo electrónico.
ACCOUNT_LOGIN_METHODS = {
    "email"
}


# Campos que tendrá el registro.
ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "password1*",
    "password2*",
]


# Redirecciones después de iniciar/cerrar sesión.
LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"


# Durante el desarrollo lo dejamos desactivado.
# Más adelante lo cambiaremos a "mandatory" para que
# el usuario tenga que confirmar su email.
ACCOUNT_EMAIL_VERIFICATION = "none"


# =========================================================
# GOOGLE
# =========================================================

SOCIALACCOUNT_EMAIL_REQUIRED = True


# =========================================================
# CLAVE PRIMARIA POR DEFECTO
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
