from flask import Blueprint, render_template, jsonify
from models.instance import Instance
from models.server import Server
from models.commit import Commit
from couch import Couch
from tasks.backup import backup as backup_instance
from tasks.dummy import empty


admin = Blueprint("admin", __name__, static_folder='static', static_url_path='/admin/static',  template_folder='templates', url_prefix='/admin')
 
 
@admin.route("/instances")
def instances():
    return render_template('instances.html', page="instances", instances=Instance.get_instances())


@admin.route("/commits")
def commits():
    return render_template('commits.html', page="git", commits=Commit.gatherInfo())


@admin.route("/server")
def server():
    return render_template('server.html', page="server", server=Server.gatherInfo())


@admin.route("/backup/<instance_name>")
def backup(instance_name):
    task = {
        "type": "backup",
        "instance": instance_name,
        "status": "new"
    }

    task_id, rev = Couch().save(task)
    instance = Instance(instance_name)

    backup_instance.delay(task_id, instance)

    return jsonify(task_id=task_id)


@admin.route("/dummy_task/<instance_name>")
def dummy_task(instance_name):
    task = {
        "type": "dummy_task",
        "instance": instance_name,
        "status": "new"
    }

    task_id, rev = Couch().save(task)

    empty.delay(task_id)

    return jsonify(task_id=task_id)


@admin.route("/status/<task_id>")
def status(task_id):
    return jsonify(Couch()[task_id])