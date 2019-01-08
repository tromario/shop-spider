from flask import Flask
from web_site.app.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('/media/roman/data/My projects/shop-spider/web_site/app/settings.py')
    app.url_map.strict_slashes = False

    db.init_app(app)

    import web_site.app.controllers as controller
    app.register_blueprint(controller.module)

    return app
