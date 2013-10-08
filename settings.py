import socket
from celery.schedules import crontab

COUCHDB = {
    'SERVER': 'http://localhost:5984/',
    'DATABASE': 'opsmate'
}
SERVER_ID = socket.gethostname()

DEBUG = True

BACKUP_KEEP_DAYS = 7
BACKUP_DIR = '/var/backups/atlas/'
INSTANCES_CONFIG_PATH = '/etc/atlas.app/instances'

### celery configuration
BROKER_URL = 'sqla+sqlite:///celery.db'
CELERY_IMPORTS = ("blueprints.dummy.tasks",)
CELERYBEAT_SCHEDULE = {
    'old_backups_cleanup': {
        'task': 'blueprints.dummy.tasks.backup.old_backups_cleanup',
        'schedule': crontab(minute='11', hour='11', day_of_week='*'),
        'args': ()
    },
    'heartbeat': {
        'task': 'blueprints.dummy.tasks.dummy.hearbeat',
        'schedule': crontab(minute='*'),
        'args': ()
    },
}

CELERY_TIMEZONE = 'America/Los_Angeles'