import socket
from flask import Blueprint, render_template, redirect, url_for

dummy = Blueprint("dummy", __name__, static_folder='static', static_url_path='/dummy/static', template_folder='templates')


@dummy.route("/favicon.ico")
def favicon():
    return redirect(url_for('.static', filename='img/favicon.ico'))


@dummy.route("/")
def index():
    return render_template('index.haml')