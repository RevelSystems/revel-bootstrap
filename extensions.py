from jinja2_hamlpy import HamlPyExtension
#from flask.ext.mail import Mail
 
 
def init_extensions(application):
    application.jinja_env.add_extension(HamlPyExtension)
    application.jinja_env.hamlish_mode = 'indented'