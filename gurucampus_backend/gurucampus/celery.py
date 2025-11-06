# gurucampus/celery.py
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gurucampus.settings")

# Create the Celery application instance
app = Celery("gurucampus")

# Load task modules from all registered Django app configs.
# This means Celery will look for a 'tasks.py' file in each app.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()