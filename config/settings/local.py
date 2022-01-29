from .common import *

DEBUG = env("DJANGO_DEBUG", default=True)
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-v9@!9+-)rsufs7qy6j4ki-ywhggph**_^8h+-*zabvj314a**y",
)

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="postgresql://postgres@localhost:5432/postgres"
    )
}
DATABASES["default"]["ATOMIC_REQUESTS"] = False
