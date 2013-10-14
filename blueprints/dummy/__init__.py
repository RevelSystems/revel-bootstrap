from flask import Blueprint, render_template, redirect, url_for, jsonify

dummy = Blueprint("dummy", __name__, static_folder='static', static_url_path='/dummy/static', template_folder='templates')


@dummy.route("/favicon.ico")
def favicon():
    return redirect(url_for('.static', filename='img/favicon.ico'))


@dummy.route("/")
def index():
    return render_template('index.haml')


@dummy.route("/status/<task_id>", methods=["GET"])
def status(task_id):
    return jsonify(task_id=task_id)
