import fnmatch
import os
from jinja2_hamlpy import HamlPyExtension
from flask.ext.assets import Environment, Bundle


def find_sass():
    for root, dir_names, file_names in os.walk('./'):
        for filename in fnmatch.filter(file_names, '*.scss'):
            scss_file = os.path.abspath(os.path.join(root, filename))
            yield scss_file


def init_extensions(application):
    application.jinja_env.add_extension(HamlPyExtension)
    application.jinja_env.hamlish_mode = 'indented'

    assets = Environment(application)
    assets.url = application.static_url_path
    scss = Bundle(*list(find_sass()), filters='pyscss', output='all.css')

    bundle = assets.register('all.css', scss)
    print bundle
    #assets.add(bundle)
    #bundle.build()
