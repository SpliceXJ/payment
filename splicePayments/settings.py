import os
from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = False if os.getenv("ENVIROMENT") == "PRODUCTION" else True

# always leave as * if hosts are not certain...

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "splice",
    "django_celery_results",
    "django_celery_beat",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "splicePayments.urls"


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


WSGI_APPLICATION = "splicePayments.wsgi.application"


if os.getenv("ENVIROMENT") in ["LOCAL", "TEST"]:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

elif os.getenv("ENVIROMENT") == "PRODUCTION":
    # use postgres
    pass


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "splice.settings.token_authentication.BearerAuthentication",
    ]
}


from kombu.utils.url import safequote

AWS_ACCESS_KEY = safequote(os.getenv("AWS_ACCESS_KEY_ID"))
AWS_SECRET_KEY = safequote(os.getenv("AWS_SECRET_ACCESS_KEY"))

BROKER_URL = "sqs://{aws_access_key}:{aws_secret_key}@".format(
    aws_access_key=AWS_ACCESS_KEY, aws_secret_key=AWS_SECRET_KEY,
)

CELERY_BROKER_URL = BROKER_URL 
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'Europe/Oslo'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
BROKER_TRANSPORT_OPTIONS = {
    'predefined_queues': {
        'testing': {
            'url': f'{os.getenv("AWS_QUEUE_URL")}testing',
            'access_key_id': os.getenv("AWS_ACCESS_KEY_ID"),
            'secret_access_key': os.getenv("AWS_SECRET_ACCESS_KEY"),
        }
    }
}
