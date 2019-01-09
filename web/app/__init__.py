from flask import Flask

from web.app import settings
from web.app.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.url_map.strict_slashes = False

    db.init_app(app)

    import web.app.controllers as controller
    app.register_blueprint(controller.module)

    return app
