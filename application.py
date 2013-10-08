from flask import Flask
from jinja2 import Environment
from hamlish_jinja import HamlishExtension, HamlishTagExtension
import jinja2
from filters.humanize_bytes import humanize_bytes
from filters.humanize_seconds import humanize_seconds
from blueprints import admin, dummy
import settings
from werkzeug.datastructures import ImmutableDict
from jinja2_hamlpy import HamlPyExtension

jinja2.filters.FILTERS['humanize_bytes'] = humanize_bytes
jinja2.filters.FILTERS['humanize_seconds'] = humanize_seconds

#class FlaskWithHamlish(Flask):
#    jinja_options = ImmutableDict(
#        extensions=['hamlish_jinja.HamlishExtension']
#    )

#class FlaskWithHamlish(Flask):
#    jinja_options = ImmutableDict(
#        extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_', 'hamlish_jinja.HamlishExtension']
#    )


#from jinja2 import Environment
#from hamlish_jinja import HamlishExtension


def create_app(settings=settings):
    app = Flask(__name__)
    #app.jinja_env = Environment(extensions=[HamlishExtension], loader=)
    app.debug = True

    app.config.from_object(settings)
    app.jinja_env.add_extension(HamlPyExtension)
    app.jinja_env.hamlish_mode = 'indented'
    # initialize extensions...
    # mail.init_app(ret_val)
    # register blueprints...
    app.register_blueprint(dummy.dummy)
    app.register_blueprint(admin.admin, url_prefix='/admin')

    return app

application = create_app()

if __name__ == "__main__":
    print application.url_map
    application.run()