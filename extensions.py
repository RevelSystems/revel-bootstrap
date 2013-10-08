import fnmatch
import os
from jinja2_hamlpy import HamlPyExtension
from flask.ext.assets import Environment, Bundle


def find(pattern):
    for root, dir_names, file_names in os.walk('./'):
        for filename in fnmatch.filter(file_names, pattern):
            matched_file = os.path.join(root, filename)
            print "bundle {!r}".format(matched_file)
            yield os.path.abspath(matched_file)


def init_extensions(application):
    application.jinja_env.add_extension(HamlPyExtension)
    application.jinja_env.hamlish_mode = 'indented'

    assets = Environment(application)
    assets.url = application.static_url_path
    bootstrap_css = Bundle(*list(find('bootstrap*.css')), filters='cssmin', output='bootstrap.css')
    scss = Bundle(*list(find('*.scss')), filters='pyscss', output='all.css')
    assets.register('all.css', bootstrap_css, scss)

    bootstrap_js = Bundle(*list(find('bootstrap*.js')), filters='jsmin', output='bootstrap.js')
    assets.register('all.js', bootstrap_js)
    #assets.add(bundle)
    #bundle.build()
