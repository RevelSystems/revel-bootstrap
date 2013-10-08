from flask import Blueprint
from tasks.dummy import empty


admin = Blueprint("admin", __name__, static_folder='static', static_url_path='/admin/static',  template_folder='templates', url_prefix='/admin')
 
 
@admin.route("/instances")
def instances():
    #return render_template('instances.html', page="instances", instances=Instance.get_instances())
    pass
