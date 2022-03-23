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
    'Send SMS':{
        'task': 'algo.tasks.send_report',
        'schedule': crontab(minute=16, hour=15, day_of_week='mon-fri'),
    },
    'STOCKS_CONFIG_FILES':{
        'task': 'algo.tasks.get_stocks_configs',
        'schedule': crontab(minute=0, hour=22, day_of_week='sun-thu'),
    },
    "UPDATE_LIMIT'S":{
        'task': 'algo.tasks.UPDATE_LIMIT',
        'schedule': crontab(minute=37, hour=9, day_of_week='mon-fri'),
    },
    "GENERATE_FYERS_TOKEN":{
        'task': 'algo.tasks.GENERATE_FYERS_TOKEN',
        'schedule': crontab(minute=45, hour=8),
    },
    'LTP':{
        'task': 'algo.tasks.ltp_of_entries',
        'schedule': 3.0,
    },
    'CRS_15_MIN':{
        'task': 'algo.tasks.CROSS_OVER_RUNS_15_MIN',
        'schedule': crontab(minute='*/5',hour='9-15', day_of_week='mon-fri'),
    },
    'CRS_30_MIN':{
        'task': 'algo.tasks.CROSS_OVER_RUNS_30_MIN',
        'schedule': crontab(minute='*/5',hour='9-15', day_of_week='mon-fri'),
    },
    # ------------------------ Not Active -----------------
    'CRS_15_MIN_TEMP':{
        'task': 'algo.tasks.CROSS_OVER_RUNS_15_MIN_TEMP',
        'schedule': crontab(minute='*/30',hour='9-15', day_of_week='mon-fri'),
    },
    'CRS_15_MIN_TEMP_DOWN':{
        'task': 'algo.tasks.DOWN_CROSS_OVER_RUNS_15_MIN_TEMP',
        'schedule': crontab(minute='*/30',hour='9-15', day_of_week='mon-fri'),
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))