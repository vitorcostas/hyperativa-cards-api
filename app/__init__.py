from flask import Flask, Blueprint
from app.config import Config
from flask_restx import Api
from app.extentions import db, migrate, jwt
from app.core.user import user_namespace
from app.core.auth import auth_namespace
from app.core.card import card_namespace

app = Flask(__name__)
blueprint = Blueprint('app', __name__)
app.register_blueprint(blueprint)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    }

api = Api(app,
          version='1.0',
          title='Hyperativa Cards API',
          description='API for managing cards data',
          prefix='/api',
          authorizations=authorizations,
          security='Bearer'
          )

api.add_namespace(user_namespace)
api.add_namespace(auth_namespace)
api.add_namespace(card_namespace)


def start():
    return app
