import os
from celery import Celery
from django.conf import settings
from celery.schedules import schedule, crontab
from django.utils.timezone import timedelta


# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mass_email_app.settings")

# Create the Celery application instance
app = Celery("mass_email_app")

# Configure Celery using Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks in Django applications
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
