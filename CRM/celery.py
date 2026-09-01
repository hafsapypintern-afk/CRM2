import os

from celery import Celery


# Tell Celery which Django settings module to use
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "CRM.settings"
)


# Create the Celery application
app = Celery("CRM")


# Load Celery settings from Django settings.py
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)


# Automatically find tasks.py inside installed apps
app.autodiscover_tasks()