from __future__ import absolute_import
from celery import Celery
import settings

celery = Celery('tasks.dummy')
celery.config_from_object(settings)

@celery.task(name="dummy.empty")
def empty(task_id):
    pass


@celery.task
def hearbeat():
    pass

if __name__ == "__main__":
    celery.start()
