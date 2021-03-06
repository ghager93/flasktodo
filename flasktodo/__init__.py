import os

from flask import Flask, g
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flasktodo import config
from flasktodo import models
from flasktodo.models import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.Config)

    # bootstrap = Bootstrap(app)
    #
    # with app.app_context():
    #     g.db = SQLAlchemy(app)
    #     migrate = Migrate(app, g.db)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from flasktodo.views.auth import bp as auth_bp
    from flasktodo.views.tasks import bp as tasks_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    return app


app = create_app()
bootstrap = Bootstrap(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': models.User, 'Post': models.Post}
