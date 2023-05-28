from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'splicePayments.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')


app = Celery('splicePayments')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'place_holder':{
        'task':'splice.tasks.request_queue_messages',
        'schedule': 60,
        # 'args': (2,),
    },
}

app.autodiscover_tasks()