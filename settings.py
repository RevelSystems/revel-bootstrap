from celery.schedules import crontab

DEBUG = True

DATABASE = "sqlite:///bootstrap.db"
### celery configuration
BROKER_URL = 'sqla+sqlite:///celery.db'
CELERY_IMPORTS = ("blueprints.dummy.tasks",)
CELERYBEAT_SCHEDULE = {
    'heartbeat': {
        'task': 'blueprints.dummy.tasks.dummy.hearbeat',
        'schedule': crontab(minute='*'),
        'args': ()
    },
}

CELERY_TIMEZONE = 'America/Los_Angeles'