from __future__ import absolute_import
from time import sleep
# from celery_runner import celery
from couch import Couch
from celery import Celery
import settings

celery = Celery('tasks.dummy')
celery.config_from_object(settings)

@celery.task(name="dummy.empty")
def empty(task_id):
    task = Couch()[task_id]
    task["status"] = "started"

    sleep(30)

    task["status"] = "success"
    return Couch().save(task)


@celery.task
def hearbeat():
    task = {
        "type": "heartbeat",
        "status": "success"
    }
    return Couch().save(task)

if __name__ == "__main__":
    celery.start()
