from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'silent_trader.settings')

app = Celery('silent_trader')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

app.conf.beat_schedule = {
    'REMOVE_CONFIG_FILES':{
        'task': 'algo.tasks.REMOVE_CONFIG_FILES',
        'schedule': crontab(minute=0, hour=0, day_of_week='mon-fri'),
    },
    'BB_5_MIN':{
        'task': 'algo.tasks.BB_RUNS_5_MIN',
        'schedule': crontab(minute='*/5',hour='9-15', day_of_week='mon-fri'),
    },
    'CRS_15_MIN':{
        'task': 'algo.tasks.CROSS_OVER_ATR_ATR30_RUNS_15_MIN',
        'schedule': crontab(minute='*/15',hour='9-15', day_of_week='mon-fri'),
    },
    'LTD_3_SEC':{
        'task': 'algo.tasks.ltp_of_entries',
        'schedule': 3.0,
    },
    'CA_SLFEMA_15_MIN':{
        'task': 'algo.tasks.CA_SLFEMA_RUNS_15_MIN',
        'schedule': crontab(minute='*/15',hour='9-15', day_of_week='mon-fri'),
    },
    'CA_ATR_S30_15_MIN':{
        'task': 'algo.tasks.CA_ATR_S30_RUNS_15_MIN',
        'schedule': crontab(minute='*/15',hour='9-15', day_of_week='mon-fri'),
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))