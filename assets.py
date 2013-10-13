from itertools import chain
import fnmatch
import os
from flask.ext.assets import Environment, Bundle


def find(pattern):
    for root, dir_names, file_names in os.walk('./blueprints/'):
        for filename in fnmatch.filter(file_names, pattern):
            matched_file = os.path.join(root, filename)
            yield os.path.abspath(matched_file)


class LogBundle(Bundle):
    def __init__(self, *contents, **options):
        super(LogBundle, self).__init__(*contents, **options)
        if contents:
            print "bundle {!r} of: {}".format(self.output, ', '.join([x.split('blueprints/')[-1] for x in contents]))

    def __len__(self):
        return len(self.contents)


def init_assets(application):
    assets = Environment(application)
    assets.url = application.static_url_path

    bootstrap_css = LogBundle(*list(find('bootstrap*.css')), filters='cssmin', output='css/bootstrap.css')
    scss = LogBundle(*list(find('*.scss')), filters='pyscss, cssmin', output='css/app.css')
    assets.register('app.css', bootstrap_css, scss)

    jq_bstrap_list = list(chain(find('jquery*.js'), find('bootstrap*.js')))
    js_list = filter(lambda x: x not in jq_bstrap_list, find('*.js'))

    jq_bstrap = LogBundle(*jq_bstrap_list, filters='rjsmin', output='js/jq-bstrap.js')
    js = LogBundle(*js_list, filters='rjsmin', output='js/all.js')
    coffee = LogBundle(*list(find('*.coffee')), filters='coffeescript, rjsmin', output='js/coffee.js')
    assets.register('app.js', *filter(lambda x: x, [jq_bstrap, js, coffee]))

    favicon = LogBundle(*list(find('favicon.ico')), output='img/favicon.ico')
    assets.register('favicon.ico', favicon)

    logo = LogBundle(*list(find('logo.png')), output='img/logo.png')
    assets.register('logo.png', logo)
    #assets.add(bundle)
    #bundle.build()