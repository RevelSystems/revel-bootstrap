from assets import init_assets
from extensions import init_extensions
from flask import Flask
import jinja2
from filters.humanize_bytes import humanize_bytes
from filters.humanize_seconds import humanize_seconds
from blueprints import dummy
import settings
from jinja2_hamlpy import HamlPyExtension

jinja2.filters.FILTERS['humanize_bytes'] = humanize_bytes
jinja2.filters.FILTERS['humanize_seconds'] = humanize_seconds


def create_app(settings=settings):
    app = Flask(__name__)
    app.config.from_object(settings)
    app.jinja_env.add_extension(HamlPyExtension)
    app.jinja_env.hamlish_mode = 'indented'
    # initialize extensions and assets
    init_extensions(application=app)
    init_assets(application=app)
    # register blueprints
    app.register_blueprint(dummy.dummy)
    return app

application = create_app()

if __name__ == "__main__":
    print application.url_map
    application.run()