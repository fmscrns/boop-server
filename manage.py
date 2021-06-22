import os
import unittest

from app import blueprint
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main import create_app, db

from app.main.model import user, breed, specie, blacklist, pet, business, business_operation, business_type, post, circle, circle_type, comment

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

if __name__ == '__main__':
    manager.run()