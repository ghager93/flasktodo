import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from . import config
from . import home

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap(app)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    app.config.from_object(config.Config)

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

    app.register_blueprint(home.bp)

    return app