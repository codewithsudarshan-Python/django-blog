from .settings import *  # noqa: F401,F403

# Production overrides for PythonAnywhere.
# Everything else (INSTALLED_APPS, TEMPLATES, login settings, etc.)
# comes from myproject/settings.py unchanged.

DEBUG = False

ALLOWED_HOSTS = ['codewithsudarshan.pythonanywhere.com']

CSRF_TRUSTED_ORIGINS = ['https://codewithsudarshan.pythonanywhere.com']

# The real key lives in a private file outside the project folder,
# so it is never committed to GitHub.
with open('/home/codewithsudarshan/secret_key.txt') as key_file:
    SECRET_KEY = key_file.read().strip()

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'