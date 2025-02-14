import os
from contextlib import suppress

from flask import Flask
from flask_migrate import Migrate

from app.models import db
from app.views.user_views import user_bp

migrate = Migrate()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object("app.config")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)

    migrate.init_app(app, db)

    # ensure the instance folder exists
    with suppress(OSError):
        os.makedirs(app.instance_path)

    app.register_blueprint(user_bp)

    return app
