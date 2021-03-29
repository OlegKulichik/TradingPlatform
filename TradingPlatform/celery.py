import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TradingPlatform.settings')

app = Celery('TradingPlatform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'create-trade': {
        'task': 'api.tasks.search_offers',
        'schedule': 60.0,
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')