from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_cors import CORS
from config import configs

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r'/api/*': {'origins': '*'}})

    from app.api import bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app


from app import models