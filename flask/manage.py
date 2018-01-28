import os
import logging
from flask_script import Manager
from flask_script import Shell
from flask_script import Server
from flask_migrate import Migrate, MigrateCommand

logger = logging.getLogger(__name__)

if os.path.exists('.env'):
    logger.info('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app  # noqa: E402
from app import db  # noqa: E402


app = create_app(os.getenv('FLASK_CONFIG', 'default'))
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command(
    'runserver',
    Server(host='0.0.0.0', port=5050, use_reloader=True)
)
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=lambda: dict(app=app, db=db)))


if __name__ == '__main__':
    manager.run()
