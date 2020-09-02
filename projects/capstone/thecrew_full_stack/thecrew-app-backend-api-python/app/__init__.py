from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_cors import CORS
from flask_talisman import Talisman
from werkzeug.exceptions import default_exceptions
from config import configs

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
talisman = Talisman()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r'/api/*': {'origins': '*'}})
    talisman.init_app(app, force_https=True, force_https_permanent=True)

    from app.api import bp as api_blueprint
    app.register_blueprint(
        api_blueprint, url_prefix=f'/api/{app.config["THECREW_API_VERSION"]}')

    from app.auth import bp as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    for code in default_exceptions:
        app.register_error_handler(code, handle_http_exception)

    return app


from app import models
from app.api.errors import handle_http_exception
