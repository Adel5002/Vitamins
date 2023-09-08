import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_cache_every_hour': {
        'task': 'Vitamins.tasks.delete_not_actual_caches',
        'schedule': crontab(),
        # minute='*/60'
    }
}