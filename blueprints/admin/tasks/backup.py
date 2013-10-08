from __future__ import absolute_import
from datetime import datetime, timedelta
import os
from shutil import copytree, move, rmtree
import tempfile
import tarfile
from couch import Couch
from celery import Celery
from settings import BACKUP_KEEP_DAYS, BACKUP_DIR
import settings
from ..utils import local_run as run
from ..utils import date_iter
from ..utils import mkdir_p
from ..utils import LocalPgpass

celery = Celery('tasks.backup')
celery.config_from_object(settings)


def perform_backup(instance, location):
    container = tempfile.mktemp()

    tar_file = "{}.tar.gz".format(instance.name)

    copy_dir = os.path.join(container, instance.name)
    #prepare archive folders: customer_name and customer_name/instances
    mkdir_p("{}/instances/".format(copy_dir))

    copytree(instance.folder, os.path.join(copy_dir, 'instances'))

    try:
        LocalPgpass(instance.db_name, instance.db_user, instance.db_password).save()

        #PostgreSQL dump
        pg_dump_file = "{}/{}.pgdump".format(copy_dir, instance.name)
        run("pg_dump -w -Fc -U{} {} > {}".format(instance.db_user, instance.db_name, pg_dump_file))

        #compress customer data along with backup
        os.chdir(container)
        tar = tarfile.open(tar_file, "w:gz")
        for name in [instance.name]:
            tar.add(name)
        tar.close()
        #move the file to desired path
        move(tar_file, location)
        return os.path.join(location, tar_file)
    finally:
        #cleanup
        rmtree(container)


@celery.task(name="backup.backup")
def backup(task_id, instance):
    task = Couch()[task_id]
    task["status"] = "started"
    Couch().save(task)

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    h = now.strftime("%H")
    m = now.strftime("%M")
    s = now.strftime("%S")
    location = os.path.join(BACKUP_DIR, instance.name, today, h, m, s)

    mkdir_p(location)
    file = perform_backup(instance.name, location)

    task["status"] = "success"
    task["file"] = file
    Couch().save(task)


@celery.task
def old_backups_cleanup():
    task = {
        "type": "old_backups_cleanup",
        "status": "started"
    }

    task_id, rev = Couch().save(task)

    #cleanup previous
    now = datetime.now()
    min_day = now - timedelta(days=BACKUP_KEEP_DAYS)
    allowed_days = [x.strftime("%Y-%m-%d") for x in date_iter(min_day, now)]

    instance_backup_dirs = filter(lambda x: os.path.isdir(x), os.listdir(BACKUP_DIR))
    for base_dir in instance_backup_dirs:
        os.chdir(base_dir)

        dir_list = filter(lambda x: os.path.isdir(os.path.join(base_dir, x)), os.listdir(base_dir))
        for dir in dir_list:
            if dir not in allowed_days:
                rmtree(dir)

    task = Couch()[task_id]
    task["status"] = "success"