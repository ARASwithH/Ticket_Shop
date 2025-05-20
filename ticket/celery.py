import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket.settings')

app = Celery('ticket')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()