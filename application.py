from flask import Flask
import jinja2
from filters.humanize_bytes import humanize_bytes
from filters.humanize_seconds import humanize_seconds
from blueprints import admin, dummy
import settings
jinja2.filters.FILTERS['humanize_bytes'] = humanize_bytes
jinja2.filters.FILTERS['humanize_seconds'] = humanize_seconds


def create_app(settings=settings):
    ret_val = Flask(__name__)
    ret_val.config.from_object(settings)
    # initialize extensions...
    # mail.init_app(ret_val)
    # register blueprints...
    ret_val.register_blueprint(dummy.dummy)
    ret_val.register_blueprint(admin.admin, url_prefix='/admin')

    return ret_val

if __name__ == "__main__":
    application = create_app()
    application.run()
    print application.url_map
