"""
usage: manage.py [--help] <command> [<args>...]

The most commonly used git commands are:
syncdb Creates db models
dropdb Drop db models

"""
from database import init_db
from docopt import docopt


def main():
    args = docopt(__doc__,
                  options_first=True)

    if args['<command>'] == 'syncdb':
        init_db()
    else:
        exit("%r is not a manage.py command. See 'manage.py help'." % args['<command>'])


if __name__ == '__main__':
    main()
