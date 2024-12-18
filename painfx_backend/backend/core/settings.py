from pathlib import Path
import environ
from django.core.management.utils import get_random_secret_key
import os
from django.core.exceptions import ImproperlyConfigured

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    DEVELOPMENTMODE=(bool, False)
)


# def read_secret(secret_name, default_value=None):
#     try:
#         with open(f"/run/secrets/{secret_name}") as secret_file:
#             return secret_file.read().strip()
#     except FileNotFoundError:
#         if default_value is not None:
#             return default_value
#         raise ImproperlyConfigured(f"Secret {secret_name} not found and no default provided.")


log_dir = BASE_DIR / "logs"
if not log_dir.exists():
    os.makedirs(log_dir)

DEBUG = env("DJANGO_DEBUG", default=False)
DEVELOPMENTMODE = env("DEVELOPMENTMODE", default=False)

print("DEBUG:", DEBUG)
print("DEVELOPMENTMODE:", DEVELOPMENTMODE)

# Secret key
SECRET_KEY = env('DJANGO_SECRET_KEY', default=get_random_secret_key())
print("SECRET_KEY : ", SECRET_KEY)

# Allowed hosts
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=["*"] if DEVELOPMENTMODE else [])

# CORS settings
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    "https://painfx.in",
    "https://api.painfx.in"
])
CORS_ALLOW_CREDENTIALS = True

if DEVELOPMENTMODE:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "drf_yasg",
    "rest_framework",
    "djoser",
    "storages",
    "social_django",
    "django_celery_beat",
    "django_celery_results",
    "apps.authentication",
    "apps.booking_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.runserver_nostatic", 
    "django.contrib.staticfiles",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI and ASGI applications
WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', default='painfx_db'),
        'USER': env('POSTGRES_USER', default='painfx_user'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='mohamedalhabob'),
        "HOST": env("POSTGRES_HOST", default="postgres"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}

# Password validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Localization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static and media files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# WhiteNoise storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Domain and site settings
DOMAIN = env("DOMAIN", default="https://painfx.in")
SITE_NAME = "PainFX"

# Custom user model
AUTH_USER_MODEL = "authentication.User"

# Stripe settings
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY", default="sk_test_51OF23EH6eN12iihY2CtKekiFQFshNhzeIGGI9ram7CypnCL89dnBpGap6DFkZDiX9h9W9KPuu72o2ITJUFv7sCvd00ZN5Z32Hl")
STRIPE_WEBHOOK_SECRET = env("STRIPE_WEBHOOK_SECRET", default="https://painfx.in")

# Google Maps API Key
GOOGLE_MAPS_API_KEY = env("GOOGLE_MAPS_API_KEY", default="https://painfx.in")

# Twilio settings
TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID", default="ACcb51bc274429a7aaee176fe26ba642e8")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN", default="47ab8efcd0a1a83629f6fa288a230a36")
TWILIO_FROM_NUMBER = env("TWILIO_FROM_NUMBER", default="+17753178557")

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER',default="supernovasoftwareco@gmail.com")
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = f"{SITE_NAME} <{EMAIL_HOST_USER}>"

# Default auto field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]


# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.authentication.authentication.CustomJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# Djoser settings
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'activation/{uid}/{token}',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': env('REDIRECT_URLS').split(','),
}

# Authentication cookies
AUTH_COOKIE = 'access'
AUTH_COOKIE_MAX_AGE = 60 * 60 * 24
AUTH_COOKIE_SECURE = env('AUTH_COOKIE_SECURE') == 'True'
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAMESITE = 'None'

# Social authentication settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('GOOGLE_AUTH_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('GOOGLE_AUTH_SECRET_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']

# Celery settings
CELERY_BROKER_URL = env('CELERY_BROKER_URL',default='redis://redis:6379/0')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND',default='redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Logging settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_dir / "django.log",
            "maxBytes": 1024*1024*5,  # 5MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "formatters": {
        "verbose": {"format": "{levelname} {asctime} {module} {message}", "style": "{"},
        "simple": {"format": "{levelname} {message}", "style": "{"},
    },
}

# Security settings for production
if not DEVELOPMENTMODE:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

    # Additional security settings
    SECURE_REFERRER_POLICY = "same-origin"
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_TRUSTED_ORIGINS = ['https://painfx.in', 'https://www.painfx.in', 'https://api.painfx.in']
    
    # Content Security Policy (CSP)
    CSP_DEFAULT_SRC = ("'self'",)
    CSP_SCRIPT_SRC = ("'self'", 'https://trustedscripts.example.com')
    CSP_STYLE_SRC = ("'self'", 'https://trustedstyles.example.com')
    CSP_IMG_SRC = ("'self'", 'data:')
    CSP_CONNECT_SRC = ("'self'", 'https://api.painfx.in')
    CSP_FONT_SRC = ("'self'",)
    CSP_OBJECT_SRC = ("'none'",)
    CSP_BASE_URI = ("'self'",)
    CSP_FORM_ACTION = ("'self'",)
    CSP_FRAME_ANCESTORS = ("'none'",)
